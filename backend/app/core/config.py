from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    API_KEY: str = os.getenv("API_KEY", "triage_secret_key")
    PROMETHEUS_PORT: int = int(os.getenv("PROMETHEUS_PORT", "9090"))
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_data")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    FASTAPI_PORT: int = int(os.getenv("FASTAPI_PORT", "8000"))
    
    # Optional external medical API keys
    MEDLINE_API_KEY: Optional[str] = None
    UMLS_API_KEY: Optional[str] = None
    CDC_API_KEY: Optional[str] = None
    WHO_API_KEY: Optional[str] = None
    NIH_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()