"""
ai_service.py — AI-powered mood recommendations.

Uses Google Gemini if GEMINI_API_KEY is set in environment.
Falls back to a curated rule-based system when no key is present.
API keys are NEVER sent to the browser.
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

# ─── Rule-based fallback data ─────────────────────────────────────────────────
FALLBACK_DATA = {
    'happy': {
        'mood_suggestion': 'happy',
        'response': "You're radiating great energy! Let's amplify those good vibes and make this moment unforgettable.",
        'genres': ['Feel-good Pop', 'Indie Pop', 'Upbeat R&B', 'Dance Pop'],
        'activities': [
            '☀️ Share your mood — send a kind message to someone you care about',
            '🎉 Channel your energy into a creative project or hobby',
            '🚶 Take a sunny walk and appreciate the little joys around you',
        ],
        'quote': '"Happiness is not something ready made. It comes from your own actions." — Dalai Lama',
        'explanation': 'Your positive energy deserves music and activities that celebrate and sustain it. These recommendations are designed to keep your spirits high and help you spread joy.',
        'playlists': ['Happy Hits!', 'Good Vibes', 'Summer Hits'],
    },
    'stressed': {
        'mood_suggestion': 'stressed',
        'response': "I hear you — stress can feel overwhelming. Let's find your calm and give your mind some breathing room.",
        'genres': ['Lo-Fi Hip Hop', 'Ambient', 'Peaceful Piano', 'Nature Sounds'],
        'activities': [
            '🌬️ Try box breathing: inhale 4 counts, hold 4, exhale 4, hold 4',
            '📝 Write down three things making you stressed, then three things you can control',
            '🧘 Take a 5-minute stretch break away from your screen',
        ],
        'quote': '"You don\'t have to control your thoughts; you just have to stop letting them control you." — Dan Millman',
        'explanation': 'When stressed, your nervous system needs grounding. Slow-tempo music with minimal lyrics reduces cortisol, while breathing exercises activate the parasympathetic nervous system.',
        'playlists': ['Calm Vibes', 'Lo-Fi Beats', 'Peaceful Piano'],
    },
    'sleepy': {
        'mood_suggestion': 'sleepy',
        'response': "Your body is telling you it needs rest. Honour that signal — sleep is where your mind and body heal.",
        'genres': ['Ambient', 'Acoustic', 'Sleep Sounds', 'Binaural Beats'],
        'activities': [
            '🌙 Dim your screen brightness and switch to night mode',
            '📵 Put your phone face-down for the next 30 minutes',
            '🛁 Try a short wind-down ritual: herbal tea, light stretching, slow breathing',
        ],
        'quote': '"Sleep is the best meditation." — Dalai Lama',
        'explanation': 'Soft, slow-tempo music below 60 BPM naturally syncs with a resting heart rate and eases your brain into sleep mode. Pair that with reduced stimulation and you\'ll drift off faster.',
        'playlists': ['Sleep', 'Night Owl', 'Deep Sleep'],
    },
    'hyped': {
        'mood_suggestion': 'hyped',
        'response': "That energy is ELECTRIC! Let's channel it into something legendary — you're unstoppable right now.",
        'genres': ['Hip-Hop', 'Electronic / EDM', 'Dance Pop', 'High-BPM Workout'],
        'activities': [
            '⚡ Knock out your most important or challenging task RIGHT NOW',
            '🏋️ Do a quick 10-minute workout — push-ups, squats, jumping jacks',
            '🎯 Set one bold goal for today and make real progress on it',
        ],
        'quote': '"The secret of getting ahead is getting started." — Mark Twain',
        'explanation': 'High-BPM music (140–160 BPM) matches your elevated energy and enhances performance and focus. Pair that with action-oriented tasks and you\'ll ride this wave at peak capacity.',
        'playlists': ['Beast Mode', 'Power Hour', 'Motivation Mix'],
    },
}

MOOD_KEYWORDS = {
    'happy': ['happy', 'joy', 'great', 'excited', 'good', 'wonderful', 'amazing', 'love', 'cheer', 'bliss', 'smile'],
    'stressed': ['stress', 'anxious', 'anxiety', 'worried', 'overwhelm', 'nervous', 'panic', 'tense', 'pressure', 'burn', 'exhaust'],
    'sleepy': ['sleep', 'sleepy', 'tired', 'fatigue', 'drowsy', 'rest', 'nap', 'exhausted', 'yawn', 'groggy', 'drain'],
    'hyped': ['hyped', 'energy', 'pump', 'motivat', 'excited', 'fire', 'ready', 'power', 'unstoppable', 'let\'s go', 'workout', 'gym'],
}


def _detect_mood_from_text(text: str) -> str:
    """Simple keyword-based mood detection from user message."""
    text_lower = text.lower()
    scores = {mood: 0 for mood in MOOD_KEYWORDS}
    for mood, keywords in MOOD_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[mood] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'happy'


def _rule_based_response(user_message: str, current_mood: str = '') -> dict:
    """Generate a rule-based recommendation without any external API."""
    mood = current_mood if current_mood else _detect_mood_from_text(user_message)
    data = FALLBACK_DATA.get(mood, FALLBACK_DATA['happy'])
    return {
        'mood_suggestion': data['mood_suggestion'],
        'response': data['response'],
        'genres': data['genres'],
        'activities': data['activities'],
        'quote': data['quote'],
        'explanation': data['explanation'],
        'playlists': data['playlists'],
        'source': 'rule-based',
    }


def _gemini_response(user_message: str, current_mood: str, api_key: str) -> dict:
    """Call Google Gemini API for AI recommendations."""
    try:
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""You are Vibe AI, an empathetic mood and music companion inside a web app called VIBE CHECK.

User message: "{user_message}"
Current mood context: {current_mood if current_mood else 'not set yet'}

Respond with a JSON object (no markdown, no code fences) containing exactly these keys:
{{
  "mood_suggestion": "<one of: happy, stressed, sleepy, hyped>",
  "response": "<2-3 sentences of warm, empathetic acknowledgment>",
  "genres": ["<genre 1>", "<genre 2>", "<genre 3>", "<genre 4>"],
  "activities": ["<activity 1 with emoji>", "<activity 2 with emoji>", "<activity 3 with emoji>"],
  "quote": "<an original or well-known motivational/calming quote with attribution>",
  "explanation": "<1-2 sentences explaining why these recommendations fit>",
  "playlists": ["<playlist name 1>", "<playlist name 2>", "<playlist name 3>"]
}}

Keep the response warm, conversational and appropriate for a college student. 
Do NOT diagnose medical or mental health conditions.
Respond ONLY with the JSON object."""

        result = model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 512},
        )
        raw = result.text.strip()
        # Strip markdown code fences if Gemini wraps output
        if raw.startswith('```'):
            raw = raw.split('```')[1]
            if raw.startswith('json'):
                raw = raw[4:]
        data = json.loads(raw)
        data['source'] = 'gemini'
        return data

    except ImportError:
        logger.warning('google-generativeai not installed; using rule-based fallback.')
        return _rule_based_response(user_message, current_mood)
    except Exception as exc:
        logger.error('Gemini API error: %s', exc)
        return _rule_based_response(user_message, current_mood)


def get_ai_recommendations(user_message: str, current_mood: str = '') -> dict:
    """
    Public entry point. Tries Gemini if GEMINI_API_KEY is configured,
    otherwise falls back to rule-based recommendations.
    """
    api_key = os.environ.get('GEMINI_API_KEY', '')
    if api_key:
        return _gemini_response(user_message, current_mood, api_key)
    return _rule_based_response(user_message, current_mood)
