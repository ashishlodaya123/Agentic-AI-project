import re
from typing import Dict, List, Any
from app.core.agent_memory import get_agent_memory

class SpecialistConsultationAgent:
    """
    Agent to recommend appropriate specialists based on case complexity and patient conditions.
    Provides specialist referral recommendations with urgency levels and consultation details.
    """
    def __init__(self):
        self.memory = get_agent_memory()
        
        # Specialist recommendation database
        self.specialist_recommendations = {
            "cardiology": {
                "conditions": ["chest_pain", "heart_failure", "arrhythmia", "hypertension", "myocardial_infarction"],
                "urgency_levels": {
                    "immediate": "Within 15 minutes - Cardiac emergency",
                    "urgent": "Within 2 hours - High-risk cardiac condition",
                    "routine": "Within 24-48 hours - Stable cardiac condition"
                },
                "consultation_details": {
                    "emergency": "Prepare for possible cardiac catheterization",
                    "routine": "Bring recent ECG and cardiac enzymes"
                }
            },
            "pulmonology": {
                "conditions": ["shortness_of_breath", "asthma", "copd", "pneumonia", "pulmonary_embolism"],
                "urgency_levels": {
                    "immediate": "Within 30 minutes - Respiratory emergency",
                    "urgent": "Within 4 hours - Significant respiratory compromise",
                    "routine": "Within 1-2 weeks - Stable respiratory condition"
                },
                "consultation_details": {
                    "emergency": "Prepare arterial blood gas results",
                    "routine": "Bring chest X-ray and pulmonary function tests"
                }
            },
            "infectious_disease": {
                "conditions": ["fever", "sepsis", "pneumonia", "uti", "meningitis"],
                "urgency_levels": {
                    "immediate": "Within 1 hour - Suspected sepsis",
                    "urgent": "Within 4 hours - Persistent fever with complications",
                    "routine": "Within 1 week - Unresolved infection"
                },
                "consultation_details": {
                    "emergency": "Provide blood cultures and antibiotic sensitivity results",
                    "routine": "Bring complete infection workup and imaging"
                }
            },
            "neurology": {
                "conditions": ["headache", "seizure", "stroke", "altered_mental_status", "migraine"],
                "urgency_levels": {
                    "immediate": "Within 15 minutes - Neurological emergency",
                    "urgent": "Within 2 hours - Significant neurological deficit",
                    "routine": "Within 1 week - Chronic neurological condition"
                },
                "consultation_details": {
                    "emergency": "Prepare for possible CT/MRI imaging",
                    "routine": "Bring neurological examination findings"
                }
            },
            "emergency_medicine": {
                "conditions": ["trauma", "overdose", "acute_abdomen", "anaphylaxis", "cardiac_arrest"],
                "urgency_levels": {
                    "immediate": "Immediately - Life-threatening emergency",
                    "urgent": "Within 1 hour - Serious acute condition",
                    "routine": "Within 24 hours - Stable acute condition"
                },
                "consultation_details": {
                    "emergency": "Activate trauma team if applicable",
                    "routine": "Provide complete history and physical"
                }
            },
            "endocrinology": {
                "conditions": ["diabetes", "thyroid_disorder", "adrenal_insufficiency"],
                "urgency_levels": {
                    "immediate": "Within 1 hour - Endocrine emergency",
                    "urgent": "Within 4 hours - Significant endocrine dysfunction",
                    "routine": "Within 1 week - Chronic endocrine condition"
                },
                "consultation_details": {
                    "emergency": "Provide recent glucose and electrolyte levels",
                    "routine": "Bring endocrine function test results"
                }
            },
            "gastroenterology": {
                "conditions": ["gi_bleeding", "liver_disease", "pancreatitis", "inflammatory_bowel_disease"],
                "urgency_levels": {
                    "immediate": "Within 1 hour - GI emergency",
                    "urgent": "Within 4 hours - Significant GI condition",
                    "routine": "Within 1 week - Chronic GI condition"
                },
                "consultation_details": {
                    "emergency": "Prepare for possible endoscopy",
                    "routine": "Bring recent liver function tests and imaging"
                }
            }
        }
        
        # Complexity assessment criteria
        self.complexity_criteria = {
            "high_complexity": {
                "risk_score_threshold": 0.7,
                "multiple_conditions": 3,
                "critical_vitals": ["severe_hypotension", "severe_tachycardia", "hypoxia"],
                "complications": ["organ_failure", "sepsis", "multi_system_involvement"]
            },
            "moderate_complexity": {
                "risk_score_threshold": 0.4,
                "multiple_conditions": 2,
                "critical_vitals": ["hypertension", "tachycardia", "fever"],
                "complications": ["single_organ_dysfunction", "moderate_sepsis"]
            },
            "low_complexity": {
                "risk_score_threshold": 0.0,
                "multiple_conditions": 0,
                "critical_vitals": [],
                "complications": []
            }
        }

    def run(self, patient_data: dict, symptoms_analysis: dict, risk_assessment: dict,
            treatment_recommendations: dict) -> dict:
        """
        Recommend appropriate specialists based on patient data, symptoms analysis, and risk assessment.
        Returns specialist recommendations with urgency levels and consultation details.
        """
        # Extract relevant information
        symptoms = patient_data.get("symptoms", "")
        vitals = patient_data.get("vitals", {})
        age = patient_data.get("age", 0)
        gender = patient_data.get("gender", "")
        
        # Identify patient complexity
        complexity_level = self._assess_patient_complexity(
            symptoms, vitals, risk_assessment, treatment_recommendations
        )
        
        # Generate specialist recommendations
        recommendations = self._generate_specialist_recommendations(
            symptoms, vitals, risk_assessment, complexity_level
        )
        
        # Store recommendations in shared memory
        self.memory.store_agent_output("specialist", {
            "patient_data": patient_data,
            "recommendations": recommendations
        })
        
        return recommendations

    def _assess_patient_complexity(self, symptoms: str, vitals: dict, risk_assessment: dict,
                                  treatment_recommendations: dict) -> str:
        """Assess patient complexity based on multiple factors."""
        complexity_score = 0
        
        # Risk-based complexity
        risk_score = risk_assessment.get("risk_score", 0)
        if risk_score > 0.7:
            complexity_score += 3
        elif risk_score > 0.4:
            complexity_score += 2
        elif risk_score > 0.2:
            complexity_score += 1
            
        # Condition-based complexity
        conditions = self._identify_conditions(symptoms, vitals)
        if len(conditions) >= 3:
            complexity_score += 3
        elif len(conditions) >= 2:
            complexity_score += 2
        elif len(conditions) >= 1:
            complexity_score += 1
            
        # Vital-based complexity
        critical_vitals = self._identify_critical_vitals(vitals)
        complexity_score += len(critical_vitals)
        
        # Treatment complexity
        treatment_plan = treatment_recommendations.get("treatment_plan", {})
        primary_recs = treatment_plan.get("primary_recommendations", [])
        if len(primary_recs) > 5:
            complexity_score += 2
        elif len(primary_recs) > 3:
            complexity_score += 1
            
        # Determine complexity level with more granular thresholds
        if complexity_score >= 7:
            return "high_complexity"
        elif complexity_score >= 4:
            return "moderate_complexity"
        else:
            return "low_complexity"

    def _identify_conditions(self, symptoms: str, vitals: dict) -> List[str]:
        """Identify medical conditions based on symptoms and vitals."""
        conditions = []
        symptoms_lower = symptoms.lower()
        
        # Symptom-based condition identification
        if "chest pain" in symptoms_lower or "chest discomfort" in symptoms_lower:
            conditions.append("chest_pain")
        if "shortness of breath" in symptoms_lower or "difficulty breathing" in symptoms_lower:
            conditions.append("shortness_of_breath")
        if "fever" in symptoms_lower or self._has_fever(vitals):
            conditions.append("fever")
        if "headache" in symptoms_lower and "severe" in symptoms_lower:
            conditions.append("headache")
        if "seizure" in symptoms_lower or "convulsion" in symptoms_lower:
            conditions.append("seizure")
        if "diabetes" in symptoms_lower or "hyperglycemia" in symptoms_lower or "hypoglycemia" in symptoms_lower:
            conditions.append("diabetes")
        if "thyroid" in symptoms_lower:
            conditions.append("thyroid_disorder")
        if "bleeding" in symptoms_lower:
            conditions.append("gi_bleeding")
        if "jaundice" in symptoms_lower or "yellow skin" in symptoms_lower:
            conditions.append("liver_disease")
        if "abdominal pain" in symptoms_lower:
            conditions.append("acute_abdomen")
            
        # Vital-based condition identification
        if self._has_hypertension(vitals):
            conditions.append("hypertension")
        if self._has_hypotension(vitals):
            conditions.append("hypotension")
        if self._has_tachycardia(vitals):
            conditions.append("arrhythmia")
            
        return list(set(conditions))  # Remove duplicates

    def _identify_critical_vitals(self, vitals: dict) -> List[str]:
        """Identify critical vital signs."""
        critical_vitals = []
        
        # Heart rate
        heart_rate = vitals.get("heart_rate")
        if heart_rate is not None:
            try:
                hr = int(heart_rate)
                if hr > 130:
                    critical_vitals.append("severe_tachycardia")
                elif hr < 50:
                    critical_vitals.append("severe_bradycardia")
            except (ValueError, TypeError):
                pass
        
        # Temperature
        temperature = vitals.get("temperature")
        if temperature is not None:
            try:
                temp = float(temperature)
                if temp > 39.5:
                    critical_vitals.append("high_fever")
                elif temp < 35.0:
                    critical_vitals.append("hypothermia")
            except (ValueError, TypeError):
                pass
        
        # Blood pressure
        blood_pressure = vitals.get("blood_pressure")
        if blood_pressure is not None:
            try:
                bp_parts = blood_pressure.split("/")
                if len(bp_parts) == 2:
                    systolic = int(bp_parts[0])
                    diastolic = int(bp_parts[1])
                    if systolic > 180 or diastolic > 120:
                        critical_vitals.append("hypertensive_crisis")
                    elif systolic < 80 or diastolic < 50:
                        critical_vitals.append("severe_hypotension")
            except (ValueError, TypeError):
                pass
        
        return critical_vitals

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

    def _has_hypotension(self, vitals: dict) -> bool:
        """Check if patient has hypotension based on vital signs."""
        blood_pressure = vitals.get("blood_pressure")
        if blood_pressure is not None:
            try:
                bp_parts = blood_pressure.split("/")
                if len(bp_parts) == 2:
                    systolic = int(bp_parts[0])
                    return systolic < 90
            except (ValueError, TypeError):
                return False
        return False

    def _has_tachycardia(self, vitals: dict) -> bool:
        """Check if patient has tachycardia based on vital signs."""
        heart_rate = vitals.get("heart_rate")
        if heart_rate is not None:
            try:
                hr = int(heart_rate)
                return hr > 100
            except (ValueError, TypeError):
                return False
        return False

    def _generate_specialist_recommendations(self, symptoms: str, vitals: dict, 
                                           risk_assessment: dict, complexity_level: str) -> dict:
        """Generate specialist recommendations based on patient conditions and complexity."""
        # Identify conditions requiring specialist consultation
        conditions = self._identify_conditions(symptoms, vitals)
        
        # Generate recommendations for each relevant specialist
        specialist_recommendations = []
        
        for specialist, info in self.specialist_recommendations.items():
            # Check if any of the patient's conditions match this specialist's expertise
            matching_conditions = [cond for cond in conditions if cond in info["conditions"]]
            
            if matching_conditions:
                # Determine urgency based on risk assessment and complexity
                urgency = self._determine_urgency(risk_assessment, complexity_level)
                urgency_description = info["urgency_levels"].get(urgency, "Consult as clinically indicated")
                
                # Get consultation details based on urgency
                consultation_type = "emergency" if urgency in ["immediate", "urgent"] else "routine"
                consultation_details = info["consultation_details"].get(consultation_type, "")
                
                specialist_recommendations.append({
                    "specialist": specialist.title(),
                    "conditions": matching_conditions,
                    "urgency": urgency,
                    "urgency_description": urgency_description,
                    "consultation_details": consultation_details,
                    "reasoning": f"Patient presents with {', '.join(matching_conditions)} requiring {specialist} expertise"
                })
        
        # Add general recommendations if no specific specialists identified
        if not specialist_recommendations:
            specialist_recommendations.append({
                "specialist": "Primary Care Physician",
                "conditions": ["general_medical_care"],
                "urgency": "routine",
                "urgency_description": "Within 1-2 weeks - Routine follow-up",
                "consultation_details": "Bring all medical records and test results",
                "reasoning": "Patient requires ongoing primary care management"
            })
        
        return {
            "specialist_recommendations": specialist_recommendations,
            "complexity_level": complexity_level,
            "confidence_score": self._calculate_confidence_score(conditions),
            "additional_considerations": self._generate_additional_considerations(complexity_level)
        }

    def _determine_urgency(self, risk_assessment: dict, complexity_level: str) -> str:
        """Determine consultation urgency based on risk and complexity."""
        risk_score = risk_assessment.get("risk_score", 0)
        
        if risk_score > 0.8 or complexity_level == "high_complexity":
            return "immediate"
        elif risk_score > 0.6 or complexity_level == "moderate_complexity":
            return "urgent"
        else:
            return "routine"

    def _generate_additional_considerations(self, complexity_level: str) -> List[str]:
        """Generate additional considerations based on complexity level."""
        considerations = []
        
        if complexity_level == "high_complexity":
            considerations.extend([
                "Consider multidisciplinary team consultation",
                "Prepare for possible ICU admission",
                "Ensure family notification and involvement",
                "Document advance care planning discussion"
            ])
        elif complexity_level == "moderate_complexity":
            considerations.extend([
                "Schedule follow-up within 24-48 hours",
                "Provide patient education materials",
                "Arrange for home care services if needed",
                "Coordinate with outpatient services"
            ])
        else:
            considerations.extend([
                "Provide discharge instructions",
                "Schedule routine follow-up",
                "Educate patient on warning signs",
                "Ensure medication compliance"
            ])
            
        return considerations

    def _calculate_confidence_score(self, conditions: List[str]) -> float:
        """Calculate confidence score for specialist recommendations."""
        if not conditions:
            return 0.4  # Lower confidence when no specific conditions identified
            
        # Higher confidence when specific conditions are identified
        base_confidence = 0.75
        confidence_boost = min(len(conditions) * 0.08, 0.2)  # Max 0.2 boost for multiple conditions
        return min(base_confidence + confidence_boost, 0.95)  # Cap at 0.95