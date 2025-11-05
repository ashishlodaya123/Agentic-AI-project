import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class PredictiveAnalyticsAgent:
    """
    Agent for forecasting potential complications based on patient history and current condition.
    """
    
    def __init__(self):
        # Complication risk factors database
        self.complication_risks = {
            "cardiac_complications": {
                "name": "Cardiac Complications",
                "risk_factors": ["chest_pain", "hypertension", "diabetes", "smoking", "age_over_65"],
                "indicators": ["high_blood_pressure", "rapid_heart_rate", "low_oxygen"],
                "severity_levels": {
                    "low": "Monitor routinely",
                    "moderate": "Enhanced monitoring recommended",
                    "high": "Continuous monitoring required"
                }
            },
            "respiratory_complications": {
                "name": "Respiratory Complications",
                "risk_factors": ["shortness_of_breath", "asthma", "copd", "smoking", "age_over_65"],
                "indicators": ["rapid_breathing", "low_oxygen", "fever"],
                "severity_levels": {
                    "low": "Monitor respiratory status",
                    "moderate": "Pulmonary function monitoring",
                    "high": "Continuous oxygen saturation monitoring"
                }
            },
            "infectious_complications": {
                "name": "Infectious Complications",
                "risk_factors": ["fever", "immunocompromised", "diabetes", "recent_surgery", "age_over_65"],
                "indicators": ["fever", "rapid_heart_rate", "low_oxygen"],
                "severity_levels": {
                    "low": "Watch for signs of infection",
                    "moderate": "Infection surveillance protocol",
                    "high": "Prophylactic antibiotics consideration"
                }
            },
            "neurological_complications": {
                "name": "Neurological Complications",
                "risk_factors": ["headache", "dizziness", "hypertension", "diabetes", "age_over_65"],
                "indicators": ["altered_mental_status", "high_blood_pressure"],
                "severity_levels": {
                    "low": "Neurological checks every 4 hours",
                    "moderate": "Neurological checks every 2 hours",
                    "high": "Continuous neurological monitoring"
                }
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
            predictions = self._predict_complications(symptoms, vitals, age, gender, medical_history)
            
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
                              medical_history: List[str]) -> List[Dict[str, Any]]:
        """Predict potential complications and their risk levels."""
        predictions = []
        
        # Check each complication type
        for comp_key, comp_data in self.complication_risks.items():
            risk_score = 0
            risk_factors_present = []
            indicators_present = []
            
            # Check risk factors from medical history
            risk_factors = comp_data["risk_factors"]
            for factor in risk_factors:
                if self._check_risk_factor(factor, symptoms, age, medical_history):
                    risk_score += 1
                    risk_factors_present.append(factor)
            
            # Check vital sign indicators
            indicators = comp_data["indicators"]
            for indicator in indicators:
                if self._check_vital_indicator(indicator, vitals):
                    risk_score += 0.5
                    indicators_present.append(indicator)
            
            # Determine risk level
            if risk_score >= 2.0:
                risk_level = "high"
            elif risk_score >= 1.0:
                risk_level = "moderate"
            else:
                risk_level = "low"
            
            # Only include complications with some risk
            if risk_score > 0:
                predictions.append({
                    "complication": comp_data["name"],
                    "complication_key": comp_key,
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                    "risk_factors_present": risk_factors_present,
                    "indicators_present": indicators_present,
                    "prevention_strategies": self._get_prevention_strategies(comp_key),
                    "monitoring_recommendations": comp_data["severity_levels"].get(risk_level, "Standard monitoring")
                })
        
        return predictions
    
    def _check_risk_factor(self, factor: str, symptoms: str, age: int, medical_history: List[str]) -> bool:
        """Check if a risk factor is present."""
        # Check symptoms
        if factor in symptoms:
            return True
            
        # Check age
        if factor == "age_over_65" and age > 65:
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
                
        return False
    
    def _get_prevention_strategies(self, complication_key: str) -> List[str]:
        """Get prevention strategies for a specific complication."""
        strategies = {
            "cardiac_complications": [
                "Continuous ECG monitoring",
                "Frequent vital sign assessments",
                "Maintain adequate oxygenation",
                "Administer prescribed cardiac medications",
                "Monitor cardiac enzymes",
                "Ensure adequate perfusion"
            ],
            "respiratory_complications": [
                "Pulmonary hygiene measures",
                "Incentive spirometry",
                "Adequate hydration",
                "Positioning for optimal lung expansion",
                "Monitor oxygen saturation",
                "Early ambulation when appropriate"
            ],
            "infectious_complications": [
                "Strict aseptic technique",
                "Hand hygiene compliance",
                "Wound care as indicated",
                "Monitor for signs of infection",
                "Maintain sterile environment",
                "Prophylactic antibiotics if indicated"
            ],
            "neurological_complications": [
                "Neurological assessments every 2 hours",
                "Monitor level of consciousness",
                "Assess pupils and motor function",
                "Maintain head elevation if indicated",
                "Monitor for signs of increased intracranial pressure",
                "Ensure safety precautions"
            ]
        }
        
        return strategies.get(complication_key, ["Standard preventive care recommended"])