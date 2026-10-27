"""
views.py — All Django views and JSON API endpoints for VIBE CHECK.
"""

import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.utils import timezone

from .forms import LoginForm, RegisterForm
from .models import MoodEntry, SavedTrack
from .music_service import get_playlists_for_mood
from .ai_service import get_ai_recommendations

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Auth views
# ─────────────────────────────────────────────────────────────────────────────

def login_view(request):
    """Login page."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm()
    error = ''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                error = 'Invalid username or password. Please try again.'

    return render(request, 'myapp/login.html', {'form': form, 'error': error})


def register_view(request):
    """Registration page."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm()
    error = ''

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # Collect first form error for display
            for field_errors in form.errors.values():
                error = field_errors[0]
                break

    return render(request, 'myapp/register.html', {'form': form, 'error': error})


def logout_view(request):
    """Logout — works on GET or POST."""
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    """Main dashboard with mood engine."""
    # Latest mood for the current user
    latest_entry = MoodEntry.objects.filter(user=request.user).first()
    current_mood = latest_entry.mood if latest_entry else ''

    # Initial playlists (default happy or latest mood)
    initial_mood = current_mood or 'happy'
    playlists = get_playlists_for_mood(initial_mood)

    context = {
        'user': request.user,
        'current_mood': current_mood,
        'playlists': playlists,
        'greeting': _time_greeting(),
    }
    return render(request, 'myapp/dashboard.html', context)


@login_required
def history_view(request):
    """Mood history page."""
    entries = MoodEntry.objects.filter(user=request.user).order_by('-created_at')

    # Build mood counts for chart
    mood_counts = {'happy': 0, 'stressed': 0, 'sleepy': 0, 'hyped': 0}
    for entry in entries:
        if entry.mood in mood_counts:
            mood_counts[entry.mood] += 1

    top_mood = max(mood_counts, key=mood_counts.get) if entries else None

    context = {
        'entries': entries,
        'mood_counts': mood_counts,
        'mood_counts_json': json.dumps(mood_counts),
        'top_mood': top_mood,
        'total': entries.count(),
    }
    return render(request, 'myapp/history.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# JSON API endpoints
# ─────────────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def api_save_mood(request):
    """POST /api/save-mood/ — save a mood entry for the logged-in user."""
    try:
        data = json.loads(request.body)
        mood = data.get('mood', '').lower().strip()
        note = data.get('note', '').strip()

        valid_moods = [m[0] for m in MoodEntry.MOOD_CHOICES]
        if mood not in valid_moods:
            return JsonResponse({'error': 'Invalid mood value.'}, status=400)

        note = note[:500]  # cap at 500 chars

        entry = MoodEntry.objects.create(
            user=request.user,
            mood=mood,
            note=note,
        )
        return JsonResponse({
            'status': 'ok',
            'mood': mood,
            'id': entry.id,
            'created_at': entry.created_at.isoformat(),
        })
    except (json.JSONDecodeError, KeyError) as exc:
        logger.error('api_save_mood error: %s', exc)
        return JsonResponse({'error': 'Bad request.'}, status=400)


@login_required
def api_get_music(request):
    """GET /api/music/?mood=happy — return curated playlists for a mood."""
    mood = request.GET.get('mood', 'happy').lower().strip()
    playlists = get_playlists_for_mood(mood)
    return JsonResponse({'mood': mood, 'playlists': playlists})


@login_required
def api_mood_history(request):
    """GET /api/history/ — return the last 20 mood entries for the user."""
    entries = MoodEntry.objects.filter(user=request.user).order_by('-created_at')[:20]
    data = [
        {
            'id': e.id,
            'mood': e.mood,
            'note': e.note,
            'created_at': e.created_at.isoformat(),
        }
        for e in entries
    ]
    return JsonResponse({'entries': data})


@login_required
@require_POST
def api_ai_recommend(request):
    """POST /api/ai/ — generate AI mood + music recommendations."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        current_mood = data.get('current_mood', '').strip()

        if not message:
            return JsonResponse({'error': 'Message is required.'}, status=400)
        if len(message) > 500:
            return JsonResponse({'error': 'Message too long (max 500 chars).'}, status=400)

        result = get_ai_recommendations(message, current_mood)
        return JsonResponse({'status': 'ok', 'data': result})

    except (json.JSONDecodeError, KeyError) as exc:
        logger.error('api_ai_recommend error: %s', exc)
        return JsonResponse({'error': 'Bad request.'}, status=400)


@login_required
@require_POST
def api_save_track(request):
    """POST /api/save-track/ — bookmark a track/playlist."""
    try:
        data = json.loads(request.body)
        track = SavedTrack.objects.create(
            user=request.user,
            mood=data.get('mood', ''),
            title=data.get('title', '')[:200],
            artist=data.get('artist', '')[:200],
            spotify_url=data.get('spotify_url', '')[:500],
            embed_url=data.get('embed_url', '')[:500],
            artwork_url=data.get('artwork_url', '')[:500],
        )
        return JsonResponse({'status': 'ok', 'id': track.id})
    except Exception as exc:
        logger.error('api_save_track error: %s', exc)
        return JsonResponse({'error': 'Could not save track.'}, status=400)


@login_required
def api_saved_tracks(request):
    """GET /api/saved-tracks/ — return the user's bookmarked tracks."""
    tracks = SavedTrack.objects.filter(user=request.user).order_by('-saved_at')[:50]
    data = [
        {
            'id': t.id,
            'mood': t.mood,
            'title': t.title,
            'artist': t.artist,
            'spotify_url': t.spotify_url,
            'embed_url': t.embed_url,
            'artwork_url': t.artwork_url,
            'saved_at': t.saved_at.isoformat(),
        }
        for t in tracks
    ]
    return JsonResponse({'tracks': data})


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _time_greeting() -> str:
    hour = timezone.localtime(timezone.now()).hour
    if hour < 12:
        return 'Good morning'
    if hour < 17:
        return 'Good afternoon'
    return 'Good evening'
