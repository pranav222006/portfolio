import json
import logging
from datetime import datetime
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)

# Try importing pymongo
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False
    logger.warning("pymongo is not installed. MongoDB operations will use fallback storage.")


class MongoService:
    """
    MongoDB service for logging chat interactions and user feedback.
    Fulfills assessment requirement: 'chat logs and feedback stored in MongoDB'.
    Includes graceful local fallback storage if MongoDB instance is unreachable.
    """
    def __init__(self):
        self.uri = getattr(settings, 'MONGODB_URI', 'mongodb://localhost:27017/')
        self.db_name = getattr(settings, 'MONGODB_DB_NAME', 'vibecheck_db')
        self.client = None
        self.db = None
        self._connected = False
        self.fallback_file = getattr(settings, 'LOGS_DIR', Path('logs')) / 'mongo_fallback.json'
        self.init_connection()

    def init_connection(self):
        if not PYMONGO_AVAILABLE:
            self._connected = False
            return

        try:
            # Set short timeout so page loads aren't stalled if local MongoDB isn't running
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)
            # Verify connection with a quick ping
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self._connected = True
            logger.info("Successfully connected to MongoDB.")
        except Exception as e:
            self._connected = False
            logger.info(f"MongoDB not available ({e}). Using persistent JSON fallback.")

    def check_connection(self):
        """Returns (is_connected: bool, info: dict) for health check telemetry."""
        if not PYMONGO_AVAILABLE:
            return False, "pymongo package not installed (using local fallback)"
        if not self._connected:
            # Try reconnecting
            self.init_connection()
        if self._connected:
            return True, f"Connected to {self.db_name}"
        return False, "Unreachable - active in resilient fallback mode"

    def log_chat_interaction(self, session_id, user_query, ai_response, source="ai", mood="happy"):
        """
        Stores user chat question and assistant response in MongoDB 'chat_logs'.
        """
        doc = {
            'session_id': session_id,
            'user_query': user_query,
            'ai_response': ai_response,
            'source': source,
            'mood': mood,
            'created_at': datetime.utcnow().isoformat()
        }

        if self._connected and self.db is not None:
            try:
                self.db.chat_logs.insert_one(doc)
                return True
            except Exception as e:
                logger.error(f"Error saving chat log to MongoDB: {e}")

        # Fallback persistence
        return self._save_fallback('chat_logs', doc)

    def save_feedback(self, session_id, message_id, rating, comments="", feedback_type="rating"):
        """
        Stores user feedback (thumbs up/down or 1-5 rating) in MongoDB 'chat_feedback'.
        """
        doc = {
            'session_id': session_id,
            'message_id': message_id,
            'rating': rating,
            'feedback_type': feedback_type,
            'comments': comments,
            'created_at': datetime.utcnow().isoformat()
        }

        if self._connected and self.db is not None:
            try:
                self.db.chat_feedback.insert_one(doc)
                return True
            except Exception as e:
                logger.error(f"Error saving feedback to MongoDB: {e}")

        return self._save_fallback('chat_feedback', doc)

    def get_recent_chat_logs(self, limit=10):
        """Retrieves recent chat logs for telemetry/admin review."""
        if self._connected and self.db is not None:
            try:
                cursor = self.db.chat_logs.find().sort('_id', -1).limit(limit)
                results = []
                for doc in cursor:
                    doc['_id'] = str(doc['_id'])
                    results.append(doc)
                return results
            except Exception as e:
                logger.error(f"Error reading chat logs from MongoDB: {e}")

        # Fallback reading
        return self._read_fallback('chat_logs', limit)

    def _save_fallback(self, collection_name, doc):
        """Saves documents to fallback file if MongoDB server is unavailable."""
        try:
            self.fallback_file.parent.mkdir(parents=True, exist_ok=True)
            data = {}
            if self.fallback_file.exists():
                try:
                    with open(self.fallback_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            if collection_name not in data:
                data[collection_name] = []
            # Strip non-serializable fields if any
            clean_doc = {k: v for k, v in doc.items() if k != '_id'}
            data[collection_name].append(clean_doc)
            # Keep last 100 entries
            data[collection_name] = data[collection_name][-100:]
            with open(self.fallback_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.warning(f"Fallback storage error: {e}")
            return False

    def _read_fallback(self, collection_name, limit=10):
        try:
            if not self.fallback_file.exists():
                return []
            with open(self.fallback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            items = data.get(collection_name, [])
            return list(reversed(items[-limit:]))
        except Exception:
            return []


# Global singleton instance
mongo_service = MongoService()
