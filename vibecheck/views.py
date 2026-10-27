import json
import uuid
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from .models import FAQ, ErrorCode, SupportTicket
from .external_api import fetch_inspirational_quote, check_external_api_health
from .mongo_service import mongo_service
from .ai_service import ai_assistant
from .middleware import REQUEST_METRICS, RECENT_REQUEST_LOGS


# -----------------------------------------------------------------------------
# PAGE VIEWS (At least 3 pages required; we provide 5 rich pages)
# -----------------------------------------------------------------------------

def home_view(request):
    """
    Page 1: Vibe Check Home & Dashboard
    Interactive mood tuner, dynamic quotes with timeout fallback, Spotify embeds.
    """
    initial_mood = request.GET.get('mood', 'happy')
    # Call third-party API with strict timeout and local fallback
    quote_data = fetch_inspirational_quote(mood=initial_mood)
    
    # Auto-seed check on first visit if DB is empty
    ensure_initial_seed()

    context = {
        'page_title': 'VIBE CHECK — Your Mood. Your Music. Your World.',
        'active_page': 'home',
        'current_mood': initial_mood,
        'quote_data': quote_data,
        'faq_count': FAQ.objects.filter(is_active=True).count(),
        'error_count': ErrorCode.objects.count(),
    }
    return render(request, 'vibecheck/home.html', context)


def faqs_view(request):
    """
    Page 2: FAQ Knowledge Base
    Fulfills requirement: 'A minimum of 10 FAQs, stored in the SQL database and displayed on the FAQ page'
    """
    ensure_initial_seed()
    category = request.GET.get('category', 'all')
    search_query = request.GET.get('q', '').strip()

    faqs = FAQ.objects.filter(is_active=True)
    if category and category != 'all':
        faqs = faqs.filter(category=category)
    if search_query:
        faqs = faqs.filter(question__icontains=search_query) | faqs.filter(answer__icontains=search_query)

    categories = FAQ.CATEGORY_CHOICES

    context = {
        'page_title': 'Frequently Asked Questions — VIBE CHECK',
        'active_page': 'faqs',
        'faqs': faqs,
        'selected_category': category,
        'search_query': search_query,
        'categories': categories,
        'total_faqs': FAQ.objects.filter(is_active=True).count(),
    }
    return render(request, 'vibecheck/faqs.html', context)


def errors_view(request):
    """
    Page 3: Error Codes & System Catalog
    Fulfills requirement: 'A minimum of 8 error codes (400, 401, 403, 404, 429, 500, 503 and one site-specific code)'
    """
    ensure_initial_seed()
    error_codes = ErrorCode.objects.all().order_by('code')

    context = {
        'page_title': 'HTTP & Custom Error Codes — VIBE CHECK',
        'active_page': 'errors',
        'error_codes': error_codes,
        'total_errors': error_codes.count(),
    }
    return render(request, 'vibecheck/errors.html', context)


def tickets_view(request):
    """
    Page 4: Support Tickets Tracker
    Fulfills requirement: 'Support tickets stored in SQL'
    """
    ensure_initial_seed()
    if request.method == 'POST':
        user_name = request.POST.get('user_name', 'Anonymous')
        user_email = request.POST.get('user_email', 'listener@vibecheck.io')
        subject = request.POST.get('subject', 'General Inquiry')
        message = request.POST.get('message', '')

        if message:
            ticket = SupportTicket.objects.create(
                user_name=user_name,
                user_email=user_email,
                subject=subject,
                message=message,
                status='open',
                priority='medium'
            )
            return redirect(f'/tickets/?created={ticket.ticket_id}')

    search_id = request.GET.get('ticket_id', '').strip()
    created_id = request.GET.get('created', '').strip()

    tickets = SupportTicket.objects.all()
    if search_id:
        tickets = tickets.filter(ticket_id__icontains=search_id)

    context = {
        'page_title': 'Support Tickets — VIBE CHECK',
        'active_page': 'tickets',
        'tickets': tickets,
        'search_id': search_id,
        'created_id': created_id,
        'total_tickets': SupportTicket.objects.count(),
        'open_tickets': SupportTicket.objects.filter(status='open').count(),
    }
    return render(request, 'vibecheck/tickets.html', context)


def health_view(request):
    """
    Page 5: Health Check & System Telemetry
    Fulfills requirement: 'Request logging and a health check page'
    """
    # 1. SQL Database Probe
    sql_ok = False
    sql_message = "Unavailable"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
            if row and row[0] == 1:
                sql_ok = True
                sql_message = f"Connected ({connection.vendor.upper()} - {FAQ.objects.count()} FAQs, {ErrorCode.objects.count()} Error Codes)"
    except Exception as e:
        sql_message = f"Error: {e}"

    # 2. MongoDB Probe
    mongo_ok, mongo_msg = mongo_service.check_connection()

    # 3. Third-party API Probe
    external_api_info = check_external_api_health()

    # 4. System Uptime & Request Telemetry
    uptime_seconds = int((datetime.utcnow() - REQUEST_METRICS['start_time']).total_seconds())
    uptime_str = f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s"

    overall_status = "HEALTHY" if (sql_ok and (external_api_info['status'] in ['success', 'fallback_activated'])) else "DEGRADED"

    health_data = {
        'status': overall_status,
        'timestamp': datetime.utcnow().isoformat() + "Z",
        'uptime': uptime_str,
        'database_sql': {
            'status': 'healthy' if sql_ok else 'unhealthy',
            'details': sql_message
        },
        'database_mongodb': {
            'status': 'healthy' if mongo_ok else 'fallback_mode',
            'details': mongo_msg
        },
        'third_party_api': external_api_info,
        'requests_telemetry': {
            'total_requests': REQUEST_METRICS['total_requests'],
            'total_errors': REQUEST_METRICS['total_errors'],
            'recent_logs': list(RECENT_REQUEST_LOGS)
        }
    }

    if request.GET.get('format') == 'json' or request.headers.get('Accept') == 'application/json':
        return JsonResponse(health_data)

    context = {
        'page_title': 'System Health & Telemetry — VIBE CHECK',
        'active_page': 'health',
        'health': health_data,
        'recent_logs': list(RECENT_REQUEST_LOGS),
    }
    return render(request, 'vibecheck/health.html', context)


