# VIBE CHECK — Mood-Adaptive Music Discovery & AI Assistant Platform

> **Final Assessment: Software Development**  
> **Individual Task Title:** Vibe Check: Responsive Mood-Adaptive Music Streaming Platform with Dual-Database AI Support Assistant  
> **Live Website Link (HTTPS):** `https://vibecheck-final.onrender.com` *(Replace with your live deployment URL)*  
> **GitHub Repository:** `https://github.com/pranav222006/portfolio`  

---

## 📋 Executive Summary & Assessment Compliance Matrix

This project is a production-ready Django web application integrated with a dual-database architecture (SQL + MongoDB), responsive glassmorphic frontend, and an intelligent AI Assistant that answers questions from stored FAQ records, explains standard & site-specific error codes, and automatically logs support tickets in SQL when an inquiry cannot be answered.

| Assessment Requirement | Project Implementation | File / Route Reference |
| :--- | :--- | :--- |
| **Responsive Website with ≥ 3 Pages** | 5 complete, responsive pages with dark neon glassmorphic design: Home/Dashboard, FAQs, Error Codes, Support Tickets, and Health Check | `templates/vibecheck/` (`/`, `/faqs/`, `/errors/`, `/tickets/`, `/health/`) |
| **Chat Widget on Every Page** | Floating interactive AI Assistant widget embedded globally in base template with real-time markdown, quick chips, and feedback | `templates/base.html`, `vibecheck/ai_service.py` |
| **≥ 10 FAQs in SQL & Displayed on Page** | 12 comprehensive FAQs stored in SQL database, filterable by category, searchable, and rendered dynamically | `vibecheck/models.py` (`FAQ`), `/faqs/` |
| **≥ 8 Error Codes (7 standard + 1 custom)** | 8 verified error codes stored in SQL: 400, 401, 403, 404, 429, 500, 503, and custom `418 VIBE_MISMATCH` | `vibecheck/models.py` (`ErrorCode`), `/errors/` |
| **Custom 404 & 500 with "Ask the Assistant"** | Themed 404 & 500 error handlers with a prominent button that auto-opens the assistant with pre-populated error context | `templates/404.html`, `templates/500.html` |
| **AI Assistant (FAQs, Errors & Auto-Tickets)** | RAG-grounded assistant that answers from SQL FAQs, explains error codes, and automatically creates a `SupportTicket` in SQL when unresolved | `vibecheck/ai_service.py`, `vibecheck/views.py` (`api_chat`) |
| **Dual Database Architecture** | **SQL (SQLite/PostgreSQL):** FAQs, Error Codes, Support Tickets.<br>**MongoDB:** Chat interaction logs & user feedback ratings. | `vibecheck/models.py`, `vibecheck/mongo_service.py` |
| **API Keys in Environment Variables** | Configured via `python-dotenv`. Zero hardcoded secrets in codebase. Clean `.gitignore` and `.env.example` provided. | `.env.example`, `.gitignore`, `settings.py` |
| **Request Logging & Health Check Page** | Custom `RequestLoggingMiddleware` logging path, IP, status, and duration (ms) to `logs/requests.log`. Live telemetry at `/health/`. | `vibecheck/middleware.py`, `/health/` |
| **Third-Party API with Timeout & Fallback** | ZenQuotes API integration with strict 2.0s time limit and automated fallback to curated local mood quotes. | `vibecheck/external_api.py` |
| **Mobile Responsiveness** | Verified across desktop, tablet, and mobile breakpoints using Tailwind CSS responsive utilities. | `templates/base.html` |

---

## 🏗️ System Architecture & Database Design

```
+---------------------------------------------------------------------------------+
|                                 CLIENT BROWSER                                  |
|   (Mobile / Desktop Responsive UI with Theme Switcher & Floating Chat Widget)   |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                             DJANGO WEB APPLICATION                              |
|                                                                                 |
|  [RequestLoggingMiddleware] -> Logs latency & status code to logs/requests.log |
|                                                                                 |
|  [VibeAIAssistant]                                                              |
|   ├── 1. Error Code Regex & Keyword Matcher (SQL ErrorCode table)               |
|   ├── 2. FAQ Semantic & Overlap Matcher (SQL FAQ table)                         |
|   ├── 3. Gemini 1.5 Flash Synthesizer (Optional API key via env)                |
|   └── 4. Automatic Support Ticket Generator (SQL SupportTicket table)          |
|                                                                                 |
|  [External API Service]                                                         |
|   └── ZenQuotes API (2.0s timeout limit) -> Local Cached Fallback Engine        |
+--------------------+------------------------------------+-----------------------+
                     |                                    |
                     v                                    v
+----------------------------------+   +------------------------------------------+
|      SQL DATABASE (Django ORM)   |   |           MONGODB DATABASE               |
|                                  |   |                                          |
|  - FAQ (12 active records)       |   |  - chat_logs collection:                 |
|  - ErrorCode (8 verified codes)  |   |    { session_id, user_query, ai_response,|
|  - SupportTicket (Open/Resolved) |   |      source, mood, created_at }          |
|                                  |   |  - chat_feedback collection:             |
|                                  |   |    { session_id, rating, comments }      |
+----------------------------------+   +------------------------------------------+
```

