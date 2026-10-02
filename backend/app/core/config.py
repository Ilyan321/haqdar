import os
from pathlib import Path
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

# Search for .env in current directory, backend directory, and root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "backend" / ".env")
load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "HaqDar (حقدار)"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Active, verified Groq models
    PRIMARY_MODEL: str = "qwen/qwen3.8-27b"
    FALLBACK_MODEL: str = "openai/gpt-oss-120b"
    
    # Groq API Keys Pool
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_API_KEYS_RAW: str = os.getenv("GROQ_API_KEYS", "")
    
    # Supabase (Optional RAG memory)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Session TTL (in seconds)
    SESSION_TTL_SECONDS: int = 3600  # 1 hour ephemeral TTL
    
    # Secret Alert Notifiers
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_CHANNEL_ID: str = os.getenv("SLACK_CHANNEL_ID", "C0BGMV9SS1K")
    SLACK_WEBHOOK_URL: str = os.getenv("SLACK_WEBHOOK_URL", "")
    ALERT_WEBHOOK_URL: str = os.getenv("ALERT_WEBHOOK_URL", "")

    @property
    def groq_key_pool(self) -> List[str]:
        keys = []
        raw = os.getenv("GROQ_API_KEYS", "") or self.GROQ_API_KEYS_RAW
        primary = os.getenv("GROQ_API_KEY", "") or self.GROQ_API_KEY
        if raw:
            keys.extend([k.strip() for k in raw.split(",") if k.strip()])
        if primary and primary not in keys:
            keys.append(primary)
        return keys

settings = Settings()
