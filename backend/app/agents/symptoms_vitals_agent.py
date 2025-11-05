import re

class SymptomsVitalsAgent:
    """
    Agent to process and analyze patient symptoms and vital signs using rule-based logic.
    """
    def __init__(self):
        pass

    def run(self, patient_data: dict) -> str:
        """
        Analyzes symptoms and vitals to produce a summary.
        """
        symptoms = patient_data.get("symptoms", "")
        vitals = patient_data.get("vitals", {})

        # Simple rule-based analysis
        analysis = self._analyze_patient_data(symptoms, vitals)
        return analysis

    def _analyze_patient_data(self, symptoms: str, vitals: dict) -> str:
        """Perform a simple rule-based analysis of patient data."""
        # Parse vitals
        vitals_dict = vitals
        
        # Generate analysis based on rules
        concerns = []
        
        # Check for high heart rate
        if "heart_rate" in vitals_dict:
            try:
                heart_rate = int(vitals_dict["heart_rate"])
                if heart_rate > 100:
                    concerns.append("elevated heart rate")
            except (ValueError, TypeError):
                pass  # Invalid heart rate value
        
        # Check for fever
        if "temperature" in vitals_dict:
            try:
                temperature = float(vitals_dict["temperature"])
                if temperature > 38.0:
                    concerns.append("fever")
            except (ValueError, TypeError):
                pass  # Invalid temperature value
        
        # Check for critical symptoms
        critical_symptoms = ["chest pain", "shortness of breath", "severe headache", "difficulty breathing"]
        found_symptoms = [symptom for symptom in critical_symptoms if symptom in symptoms.lower()]
        
        if found_symptoms:
            concerns.extend(found_symptoms)
        
        if concerns:
            return f"Based on the presented data, the primary concerns are: {', '.join(concerns)}. This suggests a potentially serious condition requiring immediate attention."
        else:
            return "The patient's symptoms and vitals do not indicate any immediately life-threatening conditions, but a thorough examination is recommended."