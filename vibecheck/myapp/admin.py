from django.contrib import admin
from .models import MoodEntry, SavedTrack


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display  = ('user', 'mood', 'created_at', 'note')
    list_filter   = ('mood', 'created_at')
    search_fields = ('user__username', 'note')
    readonly_fields = ('created_at',)
    ordering      = ('-created_at',)


@admin.register(SavedTrack)
class SavedTrackAdmin(admin.ModelAdmin):
    list_display  = ('user', 'title', 'artist', 'mood', 'saved_at')
    list_filter   = ('mood',)
    search_fields = ('user__username', 'title', 'artist')
    readonly_fields = ('saved_at',)
