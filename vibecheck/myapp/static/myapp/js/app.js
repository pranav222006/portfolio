/**
 * VIBE CHECK — app.js
 * Mood engine, theme switcher, AI companion, music cards, sidebar, history.
 */

'use strict';

/* ═══════════════════════════════════════════════════════════════════════════
   MOOD DATA (client-side config — no secrets)
   ═══════════════════════════════════════════════════════════════════════════ */
const MOOD_CONFIG = {
  happy: {
    emoji: '☀️',
    label: 'HAPPY',
    title: 'Riding the sunshine wave ☀️',
    subtitle: 'You\'re glowing — let\'s amplify those good vibes.',
    quote: '"Happiness is not something ready made. It comes from your own actions." — Dalai Lama',
    activities: [
      '☀️ Share your mood — send a kind message to someone you care about',
      '🎉 Channel your energy into a creative project or hobby',
      '🚶 Take a sunny walk and appreciate the little joys around you',
    ],
    musicTitle: '🎵 Your Happy Soundtrack',
    musicSubtitle: 'Feel-good pop, indie and dance — made for moments like this',
  },
  stressed: {
    emoji: '🌧️',
    label: 'STRESSED',
    title: 'Let\'s find your calm 🌧️',
    subtitle: 'You\'re not alone. Take a breath — relief is on its way.',
    quote: '"You don\'t have to control your thoughts; you just have to stop letting them control you." — Dan Millman',
    activities: [
      '🌬️ Try box breathing: inhale 4, hold 4, exhale 4, hold 4',
      '📝 Write down three stressors, then three things within your control',
      '🧘 5-minute stretch break away from your screen',
    ],
    musicTitle: '🎵 Your Calming Soundtrack',
    musicSubtitle: 'Lo-fi, ambient and peaceful piano to ease the tension',
  },
  sleepy: {
    emoji: '🌙',
    label: 'SLEEPY',
    title: 'Wind down & recharge 🌙',
    subtitle: 'Your body is asking for rest. Honor that signal.',
    quote: '"Sleep is the best meditation." — Dalai Lama',
    activities: [
      '🌙 Dim your screen brightness and switch to night mode',
      '📵 Put your phone face-down for the next 30 minutes',
      '🛁 Try a wind-down ritual: herbal tea, light stretch, slow breathing',
    ],
    musicTitle: '🎵 Your Sleep Soundtrack',
    musicSubtitle: 'Ambient, acoustic and gentle melodies to drift you off',
  },
  hyped: {
    emoji: '⚡',
    label: 'HYPED',
    title: 'You\'re absolutely electric ⚡',
    subtitle: 'Channel this energy — you\'re unstoppable right now.',
    quote: '"The secret of getting ahead is getting started." — Mark Twain',
    activities: [
      '⚡ Tackle your most important task RIGHT NOW',
      '🏋️ Do a quick 10-minute workout — push-ups, squats, jumping jacks',
      '🎯 Set one bold goal for today and make real progress on it',
    ],
    musicTitle: '🎵 Your Hype Soundtrack',
    musicSubtitle: 'Hip-hop, EDM and dance bangers for maximum intensity',
  },
};

const MOODS = Object.keys(MOOD_CONFIG);

/* ═══════════════════════════════════════════════════════════════════════════
   STATE
   ═══════════════════════════════════════════════════════════════════════════ */
let currentMood = (window.VIBE_DATA && window.VIBE_DATA.currentMood) || '';
let aiSuggestedMood = '';

/* ═══════════════════════════════════════════════════════════════════════════
   UTILITIES
   ═══════════════════════════════════════════════════════════════════════════ */
function getCsrf() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) return meta.content;
  const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
  return cookie ? cookie.trim().split('=')[1] : '';
}

async function postJSON(url, data) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrf(),
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

async function getJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

function el(id) { return document.getElementById(id); }

function showToast(message) {
  const toast = el('mood-toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.remove('hidden');
  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => toast.classList.add('hidden'), 4000);
}

