from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str
    API_KEY: str
    PROMETHEUS_PORT: int
    CHROMA_DB_PATH: str
    EMBEDDING_MODEL: str
    FASTAPI_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()
