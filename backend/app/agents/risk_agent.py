import re

class RiskStratificationAgent:
    """
    Agent to predict patient risk using rule-based logic instead of ML models.
    """
    def __init__(self):
        pass

    def run(self, patient_data: dict) -> float:
        """
        Predicts the risk score based on patient data using rule-based logic.
        """
        age = patient_data.get("age", 50)
        # Convert age to int if it's a string
        try:
            age = int(age)
        except (ValueError, TypeError):
            age = 50  # Default age if conversion fails
        
        vitals = patient_data.get("vitals", {})
        symptoms = patient_data.get("symptoms", "")
        
        # Calculate risk score based on rules
        risk_score = self._calculate_risk_score(age, vitals, symptoms)
        return risk_score

    def _calculate_risk_score(self, age: int, vitals: dict, symptoms: str) -> float:
        """Calculate risk score based on clinical rules."""
        risk_factors = 0.0
        total_factors = 0.0
        
        # Age factor
        total_factors += 1
        if age > 65:
            risk_factors += 1
        elif age > 50:
            risk_factors += 0.5
            
        # Heart rate factor
        total_factors += 1
        heart_rate = vitals.get("heart_rate", 70)
        try:
            heart_rate = int(heart_rate)
            if heart_rate > 120:
                risk_factors += 1
            elif heart_rate > 100:
                risk_factors += 0.5
        except (ValueError, TypeError):
            pass  # Invalid heart rate value
            
        # Temperature factor
        total_factors += 1
        temperature = vitals.get("temperature", 37.0)
        try:
            temperature = float(temperature)
            if temperature > 39.0:
                risk_factors += 1
            elif temperature > 38.0:
                risk_factors += 0.5
        except (ValueError, TypeError):
            pass  # Invalid temperature value
            
        # Blood pressure factor
        total_factors += 1
        blood_pressure = vitals.get("blood_pressure", "120/80")
        if "blood_pressure" in vitals:
            try:
                systolic = int(blood_pressure.split("/")[0])
                if systolic > 180:
                    risk_factors += 1
                elif systolic > 140:
                    risk_factors += 0.5
            except:
                pass
                
        # Symptom factors
        critical_symptoms = ["chest pain", "shortness of breath", "severe headache", 
                           "difficulty breathing", "loss of consciousness"]
        total_factors += len(critical_symptoms)
        for symptom in critical_symptoms:
            if symptom in symptoms.lower():
                risk_factors += 1
                
        # Calculate normalized risk score
        if total_factors == 0:
            return 0.0
            
        return min(1.0, risk_factors / total_factors)