/* ═══════════════════════════════════════════════════════════════════════════
   MOOD ENGINE
   ═══════════════════════════════════════════════════════════════════════════ */

/**
 * Apply a mood theme to the page and update all UI elements.
 * @param {string} mood - one of 'happy','stressed','sleepy','hyped'
 * @param {boolean} save - whether to persist to the server
 */
async function applyMood(mood, save = true) {
  if (!MOODS.includes(mood)) return;
  const config = MOOD_CONFIG[mood];
  const body = document.body;

  // 1. Theme class
  MOODS.forEach(m => body.classList.remove(`mood-${m}`));
  body.classList.add(`mood-${mood}`);
  document.documentElement.setAttribute('data-mood', mood);
  currentMood = mood;

  // 2. Mark selected card
  document.querySelectorAll('.mood-card').forEach(card => {
    card.classList.toggle('selected', card.dataset.mood === mood);
  });

  // 3. Update hero
  const heroTitle    = el('hero-title');
  const heroSubtitle = el('hero-subtitle');
  const heroQuoteBox = el('hero-quote-box');
  const heroQuote    = el('hero-quote');
  if (heroTitle)    heroTitle.textContent = config.title;
  if (heroSubtitle) heroSubtitle.textContent = config.subtitle;
  if (heroQuoteBox && heroQuote) {
    heroQuote.textContent = config.quote;
    heroQuoteBox.classList.remove('hidden');
  }

  // 4. Current mood badge in topbar
  const badge   = el('current-mood-badge');
  const badgeEmoji = el('current-mood-emoji');
  const badgeName  = el('current-mood-name');
  if (badge) {
    badge.classList.remove('hidden');
    if (badgeEmoji) badgeEmoji.textContent = config.emoji;
    if (badgeName)  badgeName.textContent  = config.label;
  }

  // 5. Show Change My Mood button
  const changeBtn = el('change-mood-btn');
  if (changeBtn) changeBtn.classList.remove('hidden');

  // 6. Activities
  renderActivities(config.activities);

  // 7. Music section header
  const musicTitle    = el('music-section-title');
  const musicSubtitle = el('music-section-subtitle');
  if (musicTitle)    musicTitle.textContent    = config.musicTitle;
  if (musicSubtitle) musicSubtitle.textContent = config.musicSubtitle;

  // 8. Load music
  await loadMusic(mood);

  // 9. Save to server
  if (save) {
    try {
      await postJSON('/api/save-mood/', { mood });
      showToast(`Your vibe is now: ${config.emoji} ${config.label} — saved!`);
    } catch (err) {
      showToast(`Vibe set to ${config.label}! (Could not save: ${err.message})`);
    }
  } else {
    showToast(`Your vibe is now: ${config.emoji} ${config.label}`);
  }
}

function renderActivities(activities) {
  const section = el('activities-section');
  const grid    = el('activities-grid');
  if (!section || !grid) return;
  grid.innerHTML = activities.map(a =>
    `<div class="activity-card">${a}</div>`
  ).join('');
  section.classList.remove('hidden');
}

/* ═══════════════════════════════════════════════════════════════════════════
   MUSIC
   ═══════════════════════════════════════════════════════════════════════════ */

async function loadMusic(mood) {
  const grid    = el('music-grid');
  const loading = el('music-loading');
  if (!grid) return;

  loading && loading.classList.remove('hidden');
  grid.innerHTML = '';

  try {
    const data = await getJSON(`/api/music/?mood=${encodeURIComponent(mood)}`);
    loading && loading.classList.add('hidden');
    renderMusicCards(data.playlists || []);
  } catch (err) {
    loading && loading.classList.add('hidden');
    grid.innerHTML = `<p style="color:var(--text-muted);padding:24px;">Could not load music. Check your connection.</p>`;
  }
}

