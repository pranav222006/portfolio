from django.db import models
from django.contrib.auth.models import User


class MoodEntry(models.Model):
    """Stores a single mood check-in for a user."""

    MOOD_CHOICES = [
        ('happy',   'Happy ☀️'),
        ('stressed','Stressed 🌧️'),
        ('sleepy',  'Sleepy 🌙'),
        ('hyped',   'Hyped ⚡'),
    ]

    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    mood      = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note      = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mood Entry'
        verbose_name_plural = 'Mood Entries'

    def __str__(self):
        return f'{self.user.username} — {self.mood} @ {self.created_at:%Y-%m-%d %H:%M}'


class SavedTrack(models.Model):
    """Stores a track or playlist that the user bookmarked."""

    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_tracks')
    mood         = models.CharField(max_length=20, blank=True)
    title        = models.CharField(max_length=200)
    artist       = models.CharField(max_length=200, blank=True)
    spotify_url  = models.URLField(blank=True)
    embed_url    = models.URLField(blank=True)
    artwork_url  = models.URLField(blank=True)
    saved_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']
        verbose_name = 'Saved Track'
        verbose_name_plural = 'Saved Tracks'

    def __str__(self):
        return f'{self.user.username} — {self.title}'