---

## 🚀 Quick Start Guide (Local Setup)

### 1. Prerequisites
- Python 3.10+
- (Optional) MongoDB local service or MongoDB Atlas cluster. *Note: If MongoDB is not running locally, the built-in resilient fallback seamlessly stores chat logs to `logs/mongo_fallback.json` without any errors.*

### 2. Clone the Repository
```bash
git clone https://github.com/pranav222006/portfolio.git
cd portfolio
```

### 3. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Inside `.env`, configure your settings:
```ini
SECRET_KEY=your-django-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Optional: Gemini API Key for synthesis (assistant operates via local RAG if omitted)
GEMINI_API_KEY=your_gemini_api_key_here

# MongoDB Connection String (defaults to local instance)
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=vibecheck_db

# Third-Party API Timeout (seconds)
EXTERNAL_API_TIMEOUT=2.0
```

### 5. Apply Migrations & Seed Database
```bash
python manage.py makemigrations vibecheck
python manage.py migrate
python manage.py seed_data
```
*The `seed_data` command automatically seeds the 12 required FAQs, 8 Error Codes, and initial Support Tickets into the SQL database.*

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🧪 Verification & Testing Checklist

### 1. Verify Pages (≥ 3 Required)
- **Home (`/`):** Test switching between Happy, Stressed, Sleepy, and Hyped vibes. Confirm Spotify embed updates, lifestyle activities adapt, and the background canvas changes hue.
- **FAQs (`/faqs/`):** Confirm 12 FAQs are loaded from SQL. Test search bar and category filters. Click "Ask Assistant this question" to test the chatbot.
- **Error Codes (`/errors/`):** Confirm all 8 codes are listed. Click "Test Endpoint" to simulate HTTP responses.
- **Support Tickets (`/tickets/`):** View tickets generated automatically by the AI assistant or submit a ticket manually.
- **Health Check (`/health/`):** Inspect SQL connectivity, MongoDB connection, third-party API latency, and live request middleware logs. Also check `http://127.0.0.1:8000/health/?format=json`.

### 2. Verify Custom 404 & 500 Pages
- Navigate to an invalid route: `http://127.0.0.1:8000/some-random-route`
  - Custom `404.html` renders with the dark neon aesthetic.
  - Click **"Ask the Assistant for Help"** to see the chat widget launch with the context preloaded.
- Trigger a 500 test: `http://127.0.0.1:8000/test-error/?code=500`

### 3. Verify AI Assistant Behavior
Open the floating chat widget on any page and test:
1. **FAQ Question:** Ask *"How does Vibe Check detect my mood?"* -> Assistant answers directly from SQL FAQ table.
2. **Error Code Question:** Ask *"Explain Error 429"* or *"What is error 418?"* -> Assistant explains causes and solutions from SQL ErrorCode table.
3. **Unanswerable Question:** Ask *"Can I order a pepperoni pizza through this app?"* -> Assistant detects no match in FAQs or Error Codes, automatically opens a **Support Ticket** in SQL, and returns your Ticket ID! Check `/tickets/` to see the new ticket appear in real time.
4. **Feedback:** Click thumbs up/down on an AI response -> Feedback is saved directly to MongoDB.

---

## 🌐 Production Deployment Guide (Render / Railway / PythonAnywhere)

### Deploying to Render:
1. Create a free account at [render.com](https://render.com).
2. Click **New +** -> **Web Service** and connect your GitHub repository.
3. Configure the build parameters:
   - **Environment:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data && python manage.py collectstatic --noinput
     ```
   - **Start Command:**
     ```bash
     gunicorn vibecheck_project.wsgi:application
     ```
4. In **Environment Variables**, add:
   - `SECRET_KEY`: `<generated-random-secret>`
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `GEMINI_API_KEY`: *(Your key, optional)*
   - `MONGODB_URI`: *(Your MongoDB Atlas connection URI)*
5. Click **Deploy Web Service**. Render provides a free `https://<app-name>.onrender.com` link.

---

## 💡 Proposed Improvement (Assessment Requirement)

### Feature Proposal: Biometric Mood Detection via Web Bluetooth & Spotify OAuth 2.0 Auto-DJ

**Description:**  
Currently, users switch moods manually or input a text prompt into the AI Companion. As a future improvement, we propose integrating:
1. **Web Bluetooth Biometric Heart Rate Monitoring:** Utilizing the Web Bluetooth API (`navigator.bluetooth`) to securely read real-time heart rate and Heart Rate Variability (HRV) metrics from wearable devices (Apple Watch, Fitbit, or Garmin). The frontend calculates stress and arousal indices, automatically transitioning the application theme (e.g., from *Stressed* to *Calming*) without manual intervention.
2. **Spotify OAuth 2.0 User Library Synchronization (Auto-DJ):** Upgrading from static Spotify embeds to full Spotify Web API user authentication. This will allow the AI assistant to read the user's saved tracks and automatically generate a dynamic, private Spotify playlist directly inside their Spotify account tailored to their current emotional state.