function renderMusicCards(playlists) {
  const grid = el('music-grid');
  if (!grid) return;

  grid.innerHTML = playlists.map(p => `
    <article class="music-card" data-playlist-id="${escHtml(p.id)}" data-embed-url="${escHtml(p.embed_url)}" data-spotify-url="${escHtml(p.spotify_url)}">
      <div class="music-card-art">
        <img
          src="${escHtml(p.artwork)}"
          alt="${escHtml(p.title)} artwork"
          loading="lazy"
          onerror="this.src='https://placehold.co/300x300/1B1630/A970FF?text=🎵'"
        />
        <div class="music-card-overlay">
          <button class="play-btn open-embed-btn" data-embed="${escHtml(p.embed_url)}" data-title="${escHtml(p.title)}" aria-label="Play ${escHtml(p.title)}">
            <svg viewBox="0 0 24 24" fill="currentColor"><polygon points="5,3 19,12 5,21"/></svg>
          </button>
        </div>
      </div>
      <div class="music-card-info">
        <div class="music-card-genre">${escHtml(p.genre)}</div>
        <h3 class="music-card-title">${escHtml(p.title)}</h3>
        <p class="music-card-desc">${escHtml(p.description)}</p>
        <div class="music-card-actions">
          <a href="${escHtml(p.spotify_url)}" target="_blank" rel="noopener noreferrer" class="btn btn--spotify btn--sm">
            <svg class="spotify-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
            </svg>
            Open in Spotify
          </a>
          <button class="btn btn--icon btn--sm save-track-btn"
            aria-label="Save ${escHtml(p.title)}"
            data-title="${escHtml(p.title)}"
            data-artist="${escHtml(p.artist)}"
            data-mood="${escHtml(p.mood)}"
            data-spotify="${escHtml(p.spotify_url)}"
            data-embed="${escHtml(p.embed_url)}"
            data-art="${escHtml(p.artwork)}">
            🔖
          </button>
        </div>
      </div>
    </article>
  `).join('');

  // Bind new buttons
  bindMusicCardEvents();
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function bindMusicCardEvents() {
  document.querySelectorAll('.open-embed-btn').forEach(btn => {
    btn.addEventListener('click', () => openEmbed(btn.dataset.embed, btn.dataset.title));
  });
  document.querySelectorAll('.save-track-btn').forEach(btn => {
    btn.addEventListener('click', () => saveTrack(btn));
  });
}

/* ─── Spotify embed modal ──────────────────────────────────────────────────── */
function openEmbed(embedUrl, title) {
  const modal     = el('embed-modal');
  const iframe    = el('spotify-embed');
  const modalTitle= document.getElementById('embed-modal-title');
  if (!modal || !iframe) return;

  if (modalTitle) modalTitle.textContent = title || 'Now Playing';
  iframe.src = embedUrl;
  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';

  // Trap focus
  setTimeout(() => {
    const closeBtn = el('embed-close-btn');
    if (closeBtn) closeBtn.focus();
  }, 100);
}

function closeEmbed() {
  const modal  = el('embed-modal');
  const iframe = el('spotify-embed');
  if (modal)  modal.classList.add('hidden');
  if (iframe) iframe.src = '';
  document.body.style.overflow = '';
}

/* ─── Save track ───────────────────────────────────────────────────────────── */
async function saveTrack(btn) {
  try {
    await postJSON('/api/save-track/', {
      title:       btn.dataset.title,
      artist:      btn.dataset.artist,
      mood:        btn.dataset.mood,
      spotify_url: btn.dataset.spotify,
      embed_url:   btn.dataset.embed,
      artwork_url: btn.dataset.art,
    });
    btn.textContent = '✅';
    btn.disabled = true;
    setTimeout(() => { btn.textContent = '🔖'; btn.disabled = false; }, 2000);
  } catch (err) {
    btn.textContent = '❌';
    setTimeout(() => { btn.textContent = '🔖'; }, 2000);
  }
}

/* ═══════════════════════════════════════════════════════════════════════════
   AI COMPANION
   ═══════════════════════════════════════════════════════════════════════════ */

function initAI() {
  const input     = el('ai-message-input');
  const genBtn    = el('ai-generate-btn');
  const clearBtn  = el('ai-clear-btn');
  const counter   = el('ai-char-counter');
  const applyBtn  = el('ai-apply-mood-btn');

  if (!input || !genBtn) return;

  // Character counter
  input.addEventListener('input', () => {
    const len = input.value.length;
    if (counter) counter.textContent = `${len} / 500`;
  });

  // Generate recommendations
  genBtn.addEventListener('click', async () => {
    const message = input.value.trim();
    if (!message) { input.focus(); return; }

    setAILoading(true);
    try {
      const data = await postJSON('/api/ai/', { message, current_mood: currentMood });
      renderAIResponse(data.data);
    } catch (err) {
      showAIError(`Could not get recommendations: ${err.message}`);
    } finally {
      setAILoading(false);
    }
  });

  // Clear
  clearBtn && clearBtn.addEventListener('click', () => {
    const responseDiv = el('ai-response');
    if (responseDiv) responseDiv.classList.add('hidden');
    input.value = '';
    if (counter) counter.textContent = '0 / 500';
  });

  // Apply suggested mood
  applyBtn && applyBtn.addEventListener('click', () => {
    if (aiSuggestedMood) applyMood(aiSuggestedMood);
  });
}

function setAILoading(loading) {
  const btn    = el('ai-generate-btn');
  const btnTxt = btn && btn.querySelector('.btn-text');
  const btnLoad= btn && btn.querySelector('.btn-loader');
  if (btn)     btn.disabled = loading;
  if (btnTxt)  btnTxt.classList.toggle('hidden', loading);
  if (btnLoad) btnLoad.classList.toggle('hidden', !loading);
}

function renderAIResponse(data) {
  const responseDiv = el('ai-response');
  if (!responseDiv) return;

  aiSuggestedMood = data.mood_suggestion || '';

  const setText = (id, text) => { const e = el(id); if (e) e.textContent = text; };

  setText('ai-response-text', data.response || '');
  setText('ai-quote',         data.quote    || '');
  setText('ai-explanation',   data.explanation || '');

  // Source badge
  const badge = el('ai-source-badge');
  if (badge) {
    badge.textContent = data.source === 'gemini' ? '✨ Gemini AI' : '🤖 Smart Recommendations';
  }

  // Genres
  const genresEl = el('ai-genres');
  if (genresEl && data.genres) {
    genresEl.innerHTML = data.genres.map(g =>
      `<span class="ai-genre-tag">${escHtml(g)}</span>`
    ).join('');
  }

  // Activities
  const activitiesEl = el('ai-activities');
  if (activitiesEl && data.activities) {
    activitiesEl.innerHTML = data.activities.map(a =>
      `<li>${escHtml(a)}</li>`
    ).join('');
  }

  // Apply mood button label
  const applyBtn = el('ai-apply-mood-btn');
  if (applyBtn && aiSuggestedMood) {
    const cfg = MOOD_CONFIG[aiSuggestedMood];
    applyBtn.textContent = cfg ? `Apply ${cfg.emoji} ${cfg.label} Mood` : 'Apply Suggested Mood';
    applyBtn.classList.remove('hidden');
  }

  responseDiv.classList.remove('hidden');
  responseDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showAIError(msg) {
  const responseDiv = el('ai-response');
  if (responseDiv) {
    const txt = el('ai-response-text');
    if (txt) txt.textContent = `⚠️ ${msg}`;
    responseDiv.classList.remove('hidden');
  }
}

/* ═══════════════════════════════════════════════════════════════════════════
   SIDEBAR & MOBILE NAV
   ═══════════════════════════════════════════════════════════════════════════ */

function initSidebar() {
  const sidebar  = el('sidebar');
  const hamburger= el('hamburger-btn');
  const overlay  = el('sidebar-overlay');
  if (!sidebar || !hamburger) return;

  const open  = () => {
    sidebar.classList.add('open');
    overlay && overlay.classList.add('visible');
    hamburger.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
  };
  const close = () => {
    sidebar.classList.remove('open');
    overlay && overlay.classList.remove('visible');
    hamburger.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
  };

  hamburger.addEventListener('click', () => sidebar.classList.contains('open') ? close() : open());
  overlay   && overlay.addEventListener('click', close);

  // Close on escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeEmbed(); close(); }
  });
}

