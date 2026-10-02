import os
from typing import Any
from app.core.config import settings

def get_crewai_llm(temperature: float = 0.1) -> Any:
    """
    Returns a configured CrewAI LLM instance targeting Groq Llama 3.3 70B Versatile,
    with safe fallback.
    """
    api_key = settings.GROQ_API_KEY or (settings.groq_key_pool[0] if settings.groq_key_pool else "")
    try:
        from crewai import LLM
        return LLM(
            model=f"groq/{settings.PRIMARY_MODEL}",
            api_key=api_key,
            temperature=temperature,
            max_tokens=4096,
            top_p=0.95
        )
    except ImportError:
        return None

def get_conversational_llm(temperature: float = 0.3) -> Any:
    """
    Returns an empathetic, conversational LLM instance for Intake interactions.
    """
    api_key = settings.GROQ_API_KEY or (settings.groq_key_pool[0] if settings.groq_key_pool else "")
    try:
        from crewai import LLM
        return LLM(
            model=f"groq/{settings.PRIMARY_MODEL}",
            api_key=api_key,
            temperature=temperature,
            max_tokens=2048,
            top_p=0.9
        )
    except ImportError:
        return None
