import re
from typing import Dict, List, Any
from datetime import datetime, timedelta
from app.core.agent_memory import get_agent_memory

class FollowupPlanningAgent:
    """
    Agent to create patient follow-up schedules and monitoring plans.
    Generates personalized follow-up recommendations based on patient conditions and risk assessment.
    """
    def __init__(self):
        self.memory = get_agent_memory()
        
        # Follow-up protocols database
        self.followup_protocols = {
            "chest_pain": {
                "immediate": {
                    "frequency": "2 hours",
                    "duration": "24 hours",
                    "parameters": ["ECG", "Cardiac enzymes", "Vital signs"],
                    "urgency": "continuous"
                },
                "short_term": {
                    "frequency": "daily",
                    "duration": "1 week",
                    "parameters": ["Chest pain assessment", "Medication compliance", "Activity tolerance"],
                    "urgency": "high"
                },
                "long_term": {
                    "frequency": "weekly",
                    "duration": "3 months",
                    "parameters": ["Cardiac function", "Lifestyle modifications", "Risk factor management"],
                    "urgency": "routine"
                }
            },
            "shortness_of_breath": {
                "immediate": {
                    "frequency": "4 hours",
                    "duration": "12 hours",
                    "parameters": ["Oxygen saturation", "Respiratory rate", "Breath sounds"],
                    "urgency": "frequent"
                },
                "short_term": {
                    "frequency": "every_other_day",
                    "duration": "2 weeks",
                    "parameters": ["Pulmonary function", "Medication response", "Symptom progression"],
                    "urgency": "moderate"
                },
                "long_term": {
                    "frequency": "monthly",
                    "duration": "6 months",
                    "parameters": ["Pulmonary rehabilitation", "Trigger avoidance", "Quality of life"],
                    "urgency": "routine"
                }
            },
            "fever": {
                "immediate": {
                    "frequency": "6 hours",
                    "duration": "48 hours",
                    "parameters": ["Temperature monitoring", "Hydration status", "Response to antipyretics"],
                    "urgency": "frequent"
                },
                "short_term": {
                    "frequency": "daily",
                    "duration": "1 week",
                    "parameters": ["Source identification", "Antibiotic response", "Complication monitoring"],
                    "urgency": "high"
                },
                "long_term": {
                    "frequency": "as_needed",
                    "duration": "2 weeks",
                    "parameters": ["Recovery assessment", "Return to normal activities", "Prevention education"],
                    "urgency": "routine"
                }
            },
            "hypertension": {
                "immediate": {
                    "frequency": "8 hours",
                    "duration": "72 hours",
                    "parameters": ["Blood pressure monitoring", "Medication side effects", "Symptom assessment"],
                    "urgency": "routine"
                },
                "short_term": {
                    "frequency": "weekly",
                    "duration": "1 month",
                    "parameters": ["Blood pressure control", "Medication titration", "Lifestyle adherence"],
                    "urgency": "moderate"
                },
                "long_term": {
                    "frequency": "monthly",
                    "duration": "indefinite",
                    "parameters": ["Target organ damage", "Comorbidity management", "Quality of life"],
                    "urgency": "routine"
                }
            }
        }
        
        # Monitoring parameters database
        self.monitoring_parameters = {
            "vital_signs": ["heart_rate", "blood_pressure", "temperature", "respiratory_rate", "oxygen_saturation"],
            "laboratory": ["complete_blood_count", "comprehensive_metabolic_panel", "cardiac_enzymes", "inflammatory_markers"],
            "imaging": ["chest_xray", "ecg", "echocardiogram"],
            "functional": ["activity_tolerance", "pain_scale", "quality_of_life_score"]
        }

    def run(self, patient_data: dict, symptoms_analysis: dict, risk_assessment: dict, 
            treatment_recommendations: dict) -> dict:
        """
        Generate follow-up plan based on patient data, symptoms analysis, risk assessment, and treatment recommendations.
        Returns comprehensive follow-up schedule with monitoring parameters and timelines.
        """
        # Extract relevant information
        symptoms = patient_data.get("symptoms", "")
        vitals = patient_data.get("vitals", {})
        age = patient_data.get("age", 0)
        gender = patient_data.get("gender", "")
        
        # Generate follow-up plan
        followup_plan = self._generate_followup_plan(
            symptoms, vitals, age, gender, symptoms_analysis, risk_assessment, treatment_recommendations
        )
        
        # Store follow-up plan in shared memory
        self.memory.store_agent_output("followup", {
            "patient_data": patient_data,
            "followup_plan": followup_plan
        })
        
        return followup_plan

    def _generate_followup_plan(self, symptoms: str, vitals: dict, age: int, gender: str,
                               symptoms_analysis: dict, risk_assessment: dict, 
                               treatment_recommendations: dict) -> dict:
        """Generate comprehensive follow-up plan."""
        # Identify primary conditions
        conditions = self._identify_conditions(symptoms, vitals)
        
        # Generate follow-up schedule for each condition
        followup_schedule = {
            "immediate_followup": [],
            "short_term_followup": [],
            "long_term_followup": [],
            "monitoring_parameters": {},
            "special_considerations": []
        }
        
        # Generate follow-up for each identified condition
        for condition in conditions:
            if condition in self.followup_protocols:
                protocols = self.followup_protocols[condition]
                
                # Immediate follow-up
                immediate = protocols.get("immediate", {})
                if immediate:
                    followup_schedule["immediate_followup"].append({
                        "condition": condition,
                        "frequency": immediate.get("frequency", "as_needed"),
                        "duration": immediate.get("duration", "24 hours"),
                        "parameters": immediate.get("parameters", []),
                        "urgency": immediate.get("urgency", "routine"),
                        "start_time": datetime.now().isoformat()
                    })
                
                # Short-term follow-up
                short_term = protocols.get("short_term", {})
                if short_term:
                    followup_schedule["short_term_followup"].append({
                        "condition": condition,
                        "frequency": short_term.get("frequency", "weekly"),
                        "duration": short_term.get("duration", "1 month"),
                        "parameters": short_term.get("parameters", []),
                        "urgency": short_term.get("urgency", "routine"),
                        "start_time": (datetime.now() + timedelta(hours=24)).isoformat()
                    })
                
                # Long-term follow-up
                long_term = protocols.get("long_term", {})
                if long_term:
                    followup_schedule["long_term_followup"].append({
                        "condition": condition,
                        "frequency": long_term.get("frequency", "monthly"),
                        "duration": long_term.get("duration", "3 months"),
                        "parameters": long_term.get("parameters", []),
                        "urgency": long_term.get("urgency", "routine"),
                        "start_time": (datetime.now() + timedelta(days=7)).isoformat()
                    })
        
        # Add monitoring parameters
        followup_schedule["monitoring_parameters"] = self._generate_monitoring_parameters(
            conditions, risk_assessment, treatment_recommendations
        )
        
        # Add special considerations based on patient demographics and risk
        followup_schedule["special_considerations"] = self._generate_special_considerations(
            age, gender, risk_assessment
        )
        
        # Add risk-based modifications
        self._add_risk_based_modifications(followup_schedule, risk_assessment)
        
        return {
            "followup_schedule": followup_schedule,
            "confidence_score": self._calculate_confidence_score(conditions),
            "personalization_factors": {
                "age": age,
                "gender": gender,
                "risk_level": risk_assessment.get("risk_category", "unknown"),
                "conditions": conditions
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

    def _generate_monitoring_parameters(self, conditions: List[str], risk_assessment: dict,
                                       treatment_recommendations: dict) -> Dict[str, List[str]]:
        """Generate monitoring parameters based on conditions and treatments."""
        parameters = {}
        
        # Add basic vital signs monitoring for all patients
        parameters["vital_signs"] = self.monitoring_parameters["vital_signs"]
        
        # Add condition-specific monitoring
        for condition in conditions:
            if condition == "chest_pain":
                parameters["cardiac"] = ["ecg", "cardiac_enzymes", "heart_sounds"]
            elif condition == "shortness_of_breath":
                parameters["respiratory"] = ["oxygen_saturation", "breath_sounds", "respiratory_rate"]
            elif condition == "fever":
                parameters["infectious"] = ["temperature", "white_blood_cell_count", "inflammatory_markers"]
            elif condition == "hypertension":
                parameters["cardiovascular"] = ["blood_pressure", "heart_rate", "peripheral_edema"]
        
        # Add treatment-specific monitoring
        treatment_plan = treatment_recommendations.get("treatment_plan", {})
        primary_treatments = treatment_plan.get("primary_recommendations", [])
        
        for treatment in primary_treatments:
            if "nitroglycerin" in treatment.lower():
                parameters["medication_response"] = ["blood_pressure", "headache", "dizziness"]
            elif "aspirin" in treatment.lower():
                parameters["medication_response"] = ["bleeding_signs", "gi_tolerance"]
            elif "ace inhibitors" in treatment.lower() or "arb" in treatment.lower():
                parameters["medication_response"] = ["blood_pressure", "kidney_function", "potassium_level"]
            elif "oxygen" in treatment.lower():
                parameters["medication_response"] = ["oxygen_saturation", "respiratory_rate", "confusion"]
        
        return parameters

    def _generate_special_considerations(self, age: int, gender: str, risk_assessment: dict) -> List[Dict[str, Any]]:
        """Generate special considerations based on patient demographics and risk."""
        considerations = []
        
        # Age-based considerations
        if age > 65:
            considerations.append({
                "type": "age_related",
                "consideration": "Increased fall risk",
                "recommendation": "Implement fall prevention measures",
                "monitoring": ["balance_assessment", "home_safety_evaluation"]
            })
            
        if age > 75:
            considerations.append({
                "type": "age_related",
                "consideration": "Polypharmacy risk",
                "recommendation": "Regular medication review",
                "monitoring": ["medication_adherence", "drug_interaction_screening"]
            })
        
        # Gender-based considerations
        if gender.lower() == "female":
            considerations.append({
                "type": "gender_related",
                "consideration": "Reproductive health",
                "recommendation": "Pregnancy test if childbearing age",
                "monitoring": ["menstrual_history", "contraceptive_counseling"]
            })
        
        # Risk-based considerations
        risk_score = risk_assessment.get("risk_score", 0)
        if risk_score > 0.7:
            considerations.append({
                "type": "risk_related",
                "consideration": "High-risk patient",
                "recommendation": "Enhanced monitoring and frequent reassessment",
                "monitoring": ["hourly_vital_signs", "neurologic_assessment", "cardiac_monitoring"]
            })
        elif risk_score > 0.4:
            considerations.append({
                "type": "risk_related",
                "consideration": "Moderate-risk patient",
                "recommendation": "Standard monitoring with attention to changes",
                "monitoring": ["four_hourly_vital_signs", "symptom_progression"]
            })
            
        return considerations

    def _add_risk_based_modifications(self, followup_schedule: dict, risk_assessment: dict):
        """Add modifications to follow-up plan based on risk assessment."""
        risk_score = risk_assessment.get("risk_score", 0)
        
        if risk_score > 0.7:
            # High-risk modifications
            for followup in followup_schedule["immediate_followup"]:
                followup["frequency"] = "1 hour" if followup["frequency"] != "continuous" else followup["frequency"]
                followup["urgency"] = "continuous"
        elif risk_score > 0.4:
            # Moderate-risk modifications
            for followup in followup_schedule["immediate_followup"]:
                if followup["frequency"] in ["4 hours", "6 hours", "8 hours"]:
                    followup["frequency"] = "2 hours"

    def _calculate_confidence_score(self, conditions: List[str]) -> float:
        """Calculate confidence score for follow-up recommendations."""
        if not conditions:
            return 0.4  # Lower confidence for general recommendations
            
        # Higher confidence when specific conditions are identified
        base_confidence = 0.75
        confidence_boost = min(len(conditions) * 0.05, 0.2)  # Max 0.2 boost for multiple conditions
        return min(base_confidence + confidence_boost, 0.9)  # Cap at 0.9