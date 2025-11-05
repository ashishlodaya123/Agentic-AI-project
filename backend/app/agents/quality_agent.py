import re
from typing import Dict, List, Any
from datetime import datetime
from app.core.agent_memory import get_agent_memory

class QualityAssuranceAgent:
    """
    Agent to review recommendations for consistency and completeness.
    Provides quality checks on all agent outputs to ensure clinical safety and completeness.
    """
    def __init__(self):
        self.memory = get_agent_memory()
        
        # Quality check criteria
        self.quality_criteria = {
            "completeness": {
                "required_sections": ["patient_data", "symptoms_analysis", "risk_assessment", 
                                    "treatment_recommendations", "followup_plan"],
                "minimum_recommendations": 3,
                "required_vitals": ["heart_rate", "blood_pressure", "temperature"]
            },
            "consistency": {
                "risk_alignment": ["symptoms_severity", "vital_abnormalities", "risk_score"],
                "treatment_alignment": ["diagnosed_conditions", "recommended_treatments", "risk_level"],
                "followup_alignment": ["treatment_plan", "risk_level", "patient_complexity"]
            },
            "safety": {
                "critical_findings": ["chest_pain", "shortness_of_breath", "severe_vitals"],
                "contraindications": ["active_bleeding", "severe_liver_disease", "pregnancy"],
                "interaction_warnings": ["high_risk_interactions", "moderate_risk_interactions"]
            }
        }
        
        # Quality scoring weights
        self.quality_weights = {
            "completeness": 0.3,
            "consistency": 0.4,
            "safety": 0.3
        }

    def run(self, patient_data: dict, symptoms_analysis: dict, risk_assessment: dict,
            treatment_recommendations: dict, followup_plan: dict, 
            drug_interactions: dict, specialist_recommendations: dict) -> dict:
        """
        Review all recommendations for consistency and completeness.
        Returns quality assurance report with identified issues and improvement suggestions.
        """
        # Perform quality checks
        completeness_check = self._check_completeness(
            patient_data, symptoms_analysis, risk_assessment, treatment_recommendations, 
            followup_plan, drug_interactions, specialist_recommendations
        )
        
        consistency_check = self._check_consistency(
            symptoms_analysis, risk_assessment, treatment_recommendations, 
            followup_plan, specialist_recommendations
        )
        
        safety_check = self._check_safety(
            patient_data, symptoms_analysis, risk_assessment, 
            treatment_recommendations, drug_interactions
        )
        
        # Generate overall quality score
        quality_score = self._calculate_overall_quality_score(
            completeness_check, consistency_check, safety_check
        )
        
        # Generate quality assurance report
        qa_report = self._generate_qa_report(
            completeness_check, consistency_check, safety_check, quality_score
        )
        
        # Store QA report in shared memory
        self.memory.store_agent_output("quality", {
            "patient_data": patient_data,
            "qa_report": qa_report
        })
        
        return qa_report

    def _check_completeness(self, patient_data: dict, symptoms_analysis: dict, risk_assessment: dict,
                           treatment_recommendations: dict, followup_plan: dict,
                           drug_interactions: dict, specialist_recommendations: dict) -> dict:
        """Check completeness of all agent outputs."""
        issues = []
        score = 1.0
        
        # Check required sections
        required_sections = {
            "patient_data": patient_data,
            "symptoms_analysis": symptoms_analysis,
            "risk_assessment": risk_assessment,
            "treatment_recommendations": treatment_recommendations,
            "followup_plan": followup_plan,
            "drug_interactions": drug_interactions,
            "specialist_recommendations": specialist_recommendations
        }
        
        missing_sections = []
        for section_name, section_data in required_sections.items():
            if not section_data:
                missing_sections.append(section_name)
                score -= 0.15
        
        if missing_sections:
            issues.append({
                "type": "missing_sections",
                "description": f"Missing required sections: {', '.join(missing_sections)}",
                "severity": "high" if len(missing_sections) > 2 else "moderate"
            })
        
        # Check minimum recommendations
        treatment_plan = treatment_recommendations.get("treatment_plan", {})
        primary_recs = treatment_plan.get("primary_recommendations", [])
        if len(primary_recs) < 3:
            issues.append({
                "type": "insufficient_recommendations",
                "description": f"Only {len(primary_recs)} primary treatment recommendations provided (minimum 3)",
                "severity": "moderate" if len(primary_recs) < 2 else "low"
            })
            score -= 0.1 * (3 - len(primary_recs))
        
        # Check required vitals
        vitals = patient_data.get("vitals", {})
        missing_vitals = []
        for vital in self.quality_criteria["completeness"]["required_vitals"]:
            if vital not in vitals or not vitals[vital]:
                missing_vitals.append(vital)
        
        if missing_vitals:
            issues.append({
                "type": "missing_vitals",
                "description": f"Missing vital signs: {', '.join(missing_vitals)}",
                "severity": "moderate" if len(missing_vitals) > 1 else "low"
            })
            score -= 0.05 * len(missing_vitals)
        
        # Check follow-up plan completeness
        followup_schedule = followup_plan.get("followup_schedule", {})
        if not followup_schedule.get("immediate_followup") and not followup_schedule.get("short_term_followup"):
            issues.append({
                "type": "incomplete_followup",
                "description": "Follow-up plan lacks immediate or short-term components",
                "severity": "moderate"
            })
            score -= 0.1
        
        return {
            "score": max(0.0, round(score, 2)),
            "issues": issues,
            "details": {
                "sections_checked": list(required_sections.keys()),
                "sections_missing": missing_sections,
                "vitals_missing": missing_vitals
            }
        }

    def _check_consistency(self, symptoms_analysis: dict, risk_assessment: dict,
                          treatment_recommendations: dict, followup_plan: dict,
                          specialist_recommendations: dict) -> dict:
        """Check consistency between different agent outputs."""
        issues = []
        score = 1.0
        
        # Check risk alignment
        risk_score = risk_assessment.get("risk_score", 0)
        symptoms_severity = self._assess_symptoms_severity(symptoms_analysis)
        
        # Risk score should align with symptoms severity
        if (risk_score > 0.7 and symptoms_severity < 0.5) or (risk_score < 0.3 and symptoms_severity > 0.7):
            issues.append({
                "type": "risk_symptom_mismatch",
                "description": f"Risk score ({risk_score}) does not align with symptoms severity ({symptoms_severity})",
                "severity": "high"
            })
            score -= 0.2
        
        # Check treatment alignment
        treatment_plan = treatment_recommendations.get("treatment_plan", {})
        diagnosed_conditions = self._extract_conditions_from_analysis(symptoms_analysis)
        recommended_treatments = self._extract_treatments_from_plan(treatment_plan)
        
        # Check if treatments match diagnosed conditions
        if diagnosed_conditions and not self._treatments_match_conditions(diagnosed_conditions, recommended_treatments):
            issues.append({
                "type": "treatment_condition_mismatch",
                "description": "Recommended treatments do not match diagnosed conditions",
                "severity": "moderate"
            })
            score -= 0.15
        
        # Check follow-up alignment
        complexity_level = specialist_recommendations.get("complexity_level", "low_complexity")
        followup_schedule = followup_plan.get("followup_schedule", {})
        
        # High complexity should have more intensive follow-up
        if complexity_level == "high_complexity" and not followup_schedule.get("immediate_followup"):
            issues.append({
                "type": "followup_intensity_mismatch",
                "description": "High complexity case lacks immediate follow-up plan",
                "severity": "moderate"
            })
            score -= 0.1
        
        return {
            "score": max(0.0, round(score, 2)),
            "issues": issues,
            "details": {
                "risk_score": risk_score,
                "symptoms_severity": symptoms_severity,
                "complexity_level": complexity_level
            }
        }

    def _check_safety(self, patient_data: dict, symptoms_analysis: dict, risk_assessment: dict,
                     treatment_recommendations: dict, drug_interactions: dict) -> dict:
        """Check safety of all recommendations."""
        issues = []
        score = 1.0
        
        # Check for critical findings that require immediate attention
        symptoms = patient_data.get("symptoms", "")
        vitals = patient_data.get("vitals", {})
        
        critical_symptoms = ["chest pain", "shortness of breath", "loss of consciousness"]
        has_critical_symptoms = any(symptom in symptoms.lower() for symptom in critical_symptoms)
        
        has_critical_vitals = self._has_critical_vitals(vitals)
        
        if (has_critical_symptoms or has_critical_vitals) and risk_assessment.get("risk_score", 0) < 0.7:
            issues.append({
                "type": "under_triage",
                "description": "Critical symptoms or vitals present but risk score is low",
                "severity": "high"
            })
            score -= 0.3
        
        # Check for contraindications
        safety_assessment = drug_interactions.get("safety_assessment", {})
        major_contraindications = safety_assessment.get("major_contraindications", [])
        high_risk_interactions = safety_assessment.get("high_risk_interactions", [])
        
        if major_contraindications:
            issues.append({
                "type": "major_contraindications",
                "description": f"{len(major_contraindications)} major contraindications identified",
                "severity": "high"
            })
            score -= 0.25 * len(major_contraindications)
        
        if high_risk_interactions:
            issues.append({
                "type": "high_risk_interactions",
                "description": f"{len(high_risk_interactions)} high-risk drug interactions identified",
                "severity": "high"
            })
            score -= 0.2 * len(high_risk_interactions)
        
        # Check treatment safety
        treatment_plan = treatment_recommendations.get("treatment_plan", {})
        contraindications_checked = treatment_plan.get("contraindications_checked", [])
        
        if not contraindications_checked:
            issues.append({
                "type": "safety_check_missing",
                "description": "No contraindications checked in treatment plan",
                "severity": "moderate"
            })
            score -= 0.1
        
        return {
            "score": max(0.0, round(score, 2)),
            "issues": issues,
            "details": {
                "has_critical_symptoms": has_critical_symptoms,
                "has_critical_vitals": has_critical_vitals,
                "major_contraindications_count": len(major_contraindications),
                "high_risk_interactions_count": len(high_risk_interactions)
            }
        }

    def _assess_symptoms_severity(self, symptoms_analysis: dict) -> float:
        """Assess severity based on symptoms analysis."""
        # This is a simplified implementation
        # In a real system, this would be more sophisticated
        concerns = symptoms_analysis.get("primary_concerns", [])
        if not concerns:
            return 0.1
            
        critical_concerns = ["chest pain", "shortness of breath", "loss of consciousness"]
        has_critical = any(concern.get("name", "").lower() in critical_concerns for concern in concerns)
        
        if has_critical:
            return 0.9
        elif len(concerns) > 2:
            return 0.7
        elif len(concerns) > 0:
            return 0.4
        else:
            return 0.1

    def _extract_conditions_from_analysis(self, symptoms_analysis: dict) -> List[str]:
        """Extract diagnosed conditions from symptoms analysis."""
        conditions = []
        symptom_categories = symptoms_analysis.get("symptom_categories", {})
        
        for category, symptoms in symptom_categories.items():
            if symptoms:
                conditions.append(category)
                
        return conditions

    def _extract_treatments_from_plan(self, treatment_plan: dict) -> List[str]:
        """Extract treatments from treatment plan."""
        treatments = []
        primary_recs = treatment_plan.get("primary_recommendations", [])
        secondary_recs = treatment_plan.get("secondary_recommendations", [])
        
        # Simplified extraction - in a real system, this would be more sophisticated
        all_recs = primary_recs + secondary_recs
        for rec in all_recs:
            if "aspirin" in rec.lower():
                treatments.append("aspirin")
            elif "nitroglycerin" in rec.lower():
                treatments.append("nitroglycerin")
            elif "oxygen" in rec.lower():
                treatments.append("oxygen")
            elif "antibiotic" in rec.lower() or "antibiotic" in rec.lower():
                treatments.append("antibiotics")
                
        return treatments

    def _treatments_match_conditions(self, conditions: List[str], treatments: List[str]) -> bool:
        """Check if treatments match diagnosed conditions."""
        # Simplified matching logic
        condition_treatment_map = {
            "cardiovascular": ["aspirin", "nitroglycerin"],
            "respiratory": ["oxygen"],
            "infectious": ["antibiotics"]
        }
        
        for condition in conditions:
            expected_treatments = condition_treatment_map.get(condition, [])
            if expected_treatments and not any(t in treatments for t in expected_treatments):
                return False
                
        return True

    def _has_critical_vitals(self, vitals: dict) -> bool:
        """Check if patient has critical vital signs."""
        # Heart rate
        heart_rate = vitals.get("heart_rate")
        if heart_rate is not None:
            try:
                hr = int(heart_rate)
                if hr > 130 or hr < 50:
                    return True
            except (ValueError, TypeError):
                pass
        
        # Temperature
        temperature = vitals.get("temperature")
        if temperature is not None:
            try:
                temp = float(temperature)
                if temp > 39.5 or temp < 35.0:
                    return True
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
                    if systolic > 180 or diastolic > 120 or systolic < 80:
                        return True
            except (ValueError, TypeError):
                pass
        
        return False

    def _calculate_overall_quality_score(self, completeness_check: dict, 
                                        consistency_check: dict, safety_check: dict) -> float:
        """Calculate overall quality score based on individual scores and weights."""
        completeness_score = completeness_check["score"]
        consistency_score = consistency_check["score"]
        safety_score = safety_check["score"]
        
        overall_score = (
            completeness_score * self.quality_weights["completeness"] +
            consistency_score * self.quality_weights["consistency"] +
            safety_score * self.quality_weights["safety"]
        )
        
        return round(overall_score, 2)

    def _generate_qa_report(self, completeness_check: dict, consistency_check: dict, 
                           safety_check: dict, quality_score: float) -> dict:
        """Generate comprehensive quality assurance report."""
        # Collect all issues
        all_issues = []
        all_issues.extend(completeness_check["issues"])
        all_issues.extend(consistency_check["issues"])
        all_issues.extend(safety_check["issues"])
        
        # Categorize issues by severity
        high_severity_issues = [issue for issue in all_issues if issue["severity"] == "high"]
        moderate_severity_issues = [issue for issue in all_issues if issue["severity"] == "moderate"]
        low_severity_issues = [issue for issue in all_issues if issue["severity"] == "low"]
        
        # Generate overall assessment
        if quality_score >= 0.8:
            overall_assessment = "High quality - recommendations are comprehensive and consistent"
        elif quality_score >= 0.6:
            overall_assessment = "Moderate quality - some improvements needed"
        else:
            overall_assessment = "Low quality - significant issues identified requiring attention"
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(
            completeness_check, consistency_check, safety_check
        )
        
        return {
            "qa_report": {
                "timestamp": datetime.now().isoformat(),
                "overall_quality_score": quality_score,
                "overall_assessment": overall_assessment,
                "component_scores": {
                    "completeness": completeness_check["score"],
                    "consistency": consistency_check["score"],
                    "safety": safety_check["score"]
                },
                "issues_summary": {
                    "total_issues": len(all_issues),
                    "high_severity": len(high_severity_issues),
                    "moderate_severity": len(moderate_severity_issues),
                    "low_severity": len(low_severity_issues)
                },
                "detailed_issues": all_issues,
                "improvement_suggestions": improvement_suggestions
            },
            "confidence_score": self._calculate_confidence_score(quality_score)
        }

    def _generate_improvement_suggestions(self, completeness_check: dict, 
                                        consistency_check: dict, safety_check: dict) -> List[str]:
        """Generate improvement suggestions based on identified issues."""
        suggestions = []
        
        # Completeness suggestions
        completeness_issues = completeness_check["issues"]
        if any(issue["type"] == "missing_sections" for issue in completeness_issues):
            suggestions.append("Ensure all required sections are completed before finalizing recommendations")
        
        if any(issue["type"] == "insufficient_recommendations" for issue in completeness_issues):
            suggestions.append("Add more specific treatment recommendations based on diagnosed conditions")
        
        if any(issue["type"] == "missing_vitals" for issue in completeness_issues):
            suggestions.append("Collect all required vital signs for comprehensive assessment")
        
        # Consistency suggestions
        consistency_issues = consistency_check["issues"]
        if any(issue["type"] == "risk_symptom_mismatch" for issue in consistency_issues):
            suggestions.append("Reassess risk score to ensure alignment with symptom severity")
        
        if any(issue["type"] == "treatment_condition_mismatch" for issue in consistency_issues):
            suggestions.append("Review treatment recommendations to ensure they match diagnosed conditions")
        
        # Safety suggestions
        safety_issues = safety_check["issues"]
        if any(issue["type"] == "under_triage" for issue in safety_issues):
            suggestions.append("Reassess patient urgency level given critical symptoms or vitals")
        
        if any(issue["type"] == "major_contraindications" for issue in safety_issues):
            suggestions.append("Review and address all identified contraindications before implementation")
        
        if any(issue["type"] == "high_risk_interactions" for issue in safety_issues):
            suggestions.append("Consult with clinical pharmacist to resolve high-risk drug interactions")
        
        # General suggestions if no specific issues
        if not suggestions:
            suggestions.append("All quality checks passed - recommendations appear comprehensive and consistent")
            suggestions.append("Continue with standard implementation procedures")
        
        return suggestions

    def _calculate_confidence_score(self, quality_score: float) -> float:
        """Calculate confidence score for quality assessment."""
        # Quality assessment confidence is based on the quality score itself
        # Higher quality scores indicate higher confidence in the assessment
        return min(0.95, quality_score + 0.05)  # Slight boost to confidence