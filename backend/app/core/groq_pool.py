import os
import time
import asyncio
from typing import List, Optional, Dict
from groq import Groq, AsyncGroq
from app.core.config import settings

class GroqKeyPoolManager:
    """
    Manages a pool of Groq API keys with round-robin rotation, 
    exponential backoff, and automatic rate-limit (HTTP 429) circuit-breaking.
    """
    def __init__(self, api_keys: Optional[List[str]] = None):
        self.api_keys = api_keys or settings.groq_key_pool
        if not self.api_keys:
            # Fallback placeholder if no keys in env yet
            self.api_keys = ["gsk_placeholder"]
            
        self.current_index = 0
        self.cooldowns: Dict[str, float] = {k: 0.0 for k in self.api_keys}
        self.lock = asyncio.Lock()

    async def get_next_key(self) -> str:
        """
        Retrieves the next available active API key, waiting if all keys are temporarily cooling down.
        """
        async with self.lock:
            now = time.time()
            attempts = 0
            while attempts < len(self.api_keys):
                key = self.api_keys[self.current_index]
                self.current_index = (self.current_index + 1) % len(self.api_keys)
                if self.cooldowns[key] <= now:
                    return key
                attempts += 1
            
            # If all keys are in cooldown, pick the one that expires earliest
            soonest_key = min(self.cooldowns, key=self.cooldowns.get)
            wait_time = max(0.5, self.cooldowns[soonest_key] - now)
            await asyncio.sleep(wait_time)
            return soonest_key

    def mark_rate_limited(self, key: str, cooldown_seconds: float = 60.0):
        """
        Marks an API key as rate-limited, cooling it down for `cooldown_seconds`.
        """
        self.cooldowns[key] = time.time() + cooldown_seconds

    async def get_client(self) -> Groq:
        """
        Returns a sync Groq client configured with an active key.
        """
        key = await self.get_next_key()
        return Groq(api_key=key)

    async def get_async_client(self) -> AsyncGroq:
        """
        Returns an async Groq client configured with an active key.
        """
        key = await self.get_next_key()
        return AsyncGroq(api_key=key)

groq_pool = GroqKeyPoolManager()
