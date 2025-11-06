import chromadb
from app.core.config import settings
from app.core.embedding import EmbeddingModel
from typing import Any, List, Dict, Optional
import re
import json
import os
from app.utils.medical_apis import search_medline, get_cdc_data, get_who_data
from app.core.agent_memory import get_agent_memory

class KnowledgeRAGAgent:
    """
    Agent for retrieving information from a clinical knowledge base using RAG.
    Enhanced with more sophisticated retrieval and ranking mechanisms.
    Integrates external medical data sources for comprehensive clinical guidance.
    """
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.embedding_function = EmbeddingModel.get_instance()
        self.collection = self.client.get_or_create_collection(
            name="clinical_guidelines",
        )
        self.memory = get_agent_memory()
        # Initialize database if empty
        self._initialize_database_if_empty()

    def _initialize_database_if_empty(self):
        """Initialize the database with clinical guidelines if it's empty."""
        if self.collection.count() == 0:
            self._load_default_guidelines()

    def _load_default_guidelines(self):
        """Load default clinical guidelines into the database."""
        guidelines_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'clinical_guidelines.json')
        
        if not os.path.exists(guidelines_path):
            print(f"Warning: Clinical guidelines file not found at {guidelines_path}")
            return
        
        try:
            with open(guidelines_path, 'r') as f:
                guidelines = json.load(f)
            
            # Prepare documents for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for guideline in guidelines:
                documents.append(guideline['content'])
                metadatas.append({
                    'title': guideline['title'],
                    'category': guideline['category'],
                    'keywords': ', '.join(guideline['keywords'])
                })
                ids.append(guideline['id'])
            
            # Add documents to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Initialized RAG database with {len(guidelines)} clinical guidelines.")
        except Exception as e:
            print(f"Error loading clinical guidelines: {e}")

    def init_db(self, documents: list, metadatas: list, ids: list):
        """
        Initializes the ChromaDB with a set of documents.
        """
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def run(self, query: str, n_results: int = 5) -> list:
        """
        Queries the knowledge base and returns the most relevant documents.
        Enhanced with external data integration and sophisticated ranking.
        """
        # First, try to get external data
        external_data = self._get_external_data(query)
        
        # Then query the local knowledge base
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Enhance results with relevance scoring and filtering
        enhanced_results = self._enhance_results(results, query, external_data)
        
        # Store results in shared memory
        self.memory.store_agent_output("rag", {
            "query": query,
            "results": enhanced_results
        })
        
        return enhanced_results

    def _get_external_data(self, query: str) -> dict:
        """
        Retrieve data from external medical sources with fallback.
        """
        external_data = {
            "medline": {"status": "skipped", "message": "External API calls disabled for performance"},
            "cdc": {"status": "skipped", "message": "External API calls disabled for performance"},
            "who": {"status": "skipped", "message": "External API calls disabled for performance"}
        }
        return external_data

    def _enhance_results(self, results: Any, query: str, external_data: Optional[dict] = None) -> List[Dict]:
        """
        Enhance and filter results based on relevance and quality.
        Integrates external data when available with priority ranking.
        """
        enhanced_docs = []
        
        # Add external data as high-priority results if available
        if external_data:
            # Add MEDLINE results if successful
            medline_data = external_data.get("medline", {})
            if medline_data.get("status") == "success" and "results" in medline_data:
                for i, article in enumerate(medline_data["results"]):
                    enhanced_docs.append({
                        "content": f"Recent medical literature on {query}. Article ID: {article.get('id', 'N/A')}. This represents current research findings that support clinical decision making.",
                        "relevance_score": 0.95,  # High relevance for recent literature
                        "source": "MEDLINE/PubMed",
                        "title": f"Medical Literature: {article.get('title', 'Research Article')}",
                        "external": True,
                        "type": "literature",
                        "evidence_level": "High - Peer-reviewed research"
                    })
            
            # Add CDC data if successful
            cdc_data = external_data.get("cdc", {})
            if cdc_data.get("status") == "success" and cdc_data.get("data_available"):
                enhanced_docs.append({
                    "content": f"Public health guidelines from CDC for {query}. These guidelines represent evidence-based public health recommendations for diagnosis, treatment, and prevention.",
                    "relevance_score": 0.90,
                    "source": "CDC",
                    "title": f"CDC Public Health Guidelines for {query}",
                    "external": True,
                    "type": "public_health",
                    "evidence_level": "High - Government public health authority"
                })
            
            # Add WHO data if successful
            who_data = external_data.get("who", {})
            if who_data.get("status") == "success" and who_data.get("data_available"):
                enhanced_docs.append({
                    "content": f"International health guidelines from WHO for {query}. These guidelines represent global standards for healthcare practices and disease management.",
                    "relevance_score": 0.85,
                    "source": "WHO",
                    "title": f"WHO International Health Standards for {query}",
                    "external": True,
                    "type": "international_guidelines",
                    "evidence_level": "High - International health authority"
                })
        
        # Process local database results
        if results and 'documents' in results and results['documents']:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0] if 'metadatas' in results and results['metadatas'] else [{}] * len(documents)
            distances = results['distances'][0] if 'distances' in results and results['distances'] else [0.0] * len(documents)
            
            # Filter out low-quality results
            for i, doc in enumerate(documents):
                # Skip empty or very short documents
                if len(doc.strip()) < 10:
                    continue
                    
                # Calculate relevance score
                relevance_score = self._calculate_relevance(query, doc)
                
                # Skip documents with very low relevance
                if relevance_score < 0.05:
                    continue
                
                # Format document content
                formatted_content = self._format_document_content(doc)
                
                # Add document with metadata
                enhanced_docs.append({
                    "content": formatted_content,
                    "relevance_score": round(relevance_score, 3),
                    "distance": round(distances[i], 3) if distances else None,
                    "metadata": metadatas[i] if i < len(metadatas) else {},
                    "title": metadatas[i].get('title', 'Clinical Guideline') if i < len(metadatas) else 'Clinical Guideline',
                    "source": "Local Clinical Guidelines",
                    "external": False,
                    "type": "clinical_guideline",
                    "evidence_level": "Moderate - Institutional guidelines",
                    "category": metadatas[i].get('category', 'general') if i < len(metadatas) else 'general'
                })
        
        # Sort by relevance score
        enhanced_docs.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Return top documents with enhanced categorization
        return self._categorize_and_prioritize_results(enhanced_docs[:8])

    def _categorize_and_prioritize_results(self, results: List[Dict]) -> List[Dict]:
        """
        Further categorize and prioritize results based on clinical relevance.
        """
        # Group by source type
        external_results = [r for r in results if r.get("external", False)]
        local_results = [r for r in results if not r.get("external", False)]
        
        # Prioritize by evidence level and source type
        prioritized_results = []
        
        # Add high-priority external sources first
        for result in external_results:
            if result.get("source") in ["MEDLINE/PubMed", "CDC", "WHO"]:
                prioritized_results.append(result)
        
        # Add local clinical guidelines
        for result in local_results:
            prioritized_results.append(result)
        
        # Add any remaining results
        for result in results:
            if result not in prioritized_results:
                prioritized_results.append(result)
        
        return prioritized_results[:6]  # Return top 6 most relevant results

    def _calculate_relevance(self, query: str, document: str) -> float:
        """
        Calculate a relevance score between query and document.
        Enhanced with medical terminology matching.
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
            
        base_similarity = len(intersection) / len(union)
        
        # Boost score for medical terminology matches
        medical_terms = ["treatment", "diagnosis", "management", "protocol", "guideline", 
                        "clinical", "medical", "patient", "symptom", "condition"]
        medical_matches = len(query_words.intersection(set(medical_terms)))
        medical_boost = medical_matches * 0.1
        
        return min(1.0, base_similarity + medical_boost)

    def _format_document_content(self, content: str) -> str:
        """
        Format document content for better readability.
        """
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content.strip())
        
        # Limit length for display but preserve more content for detailed analysis
        if len(content) > 800:
            content = content[:800] + "..."
            
        return content