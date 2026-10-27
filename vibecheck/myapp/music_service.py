"""
music_service.py — Curated Spotify playlist data per mood.

Uses real Spotify playlist embed URLs — no API key required.
Each playlist is publicly accessible on Spotify.
"""

# ─── Curated playlists per mood ──────────────────────────────────────────────
MOOD_PLAYLISTS = {
    'happy': [
        {
            'id': 'happy_1',
            'title': 'Happy Hits!',
            'artist': 'Spotify',
            'description': 'Feel-good pop anthems to boost your mood instantly.',
            'mood': 'happy',
            'genre': 'Pop',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000027ea4d505212b9de1f72b0c4e',
        },
        {
            'id': 'happy_2',
            'title': 'Good Vibes',
            'artist': 'Spotify',
            'description': 'Upbeat indie pop and feel-good tracks.',
            'mood': 'happy',
            'genre': 'Indie Pop',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f00000002bd0e19e810bb4b55ab164a95',
        },
        {
            'id': 'happy_3',
            'title': 'Summer Hits',
            'artist': 'Spotify',
            'description': 'Sunny vibes and carefree summer anthems.',
            'mood': 'happy',
            'genre': 'Pop / Dance',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX4o1oenSJRJd',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX4o1oenSJRJd?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f00000002f21a0a4f56e7fe635e4f0f6c',
        },
        {
            'id': 'happy_4',
            'title': 'Dance Pop Hits',
            'artist': 'Spotify',
            'description': 'Pop bangers made for moving and grooving.',
            'mood': 'happy',
            'genre': 'Dance Pop',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DXaXB8fQg7Xwb',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DXaXB8fQg7Xwb?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f00000002f4d181cad8be61a2b9e5b6e6',
        },
    ],
    'stressed': [
        {
            'id': 'stressed_1',
            'title': 'Calm Vibes',
            'artist': 'Spotify',
            'description': 'Soothing instrumental and ambient music to ease tension.',
            'mood': 'stressed',
            'genre': 'Ambient',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwq3LiO?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f00000002df9b4ef9c19c85c01aecaa01',
        },
        {
            'id': 'stressed_2',
            'title': 'Lo-Fi Beats',
            'artist': 'Spotify',
            'description': 'Chill lo-fi hip-hop beats for focus and relaxation.',
            'mood': 'stressed',
            'genre': 'Lo-Fi',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DWWQRwui0ExPn?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000025eb38e8498b1424ab0849af7',
        },
        {
            'id': 'stressed_3',
            'title': 'Peaceful Piano',
            'artist': 'Spotify',
            'description': 'Gentle piano melodies for a calmer mind.',
            'mood': 'stressed',
            'genre': 'Classical / Piano',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwq3LiO?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000025eb38e8498b1424ab0849af7',
        },
        {
            'id': 'stressed_4',
            'title': 'Nature Sounds',
            'artist': 'Spotify',
            'description': 'Rain, ocean waves and forest ambience.',
            'mood': 'stressed',
            'genre': 'Ambient / Nature',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX4wta20PHzhB',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX4wta20PHzhB?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f0000000260d6e9a38d9f739b4ea1dde0',
        },
    ],
    'sleepy': [
        {
            'id': 'sleepy_1',
            'title': 'Sleep',
            'artist': 'Spotify',
            'description': 'Soft instrumental and acoustic for drifting off.',
            'mood': 'sleepy',
            'genre': 'Sleep / Ambient',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DWZd79rJ6a7lp',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DWZd79rJ6a7lp?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000021aba648f9df19a6c5a5c4d48',
        },
        {
            'id': 'sleepy_2',
            'title': 'Night Owl',
            'artist': 'Spotify',
            'description': 'Mellow late-night tracks to wind down.',
            'mood': 'sleepy',
            'genre': 'Indie / Acoustic',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX2UgsUIg75Vg',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX2UgsUIg75Vg?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000026c7e0a2f28db2b4fae3e24a8',
        },
        {
            'id': 'sleepy_3',
            'title': 'Deep Sleep',
            'artist': 'Spotify',
            'description': 'Ultra-relaxing binaural and ambient sounds.',
            'mood': 'sleepy',
            'genre': 'Binaural / Meditation',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DWZd79rJ6a7lp',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DWZd79rJ6a7lp?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000021aba648f9df19a6c5a5c4d48',
        },
        {
            'id': 'sleepy_4',
            'title': 'Acoustic Lullabies',
            'artist': 'Spotify',
            'description': 'Soft acoustic guitar and dreamy vocals.',
            'mood': 'sleepy',
            'genre': 'Acoustic',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX2UgsUIg75Vg',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX2UgsUIg75Vg?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000026c7e0a2f28db2b4fae3e24a8',
        },
    ],
    'hyped': [
        {
            'id': 'hyped_1',
            'title': 'Beast Mode',
            'artist': 'Spotify',
            'description': 'High-energy bangers for maximum intensity.',
            'mood': 'hyped',
            'genre': 'Hip-Hop / Rap',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7AP?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000028b60a94e14d5c6b5a62eb8c3',
        },
        {
            'id': 'hyped_2',
            'title': 'Power Hour',
            'artist': 'Spotify',
            'description': 'Electrifying electronic and dance tracks.',
            'mood': 'hyped',
            'genre': 'Electronic / EDM',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX32NsLKyzScr',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX32NsLKyzScr?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000026d8f9ee9e88b7da00b3e3a2f',
        },
        {
            'id': 'hyped_3',
            'title': 'Motivation Mix',
            'artist': 'Spotify',
            'description': 'Pump-up tracks for workouts and big tasks.',
            'mood': 'hyped',
            'genre': 'Pop / Dance',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7AP?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f000000028b60a94e14d5c6b5a62eb8c3',
        },
        {
            'id': 'hyped_4',
            'title': 'Party Hits',
            'artist': 'Spotify',
            'description': 'Chart-topping party anthems for full energy.',
            'mood': 'hyped',
            'genre': 'Pop / Electronic',
            'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DXaXB8fQg7Xwb',
            'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DXaXB8fQg7Xwb?utm_source=generator&theme=0',
            'artwork': 'https://i.scdn.co/image/ab67706f00000002f4d181cad8be61a2b9e5b6e6',
        },
    ],
}


def get_playlists_for_mood(mood: str) -> list:
    """Return the curated playlist list for a given mood."""
    mood = mood.lower().strip()
    return MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS['happy'])


def get_all_moods() -> list:
    return list(MOOD_PLAYLISTS.keys())
