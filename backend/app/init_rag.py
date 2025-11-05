#!/usr/bin/env python3
"""
Script to initialize the RAG system with clinical guidelines.
"""
import json
import os
import sys
from app.agents.rag_agent import KnowledgeRAGAgent

def load_clinical_guidelines():
    """Load clinical guidelines from JSON file."""
    guidelines_path = os.path.join(os.path.dirname(__file__), 'data', 'clinical_guidelines.json')
    
    if not os.path.exists(guidelines_path):
        print(f"Error: Clinical guidelines file not found at {guidelines_path}")
        return []
    
    with open(guidelines_path, 'r') as f:
        guidelines = json.load(f)
    
    return guidelines

def initialize_rag_database():
    """Initialize the RAG database with clinical guidelines."""
    print("Initializing RAG database with clinical guidelines...")
    
    # Load clinical guidelines
    guidelines = load_clinical_guidelines()
    
    if not guidelines:
        print("No clinical guidelines found. Exiting.")
        return
    
    print(f"Loaded {len(guidelines)} clinical guidelines.")
    
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
    
    # Initialize RAG agent and populate database
    rag_agent = KnowledgeRAGAgent()
    rag_agent.init_db(documents, metadatas, ids)
    
    print("RAG database initialized successfully!")
    
    # Test query to verify
    print("\nTesting RAG system with sample query...")
    test_results = rag_agent.run("patient with chest pain and shortness of breath")
    
    print(f"Retrieved {len(test_results)} relevant guidelines:")
    for result in test_results:
        print(f"  - {result.get('title', 'Untitled')}: {result.get('content', '')[:100]}...")

if __name__ == "__main__":
    initialize_rag_database()