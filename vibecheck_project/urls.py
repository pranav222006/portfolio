"""
URL configuration for vibecheck_project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vibecheck.urls')),
]

# Custom Error Handlers for 404 and 500
handler404 = 'vibecheck.views.custom_404'
handler500 = 'vibecheck.views.custom_500'
