import re
from app.core.agent_memory import get_agent_memory

class RiskStratificationAgent:
    """
    Agent to predict patient risk using sophisticated rule-based logic.
    Provides comprehensive risk assessment with detailed categorization.
    """
    def __init__(self):
        self.memory = get_agent_memory()

    def run(self, patient_data: dict) -> dict:
        """
        Predicts the risk score and provides detailed risk assessment.
        Returns comprehensive risk analysis with categorization.
        """
        age = patient_data.get("age", 50)
        # Convert age to int if it's a string
        try:
            age = int(age)
        except (ValueError, TypeError):
            age = 50  # Default age if conversion fails
        
        vitals = patient_data.get("vitals", {})
        symptoms = patient_data.get("symptoms", "")
        gender = patient_data.get("gender", "")
        
        # Calculate comprehensive risk assessment
        risk_assessment = self._comprehensive_risk_assessment(age, vitals, symptoms, gender)
        
        # Store risk assessment in shared memory
        self.memory.store_agent_output("risk", risk_assessment)
        
        return risk_assessment

    def _comprehensive_risk_assessment(self, age: int, vitals: dict, symptoms: str, gender: str) -> dict:
        """Calculate comprehensive risk assessment with detailed categorization."""
        # Initialize risk components
        vital_risks = self._assess_vital_risks(vitals)
        symptom_risks = self._assess_symptom_risks(symptoms)
        demographic_risks = self._assess_demographic_risks(age, gender)
        
        # Calculate overall risk score
        risk_score = self._calculate_weighted_risk_score(vital_risks, symptom_risks, demographic_risks)
        
        # Categorize risk level
        risk_category = self._categorize_risk_level(risk_score)
        
        # Generate risk explanation
        risk_explanation = self._generate_risk_explanation(vital_risks, symptom_risks, demographic_risks)
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_category": risk_category,
            "vital_risks": vital_risks,
            "symptom_risks": symptom_risks,
            "demographic_risks": demographic_risks,
            "risk_explanation": risk_explanation,
            "triage_recommendation": self._generate_triage_recommendation(risk_score)
        }

    def _assess_vital_risks(self, vitals: dict) -> dict:
        """Assess risks based on vital signs."""
        risks = {
            "heart_rate_risk": 0.0,
            "temperature_risk": 0.0,
            "blood_pressure_risk": 0.0,
            "overall_vital_risk": 0.0,
            "critical_vitals": []
        }
        
        # Heart rate risk assessment
        heart_rate = vitals.get("heart_rate")
        if heart_rate is not None:
            try:
                hr = int(heart_rate)
                if hr > 130:
                    risks["heart_rate_risk"] = 0.9
                    risks["critical_vitals"].append("Severe tachycardia")
                elif hr > 120:
                    risks["heart_rate_risk"] = 0.7
                elif hr > 100:
                    risks["heart_rate_risk"] = 0.4
                elif hr < 50:
                    risks["heart_rate_risk"] = 0.8
                    risks["critical_vitals"].append("Severe bradycardia")
                elif hr < 60:
                    risks["heart_rate_risk"] = 0.3
            except (ValueError, TypeError):
                pass
        
        # Temperature risk assessment
        temperature = vitals.get("temperature")
        if temperature is not None:
            try:
                temp = float(temperature)
                if temp > 39.5:
                    risks["temperature_risk"] = 0.9
                    risks["critical_vitals"].append("High fever")
                elif temp > 39.0:
                    risks["temperature_risk"] = 0.7
                elif temp > 38.0:
                    risks["temperature_risk"] = 0.5
                elif temp < 35.0:
                    risks["temperature_risk"] = 0.8
                    risks["critical_vitals"].append("Hypothermia")
                elif temp < 36.0:
                    risks["temperature_risk"] = 0.4
            except (ValueError, TypeError):
                pass
        
        # Blood pressure risk assessment
        blood_pressure = vitals.get("blood_pressure")
        if blood_pressure is not None:
            try:
                bp_parts = blood_pressure.split("/")
                if len(bp_parts) == 2:
                    systolic = int(bp_parts[0])
                    diastolic = int(bp_parts[1])
                    if systolic > 180 or diastolic > 120:
                        risks["blood_pressure_risk"] = 0.9
                        risks["critical_vitals"].append("Hypertensive crisis")
                    elif systolic > 140 or diastolic > 90:
                        risks["blood_pressure_risk"] = 0.6
                    elif systolic < 80 or diastolic < 50:
                        risks["blood_pressure_risk"] = 0.8
                        risks["critical_vitals"].append("Severe hypotension")
                    elif systolic < 90 or diastolic < 60:
                        risks["blood_pressure_risk"] = 0.4
            except (ValueError, TypeError):
                pass
        
        # Calculate overall vital risk
        risks["overall_vital_risk"] = max(
            risks["heart_rate_risk"],
            risks["temperature_risk"],
            risks["blood_pressure_risk"]
        )
        
        return risks

    def _assess_symptom_risks(self, symptoms: str) -> dict:
        """Assess risks based on symptoms."""
        risks = {
            "critical_symptom_risk": 0.0,
            "moderate_symptom_risk": 0.0,
            "mild_symptom_risk": 0.0,
            "overall_symptom_risk": 0.0,
            "identified_symptoms": []
        }
        
        # Critical symptoms (high risk)
        critical_symptoms = [
            ("chest pain", 0.9),
            ("shortness of breath", 0.85),
            ("loss of consciousness", 0.95),
            ("severe headache", 0.7),
            ("difficulty breathing", 0.9),
            ("severe dizziness", 0.75),
            ("persistent vomiting", 0.6),
            ("high fever", 0.7),
            ("severe abdominal pain", 0.7)
        ]
        
        # Moderate symptoms
        moderate_symptoms = [
            ("fatigue", 0.3),
            ("mild fever", 0.4),
            ("nausea", 0.35),
            ("dizziness", 0.4),
            ("cough", 0.2),
            ("sore throat", 0.15)
        ]
        
        symptoms_lower = symptoms.lower()
        
        # Check for critical symptoms
        for symptom, risk_value in critical_symptoms:
            if symptom in symptoms_lower:
                risks["critical_symptom_risk"] = max(risks["critical_symptom_risk"], risk_value)
                risks["identified_symptoms"].append({
                    "symptom": symptom,
                    "severity": "critical",
                    "risk_contribution": risk_value
                })
        
        # Check for moderate symptoms
        for symptom, risk_value in moderate_symptoms:
            if symptom in symptoms_lower:
                risks["moderate_symptom_risk"] = max(risks["moderate_symptom_risk"], risk_value)
                if not any(s["symptom"] == symptom for s in risks["identified_symptoms"]):
                    risks["identified_symptoms"].append({
                        "symptom": symptom,
                        "severity": "moderate",
                        "risk_contribution": risk_value
                    })
        
        # Calculate overall symptom risk
        risks["overall_symptom_risk"] = max(
            risks["critical_symptom_risk"],
            risks["moderate_symptom_risk"]
        )
        
        return risks

    def _assess_demographic_risks(self, age: int, gender: str) -> dict:
        """Assess risks based on demographic factors."""
        risks = {
            "age_risk": 0.0,
            "gender_risk": 0.0,
            "overall_demographic_risk": 0.0
        }
        
        # Age risk assessment
        if age > 80:
            risks["age_risk"] = 0.7
        elif age > 65:
            risks["age_risk"] = 0.5
        elif age > 50:
            risks["age_risk"] = 0.3
        elif age < 18:
            risks["age_risk"] = 0.4  # Pediatric risk
        elif age < 5:
            risks["age_risk"] = 0.6  # High pediatric risk
        
        # Gender-specific considerations (simplified)
        if gender.lower() in ["male", "female"]:
            risks["gender_risk"] = 0.1  # Minimal baseline risk
        
        # Calculate overall demographic risk
        risks["overall_demographic_risk"] = max(
            risks["age_risk"],
            risks["gender_risk"]
        )
        
        return risks

    def _calculate_weighted_risk_score(self, vital_risks: dict, symptom_risks: dict, demographic_risks: dict) -> float:
        """Calculate weighted risk score based on all risk factors."""
        # Weight factors (can be adjusted based on clinical importance)
        vital_weight = 0.4
        symptom_weight = 0.5
        demographic_weight = 0.1
        
        # Calculate weighted components
        weighted_vital_risk = vital_risks["overall_vital_risk"] * vital_weight
        weighted_symptom_risk = symptom_risks["overall_symptom_risk"] * symptom_weight
        weighted_demographic_risk = demographic_risks["overall_demographic_risk"] * demographic_weight
        
        # Combine weighted risks
        total_risk = weighted_vital_risk + weighted_symptom_risk + weighted_demographic_risk
        
        # Apply critical factor multiplier if critical vitals or symptoms are present
        critical_factor = 1.0
        if (vital_risks["critical_vitals"] and len(vital_risks["critical_vitals"]) > 0) or \
           any(s["severity"] == "critical" for s in symptom_risks["identified_symptoms"]):
            critical_factor = 1.2  # Increase risk for critical findings
        
        return min(1.0, total_risk * critical_factor)

    def _categorize_risk_level(self, risk_score: float) -> str:
        """Categorize risk level based on score."""
        if risk_score >= 0.8:
            return "Critical"
        elif risk_score >= 0.6:
            return "High"
        elif risk_score >= 0.4:
            return "Moderate"
        elif risk_score >= 0.2:
            return "Low"
        else:
            return "Minimal"

    def _generate_risk_explanation(self, vital_risks: dict, symptom_risks: dict, demographic_risks: dict) -> str:
        """Generate detailed explanation of risk assessment."""
        explanations = []
        
        # Vital risks explanation
        if vital_risks["critical_vitals"] and len(vital_risks["critical_vitals"]) > 0:
            explanations.append(f"Critical vital signs detected: {', '.join(vital_risks['critical_vitals'])}")
        elif vital_risks["overall_vital_risk"] > 0.5:
            explanations.append("Significant abnormalities in vital signs")
        elif vital_risks["overall_vital_risk"] > 0:
            explanations.append("Mild abnormalities in vital signs")
        
        # Symptom risks explanation
        critical_symptoms = [s for s in symptom_risks["identified_symptoms"] if s["severity"] == "critical"]
        if critical_symptoms:
            symptom_names = [s["symptom"] for s in critical_symptoms]
            explanations.append(f"Critical symptoms present: {', '.join(symptom_names)}")
        elif symptom_risks["overall_symptom_risk"] > 0.5:
            explanations.append("Moderate symptom burden")
        elif symptom_risks["overall_symptom_risk"] > 0:
            explanations.append("Mild symptom burden")
        
        # Demographic risks explanation
        if demographic_risks["overall_demographic_risk"] > 0.5:
            explanations.append("High-risk demographic factors")
        elif demographic_risks["overall_demographic_risk"] > 0:
            explanations.append("Moderate demographic risk factors")
        
        if not explanations:
            return "No significant risk factors identified. Patient appears stable based on provided information."
        
        return "Risk factors identified: " + "; ".join(explanations)

    def _generate_triage_recommendation(self, risk_score: float) -> dict:
        """Generate triage recommendation based on risk score."""
        if risk_score >= 0.8:
            return {
                "priority": "Immediate",
                "urgency": "Red",
                "action": "Emergency intervention required",
                "facility": "Emergency Department",
                "specialist": "Emergency Medicine",
                "timeframe": "Immediate (within 15 minutes)"
            }
        elif risk_score >= 0.6:
            return {
                "priority": "Urgent",
                "urgency": "Orange",
                "action": "Prompt medical evaluation",
                "facility": "Urgent Care or Emergency Department",
                "specialist": "Internal Medicine or Emergency Medicine",
                "timeframe": "Within 1 hour"
            }
        elif risk_score >= 0.4:
            return {
                "priority": "Priority",
                "urgency": "Yellow",
                "action": "Timely medical evaluation",
                "facility": "Outpatient Clinic",
                "specialist": "Primary Care or Relevant Specialty",
                "timeframe": "Within 24 hours"
            }
        elif risk_score >= 0.2:
            return {
                "priority": "Routine",
                "urgency": "Green",
                "action": "Routine medical evaluation",
                "facility": "Outpatient Clinic",
                "specialist": "Primary Care",
                "timeframe": "Within 72 hours"
            }
        else:
            return {
                "priority": "Non-urgent",
                "urgency": "Blue",
                "action": "Routine monitoring",
                "facility": "Outpatient Clinic",
                "specialist": "Primary Care",
                "timeframe": "Within 1 week"
            }