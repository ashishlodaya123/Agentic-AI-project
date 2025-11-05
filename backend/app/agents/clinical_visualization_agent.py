import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ClinicalVisualizationAgent:
    """
    Agent for generating clinical visualization data for the frontend.
    """
    
    def __init__(self):
        pass
    
    def run(self, patient_data: dict, symptoms_analysis: dict, risk_assessment: dict, 
            treatment_recommendations: dict, followup_plan: Optional[dict] = None,
            drug_interactions: Optional[dict] = None, specialist_recommendations: Optional[dict] = None) -> Dict[str, Any]:
        """
        Generate visualization data for clinical information.
        
        Args:
            patient_data: Patient information including age, gender, medical history
            symptoms_analysis: Analysis of symptoms and vitals
            risk_assessment: Risk stratification results
            treatment_recommendations: Current treatment recommendations
            followup_plan: Follow-up care plan
            drug_interactions: Drug interaction analysis
            specialist_recommendations: Specialist recommendations
            
        Returns:
            Dict containing visualization data for various clinical aspects
        """
        try:
            logger.info("Generating clinical visualization data")
            
            # Generate various visualization datasets
            vital_signs_data = self._generate_vital_signs_visualization(patient_data)
            risk_stratification_data = self._generate_risk_visualization(risk_assessment)
            treatment_timeline_data = self._generate_treatment_timeline(treatment_recommendations, followup_plan or {})
            symptom_progression_data = self._generate_symptom_visualization(symptoms_analysis)
            
            result = {
                "vital_signs_chart": vital_signs_data,
                "risk_stratification_chart": risk_stratification_data,
                "treatment_timeline": treatment_timeline_data,
                "symptom_progression": symptom_progression_data,
                "timestamp": datetime.now().isoformat(),
                "patient_summary": self._generate_patient_summary(patient_data)
            }
            
            logger.info("Generated clinical visualization data")
            return result
            
        except Exception as e:
            logger.error(f"Error in clinical visualization generation: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_vital_signs_visualization(self, patient_data: dict) -> Dict[str, Any]:
        """Generate data for vital signs visualization."""
        vitals = patient_data.get("vital_signs", {})
        
        # Convert vital signs to chart-friendly format
        vital_data = []
        normal_ranges = {
            "heart_rate": {"normal": [60, 100], "unit": "bpm"},
            "blood_pressure_systolic": {"normal": [90, 120], "unit": "mmHg"},
            "blood_pressure_diastolic": {"normal": [60, 80], "unit": "mmHg"},
            "respiratory_rate": {"normal": [12, 20], "unit": "breaths/min"},
            "temperature": {"normal": [36.1, 37.2], "unit": "°C"},
            "oxygen_saturation": {"normal": [95, 100], "unit": "%"}
        }
        
        # Process heart rate
        if "heart_rate" in vitals:
            try:
                hr = int(vitals["heart_rate"])
                vital_data.append({
                    "metric": "Heart Rate",
                    "value": hr,
                    "normal_range": normal_ranges["heart_rate"]["normal"],
                    "unit": normal_ranges["heart_rate"]["unit"],
                    "status": self._determine_vital_status(hr, normal_ranges["heart_rate"]["normal"])
                })
            except (ValueError, TypeError):
                pass
        
        # Process blood pressure
        if "blood_pressure" in vitals:
            try:
                bp_parts = vitals["blood_pressure"].split("/")
                if len(bp_parts) == 2:
                    systolic = int(bp_parts[0])
                    diastolic = int(bp_parts[1])
                    vital_data.append({
                        "metric": "Blood Pressure (Systolic)",
                        "value": systolic,
                        "normal_range": normal_ranges["blood_pressure_systolic"]["normal"],
                        "unit": normal_ranges["blood_pressure_systolic"]["unit"],
                        "status": self._determine_vital_status(systolic, normal_ranges["blood_pressure_systolic"]["normal"])
                    })
                    vital_data.append({
                        "metric": "Blood Pressure (Diastolic)",
                        "value": diastolic,
                        "normal_range": normal_ranges["blood_pressure_diastolic"]["normal"],
                        "unit": normal_ranges["blood_pressure_diastolic"]["unit"],
                        "status": self._determine_vital_status(diastolic, normal_ranges["blood_pressure_diastolic"]["normal"])
                    })
            except (ValueError, IndexError, TypeError):
                pass
        
        # Process respiratory rate
        if "respiratory_rate" in vitals:
            try:
                rr = int(vitals["respiratory_rate"])
                vital_data.append({
                    "metric": "Respiratory Rate",
                    "value": rr,
                    "normal_range": normal_ranges["respiratory_rate"]["normal"],
                    "unit": normal_ranges["respiratory_rate"]["unit"],
                    "status": self._determine_vital_status(rr, normal_ranges["respiratory_rate"]["normal"])
                })
            except (ValueError, TypeError):
                pass
        
        # Process temperature
        if "temperature" in vitals:
            try:
                temp = float(vitals["temperature"])
                vital_data.append({
                    "metric": "Temperature",
                    "value": temp,
                    "normal_range": normal_ranges["temperature"]["normal"],
                    "unit": normal_ranges["temperature"]["unit"],
                    "status": self._determine_vital_status(temp, normal_ranges["temperature"]["normal"])
                })
            except (ValueError, TypeError):
                pass
        
        # Process oxygen saturation
        if "oxygen_saturation" in vitals:
            try:
                oxygen = float(vitals["oxygen_saturation"].replace("%", ""))
                vital_data.append({
                    "metric": "Oxygen Saturation",
                    "value": oxygen,
                    "normal_range": normal_ranges["oxygen_saturation"]["normal"],
                    "unit": normal_ranges["oxygen_saturation"]["unit"],
                    "status": self._determine_vital_status(oxygen, normal_ranges["oxygen_saturation"]["normal"])
                })
            except (ValueError, TypeError):
                pass
        
        return {
            "data": vital_data,
            "chart_type": "radar",
            "title": "Vital Signs Overview"
        }
    
    def _determine_vital_status(self, value: float, normal_range: List[float]) -> str:
        """Determine if a vital sign is normal, high, or low."""
        if value < normal_range[0]:
            return "low"
        elif value > normal_range[1]:
            return "high"
        else:
            return "normal"
    
    def _generate_risk_visualization(self, risk_assessment: dict) -> Dict[str, Any]:
        """Generate data for risk stratification visualization."""
        risk_factors = risk_assessment.get("risk_factors", [])
        risk_score = risk_assessment.get("risk_score", 0)
        triage_recommendation = risk_assessment.get("triage_recommendation", {})
        
        # Create risk factor data
        risk_data = []
        for factor in risk_factors:
            risk_data.append({
                "factor": factor.get("name", "Unknown"),
                "weight": factor.get("weight", 0),
                "description": factor.get("description", "")
            })
        
        # Sort by weight (highest first)
        risk_data.sort(key=lambda x: x["weight"], reverse=True)
        
        return {
            "risk_factors": risk_data,
            "risk_score": risk_score,
            "urgency_level": triage_recommendation.get("urgency", "Unknown"),
            "chart_type": "bar",
            "title": "Risk Stratification Analysis"
        }
    
    def _generate_treatment_timeline(self, treatment_recommendations: dict, followup_plan: Optional[dict]) -> Dict[str, Any]:
        """Generate data for treatment timeline visualization."""
        timeline_events = []
        
        # Add treatment recommendations
        if treatment_recommendations and "treatment_plan" in treatment_recommendations:
            plan = treatment_recommendations["treatment_plan"]
            
            # Add primary recommendations
            primary_recs = plan.get("primary_recommendations", [])
            for i, rec in enumerate(primary_recs):
                timeline_events.append({
                    "event": f"Primary Treatment: {rec[:30]}...",
                    "time": f"Immediate +{i*5}min",
                    "category": "treatment",
                    "priority": "high"
                })
            
            # Add secondary recommendations
            secondary_recs = plan.get("secondary_recommendations", [])
            for i, rec in enumerate(secondary_recs):
                timeline_events.append({
                    "event": f"Secondary: {rec[:30]}...",
                    "time": f"Within 1hr +{i*10}min",
                    "category": "treatment",
                    "priority": "medium"
                })
        
        # Add follow-up events
        if followup_plan and "followup_schedule" in followup_plan:
            schedule = followup_plan["followup_schedule"]
            
            # Add immediate follow-up
            immediate = schedule.get("immediate_followup", [])
            for followup in immediate:
                timeline_events.append({
                    "event": f"Follow-up: {followup.get('condition', 'Check')}",
                    "time": followup.get("start_time", "Soon"),
                    "category": "followup",
                    "priority": followup.get("urgency", "routine")
                })
            
            # Add short-term follow-up
            short_term = schedule.get("short_term_followup", [])
            for followup in short_term:
                timeline_events.append({
                    "event": f"Follow-up: {followup.get('condition', 'Check')}",
                    "time": followup.get("start_time", "Days 1-7"),
                    "category": "followup",
                    "priority": followup.get("urgency", "routine")
                })
        
        return {
            "events": timeline_events,
            "chart_type": "timeline",
            "title": "Treatment and Follow-up Timeline"
        }
    
    def _generate_symptom_visualization(self, symptoms_analysis: dict) -> Dict[str, Any]:
        """Generate data for symptom progression visualization."""
        if not symptoms_analysis:
            return {
                "symptoms": [],
                "chart_type": "pie",
                "title": "Symptom Distribution"
            }
        
        # Extract symptom categories
        categories = symptoms_analysis.get("symptom_categories", {})
        symptom_data = []
        
        for category, symptoms in categories.items():
            if symptoms:
                symptom_data.append({
                    "category": category.replace("_", " ").title(),
                    "count": len(symptoms),
                    "symptoms": symptoms
                })
        
        return {
            "symptoms": symptom_data,
            "chart_type": "pie",
            "title": "Symptom Distribution by System"
        }
    
    def _generate_patient_summary(self, patient_data: dict) -> Dict[str, Any]:
        """Generate patient summary information."""
        return {
            "age": patient_data.get("age", "N/A"),
            "gender": patient_data.get("gender", "N/A"),
            "chief_complaint": patient_data.get("chief_complaint", "N/A")[:50] + "..." if len(patient_data.get("chief_complaint", "")) > 50 else patient_data.get("chief_complaint", "N/A"),
            "medical_history_count": len(patient_data.get("medical_history", []))
        }