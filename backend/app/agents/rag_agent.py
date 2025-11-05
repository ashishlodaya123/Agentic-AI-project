import chromadb
from app.core.config import settings
from app.main import EmbeddingModel

class KnowledgeRAGAgent:
    """
    Agent for retrieving information from a clinical knowledge base using RAG.
    """
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.embedding_function = EmbeddingModel.get_instance()
        self.collection = self.client.get_or_create_collection(
            name="clinical_guidelines",
        )

    def init_db(self, documents: list, metadatas: list, ids: list):
        """
        Initializes the ChromaDB with a set of documents.
        """
        # Workaround for SentenceTransformerEmbeddingFunction not being pickleable
        # We add the documents with the embedding function, then clear it
        # so the agent can be pickled by Celery.
        collection = self.client.get_or_create_collection(
            name="clinical_guidelines",
            embedding_function=self.embedding_function
        )
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def run(self, query: str, n_results: int = 2) -> list:
        """
        Queries the knowledge base and returns the most relevant documents.
        """
        # Re-add the embedding function for querying
        collection = self.client.get_or_create_collection(
            name="clinical_guidelines",
            embedding_function=self.embedding_function
        )
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0]
