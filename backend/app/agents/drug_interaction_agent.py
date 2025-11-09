import re
from typing import Dict, List, Any
from app.core.agent_memory import get_agent_memory

class DrugInteractionAgent:
    """
    Agent to check for potential drug interactions and contraindications.
    Provides safety screening for prescribed medications based on patient data and current medications.
    """
    def __init__(self):
        self.memory = get_agent_memory()
        
        # Drug interaction database
        self.drug_interactions = {
            "aspirin": {
                "warfarin": {
                    "severity": "high",
                    "description": "Increased bleeding risk due to additive anticoagulant effects",
                    "management": "Monitor INR closely, consider dose adjustment"
                },
                "clopidogrel": {
                    "severity": "moderate",
                    "description": "Increased risk of bleeding",
                    "management": "Use with caution, monitor for bleeding signs"
                },
                "ibuprofen": {
                    "severity": "moderate",
                    "description": "Reduced antiplatelet effect of aspirin, increased GI bleeding risk",
                    "management": "Avoid concurrent use, consider alternative NSAIDs"
                },
                "heparin": {
                    "severity": "high",
                    "description": "Additive anticoagulant effect increases bleeding risk",
                    "management": "Avoid concurrent use, monitor coagulation parameters"
                }
            },
            "nitroglycerin": {
                "sildenafil": {
                    "severity": "high",
                    "description": "Severe hypotension due to synergistic vasodilation",
                    "management": "Contraindicated, avoid concurrent use"
                },
                "tadalafil": {
                    "severity": "high",
                    "description": "Severe hypotension due to synergistic vasodilation",
                    "management": "Contraindicated, avoid concurrent use"
                },
                "vardenafil": {
                    "severity": "high",
                    "description": "Severe hypotension due to synergistic vasodilation",
                    "management": "Contraindicated, avoid concurrent use"
                }
            },
            "ace_inhibitors": {
                "potassium_supplements": {
                    "severity": "high",
                    "description": "Risk of hyperkalemia",
                    "management": "Monitor serum potassium levels, avoid potassium supplements"
                },
                "spironolactone": {
                    "severity": "high",
                    "description": "Increased risk of hyperkalemia",
                    "management": "Monitor serum potassium frequently, consider alternative therapy"
                },
                "nsaids": {
                    "severity": "moderate",
                    "description": "Reduced antihypertensive effect, risk of renal impairment",
                    "management": "Monitor blood pressure and renal function, avoid concurrent use if possible"
                }
            },
            "warfarin": {
                "amiodarone": {
                    "severity": "high",
                    "description": "Increased INR due to CYP2C9 inhibition",
                    "management": "Monitor INR frequently, reduce warfarin dose"
                },
                "fluconazole": {
                    "severity": "high",
                    "description": "Increased INR due to CYP2C9 inhibition",
                    "management": "Monitor INR frequently, reduce warfarin dose"
                },
                "metronidazole": {
                    "severity": "moderate",
                    "description": "Increased INR due to CYP2C9 inhibition",
                    "management": "Monitor INR, consider temporary discontinuation"
                }
            },
            "digoxin": {
                "amiodarone": {
                    "severity": "moderate",
                    "description": "Increased digoxin levels, risk of toxicity",
                    "management": "Monitor digoxin levels, reduce dose by 50%"
                }
            }
        }
        
        # Contraindication database
        self.contraindications = {
            "aspirin": {
                "conditions": ["active_bleeding", "severe_liver_disease", "allergy_to_nsaids", "peptic_ulcer_disease"],
                "description": "Contraindicated in patients with active bleeding, severe liver disease, or peptic ulcer disease"
            },
            "nitroglycerin": {
                "conditions": ["severe_anemia", "increased_intracranial_pressure", "phosphodiesterase_inhibitors"],
                "description": "Contraindicated in patients with severe anemia or recent phosphodiesterase inhibitor use"
            },
            "ace_inhibitors": {
                "conditions": ["pregnancy", "angioedema_history", "bilateral_renal_artery_stenosis", "hereditary_angioedema"],
                "description": "Contraindicated in pregnancy and patients with history of angioedema or bilateral renal artery stenosis"
            },
            "warfarin": {
                "conditions": ["active_bleeding", "severe_liver_disease", "pregnancy", "recent_surgery"],
                "description": "Contraindicated in patients with active bleeding, severe liver disease, or recent surgery"
            },
            "digoxin": {
                "conditions": ["ventricular_fibrillation", "hypertrophic_obstructive_cardiomyopathy"],
                "description": "Contraindicated in ventricular fibrillation and hypertrophic obstructive cardiomyopathy"
            }
        }
        
        # Patient condition database
        self.patient_conditions = {
            "active_bleeding": "Patient has active bleeding",
            "severe_liver_disease": "Patient has severe liver disease",
            "allergy_to_nsaids": "Patient has known allergy to NSAIDs",
            "severe_anemia": "Patient has severe anemia",
            "increased_intracranial_pressure": "Patient has increased intracranial pressure",
            "phosphodiesterase_inhibitors": "Patient is taking phosphodiesterase inhibitors",
            "pregnancy": "Patient is pregnant or of childbearing potential",
            "angioedema_history": "Patient has history of angioedema",
            "bilateral_renal_artery_stenosis": "Patient has bilateral renal artery stenosis",
            "severe_liver_disease": "Patient has severe liver disease"
        }

    def run(self, patient_data: dict, treatment_recommendations: dict) -> dict:
        """
        Check for potential drug interactions and contraindications.
        Returns comprehensive safety screening with identified risks and management recommendations.
        """
        # Extract relevant information
        current_medications = patient_data.get("current_medications", [])
        medical_history = patient_data.get("medical_history", [])
        symptoms = patient_data.get("symptoms", "")
        vitals = patient_data.get("vitals", {})
        age = patient_data.get("age", 0)
        gender = patient_data.get("gender", "")
        
        # Extract proposed medications from treatment recommendations
        proposed_medications = self._extract_proposed_medications(treatment_recommendations)
        
        # Check for drug interactions
        interactions = self._check_drug_interactions(proposed_medications, current_medications)
        
        # Check for contraindications
        contraindications = self._check_contraindications(
            proposed_medications, medical_history, age, gender, symptoms, vitals
        )
        
        # Generate safety screening report
        safety_report = self._generate_safety_report(interactions, contraindications)
        
        # Store safety report in shared memory
        self.memory.store_agent_output("drug_interactions", {
            "patient_data": patient_data,
            "safety_report": safety_report
        })
        
        return safety_report

    def _extract_proposed_medications(self, treatment_recommendations: dict) -> List[str]:
        """Extract proposed medications from treatment recommendations."""
        medications = []
        treatment_plan = treatment_recommendations.get("treatment_plan", {})
        
        # Check primary recommendations
        primary_recs = treatment_plan.get("primary_recommendations", [])
        medications.extend(self._extract_medications_from_text(primary_recs))
        
        # Check secondary recommendations
        secondary_recs = treatment_plan.get("secondary_recommendations", [])
        medications.extend(self._extract_medications_from_text(secondary_recs))
        
        # Check follow-up recommendations
        followup_recs = treatment_plan.get("follow_up_recommendations", [])
        medications.extend(self._extract_medications_from_text(followup_recs))
        
        return list(set(medications))  # Remove duplicates

    def _extract_medications_from_text(self, recommendations: List[str]) -> List[str]:
        """Extract medication names from text recommendations."""
        medications = []
        medication_keywords = [
            "aspirin", "nitroglycerin", "warfarin", "clopidogrel", "ibuprofen",
            "sildenafil", "tadalafil", "vardenafil", "ace inhibitors", "arb", 
            "potassium", "spironolactone", "amiodarone", "fluconazole", "oxygen",
            "digoxin", "heparin", "metronidazole", "nsaids", "furosemide"
        ]
        
        for recommendation in recommendations:
            # Convert to lowercase for case-insensitive matching
            rec_lower = recommendation.lower()
            for keyword in medication_keywords:
                if keyword.lower() in rec_lower:
                    medications.append(keyword.lower())
                    
        return list(set(medications))  # Remove duplicates and return unique medications

    def _check_drug_interactions(self, proposed_medications: List[str], 
                                current_medications: List[str]) -> List[Dict[str, Any]]:
        """Check for potential drug interactions between proposed and current medications."""
        interactions_found = []
        
        # Check each proposed medication against current medications
        for proposed in proposed_medications:
            if proposed in self.drug_interactions:
                for current in current_medications:
                    if current in self.drug_interactions[proposed]:
                        interaction_details = self.drug_interactions[proposed][current]
                        interactions_found.append({
                            "drug1": proposed,
                            "drug2": current,
                            "severity": interaction_details["severity"],
                            "description": interaction_details["description"],
                            "management": interaction_details["management"]
                        })
        
        # Check for interactions within proposed medications
        for i, drug1 in enumerate(proposed_medications):
            if drug1 in self.drug_interactions:
                for j in range(i + 1, len(proposed_medications)):
                    drug2 = proposed_medications[j]
                    if drug2 in self.drug_interactions[drug1]:
                        interaction_details = self.drug_interactions[drug1][drug2]
                        interactions_found.append({
                            "drug1": drug1,
                            "drug2": drug2,
                            "severity": interaction_details["severity"],
                            "description": interaction_details["description"],
                            "management": interaction_details["management"]
                        })
        
        return interactions_found

    def _check_contraindications(self, proposed_medications: List[str], medical_history: List[str],
                                age: int, gender: str, symptoms: str, vitals: dict) -> List[Dict[str, Any]]:
        """Check for contraindications based on patient data."""
        contraindications_found = []
        
        # Check medical history contraindications
        for medication in proposed_medications:
            if medication in self.contraindications:
                contraindication_info = self.contraindications[medication]
                for condition in contraindication_info["conditions"]:
                    if condition in medical_history:
                        contraindications_found.append({
                            "medication": medication,
                            "contraindication": condition,
                            "description": contraindication_info["description"],
                            "reason": self.patient_conditions.get(condition, "Patient condition")
                        })
        
        # Check demographic-based contraindications
        if age > 75:
            # Add age-related considerations
            for medication in proposed_medications:
                if medication in ["aspirin", "warfarin"]:
                    contraindications_found.append({
                        "medication": medication,
                        "contraindication": "advanced_age",
                        "description": "Increased bleeding risk in elderly patients",
                        "reason": "Patient age > 75 years"
                    })
        
        # Check gender-based contraindications
        if gender.lower() == "female" and age >= 12 and age <= 50:
            for medication in proposed_medications:
                if medication in ["ace inhibitors", "arb"]:
                    contraindications_found.append({
                        "medication": medication,
                        "contraindication": "pregnancy_potential",
                        "description": "Contraindicated in pregnancy",
                        "reason": "Female patient of childbearing age"
                    })
        
        # Check symptom-based contraindications
        symptoms_lower = symptoms.lower()
        if "active bleeding" in symptoms_lower:
            for medication in proposed_medications:
                if medication in ["aspirin", "warfarin", "clopidogrel"]:
                    contraindications_found.append({
                        "medication": medication,
                        "contraindication": "active_bleeding",
                        "description": "Contraindicated in active bleeding",
                        "reason": "Patient presenting with active bleeding"
                    })
        
        # Check vital-based contraindications
        if self._has_severe_hypotension(vitals):
            for medication in proposed_medications:
                if medication in ["nitroglycerin", "ace inhibitors"]:
                    contraindications_found.append({
                        "medication": medication,
                        "contraindication": "severe_hypotension",
                        "description": "Contraindicated in severe hypotension",
                        "reason": "Patient has severe hypotension"
                    })
        
        return contraindications_found

    def _has_severe_hypotension(self, vitals: dict) -> bool:
        """Check if patient has severe hypotension."""
        blood_pressure = vitals.get("blood_pressure")
        if blood_pressure is not None:
            try:
                bp_parts = blood_pressure.split("/")
                if len(bp_parts) == 2:
                    systolic = int(bp_parts[0])
                    return systolic < 80
            except (ValueError, TypeError):
                return False
        return False

    def _generate_safety_report(self, interactions: List[Dict[str, Any]], 
                               contraindications: List[Dict[str, Any]]) -> dict:
        """Generate comprehensive safety screening report."""
        # Categorize interactions by severity
        high_risk_interactions = [i for i in interactions if i["severity"] == "high"]
        moderate_risk_interactions = [i for i in interactions if i["severity"] == "moderate"]
        
        # Categorize contraindications by severity
        major_contraindications = [c for c in contraindications if c.get("contraindication") in 
                                  ["active_bleeding", "severe_liver_disease", "pregnancy", 
                                   "severe_anemia", "phosphodiesterase_inhibitors"]]
        moderate_contraindications = [c for c in contraindications if c not in major_contraindications]
        
        # Generate overall safety assessment
        safety_level = "safe"
        if high_risk_interactions or major_contraindications:
            safety_level = "unsafe"
        elif moderate_risk_interactions or moderate_contraindications:
            safety_level = "caution"
        
        return {
            "safety_assessment": {
                "overall_safety_level": safety_level,
                "high_risk_interactions": high_risk_interactions,
                "moderate_risk_interactions": moderate_risk_interactions,
                "major_contraindications": major_contraindications,
                "moderate_contraindications": moderate_contraindications,
                "recommendations": self._generate_safety_recommendations(
                    high_risk_interactions, moderate_risk_interactions,
                    major_contraindications, moderate_contraindications
                )
            },
            "confidence_score": self._calculate_confidence_score(interactions, contraindications)
        }

    def _generate_safety_recommendations(self, high_risk_interactions: List[Dict[str, Any]],
                                        moderate_risk_interactions: List[Dict[str, Any]],
                                        major_contraindications: List[Dict[str, Any]],
                                        moderate_contraindications: List[Dict[str, Any]]) -> List[str]:
        """Generate safety recommendations based on identified risks."""
        recommendations = []
        
        # High-risk interaction recommendations
        for interaction in high_risk_interactions:
            recommendations.append(
                f"CONTRAINDICATED: {interaction['drug1']} with {interaction['drug2']} - "
                f"{interaction['description']}. {interaction['management']}"
            )
        
        # Moderate-risk interaction recommendations
        for interaction in moderate_risk_interactions:
            recommendations.append(
                f"CAUTION: {interaction['drug1']} with {interaction['drug2']} - "
                f"{interaction['description']}. {interaction['management']}"
            )
        
        # Major contraindication recommendations
        for contraindication in major_contraindications:
            recommendations.append(
                f"CONTRAINDICATED: {contraindication['medication']} - "
                f"{contraindication['description']}. Reason: {contraindication['reason']}"
            )
        
        # Moderate contraindication recommendations
        for contraindication in moderate_contraindications:
            recommendations.append(
                f"CAUTION: {contraindication['medication']} - "
                f"{contraindication['description']}. Reason: {contraindication['reason']}"
            )
        
        # General safety recommendations
        if not recommendations:
            recommendations.append("No significant drug interactions or contraindications identified.")
            recommendations.append("Continue with prescribed treatment plan.")
            recommendations.append("Monitor patient for expected therapeutic response and adverse effects.")
        else:
            recommendations.append("Consult with clinical pharmacist for detailed review of identified interactions.")
            recommendations.append("Monitor patient closely for adverse effects and therapeutic response.")
            recommendations.append("Document all findings in patient medical record and communicate with prescribing physician.")
        
        return recommendations

    def _calculate_confidence_score(self, interactions: List[Dict[str, Any]], 
                                   contraindications: List[Dict[str, Any]]) -> float:
        """Calculate confidence score for safety screening."""
        # Base confidence
        base_confidence = 0.85
        
        # Count high-severity findings
        high_severity_findings = len([i for i in interactions if i["severity"] == "high"]) + \
                               len([c for c in contraindications if c.get("contraindication") in 
                                   ["active_bleeding", "severe_liver_disease", "pregnancy", 
                                    "severe_anemia", "phosphodiesterase_inhibitors"]])
        
        # Adjust based on number and severity of findings
        total_findings = len(interactions) + len(contraindications)
        if high_severity_findings > 0:
            # Higher confidence when high-severity findings are present
            confidence = min(0.95, base_confidence + (high_severity_findings * 0.05))
        elif total_findings > 5:
            # Lower confidence if many potential interactions (may be false positives)
            confidence = max(0.6, base_confidence - (total_findings * 0.03))
        else:
            confidence = base_confidence
            
        return round(confidence, 3)