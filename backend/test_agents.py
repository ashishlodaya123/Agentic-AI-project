#!/usr/bin/env python3

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_decision_agent():
    # Import the agent
    from app.agents.decision_agent import DecisionSupportAgent
    
    # Test data
    test_patient_data = {
        "symptoms": "Patient reports experiencing persistent cough and shortness of breath for the past 5 days. The cough is dry, with occasional mild chest discomfort. No history of asthma or allergies. Reports mild fatigue and a sore throat but denies fever, nausea, or vomiting.",
        "vitals": {
            "heart_rate": "88",
            "blood_pressure": "128/82",
            "temperature": "37.6"
        },
        "age": 34,
        "gender": "Female",
        "image_path": None
    }
    
    print("Testing DecisionSupportAgent...")
    decision_agent = DecisionSupportAgent()
    result = decision_agent.run(test_patient_data)
    
    print("Decision Agent Result:")
    print(f"Type: {type(result)}")
    
    if isinstance(result, dict):
        final_recommendation = result.get('final_recommendation', {})
        symptoms_analysis = final_recommendation.get('patient_analysis', {})
        
        print(f"Symptoms Analysis Type: {type(symptoms_analysis)}")
        if isinstance(symptoms_analysis, dict):
            print(f"Keys: {list(symptoms_analysis.keys())}")
            print(f"Summary: {symptoms_analysis.get('summary', 'No summary')}")
            print(f"Vital Signs: {symptoms_analysis.get('vital_signs', 'No vital signs')}")
            print(f"Symptom Categories: {symptoms_analysis.get('symptom_categories', 'No symptom categories')}")
            print(f"Primary Concerns: {symptoms_analysis.get('primary_concerns', 'No primary concerns')}")
            
            # Check if vital signs section has data
            vital_signs = symptoms_analysis.get('vital_signs', {})
            if vital_signs:
                print("\nVital Signs Details:")
                for name, data in vital_signs.items():
                    print(f"  {name}: {data}")
            
            # Check if symptom categories section has data
            symptom_categories = symptoms_analysis.get('symptom_categories', {})
            if symptom_categories:
                print("\nSymptom Categories Details:")
                for category, symptoms in symptom_categories.items():
                    if symptoms:
                        print(f"  {category}: {symptoms}")
        else:
            print(f"Symptoms Analysis: {symptoms_analysis}")
    else:
        print(f"Result: {result}")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_decision_agent()