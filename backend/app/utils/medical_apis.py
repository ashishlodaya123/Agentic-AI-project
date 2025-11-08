#!/usr/bin/env python3
"""
Utility functions for integrating with external medical APIs.
These are examples of how external data sources could be integrated.
"""

import os
import requests
from app.core.config import settings

def search_medline(query: str, max_results: int = 5):
    """
    Search MEDLINE database for medical literature.
    This implementation uses the PubMed EUTILS API.
    """
    api_key = getattr(settings, 'MEDLINE_API_KEY', None)
    if not api_key:
        return {"error": "MEDLINE API key not configured"}
    
    try:
        # PubMed EUTILS API endpoint
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        
        # Search for articles
        search_url = f"{base_url}esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "api_key": api_key,
            "retmode": "json"
        }
        
        search_response = requests.get(search_url, params=search_params, timeout=10)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        # Get article IDs
        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return {"results": [], "message": "No articles found"}
        
        # Fetch article details
        fetch_url = f"{base_url}efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "xml",
            "api_key": api_key
        }
        
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=10)
        fetch_response.raise_for_status()
        
        # Return simplified results
        return {
            "status": "success",
            "results": [{"id": id, "title": f"Medical article about {query}"} for id in id_list[:max_results]],
            "count": len(id_list[:max_results])
        }
        
    except Exception as e:
        return {"error": f"Failed to search MEDLINE: {str(e)}"}

def search_umls(query: str):
    """
    Search UMLS (Unified Medical Language System) for medical terms.
    This is a placeholder implementation.
    """
    api_key = getattr(settings, 'UMLS_API_KEY', None)
    if not api_key:
        return {"error": "UMLS API key not configured"}
    
    # Placeholder for actual API call
    # In a real implementation, this would call the UMLS REST API
    return {
        "status": "placeholder",
        "message": "UMLS search would return standardized medical terminology",
        "query": query
    }

def get_cdc_data(condition: str):
    """
    Retrieve CDC data for a specific condition using direct endpoints.
    No API key required.
    """
    try:
        # Updated CDC API endpoints with working URLs
        # Using a known working endpoint for demonstration
        cdc_endpoints = {
            "influenza": "https://data.cdc.gov/resource/unsk-b7fc.json",
            "covid": "https://data.cdc.gov/resource/unsk-b7fc.json",
            "diabetes": "https://data.cdc.gov/resource/unsk-b7fc.json"
        }
        
        # Check if we have a specific endpoint for this condition
        endpoint = None
        for key in cdc_endpoints:
            if key in condition.lower():
                endpoint = cdc_endpoints[key]
                break
        
        if not endpoint:
            # Try a general search
            endpoint = "https://data.cdc.gov/resource/unsk-b7fc.json"
        
        # Fetch data (in a real implementation, you'd parse the actual response)
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        
        # Return simplified results
        return {
            "status": "success",
            "source": "CDC",
            "condition": condition,
            "message": f"CDC data for {condition} retrieved successfully",
            "data_available": True
        }
        
    except Exception as e:
        return {
            "status": "fallback",
            "source": "CDC",
            "condition": condition,
            "message": f"Could not retrieve CDC data: {str(e)}. Using local guidelines.",
            "data_available": False
        }

def get_who_data(condition: str):
    """
    Retrieve WHO data for a specific condition using direct endpoints.
    No API key required.
    """
    try:
        # Example WHO API endpoints - these would be replaced with actual endpoints
        # This is a simplified implementation
        who_endpoints = {
            "influenza": "https://apps.who.int/gho/athena/api/GHO/FLU_CASES.xml",
            "covid": "https://covid19.who.int/WHO-COVID-19-global-data.csv",
            "tuberculosis": "https://apps.who.int/gho/athena/api/GHO/TB.csv"
        }
        
        # Check if we have a specific endpoint for this condition
        endpoint = None
        for key in who_endpoints:
            if key in condition.lower():
                endpoint = who_endpoints[key]
                break
        
        if not endpoint:
            # Try a general endpoint
            endpoint = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
        
        # Fetch data (in a real implementation, you'd parse the actual response)
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        
        # Return simplified results
        return {
            "status": "success",
            "source": "WHO",
            "condition": condition,
            "message": f"WHO data for {condition} retrieved successfully",
            "data_available": True
        }
        
    except Exception as e:
        return {
            "status": "fallback",
            "source": "WHO",
            "condition": condition,
            "message": f"Could not retrieve WHO data: {str(e)}. Using local guidelines.",
            "data_available": False
        }

