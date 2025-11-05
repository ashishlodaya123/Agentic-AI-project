from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingModel:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            cls._instance = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
            logger.info("Embedding model loaded successfully.")
        return cls._instance