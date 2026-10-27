from django.core.management.base import BaseCommand
from vibecheck.models import FAQ, ErrorCode, SupportTicket

class Command(BaseCommand):
    help = "Seeds database with required 10+ FAQs, 8 Error Codes, and initial Support Tickets"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database for Vibe Check...")

        # ---------------------------------------------------------
        # 1. SEED FAQS (Minimum 10 required, providing 12 detailed FAQs)
        # ---------------------------------------------------------
        faqs_data = [
            {
                "question": "What is Vibe Check and how does it work?",
                "answer": "Vibe Check is an intelligent mood-driven platform that dynamically adapts its interface theme, playlists, lifestyle activities, and recommendations to mirror your emotional state in real time.",
                "category": "general",
                "order": 1
            },
            {
                "question": "How does Vibe Check detect or change my mood?",
                "answer": "You can switch moods manually via the 4 core vibe cards (Happy, Stressed, Sleepy, Hyped), roll the 'Surprise Me' dice, or enter how you feel into our Vibe AI Companion which analyzes sentiment and prescribes a matching vibe.",
                "category": "ai",
                "order": 2
            },
            {
                "question": "How is Spotify integrated into the application?",
                "answer": "We integrate official Spotify embedded players and deep links. You can play previews directly inside the dashboard or open curated full playlists on Spotify with one click.",
                "category": "music",
                "order": 3
            },
            {
                "question": "Is an official Spotify Premium account required?",
                "answer": "No! Embedded previews and curated links work with both free and premium Spotify accounts. Free accounts can listen to previews directly and launch web/mobile Spotify players.",
                "category": "music",
                "order": 4
            },
            {
                "question": "Where is my mood history and data stored?",
                "answer": "Your active session and mood history timeline are saved locally and synchronized with our dual database architecture: support tickets and catalog items in SQL, and conversation history and feedback in MongoDB.",
                "category": "system",
                "order": 5
            },
            {
                "question": "How does the Vibe AI Companion determine recommendations?",
                "answer": "The AI assistant processes your emotional description through Gemini AI (or our local RAG rule engine) to classify your energy level, generating an empathetic message, suggested musical genres, and a mindful activity.",
                "category": "ai",
                "order": 6
            },
            {
                "question": "What happens if the AI Assistant cannot answer my question?",
                "answer": "If your question cannot be matched with our FAQs or error catalog, the assistant automatically creates a Support Ticket in our SQL database, assigns you a Ticket ID, and alerts our team.",
                "category": "ai",
                "order": 7
            },
            {
                "question": "How do I check the status of my support tickets?",
                "answer": "Navigate to the Support Tickets page (/tickets/) in the top navigation or ask the assistant with your Ticket ID to review its current status (Open, In Progress, or Resolved).",
                "category": "general",
                "order": 8
            },
            {
                "question": "Why is the background color and canvas changing automatically?",
                "answer": "Each vibe has a designated color palette: Happy (amber/gold), Stressed (serene cyan/slate), Sleepy (deep violet), and Hyped (vibrant magenta/neon). The background particle canvas dynamically updates its glow to match.",
                "category": "general",
                "order": 9
            },
            {
                "question": "What should I do if a Spotify embed fails to play or load?",
                "answer": "Ensure your browser does not block third-party cookies or iframes from open.spotify.com, check your internet connectivity, or click the direct 'Open in Spotify' button.",
                "category": "errors",
                "order": 10
            },
            {
                "question": "Is my chat data and personal information secure?",
                "answer": "Yes. We do not sell user data. Conversation logs and feedback are stored safely in MongoDB without passwords, and API credentials are kept securely in server-side environment variables.",
                "category": "system",
                "order": 11
            },
            {
                "question": "Can I submit feedback or ratings on AI responses?",
                "answer": "Yes! Every AI response in the chat widget includes thumbs up/down and rating options. Your feedback is sent directly to MongoDB to help us continuously train and refine our assistant.",
                "category": "ai",
                "order": 12
            }
        ]

        faq_created_count = 0
        for item in faqs_data:
            obj, created = FAQ.objects.update_or_create(
                question=item["question"],
                defaults={
                    "answer": item["answer"],
                    "category": item["category"],
                    "order": item["order"],
                    "is_active": True
                }
            )
            if created:
                faq_created_count += 1

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(faqs_data)} FAQs ({faq_created_count} newly created)."))

        # ---------------------------------------------------------
        # 2. SEED ERROR CODES (Minimum 8 required: 7 standard + 1 custom)
        # ---------------------------------------------------------
        errors_data = [
            {
                "code": 400,
                "title": "Bad Request",
                "category": "Client Error (4xx)",
                "description": "The server could not understand the request due to invalid syntax, malformed parameters, or invalid JSON payload.",
                "common_causes": "Missing required fields in POST requests, corrupted form input, or invalid mood parameter.",
                "resolution_steps": "Verify request payload syntax, check query parameters, and ensure request headers contain 'Content-Type: application/json'.",
                "is_custom": False
            },
            {
                "code": 401,
                "title": "Unauthorized",
                "category": "Client Error (4xx)",
                "description": "The requested resource requires valid user authentication credentials that are either missing or invalid.",
                "common_causes": "Expired session token, invalid API key, or attempting to access protected endpoints without signing in.",
                "resolution_steps": "Sign in with valid credentials, verify the session cookie is active, or check the Authorization bearer token.",
                "is_custom": False
            },
            {
                "code": 403,
                "title": "Forbidden",
                "category": "Client Error (4xx)",
                "description": "The server understood the request, but refuses to authorize access because the user lacks necessary permissions.",
                "common_causes": "Attempting to access administrative telemetry or modify another user's support ticket.",
                "resolution_steps": "Check user roles and access rights. Contact the site administrator if you believe your account should have access.",
                "is_custom": False
            },
            {
                "code": 404,
                "title": "Not Found",
                "category": "Client Error (4xx)",
                "description": "The server cannot find the requested resource or URL route.",
                "common_causes": "Mistyped URL route, removed playlist ID, non-existent ticket number, or deleted mood record.",
                "resolution_steps": "Double check the URL spelling, navigate back to the Home page, or ask our AI assistant to help locate the resource.",
                "is_custom": False
            },
            {
                "code": 429,
                "title": "Too Many Requests",
                "category": "Client Error (4xx)",
                "description": "The user has sent too many requests in a given amount of time (rate limit exceeded).",
                "common_causes": "Spamming the AI chat endpoint, excessive rapid mood switching, or automated bot requests.",
                "resolution_steps": "Wait 30-60 seconds before sending another message, reduce request frequency, or use caching.",
                "is_custom": False
            },
            {
                "code": 500,
                "title": "Internal Server Error",
                "category": "Server Error (5xx)",
                "description": "A generic error message indicating that the server encountered an unexpected condition that prevented it from fulfilling the request.",
                "common_causes": "Unhandled Python exceptions, database schema mismatch, or crashing background workers.",
                "resolution_steps": "Check server debug logs in logs/requests.log, verify database migrations, and report the incident via a Support Ticket.",
                "is_custom": False
            },
            {
                "code": 503,
                "title": "Service Unavailable",
                "category": "Server Error (5xx)",
                "description": "The server is currently unable to handle the request due to temporary overloading or maintenance.",
                "common_causes": "External Spotify or Gemini API outages, database maintenance, or thread pool exhaustion.",
                "resolution_steps": "Wait a few moments and refresh. Our fallback engine will automatically serve cached playlists and quotes.",
                "is_custom": False
            },
            {
                "code": 418,
                "title": "Vibe Mismatch (Energy Out of Range)",
                "category": "Site-Specific Custom Error",
                "description": "The requested emotional energy could not be synchronized with current acoustic parameters. Your soul frequency is in uncharted sonic territory!",
                "common_causes": "Attempting to play heavy metal in Sleepy mode, submitting paradoxical mood prompts, or exceeding the maximum chill threshold.",
                "resolution_steps": "Click 'Surprise Me' to recalibrate your frequency, or ask the AI assistant to prescribe a hybrid harmonic playlist.",
                "is_custom": True
            }
        ]

        err_created_count = 0
        for item in errors_data:
            obj, created = ErrorCode.objects.update_or_create(
                code=item["code"],
                defaults={
                    "title": item["title"],
                    "category": item["category"],
                    "description": item["description"],
                    "common_causes": item["common_causes"],
                    "resolution_steps": item["resolution_steps"],
                    "is_custom": item["is_custom"]
                }
            )
            if created:
                err_created_count += 1

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(errors_data)} Error Codes ({err_created_count} newly created)."))

        # ---------------------------------------------------------
        # 3. SEED INITIAL SAMPLE SUPPORT TICKETS
        # ---------------------------------------------------------
        if SupportTicket.objects.count() == 0:
            SupportTicket.objects.create(
                ticket_id="TCK-9A1024",
                user_name="Alex Vibe",
                user_email="alex@vibecheck.io",
                subject="Inquiry: Can I connect Apple Music or YouTube Music?",
                message="Is there any future plan to support Apple Music playlists in addition to Spotify?",
                ai_context="Question asked to AI assistant; no direct FAQ match.",
                status="open",
                priority="medium"
            )
            SupportTicket.objects.create(
                ticket_id="TCK-3F8812",
                user_name="Jordan Reed",
                user_email="jordan@domain.com",
                subject="Error 429 encountered during morning study session",
                message="I was generating multiple AI prompts for my study playlist and hit a 429 code.",
                ai_context="Assistant explained 429 and created ticket for quota review.",
                status="resolved",
                priority="low"
            )
            self.stdout.write(self.style.SUCCESS("[OK] Seeded sample support tickets."))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