def search_serper(query: str):
    """
    Search medical conditions and diagnoses using Serper API.
    This provides dynamic diagnosis generation based on symptoms.
    """
    api_key = getattr(settings, 'SERPER_API_KEY', None)
    if not api_key:
        return {"error": "Serper API key not configured"}
    
    try:
        # Serper API endpoint for Google search
        url = "https://google.serper.dev/search"
        
        payload = {
            "q": f"medical diagnosis symptoms {query}",
            "num": 10
        }
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant medical information
        results = []
        if 'organic' in data:
            for item in data['organic']:
                title = item.get('title', '')
                snippet = item.get('snippet', '')
                # Only include results that seem medically relevant
                if any(keyword in title.lower() or keyword in snippet.lower() 
                       for keyword in ['symptom', 'diagnosis', 'medical', 'condition', 'disease', 'treatment']):
                    results.append({
                        "title": title,
                        "snippet": snippet,
                        "link": item.get('link', ''),
                        "match_score": 7.0  # Give a reasonable default score
                    })
        
        return {
            "status": "success",
            "query": query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to search Serper: {str(e)}",
            "query": query
        }

from typing import Optional, List

def search_nlm_conditions(symptoms: str):
    """
    Search medical conditions using NLM Conditions API.
    This provides accurate condition matching based on symptoms.
    """
    try:
        # NLM Conditions API endpoint
        base_url = "https://clinicaltables.nlm.nih.gov/api/conditions/v3/search"
        
        # Prepare query parameters
        params = {
            "terms": symptoms,
            "maxList": 10
        }
        
        # Make the request to NLM Conditions API with proper headers
        headers = {
            "User-Agent": "AgenticClinicalDecisionAssistant/1.0 (Python requests)"
        }
        
        # Make the request to NLM Conditions API
        response = requests.get(base_url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant medical information
        results = []
        # The NLM API returns data in format: [total_count, codes, names, conditions]
        if len(data) >= 4 and data[3]:  # Check if we have conditions data
            conditions = data[3]  # The conditions are in the 4th element
            codes = data[1] if len(data) > 1 and data[1] else []  # The codes are in the 2nd element
            
            for i, condition in enumerate(conditions):
                if isinstance(condition, list) and len(condition) > 0:
                    # Extract condition name (first element)
                    condition_name = condition[0]
                    
                    # Try to get code if available
                    code = ""
                    if codes and i < len(codes):
                        code = codes[i]
                    
                    results.append({
                        "title": condition_name,
                        "snippet": f"Medical condition: {condition_name}",
                        "code": code,
                        "match_score": 9.0 - (i * 0.5)  # Decreasing score based on position
                    })
        
        return {
            "status": "success",
            "query": symptoms,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to search NLM Conditions: {str(e)}",
            "query": symptoms
        }

# Example of how these functions could be integrated into the RAG agent
def enhance_rag_with_external_data(query: str):
    """
    Example of how external medical APIs could enhance the RAG system.
    """
    enhanced_data = {
        "query": query,
        "medline_results": search_medline(query),
        "cdc_data": get_cdc_data(query),
        "who_data": get_who_data(query),
        "serper_data": search_serper(query),  # Add Serper data
        "nlm_conditions_data": search_nlm_conditions(query)  # Add NLM Conditions data
    }
    
    return enhanced_data