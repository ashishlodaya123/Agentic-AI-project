import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class PredictiveAnalyticsAgent:
    """
    Agent for forecasting potential complications based on patient history and current condition.
    """
    
    def __init__(self):
        # Complication risk factors database with more detailed information
        self.complication_risks = {
            "cardiac_complications": {
                "name": "Cardiac Complications",
                "risk_factors": ["chest_pain", "hypertension", "diabetes", "smoking", "age_over_65", "male", "family_history", "high_cholesterol"],
                "indicators": ["high_blood_pressure", "rapid_heart_rate", "low_oxygen", "irregular_heartbeat"],
                "severity_levels": {
                    "low": "Monitor routinely",
                    "moderate": "Enhanced monitoring recommended",
                    "high": "Continuous monitoring required"
                },
                "prevention_strategies": [
                    "Continuous ECG monitoring",
                    "Frequent vital sign assessments",
                    "Maintain adequate oxygenation",
                    "Administer prescribed cardiac medications",
                    "Monitor cardiac enzymes",
                    "Ensure adequate perfusion"
                ]
            },
            "respiratory_complications": {
                "name": "Respiratory Complications",
                "risk_factors": ["shortness_of_breath", "asthma", "copd", "smoking", "age_over_65", "pneumonia_history", "obesity"],
                "indicators": ["rapid_breathing", "low_oxygen", "fever", "abnormal_breath_sounds"],
                "severity_levels": {
                    "low": "Monitor respiratory status",
                    "moderate": "Pulmonary function monitoring",
                    "high": "Continuous oxygen saturation monitoring"
                },
                "prevention_strategies": [
                    "Pulmonary hygiene measures",
                    "Incentive spirometry",
                    "Adequate hydration",
                    "Positioning for optimal lung expansion",
                    "Monitor oxygen saturation",
                    "Early ambulation when appropriate"
                ]
            },
            "infectious_complications": {
                "name": "Infectious Complications",
                "risk_factors": ["fever", "immunocompromised", "diabetes", "recent_surgery", "age_over_65", "chronic_disease", "hospitalization"],
                "indicators": ["fever", "rapid_heart_rate", "low_oxygen", "elevated_white_blood_cell_count"],
                "severity_levels": {
                    "low": "Watch for signs of infection",
                    "moderate": "Infection surveillance protocol",
                    "high": "Prophylactic antibiotics consideration"
                },
                "prevention_strategies": [
                    "Strict aseptic technique",
                    "Hand hygiene compliance",
                    "Wound care as indicated",
                    "Monitor for signs of infection",
                    "Maintain sterile environment",
                    "Prophylactic antibiotics if indicated"
                ]
            },
            "neurological_complications": {
                "name": "Neurological Complications",
                "risk_factors": ["headache", "dizziness", "hypertension", "diabetes", "age_over_65", "stroke_history", "seizure_history"],
                "indicators": ["altered_mental_status", "high_blood_pressure", "asymmetric_reflexes", "abnormal_pupil_response"],
                "severity_levels": {
                    "low": "Neurological checks every 4 hours",
                    "moderate": "Neurological checks every 2 hours",
                    "high": "Continuous neurological monitoring"
                },
                "prevention_strategies": [
                    "Neurological assessments every 2 hours",
                    "Monitor level of consciousness",
                    "Assess pupils and motor function",
                    "Maintain head elevation if indicated",
                    "Monitor for signs of increased intracranial pressure",
                    "Ensure safety precautions"
                ]
            },
            "renal_complications": {
                "name": "Renal Complications",
                "risk_factors": ["diabetes", "hypertension", "age_over_65", "chronic_kidney_disease", "dehydration", "medication_nephrotoxicity"],
                "indicators": ["decreased_urine_output", "elevated_creatinine", "fluid_retention", "electrolyte_imbalance"],
                "severity_levels": {
                    "low": "Monitor urine output and hydration",
                    "moderate": "Daily renal function tests",
                    "high": "Continuous renal monitoring"
                },
                "prevention_strategies": [
                    "Monitor urine output hourly",
                    "Daily electrolyte and creatinine monitoring",
                    "Maintain adequate hydration",
                    "Avoid nephrotoxic medications",
                    "Monitor for signs of fluid overload",
                    "Adjust medications for renal function"
                ]
            },
            "metabolic_complications": {
                "name": "Metabolic Complications",
                "risk_factors": ["diabetes", "obesity", "age_over_65", "chronic_disease", "medication_side_effects", "poor_nutrition"],
                "indicators": ["abnormal_blood_sugar", "electrolyte_imbalance", "acid_base_disturbance", "altered_mental_status"],
                "severity_levels": {
                    "low": "Routine metabolic monitoring",
                    "moderate": "Enhanced metabolic surveillance",
                    "high": "Continuous metabolic monitoring"
                },
                "prevention_strategies": [
                    "Regular blood glucose monitoring",
                    "Electrolyte panel every 12 hours",
                    "Monitor for signs of dehydration",
                    "Ensure adequate nutrition",
                    "Watch for medication interactions",
                    "Adjust insulin/diabetic medications as needed"
                ]
            }
        }
    
    def run(self, patient_data: dict, symptoms_analysis: dict, risk_assessment: dict, 
            treatment_recommendations: dict) -> Dict[str, Any]:
        """
        Forecast potential complications based on patient data.
        
        Args:
            patient_data: Patient information including age, gender, medical history
            symptoms_analysis: Analysis of symptoms and vitals
            risk_assessment: Risk stratification results
            treatment_recommendations: Current treatment recommendations
            
        Returns:
            Dict containing predicted complications with risk levels
        """
        try:
            logger.info("Generating predictive analytics for complications")
            
            # Extract relevant information
            symptoms = patient_data.get("chief_complaint", "").lower()
            vitals = patient_data.get("vital_signs", {})
            age = patient_data.get("age", 0)
            gender = patient_data.get("gender", "")
            medical_history = patient_data.get("medical_history", [])
            
            # Generate complication predictions
            predictions = self._predict_complications(symptoms, vitals, age, gender, medical_history, symptoms_analysis)
            
            # Rank predictions based on risk score
            ranked_predictions = sorted(predictions, key=lambda x: x["risk_score"], reverse=True)
            
            result = {
                "complication_predictions": ranked_predictions,
                "total_predictions": len(ranked_predictions),
                "timestamp": datetime.now().isoformat(),
                "analysis_factors": {
                    "symptom_analysis": bool(symptoms_analysis),
                    "risk_assessment": bool(risk_assessment),
                    "treatment_recommendations": bool(treatment_recommendations)
                }
            }
            
            logger.info(f"Generated {len(ranked_predictions)} complication predictions")
            return result
            
        except Exception as e:
            logger.error(f"Error in predictive analytics generation: {e}")
            return {
                "complication_predictions": [],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _predict_complications(self, symptoms: str, vitals: dict, age: int, gender: str, 
                              medical_history: List[str], symptoms_analysis: dict) -> List[Dict[str, Any]]:
        """Predict potential complications and their risk levels."""
        predictions = []
        
        # Check each complication type
        for comp_key, comp_data in self.complication_risks.items():
            risk_score = 0
            risk_factors_present = []
            indicators_present = []
            
            # Check risk factors from medical history and demographics
            risk_factors = comp_data["risk_factors"]
            for factor in risk_factors:
                if self._check_risk_factor(factor, symptoms, age, gender, medical_history, symptoms_analysis):
                    risk_score += 1.2  # Increased weight for comprehensive matching
                    risk_factors_present.append(factor)
            
            # Check vital sign indicators
            indicators = comp_data["indicators"]
            for indicator in indicators:
                if self._check_vital_indicator(indicator, vitals):
                    risk_score += 0.8
                    indicators_present.append(indicator)
            
            # Adjust for symptom severity if available
            if symptoms_analysis:
                # Check if symptoms suggest this type of complication
                primary_concerns = symptoms_analysis.get("primary_concerns", [])
                for concern in primary_concerns:
                    concern_type = concern.get("type", "").lower()
                    concern_significance = concern.get("significance", "").lower()
                    
                    # Match concern types to complication categories
                    if (("cardiac" in concern_type or "heart" in concern_type) and "cardiac" in comp_key) or \
                       (("respiratory" in concern_type or "lung" in concern_type) and "respiratory" in comp_key) or \
                       (("neurological" in concern_type or "brain" in concern_type) and "neurological" in comp_key) or \
                       (("renal" in concern_type or "kidney" in concern_type) and "renal" in comp_key) or \
                       (("metabolic" in concern_type or "diabetes" in concern_type) and "metabolic" in comp_key):
                        risk_score += 0.5
            
            # Determine risk level with more granular scoring
            if risk_score >= 2.5:
                risk_level = "high"
            elif risk_score >= 1.5:
                risk_level = "moderate"
            else:
                risk_level = "low"
            
            # Only include complications with some risk
            if risk_score > 0:
                predictions.append({
                    "complication": comp_data["name"],
                    "complication_key": comp_key,
                    "risk_score": round(risk_score, 2),
                    "risk_level": risk_level,
                    "risk_factors_present": risk_factors_present,
                    "indicators_present": indicators_present,
                    "prevention_strategies": comp_data["prevention_strategies"],
                    "monitoring_recommendations": comp_data["severity_levels"].get(risk_level, "Standard monitoring")
                })
        
        # Sort by risk score and limit to top 4 complications for better performance
        predictions = sorted(predictions, key=lambda x: x["risk_score"], reverse=True)
        return predictions[:4]  # Return only top 4 instead of all
    
    def _check_risk_factor(self, factor: str, symptoms: str, age: int, gender: str, 
                          medical_history: List[str], symptoms_analysis: dict) -> bool:
        """Check if a risk factor is present."""
        # Check symptoms
        if factor in symptoms:
            return True
            
        # Check age
        if factor == "age_over_65" and age > 65:
            return True
            
        # Check gender
        if factor == "male" and gender.lower() == "male":
            return True
            
        # Check medical history
        for history_item in medical_history:
            history_lower = history_item.lower()
            if factor == "hypertension" and "hypertension" in history_lower:
                return True
            elif factor == "diabetes" and "diabetes" in history_lower:
                return True
            elif factor == "smoking" and ("smoking" in history_lower or "smoker" in history_lower):
                return True
            elif factor == "asthma" and "asthma" in history_lower:
                return True
            elif factor == "copd" and ("copd" in history_lower or "chronic obstructive pulmonary" in history_lower):
                return True
            elif factor == "immunocompromised" and ("immunocompromised" in history_lower or "immunosuppressed" in history_lower):
                return True
            elif factor == "recent_surgery" and "surgery" in history_lower:
                return True
            elif factor == "chronic_kidney_disease" and ("kidney" in history_lower or "renal" in history_lower):
                return True
            elif factor == "obesity" and ("obesity" in history_lower or "morbid" in history_lower):
                return True
            elif factor == "chronic_disease" and ("chronic" in history_lower):
                return True
            elif factor == "family_history" and "family" in history_lower:
                return True
            elif factor == "high_cholesterol" and ("cholesterol" in history_lower or "hyperlipidemia" in history_lower):
                return True
            elif factor == "pneumonia_history" and "pneumonia" in history_lower:
                return True
            elif factor == "stroke_history" and ("stroke" in history_lower or "cva" in history_lower):
                return True
            elif factor == "seizure_history" and ("seizure" in history_lower or "epilepsy" in history_lower):
                return True
            elif factor == "hospitalization" and ("hospital" in history_lower):
                return True
            elif factor == "medication_nephrotoxicity" and ("nsaid" in history_lower or "contrast" in history_lower):
                return True
            elif factor == "poor_nutrition" and ("malnutrition" in history_lower or "underweight" in history_lower):
                return True
                
        # Check symptoms analysis for additional factors
        if symptoms_analysis:
            primary_concerns = symptoms_analysis.get("primary_concerns", [])
            for concern in primary_concerns:
                concern_name = concern.get("name", "").lower()
                concern_type = concern.get("type", "").lower()
                
                if factor == "chest_pain" and "chest" in concern_name:
                    return True
                elif factor == "shortness_of_breath" and ("breath" in concern_name or "dyspnea" in concern_name):
                    return True
                elif factor == "headache" and "headache" in concern_name:
                    return True
                elif factor == "dizziness" and ("dizziness" in concern_name or "vertigo" in concern_name):
                    return True
                elif factor == "fever" and "fever" in concern_name:
                    return True
                    
        return False
    
    def _check_vital_indicator(self, indicator: str, vitals: dict) -> bool:
        """Check if a vital sign indicator is present."""
        if indicator == "fever":
            temp = vitals.get("temperature")
            if temp:
                try:
                    return float(temp) > 38.0
                except (ValueError, TypeError):
                    return False
        elif indicator == "high_blood_pressure":
            bp = vitals.get("blood_pressure")
            if bp:
                try:
                    systolic = int(bp.split("/")[0])
                    return systolic > 140
                except (ValueError, IndexError, TypeError):
                    return False
        elif indicator == "rapid_heart_rate":
            hr = vitals.get("heart_rate")
            if hr:
                try:
                    return int(hr) > 100
                except (ValueError, TypeError):
                    return False
        elif indicator == "rapid_breathing":
            rr = vitals.get("respiratory_rate")
            if rr:
                try:
                    return int(rr) > 20
                except (ValueError, TypeError):
                    return False
        elif indicator == "low_oxygen":
            oxygen = vitals.get("oxygen_saturation")
            if oxygen:
                try:
                    return float(oxygen.replace("%", "")) < 95
                except (ValueError, TypeError):
                    return False
        elif indicator == "altered_mental_status":
            # This would typically come from a separate assessment
            return False  # Placeholder
        elif indicator == "irregular_heartbeat":
            hr = vitals.get("heart_rate")
            if hr:
                try:
                    # Irregular if heart rate is very high or shows concerning patterns
                    return int(hr) > 120
                except (ValueError, TypeError):
                    return False
        elif indicator == "abnormal_breath_sounds":
            # Placeholder - would come from physical exam
            return False
        elif indicator == "elevated_white_blood_cell_count":
            # Placeholder - would come from lab results
            return False
        elif indicator == "decreased_urine_output":
            # Placeholder - would come from intake/output monitoring
            return False
        elif indicator == "elevated_creatinine":
            # Placeholder - would come from lab results
            return False
        elif indicator == "fluid_retention":
            # Placeholder - would come from physical exam
            return False
        elif indicator == "electrolyte_imbalance":
            # Placeholder - would come from lab results
            return False
        elif indicator == "acid_base_disturbance":
            # Placeholder - would come from lab results
            return False
        elif indicator == "abnormal_blood_sugar":
            # Placeholder - would come from lab results
            return False
        elif indicator == "asymmetric_reflexes":
            # Placeholder - would come from neurological exam
            return False
        elif indicator == "abnormal_pupil_response":
            # Placeholder - would come from neurological exam
            return False
                
        return False