/* ═══════════════════════════════════════════════════════════════════════════
   AUTH PAGES
   ═══════════════════════════════════════════════════════════════════════════ */

function initAuth() {
  // Password visibility toggles
  document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = document.getElementById(btn.dataset.target);
      if (!input) return;
      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';
      btn.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
    });
  });

  // Login form loading state
  const loginForm = el('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', () => {
      const btn  = el('login-btn');
      const text = btn && btn.querySelector('.btn-text');
      const load = btn && btn.querySelector('.btn-loader');
      if (text) text.classList.add('hidden');
      if (load) load.classList.remove('hidden');
      if (btn)  btn.disabled = true;
    });
  }

  // Register form loading state
  const registerForm = el('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', () => {
      const btn  = el('register-btn');
      const text = btn && btn.querySelector('.btn-text');
      const load = btn && btn.querySelector('.btn-loader');
      if (text) text.classList.add('hidden');
      if (load) load.classList.remove('hidden');
      if (btn)  btn.disabled = true;
    });
  }
}

/* ═══════════════════════════════════════════════════════════════════════════
   DASHBOARD INIT
   ═══════════════════════════════════════════════════════════════════════════ */

function initDashboard() {
  // Mood card clicks
  document.querySelectorAll('.mood-card').forEach(card => {
    card.addEventListener('click', () => applyMood(card.dataset.mood));
    // Keyboard
    card.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        applyMood(card.dataset.mood);
      }
    });
  });

  // Surprise Me
  const surpriseBtn = el('surprise-btn');
  if (surpriseBtn) {
    surpriseBtn.addEventListener('click', () => {
      const random = MOODS[Math.floor(Math.random() * MOODS.length)];
      applyMood(random);
    });
  }

  // Change My Mood — scroll to mood grid
  const changeBtn = el('change-mood-btn');
  if (changeBtn) {
    changeBtn.addEventListener('click', () => {
      const moodSection = el('mood-section');
      if (moodSection) moodSection.scrollIntoView({ behavior: 'smooth' });
    });
  }

  // Embed modal close
  const closeBtn = el('embed-close-btn');
  if (closeBtn) closeBtn.addEventListener('click', closeEmbed);
  const embedModal = el('embed-modal');
  if (embedModal) {
    embedModal.addEventListener('click', e => {
      if (e.target === embedModal) closeEmbed();
    });
  }

  // Play buttons on initial SSR-rendered cards
  bindMusicCardEvents();

  // Restore previous mood theme without saving
  if (currentMood && MOODS.includes(currentMood)) {
    applyMood(currentMood, false);
  }

  // AI
  initAI();
}

/* ═══════════════════════════════════════════════════════════════════════════
   HISTORY PAGE — animated bars
   ═══════════════════════════════════════════════════════════════════════════ */

function initHistory() {
  // Animate bar fills via IntersectionObserver
  const bars = document.querySelectorAll('.mood-bar-fill');
  if (!bars.length) return;

  // Store the target width then set to 0 for animation
  bars.forEach(bar => {
    const target = bar.style.width;
    bar.dataset.target = target;
    bar.style.width = '0%';
  });

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        bar.style.width = bar.dataset.target || '0%';
        observer.unobserve(bar);
      }
    });
  }, { threshold: 0.1 });

  bars.forEach(bar => observer.observe(bar));
}

/* ═══════════════════════════════════════════════════════════════════════════
   BOOT
   ═══════════════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
  initAuth();
  initSidebar();

  const body = document.body;
  if (body.classList.contains('dashboard-page') && !body.classList.contains('history-page')) {
    initDashboard();
  }
  if (body.classList.contains('history-page')) {
    initHistory();
  }
});
