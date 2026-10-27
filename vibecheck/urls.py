from django.urls import path
from . import views

urlpatterns = [
    # Core Application Pages
    path('', views.home_view, name='home'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('errors/', views.errors_view, name='errors'),
    path('tickets/', views.tickets_view, name='tickets'),
    path('health/', views.health_view, name='health'),

    # REST & Chat APIs
    path('api/chat/', views.api_chat, name='api_chat'),
    path('api/feedback/', views.api_feedback, name='api_feedback'),
    path('api/quote/', views.api_quote, name='api_quote'),

    # Diagnostic Error Route
    path('test-error/', views.test_error_trigger, name='test_error'),
]
