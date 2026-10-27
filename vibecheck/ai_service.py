import re
import logging
from django.conf import settings
from .models import FAQ, ErrorCode, SupportTicket
from .mongo_service import mongo_service

logger = logging.getLogger(__name__)

# Check Gemini SDK availability
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai is not installed. AI assistant will run with local RAG engine.")


class VibeAIAssistant:
    """
    AI Assistant fulfilling the final assessment requirements:
    1. Answers questions from the FAQ data (SQL).
    2. Explains error codes (SQL).
    3. Automatically creates a support ticket in SQL when it cannot answer.
    4. Logs conversation and feedback to MongoDB.
    5. Reads API keys strictly from environment variables.
    """
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', '')
        self.gemini_model = None
        self._init_gemini()

    def _init_gemini(self):
        if GEMINI_AVAILABLE and self.api_key and self.api_key.strip():
            try:
                genai.configure(api_key=self.api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Gemini AI Model successfully initialized.")
            except Exception as e:
                logger.warning(f"Could not configure Gemini API: {e}. Running local RAG mode.")
                self.gemini_model = None

    def process_query(self, user_query, session_id="anonymous", user_name="Listener", user_email="", current_mood="happy"):
        """
        Main query pipeline.
        Returns a dictionary:
        {
            'response': str,
            'source': 'faq' | 'error_code' | 'gemini' | 'ticket_created' | 'rule',
            'ticket_id': str | None,
            'matched_item': dict | None
        }
        """
        query_clean = user_query.strip()
        lower_q = query_clean.lower()

        # Step 1: Explicit user request to create a ticket
        if any(trigger in lower_q for trigger in ["create ticket", "submit ticket", "support ticket", "contact support", "open a ticket", "human agent"]):
            ticket = self._create_ticket(user_name, user_email, query_clean, "User requested support ticket via assistant")
            resp_text = (
                f"I've created a support ticket for you!\n\n"
                f"🎫 **Ticket ID: {ticket.ticket_id}**\n"
                f"**Subject:** {ticket.subject}\n\n"
                f"Our engineering and support team has been notified. You can check its live status on our "
                f"<a href='/tickets/' class='text-accent-secondary underline'>Support Tickets</a> page."
            )
            mongo_service.log_chat_interaction(session_id, user_query, resp_text, source="ticket_created", mood=current_mood)
            return {
                'response': resp_text,
                'source': 'ticket_created',
                'ticket_id': ticket.ticket_id,
                'status': 'ticket_opened'
            }

        # Step 2: Error Code Lookup (detect numbers or keywords)
        error_match = self._search_error_codes(lower_q)
        if error_match:
            explanation = self._format_error_explanation(error_match)
            # If Gemini is available, we can optionally enhance the phrasing
            final_resp = explanation
            if self.gemini_model:
                enhanced = self._gemini_synthesize(user_query, context=explanation, system_hint="Explain this HTTP error code clearly and empathetically.")
                if enhanced:
                    final_resp = enhanced

            mongo_service.log_chat_interaction(session_id, user_query, final_resp, source="error_code", mood=current_mood)
            return {
                'response': final_resp,
                'source': 'error_code',
                'ticket_id': None,
                'matched_item': {'code': error_match.code, 'title': error_match.title}
            }

        # Step 3: FAQ Database Lookup (SQL)
        faq_match, confidence = self._search_faqs(lower_q)
        if faq_match and confidence >= 0.35:
            faq_text = (
                f"**{faq_match.question}**\n\n"
                f"{faq_match.answer}\n\n"
                f"*(Category: {faq_match.get_category_display()})*"
            )
            final_resp = faq_text
            if self.gemini_model:
                enhanced = self._gemini_synthesize(user_query, context=faq_text, system_hint="Answer the user's question directly using this verified FAQ knowledge base item.")
                if enhanced:
                    final_resp = enhanced

            mongo_service.log_chat_interaction(session_id, user_query, final_resp, source="faq", mood=current_mood)
            return {
                'response': final_resp,
                'source': 'faq',
                'ticket_id': None,
                'matched_item': {'id': faq_match.id, 'question': faq_match.question}
            }

        # Step 4: Fallback / Unanswered Query -> Automatic Support Ticket Creation
        # Requirement: "creates a support ticket when it cannot answer"
        ticket = self._create_ticket(
            user_name=user_name,
            user_email=user_email,
            query=query_clean,
            context="AI assistant could not find a confident match in FAQs or Error Codes catalog."
        )

        resp_text = (
            f"I searched our FAQ knowledge base and error documentation, but I don't have a verified answer for that specific question.\n\n"
            f"To make sure your question gets addressed, I've automatically generated a **Support Ticket** for our team:\n\n"
            f"🎫 **Ticket Reference: {ticket.ticket_id}**\n"
            f"**Query Logged:** \"{query_clean}\"\n"
            f"**Status:** Open / Awaiting Support Review\n\n"
            f"You can view and track your ticket on our <a href='/tickets/' class='text-accent-secondary underline'>Support Tickets</a> page."
        )

        mongo_service.log_chat_interaction(session_id, user_query, resp_text, source="ticket_created", mood=current_mood)
        return {
            'response': resp_text,
            'source': 'ticket_created',
            'ticket_id': ticket.ticket_id,
            'status': 'unanswered_ticket_created'
        }

    def _search_error_codes(self, lower_q):
        """Finds matching ErrorCode in SQL database."""
        # Check for numeric code matches (e.g., "404", "500", "418")
        code_candidates = re.findall(r'\b\d{3}\b', lower_q)
        for code_str in code_candidates:
            try:
                code_int = int(code_str)
                match = ErrorCode.objects.filter(code=code_int).first()
                if match:
                    return match
            except Exception:
                continue

        # Check for phrase matches
        for err in ErrorCode.objects.all():
            if err.title.lower() in lower_q or str(err.code) in lower_q:
                return err
            if err.is_custom and "vibe mismatch" in lower_q:
                return err

        return None

    def _search_faqs(self, lower_q):
        """
        Ranks active FAQs in SQL by token overlap & relevance score.
        """
        faqs = list(FAQ.objects.filter(is_active=True))
        if not faqs:
            return None, 0.0

        query_tokens = set(re.findall(r'\w+', lower_q))
        stop_words = {'the', 'a', 'an', 'is', 'are', 'what', 'how', 'why', 'can', 'i', 'do', 'in', 'on', 'to', 'for', 'of', 'and'}
        meaningful_tokens = query_tokens - stop_words

        if not meaningful_tokens:
            meaningful_tokens = query_tokens

        best_faq = None
        best_score = 0.0

        for f in faqs:
            q_tokens = set(re.findall(r'\w+', f.question.lower()))
            a_tokens = set(re.findall(r'\w+', f.answer.lower()))

            # Weight question tokens more heavily than answer tokens
            q_overlap = len(meaningful_tokens & q_tokens)
            a_overlap = len(meaningful_tokens & a_tokens)

            score = (q_overlap * 2.0 + a_overlap * 0.5) / (len(meaningful_tokens) or 1)
            
            # Exact phrase bonus
            if f.question.lower() in lower_q or lower_q in f.question.lower():
                score += 1.5

            if score > best_score:
                best_score = score
                best_faq = f

        return best_faq, best_score

    def _format_error_explanation(self, err: ErrorCode):
        """Formats an ErrorCode object into a rich, structured markdown reply."""
        custom_tag = " [Site-Specific Custom Error]" if err.is_custom else ""
        return (
            f"### ⚠️ Error {err.code}: {err.title}{custom_tag}\n\n"
            f"**What it means:** {err.description}\n\n"
            f"**Common Causes:**\n{err.common_causes}\n\n"
            f"**How to Fix It:**\n{err.resolution_steps}\n\n"
            f"*(Category: {err.category})*"
        )

    def _gemini_synthesize(self, user_query, context, system_hint=""):
        """Calls Gemini API with RAG grounded context."""
        if not self.gemini_model:
            return None
        try:
            prompt = (
                f"You are the empathetic Vibe Check AI Assistant.\n"
                f"{system_hint}\n\n"
                f"Verified Knowledge Base Context:\n{context}\n\n"
                f"User Question: {user_query}\n\n"
                f"Instructions:\n"
                f"- Answer politely, clearly, and accurately using ONLY the context provided.\n"
                f"- Keep formatting friendly with markdown bullet points if helpful.\n"
                f"- Do not invent facts outside the context."
            )
            response = self.gemini_model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini generation call failed ({e}). Reverting to direct database text.")
        return None

    def _create_ticket(self, user_name, user_email, query, context=""):
        """Saves a new SupportTicket model to SQL."""
        name = user_name.strip() if user_name and user_name.strip() else "Anonymous Listener"
        email = user_email.strip() if user_email and user_email.strip() else "listener@vibecheck.io"
        subject = (query[:60] + "...") if len(query) > 60 else query

        ticket = SupportTicket.objects.create(
            user_name=name,
            user_email=email,
            subject=f"Inquiry: {subject}",
            message=query,
            ai_context=context,
            status='open',
            priority='medium'
        )
        return ticket


# Global singleton instance
ai_assistant = VibeAIAssistant()
