from django.apps import AppConfig


class VibecheckConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vibecheck'
    verbose_name = 'Vibe Check & AI Assistant'

    def ready(self):
        # Optional startup initializations
        pass
