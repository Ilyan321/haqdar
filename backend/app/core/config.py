import os
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "HaqDar (حقدار)"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Primary & fallback Groq models (Non-deprecated)
    PRIMARY_MODEL: str = "llama-3.3-70b-versatile"
    FALLBACK_MODEL: str = "llama3-8b-8192"
    
    # Groq API Keys Pool
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_API_KEYS_RAW: str = os.getenv("GROQ_API_KEYS", "")
    
    # Supabase (Optional RAG memory)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Session TTL (in seconds)
    SESSION_TTL_SECONDS: int = 3600  # 1 hour ephemeral TTL

    @property
    def groq_key_pool(self) -> List[str]:
        keys = []
        if self.GROQ_API_KEYS_RAW:
            keys.extend([k.strip() for k in self.GROQ_API_KEYS_RAW.split(",") if k.strip()])
        if self.GROQ_API_KEY and self.GROQ_API_KEY not in keys:
            keys.append(self.GROQ_API_KEY)
        return keys

settings = Settings()
