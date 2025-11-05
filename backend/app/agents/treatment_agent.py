import re
from typing import Dict, List, Any
from app.core.agent_memory import get_agent_memory

class TreatmentRecommendationAgent:
    """
    Agent to generate evidence-based treatment recommendations.
    Provides personalized treatment suggestions based on patient data and clinical guidelines.
    """
    def __init__(self):
        self.memory = get_agent_memory()
        
        # Treatment guidelines database
        self.treatment_guidelines = {
            "chest_pain": {
                "primary": ["Nitroglycerin for acute relief", "Aspirin 325mg chewable", "Oxygen therapy if hypoxic"],
                "secondary": ["ECG monitoring", "Cardiac enzymes panel", "IV access establishment"],
                "follow_up": ["Cardiology consultation within 24 hours", "Stress testing as indicated"]
            },
            "shortness_of_breath": {
                "primary": ["Oxygen therapy to maintain SpO2 >92%", "Bronchodilators for wheezing", "Diuretics for heart failure"],
                "secondary": ["Chest X-ray", "Arterial blood gas analysis", "Complete blood count"],
                "follow_up": ["Pulmonology consultation for persistent symptoms", "Pulmonary function tests"]
            },
            "fever": {
                "primary": ["Acetaminophen 650mg every 4 hours", "Adequate hydration", "Rest"],
                "secondary": ["Blood cultures if >39°C", "Urinalysis", "Complete blood count"],
                "follow_up": ["Infectious disease consultation for persistent fever", "Antibiotic therapy as indicated"]
            },
            "hypertension": {
                "primary": ["Lifestyle modifications", "ACE inhibitors or ARBs", "Calcium channel blockers"],
                "secondary": ["Electrolyte panel", "Renal function tests", "Echocardiogram"],
                "follow_up": ["Cardiology follow-up in 2 weeks", "Home blood pressure monitoring"]
            }
        }
        
        # Contraindication database
        self.contraindications = {
            "aspirin": ["allergy_to_nsaids", "active_bleeding", "severe_liver_disease"],
            "nitroglycerin": ["severe_anemia", "increased_intracranial_pressure", "phosphodiesterase_inhibitors"],
            "ace_inhibitors": ["pregnancy", "angioedema_history", "bilateral_renal_artery_stenosis"]
        }

    def run(self, patient_data: dict, symptoms_analysis: dict, risk_assessment: dict) -> dict:
        """
        Generate treatment recommendations based on patient data, symptoms analysis, and risk assessment.
        Returns comprehensive treatment plan with primary, secondary, and follow-up recommendations.
        """
        # Extract relevant information
        symptoms = patient_data.get("symptoms", "")
        vitals = patient_data.get("vitals", {})
        age = patient_data.get("age", 0)
        gender = patient_data.get("gender", "")
        
        # Generate treatment recommendations
        recommendations = self._generate_treatment_recommendations(
            symptoms, vitals, age, gender, symptoms_analysis, risk_assessment
        )
        
        # Store recommendations in shared memory
        self.memory.store_agent_output("treatment", {
            "patient_data": patient_data,
            "recommendations": recommendations
        })
        
        return recommendations

    def _generate_treatment_recommendations(self, symptoms: str, vitals: dict, age: int, 
                                          gender: str, symptoms_analysis: dict, risk_assessment: dict) -> dict:
        """Generate comprehensive treatment recommendations."""
        # Identify primary conditions
        conditions = self._identify_conditions(symptoms, vitals)
        
        # Generate recommendations for each condition
        treatment_plan = {
            "primary_recommendations": [],
            "secondary_recommendations": [],
            "follow_up_recommendations": [],
            "contraindications_checked": [],
            "rationale": []
        }
        
        # Check for contraindications
        contraindications = self._check_contraindications(patient_data={"age": age, "gender": gender})
        treatment_plan["contraindications_checked"] = contraindications
        
        # Generate recommendations for each identified condition
        for condition in conditions:
            if condition in self.treatment_guidelines:
                guidelines = self.treatment_guidelines[condition]
                treatment_plan["primary_recommendations"].extend(guidelines.get("primary", []))
                treatment_plan["secondary_recommendations"].extend(guidelines.get("secondary", []))
                treatment_plan["follow_up_recommendations"].extend(guidelines.get("follow_up", []))
                
                # Add rationale for recommendations
                treatment_plan["rationale"].append({
                    "condition": condition,
                    "evidence_based": True,
                    "guideline_reference": f"Clinical guidelines for {condition}",
                    "urgency": self._determine_treatment_urgency(condition, risk_assessment)
                })
        
        # Add general supportive care if no specific conditions identified
        if not treatment_plan["primary_recommendations"]:
            treatment_plan["primary_recommendations"] = [
                "Monitor vital signs every 15 minutes",
                "Establish IV access",
                "Provide emotional support to patient"
            ]
            treatment_plan["rationale"].append({
                "condition": "general_supportive_care",
                "evidence_based": True,
                "guideline_reference": "Standard emergency care protocols",
                "urgency": "routine"
            })
        
        # Add risk-based modifications
        self._add_risk_based_modifications(treatment_plan, risk_assessment)
        
        return {
            "treatment_plan": treatment_plan,
            "confidence_score": self._calculate_confidence_score(conditions),
            "personalization_factors": {
                "age": age,
                "gender": gender,
                "risk_level": risk_assessment.get("risk_category", "unknown")
            }
        }

    def _identify_conditions(self, symptoms: str, vitals: dict) -> List[str]:
        """Identify medical conditions based on symptoms and vitals."""
        conditions = []
        symptoms_lower = symptoms.lower()
        
        # Symptom-based condition identification
        if "chest pain" in symptoms_lower:
            conditions.append("chest_pain")
        if "shortness of breath" in symptoms_lower or "difficulty breathing" in symptoms_lower:
            conditions.append("shortness_of_breath")
        if "fever" in symptoms_lower or self._has_fever(vitals):
            conditions.append("fever")
            
        # Vital-based condition identification
        if self._has_hypertension(vitals):
            conditions.append("hypertension")
            
        return conditions

    def _has_fever(self, vitals: dict) -> bool:
        """Check if patient has fever based on vital signs."""
        temperature = vitals.get("temperature")
        if temperature is not None:
            try:
                temp = float(temperature)
                return temp > 38.0
            except (ValueError, TypeError):
                return False
        return False

    def _has_hypertension(self, vitals: dict) -> bool:
        """Check if patient has hypertension based on vital signs."""
        blood_pressure = vitals.get("blood_pressure")
        if blood_pressure is not None:
            try:
                bp_parts = blood_pressure.split("/")
                if len(bp_parts) == 2:
                    systolic = int(bp_parts[0])
                    diastolic = int(bp_parts[1])
                    return systolic > 140 or diastolic > 90
            except (ValueError, TypeError):
                return False
        return False

    def _check_contraindications(self, patient_data: dict) -> List[Dict[str, Any]]:
        """Check for potential contraindications based on patient data."""
        # This is a simplified implementation - in a real system, this would be more comprehensive
        contraindications_found = []
        
        age = patient_data.get("age", 0)
        gender = patient_data.get("gender", "")
        
        # Age-based contraindications
        if age > 75:
            contraindications_found.append({
                "medication": "aggressive_antihypertensives",
                "reason": "Increased fall risk in elderly",
                "recommendation": "Use caution with blood pressure lowering agents"
            })
            
        # Gender-based considerations
        if gender.lower() == "female" and age >= 12 and age <= 50:
            contraindications_found.append({
                "medication": "ace_inhibitors",
                "reason": "Pregnancy potential",
                "recommendation": "Verify pregnancy status before ACE inhibitor use"
            })
            
        return contraindications_found

    def _determine_treatment_urgency(self, condition: str, risk_assessment: dict) -> str:
        """Determine treatment urgency based on condition and risk assessment."""
        risk_score = risk_assessment.get("risk_score", 0)
        
        # High-risk conditions
        high_urgency_conditions = ["chest_pain", "shortness_of_breath"]
        if condition in high_urgency_conditions:
            if risk_score > 0.7:
                return "immediate"
            elif risk_score > 0.4:
                return "urgent"
            else:
                return "prompt"
                
        # Moderate-risk conditions
        moderate_urgency_conditions = ["fever", "hypertension"]
        if condition in moderate_urgency_conditions:
            if risk_score > 0.6:
                return "urgent"
            elif risk_score > 0.3:
                return "prompt"
            else:
                return "routine"
                
        return "routine"

    def _add_risk_based_modifications(self, treatment_plan: dict, risk_assessment: dict):
        """Add modifications to treatment plan based on risk assessment."""
        risk_score = risk_assessment.get("risk_score", 0)
        risk_category = risk_assessment.get("risk_category", "low")
        
        if risk_score > 0.7:
            # High-risk modifications
            treatment_plan["primary_recommendations"].insert(0, "Continuous cardiac monitoring")
            treatment_plan["primary_recommendations"].insert(1, "Frequent neurologic assessments")
            treatment_plan["secondary_recommendations"].append("STAT cardiac enzymes")
        elif risk_score > 0.4:
            # Moderate-risk modifications
            treatment_plan["primary_recommendations"].insert(0, "Hourly vital signs monitoring")
            treatment_plan["secondary_recommendations"].append("Repeat ECG in 30 minutes")

    def _calculate_confidence_score(self, conditions: List[str]) -> float:
        """Calculate confidence score for treatment recommendations."""
        if not conditions:
            return 0.3  # Low confidence for general recommendations
            
        # Higher confidence when specific conditions are identified
        base_confidence = 0.7
        confidence_boost = min(len(conditions) * 0.1, 0.3)  # Max 0.3 boost for multiple conditions
        return min(base_confidence + confidence_boost, 0.95)  # Cap at 0.95