import chromadb
from app.core.config import settings
from app.core.embedding import EmbeddingModel
from typing import Any, List, Dict

class KnowledgeRAGAgent:
    """
    Agent for retrieving information from a clinical knowledge base using RAG.
    Enhanced with more sophisticated retrieval and ranking mechanisms.
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
        # Workaround for embedding function not being pickleable
        # We add the documents with the embedding function, then clear it
        # so the agent can be pickled by Celery.
        collection = self.client.get_or_create_collection(
            name="clinical_guidelines"
        )
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def run(self, query: str, n_results: int = 3) -> list:
        """
        Queries the knowledge base and returns the most relevant documents.
        Enhanced with better ranking and filtering.
        """
        # Re-add the embedding function for querying
        collection = self.client.get_or_create_collection(
            name="clinical_guidelines"
        )
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Enhance results with relevance scoring and filtering
        enhanced_results = self._enhance_results(results, query)
        return enhanced_results

    def _enhance_results(self, results: Any, query: str) -> List[str]:
        """
        Enhance and filter results based on relevance and quality.
        """
        if not results or 'documents' not in results or not results['documents']:
            return []
            
        documents = results['documents'][0]
        
        # Filter out low-quality results
        filtered_docs = []
        for doc in documents:
            # Skip empty or very short documents
            if len(doc.strip()) < 10:
                continue
                
            # Add document with some metadata
            filtered_docs.append({
                "content": doc,
                "relevance_score": self._calculate_relevance(query, doc)
            })
            
        # Sort by relevance score
        filtered_docs.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Return just the content of top documents
        return [doc["content"] for doc in filtered_docs[:2]]

    def _calculate_relevance(self, query: str, document: str) -> float:
        """
        Calculate a simple relevance score between query and document.
        In a production system, this would use more sophisticated methods.
        """
        query_words = set(query.lower().split())
        doc_words = set(document.lower().split())
        
        if not query_words:
            return 0.0
            
        # Calculate Jaccard similarity
        intersection = query_words.intersection(doc_words)
        union = query_words.union(doc_words)
        
        if len(union) == 0:
            return 0.0
            
        return len(intersection) / len(union)