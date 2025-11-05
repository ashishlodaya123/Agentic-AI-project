#!/usr/bin/env python3

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_conversion():
    # Import the conversion function
    from app.agents.decision_agent import _convert_string_to_structured_data
    
    # Test string response
    test_response = "Based on the presented data, the primary concerns are: shortness of breath. This suggests a potentially serious condition requiring immediate attention."
    
    print("Testing conversion function...")
    result = _convert_string_to_structured_data(test_response)
    
    print("Conversion Result:")
    print(f"Type: {type(result)}")
    if isinstance(result, dict):
        print(f"Keys: {list(result.keys())}")
        print(f"Summary: {result.get('summary', 'No summary')}")
        print(f"Vital Signs: {result.get('vital_signs', 'No vital signs')}")
        print(f"Symptom Categories: {result.get('symptom_categories', 'No symptom categories')}")
        print(f"Primary Concerns: {result.get('primary_concerns', 'No primary concerns')}")
        
        # Check if vital signs section has data
        vital_signs = result.get('vital_signs', {})
        if vital_signs:
            print("\nVital Signs Details:")
            for name, data in vital_signs.items():
                print(f"  {name}: {data}")
        
        # Check if symptom categories section has data
        symptom_categories = result.get('symptom_categories', {})
        if symptom_categories:
            print("\nSymptom Categories Details:")
            for category, symptoms in symptom_categories.items():
                if symptoms:
                    print(f"  {category}: {symptoms}")
    else:
        print(f"Result: {result}")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_conversion()