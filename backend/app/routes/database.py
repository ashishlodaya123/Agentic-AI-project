from fastapi import APIRouter, HTTPException
from app.agents.rag_agent import KnowledgeRAGAgent

router = APIRouter()

@router.get("/initdb")
async def init_database():
    """
    Initializes ChromaDB with sample clinical guidelines.
    """
    rag_agent = KnowledgeRAGAgent()

    # Sample documents (in a real scenario, this would come from a file or database)
    documents = [
        "For chest pain, consider acute coronary syndrome (ACS). Perform an ECG immediately.",
        "Shortness of breath could indicate heart failure or a pulmonary embolism. Assess oxygen saturation.",
        "High fever with a cough may suggest pneumonia. A chest X-ray is recommended.",
        "Abdominal pain in the lower right quadrant could be appendicitis. A CT scan may be necessary."
    ]
    metadatas = [
        {"source": "Cardiology Guidelines"},
        {"source": "Pulmonology Guidelines"},
        {"source": "Infectious Disease Guidelines"},
        {"source": "Emergency Medicine Handbook"}
    ]
    ids = [f"doc_{i+1}" for i in range(len(documents))]

    try:
        rag_agent.init_db(documents, metadatas, ids)
        return {"message": "ChromaDB initialized successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing ChromaDB: {str(e)}")
