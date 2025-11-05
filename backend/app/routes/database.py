from fastapi import APIRouter, HTTPException
from app.agents.rag_agent import KnowledgeRAGAgent
import os
import json

router = APIRouter()

@router.get("/initdb")
async def initialize_database():
    """
    Initializes the ChromaDB with sample clinical guidelines.
    """
    try:
        # Initialize RAG agent which will automatically load default guidelines
        rag_agent = KnowledgeRAGAgent()
        
        # Test the initialization with a sample query
        test_results = rag_agent.run("chest pain and shortness of breath")
        
        return {
            "status": "success",
            "message": f"Database initialized successfully with {rag_agent.collection.count()} clinical guidelines.",
            "test_query_results": len(test_results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize database: {str(e)}")

@router.get("/status")
async def database_status():
    """
    Returns the current status of the database.
    """
    try:
        rag_agent = KnowledgeRAGAgent()
        count = rag_agent.collection.count()
        
        return {
            "status": "success",
            "document_count": count,
            "message": f"Database contains {count} clinical guidelines."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get database status: {str(e)}")