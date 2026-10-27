"""myapp URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────────────────────
    path('',        views.login_view,    name='home'),
    path('login/',  views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view,   name='logout'),

    # ── Pages ─────────────────────────────────────────────────────────────────
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('history/',   views.history_view,   name='history'),

    # ── JSON API ──────────────────────────────────────────────────────────────
    path('api/save-mood/',    views.api_save_mood,    name='api_save_mood'),
    path('api/music/',        views.api_get_music,    name='api_get_music'),
    path('api/history/',      views.api_mood_history, name='api_mood_history'),
    path('api/ai/',           views.api_ai_recommend, name='api_ai_recommend'),
    path('api/save-track/',   views.api_save_track,   name='api_save_track'),
    path('api/saved-tracks/', views.api_saved_tracks, name='api_saved_tracks'),
]
