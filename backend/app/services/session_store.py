import time
from typing import Dict, Any, Optional
from app.core.config import settings

class EphemeralSessionStore:
    """
    Thread-safe in-memory session store with TTL auto-expiry.
    Ensures zero persistent PII storage for vulnerable claimant safety.
    """
    def __init__(self, ttl_seconds: Optional[int] = None):
        self.ttl = ttl_seconds or settings.SESSION_TTL_SECONDS
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.timestamps: Dict[str, float] = {}

    def create(self, session_id: str, initial_data: Dict[str, Any]) -> None:
        self._purge_expired()
        self.sessions[session_id] = initial_data
        self.timestamps[session_id] = time.time()

    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        self._purge_expired()
        return self.sessions.get(session_id)

    def update(self, session_id: str, data: Dict[str, Any]) -> None:
        if session_id in self.sessions:
            self.sessions[session_id].update(data)
            self.timestamps[session_id] = time.time()

    def exists(self, session_id: str) -> bool:
        self._purge_expired()
        return session_id in self.sessions

    def delete(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)
        self.timestamps.pop(session_id, None)

    def _purge_expired(self) -> None:
        now = time.time()
        expired = [sid for sid, ts in self.timestamps.items() if now - ts > self.ttl]
        for sid in expired:
            self.sessions.pop(sid, None)
            self.timestamps.pop(sid, None)

session_store = EphemeralSessionStore()