# -----------------------------------------------------------------------------
# REST & CHAT API ENDPOINTS
# -----------------------------------------------------------------------------

@csrf_exempt
def api_chat(request):
    """
    POST API for the integrated AI Assistant chat widget.
    Processes queries against SQL FAQs and Error Codes, creates tickets when needed,
    and logs interactions to MongoDB.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    user_query = data.get('message', '').strip()
    session_id = data.get('session_id', 'session_' + uuid.uuid4().hex[:8])
    user_name = data.get('user_name', 'Listener')
    user_email = data.get('user_email', '')
    current_mood = data.get('mood', 'happy')

    if not user_query:
        return JsonResponse({'error': 'Message parameter is required'}, status=400)

    # Process query through AI pipeline
    result = ai_assistant.process_query(
        user_query=user_query,
        session_id=session_id,
        user_name=user_name,
        user_email=user_email,
        current_mood=current_mood
    )

    return JsonResponse({
        'success': True,
        'session_id': session_id,
        'response': result['response'],
        'source': result['source'],
        'ticket_id': result.get('ticket_id'),
        'timestamp': datetime.utcnow().strftime('%H:%M')
    })


@csrf_exempt
def api_feedback(request):
    """
    POST API for logging chat rating/feedback directly into MongoDB.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    session_id = data.get('session_id', 'anonymous')
    message_id = data.get('message_id', str(uuid.uuid4()))
    rating = data.get('rating', 'positive')
    comments = data.get('comments', '')

    success = mongo_service.save_feedback(
        session_id=session_id,
        message_id=message_id,
        rating=rating,
        comments=comments
    )

    return JsonResponse({'success': success, 'message': 'Feedback recorded in MongoDB.'})


@csrf_exempt
def api_quote(request):
    """
    Returns third-party inspirational quote with time limit and fallback info.
    """
    mood = request.GET.get('mood', 'happy')
    data = fetch_inspirational_quote(mood=mood)
    return JsonResponse(data)


# -----------------------------------------------------------------------------
# ERROR SIMULATION & CUSTOM ERROR HANDLERS (404 and 500 with "Ask the Assistant")
# -----------------------------------------------------------------------------

def test_error_trigger(request):
    """
    Developer diagnostic view to test error codes and custom error pages.
    Usage: /test-error/?code=404 or ?code=500 or ?code=418
    """
    code = request.GET.get('code', '404')
    if code == '400':
        return HttpResponseBadRequest("Error 400: Bad Request simulation")
    elif code == '401':
        return HttpResponse("Error 401: Unauthorized access", status=401)
    elif code == '403':
        return HttpResponseForbidden("Error 403: Forbidden access")
    elif code == '404':
        raise Http404("Simulated 404 Page Not Found")
    elif code == '429':
        return HttpResponse("Error 429: Too Many Requests (Rate limit exceeded)", status=429)
    elif code == '500':
        raise Exception("Simulated 500 Internal Server Error for testing custom 500 page")
    elif code == '503':
        return HttpResponse("Error 503: Service Temporarily Unavailable", status=503)
    elif code == '418':
        return HttpResponse("Error 418: VIBE MISMATCH (Energy Out of Range)", status=418)
    return HttpResponse(f"Testing Error Code: {code}", status=int(code))


def custom_404(request, exception=None):
    """
    Custom 404 Handler.
    Fulfills requirement: 'Custom 404 and 500 pages with an "Ask the assistant" option'
    """
    context = {
        'page_title': '404 — Page Not Found | VIBE CHECK',
        'requested_url': request.path,
        'error_code': 404,
        'error_title': 'Page Not Found',
        'assistant_prompt': f"Why did I get a 404 error when visiting {request.path}?",
    }
    return render(request, '404.html', context, status=404)


def custom_500(request):
    """
    Custom 500 Handler.
    Fulfills requirement: 'Custom 404 and 500 pages with an "Ask the assistant" option'
    """
    context = {
        'page_title': '500 — Internal Server Error | VIBE CHECK',
        'error_code': 500,
        'error_title': 'Internal Server Error',
        'assistant_prompt': "Explain Error 500 Internal Server Error and help me resolve it.",
    }
    return render(request, '500.html', context, status=500)


# -----------------------------------------------------------------------------
# AUTO-SEED HELPER
# -----------------------------------------------------------------------------
def ensure_initial_seed():
    """Seeds DB automatically if FAQs or ErrorCodes are missing."""
    try:
        if FAQ.objects.count() == 0 or ErrorCode.objects.count() == 0:
            from django.core.management import call_command
            call_command('seed_data')
    except Exception:
        pass
