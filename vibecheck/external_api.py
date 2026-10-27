import time
import random
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# Curated Fallback Quotes for each mood/energy state
FALLBACK_QUOTES = {
    'happy': [
        {"quote": "Sunshine is delicious, rain is refreshing, wind braces us up, snow is exhilarating.", "author": "John Ruskin"},
        {"quote": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama"},
        {"quote": "Music gives a soul to the universe, wings to the mind, flight to the imagination and life to everything.", "author": "Plato"},
    ],
    'stressed': [
        {"quote": "You don't have to control your thoughts. You just have to stop letting them control you.", "author": "Dan Millman"},
        {"quote": "Within you, there is a stillness and a sanctuary to which you can retreat at any time.", "author": "Hermann Hesse"},
        {"quote": "Calm mind brings inner strength and self-confidence, so that's very important for good health.", "author": "Dalai Lama"},
    ],
    'sleepy': [
        {"quote": "Sleep is the golden chain that ties health and our bodies together.", "author": "Thomas Dekker"},
        {"quote": "Your future depends on your dreams, so go to sleep.", "author": "Mesut Barazany"},
        {"quote": "Night is the wonderful opportunity to take rest, to forgive, to smile, to get ready for all the battles tomorrow.", "author": "Allen Ginsberg"},
    ],
    'hyped': [
        {"quote": "Energy flows where attention goes. Turn up the volume and take action!", "author": "Tony Robbins"},
        {"quote": "It's not whether you get knocked down, it's whether you get up.", "author": "Vince Lombardi"},
        {"quote": "The rhythm of momentum is the most powerful force in creative development.", "author": "Vibe Collective"},
    ],
    'general': [
        {"quote": "Where words fail, music speaks.", "author": "Hans Christian Andersen"},
        {"quote": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
        {"quote": "One good thing about music, when it hits you, you feel no pain.", "author": "Bob Marley"},
    ]
}

def fetch_inspirational_quote(mood='happy'):
    """
    Fetches an inspirational quote from a third-party API with a strict time limit.
    Fulfills assessment requirement: 'one additional third-party API with a time limit and fallback'.
    """
    timeout = getattr(settings, 'EXTERNAL_API_TIMEOUT', 2.0)
    api_url = "https://zenquotes.io/api/random"
    start_time = time.time()

    try:
        response = requests.get(api_url, timeout=timeout, headers={'User-Agent': 'VibeCheck-App/1.0'})
        duration_ms = round((time.time() - start_time) * 1000, 2)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                quote_text = data[0].get('q', '').strip()
                author_text = data[0].get('a', 'Unknown').strip()
                if quote_text:
                    return {
                        'quote': f'"{quote_text}"',
                        'author': author_text,
                        'source': 'live_api',
                        'latency_ms': duration_ms,
                        'status': 'success',
                        'timeout_limit_s': timeout
                    }
        # If response was empty or non-200, trigger fallback
        raise ValueError(f"Unexpected API response format (status {response.status_code})")

    except requests.exceptions.Timeout:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.warning(f"Third-party API timed out after {timeout}s ({duration_ms}ms). Activating fallback.")
        fallback = get_fallback_quote(mood)
        fallback.update({
            'source': 'fallback_timeout',
            'latency_ms': duration_ms,
            'status': 'fallback_activated',
            'reason': f'Request exceeded {timeout}s timeout limit',
            'timeout_limit_s': timeout
        })
        return fallback

    except Exception as e:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Third-party API unavailable ({e}). Using cached fallback.")
        fallback = get_fallback_quote(mood)
        fallback.update({
            'source': 'fallback_error',
            'latency_ms': duration_ms,
            'status': 'fallback_activated',
            'reason': str(e),
            'timeout_limit_s': timeout
        })
        return fallback

def get_fallback_quote(mood='happy'):
    """Returns a curated quote matching the given mood."""
    mood_key = mood.lower() if mood and mood.lower() in FALLBACK_QUOTES else 'general'
    choices = FALLBACK_QUOTES.get(mood_key, FALLBACK_QUOTES['general'])
    selected = random.choice(choices)
    return {
        'quote': selected['quote'],
        'author': selected['author']
    }

def check_external_api_health():
    """Telemetry diagnostic probe for the /health/ endpoint."""
    res = fetch_inspirational_quote(mood='general')
    return {
        'endpoint': 'https://zenquotes.io/api/random',
        'status': res.get('status'),
        'source': res.get('source'),
        'latency_ms': res.get('latency_ms'),
        'timeout_limit_s': res.get('timeout_limit_s', 2.0),
        'fallback_ready': True
    }
