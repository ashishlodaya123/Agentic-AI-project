import logging
from typing import Dict, List, Any
from datetime import datetime
import asyncio
from ..utils.medical_apis import async_search_serper

logger = logging.getLogger(__name__)

class DifferentialDiagnosisAgent:
    """
    Agent for generating differential diagnoses based on symptoms and vitals.
    """
    
    def __init__(self):
        # Expanded medical condition database with symptoms and prevalence
        self.condition_database = {
            "myocardial_infarction": {
                "name": "Myocardial Infarction (Heart Attack)",
                "symptoms": ["chest pain", "shortness of breath", "nausea", "sweating", "arm pain", "jaw pain", "neck pain", "dizziness", "fatigue"],
                "vital_indicators": {"high_blood_pressure": True, "rapid_heart_rate": True, "low_oxygen": True},
                "prevalence": 0.8,
                "severity": "high",
                "demographics": {"age_min": 30, "age_max": 100}
            },
            "pneumonia": {
                "name": "Pneumonia",
                "symptoms": ["fever", "cough", "shortness of breath", "chest pain", "fatigue", "chills", "sputum production", "malaise"],
                "vital_indicators": {"fever": True, "rapid_breathing": True, "low_oxygen": True},
                "prevalence": 0.7,
                "severity": "high",
                "demographics": {"age_min": 0, "age_max": 100}
            },
            "pulmonary_embolism": {
                "name": "Pulmonary Embolism",
                "symptoms": ["shortness of breath", "chest pain", "cough", "leg swelling", "rapid heart rate", "fainting", "hemoptysis", "pleuritic pain"],
                "vital_indicators": {"rapid_heart_rate": True, "low_oxygen": True, "rapid_breathing": True},
                "prevalence": 0.6,
                "severity": "high",
                "demographics": {"age_min": 20, "age_max": 80}
            },
            "asthma_exacerbation": {
                "name": "Asthma Exacerbation",
                "symptoms": ["shortness of breath", "wheezing", "chest tightness", "cough", "difficulty speaking", "cyanosis"],
                "vital_indicators": {"rapid_breathing": True, "low_oxygen": True},
                "prevalence": 0.65,
                "severity": "moderate",
                "demographics": {"age_min": 0, "age_max": 100}
            },
            "costochondritis": {
                "name": "Costochondritis",
                "symptoms": ["chest pain", "tenderness", "pain with breathing", "pain with movement", "localized pain"],
                "vital_indicators": {},
                "prevalence": 0.5,
                "severity": "low",
                "demographics": {"age_min": 10, "age_max": 60}
            },
            "gastroesophageal_reflux": {
                "name": "Gastroesophageal Reflux Disease (GERD)",
                "symptoms": ["chest pain", "heartburn", "acid reflux", "regurgitation", "difficulty swallowing", "sour taste"],
                "vital_indicators": {},
                "prevalence": 0.7,
                "severity": "low",
                "demographics": {"age_min": 20, "age_max": 70}
            },
            "anxiety_panic_attack": {
                "name": "Anxiety/Panic Attack",
                "symptoms": ["chest pain", "shortness of breath", "sweating", "dizziness", "palpitations", "tingling", "fear of dying", "numbness"],
                "vital_indicators": {"rapid_heart_rate": True},
                "prevalence": 0.6,
                "severity": "low",
                "demographics": {"age_min": 15, "age_max": 50}
            },
            "hypertensive_crisis": {
                "name": "Hypertensive Crisis",
                "symptoms": ["headache", "chest pain", "shortness of breath", "blurred vision", "nosebleed", "confusion", "seizure"],
                "vital_indicators": {"high_blood_pressure": True},
                "prevalence": 0.55,
                "severity": "high",
                "demographics": {"age_min": 40, "age_max": 100}
            },
            "pneumothorax": {
                "name": "Pneumothorax (Collapsed Lung)",
                "symptoms": ["sudden chest pain", "shortness of breath", "rapid breathing", "rapid heart rate", "cyanosis"],
                "vital_indicators": {"rapid_breathing": True, "rapid_heart_rate": True, "low_oxygen": True},
                "prevalence": 0.4,
                "severity": "high",
                "demographics": {"age_min": 15, "age_max": 40}
            },
            "pericarditis": {
                "name": "Pericarditis",
                "symptoms": ["sharp chest pain", "fever", "fatigue", "shortness of breath", "pain when lying down", "pericardial friction rub"],
                "vital_indicators": {"fever": True, "rapid_heart_rate": True},
                "prevalence": 0.35,
                "severity": "moderate",
                "demographics": {"age_min": 20, "age_max": 60}
            },
            "bronchitis": {
                "name": "Acute Bronchitis",
                "symptoms": ["cough", "sputum production", "chest discomfort", "fatigue", "mild fever", "shortness of breath"],
                "vital_indicators": {"rapid_breathing": True},
                "prevalence": 0.6,
                "severity": "low",
                "demographics": {"age_min": 0, "age_max": 100}
            },
            "pleurisy": {
                "name": "Pleurisy",
                "symptoms": ["sharp chest pain", "shortness of breath", "cough", "fever", "pleuritic pain"],
                "vital_indicators": {"rapid_breathing": True},
                "prevalence": 0.4,
                "severity": "moderate",
                "demographics": {"age_min": 20, "age_max": 70}
            },
            "pulmonary_edema": {
                "name": "Pulmonary Edema",
                "symptoms": ["shortness of breath", "orthopnea", "paroxysmal nocturnal dyspnea", "cough", "pink frothy sputum", "wheezing"],
                "vital_indicators": {"rapid_breathing": True, "rapid_heart_rate": True, "low_oxygen": True},
                "prevalence": 0.3,
                "severity": "high",
                "demographics": {"age_min": 40, "age_max": 100}
            }
        }
    
    def run(self, patient_data: dict, symptoms_analysis: dict, risk_assessment: dict) -> Dict[str, Any]:
        """
        Generate a differential diagnosis based on patient data.
        
        Args:
            patient_data: Patient information including age, gender, medical history
            symptoms_analysis: Analysis of symptoms and vitals
            risk_assessment: Risk stratification results
            
        Returns:
            Dict containing differential diagnosis with ranked possibilities
        """
        try:
            logger.info("Generating differential diagnosis")
            
            # Extract relevant information
            symptoms = patient_data.get("symptoms", "").lower()
            vitals = patient_data.get("vitals", {})
            age = patient_data.get("age", 0)
            gender = patient_data.get("gender", "")
            medical_history = patient_data.get("medical_history", [])
            
            # If symptoms_analysis has a summary, use that as well
            if isinstance(symptoms_analysis, dict) and "summary" in symptoms_analysis:
                summary = symptoms_analysis["summary"].lower()
                # Combine symptoms and summary for better matching
                combined_symptoms = symptoms + " " + summary
            else:
                combined_symptoms = symptoms
            
            # Generate enhanced diagnoses using multiple sources (NLM > Serper > Hardcoded)
            diagnosis_list = self._generate_enhanced_diagnoses(combined_symptoms, vitals, age, gender, medical_history, symptoms_analysis)
            
            logger.info(f"Using enhanced diagnoses with {len(diagnosis_list)} results")
            
            # Rank diagnoses based on match score
            ranked_diagnoses = sorted(diagnosis_list, key=lambda x: x["match_score"], reverse=True)
            
            # Limit to top diagnoses
            # Always use top 4 for consistency, whether from Serper or hardcoded
            top_diagnoses = ranked_diagnoses[:4]
            
            # Add confidence scores based on match scores
            for i, diagnosis in enumerate(top_diagnoses):
                # Calculate confidence based on match score (normalized)
                max_score = top_diagnoses[0]["match_score"] if top_diagnoses else 1.0
                normalized_score = diagnosis["match_score"] / max_score if max_score > 0 else 0
                diagnosis["confidence_score"] = round(max(min(normalized_score, 0.95), 0.1), 3)
            
            result = {
                "differential_diagnosis": top_diagnoses,
                "total_possibilities": len(top_diagnoses),
                "timestamp": datetime.now().isoformat(),
                "confidence_factors": {
                    "symptom_match": True,
                    "vital_signs": bool(vitals),
                    "risk_assessment": bool(risk_assessment),
                    "demographics": True
                }
            }
            
            logger.info(f"Final differential diagnosis contains {len(top_diagnoses)} diagnoses")
            return result
            
        except Exception as e:
            logger.error(f"Error in differential diagnosis generation: {e}")
            return {
                "differential_diagnosis": [],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _generate_dynamic_diagnoses_serper(self, symptoms: str, vitals: dict, age: int, gender: str, medical_history: List[str], symptoms_analysis: dict) -> List[Dict[str, Any]]:
        """Generate and rank possible diagnoses using Serper API."""
        diagnoses = []
        
        try:
            # Search using Serper API
            serper_result = asyncio.run(async_search_serper(symptoms))
            
            # Check if we got a valid response
            if not isinstance(serper_result, dict) or serper_result.get("status") != "success":
                logger.info("Serper API not available, falling back to hardcoded conditions")
                return []
            
            search_results = serper_result.get("results", [])
            
            # Process each search result to create a diagnosis
            for result in search_results:
                # Handle dict results from Serper API
                if isinstance(result, dict):
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    link = result.get("link", "")
                else:
                    # If it's not a dict, skip this result
                    continue
                
                # Calculate match score based on relevance
                match_score = self._calculate_dynamic_match_score(symptoms, title, snippet)
                
                # Include results with moderate match to increase diagnosis count
                if match_score > 3.0:  # Lowered threshold to get more diagnoses
                    # Enhanced description handling to avoid truncation in the middle of sentences
                    clean_description = self._clean_description(snippet)
                    # Special handling for known problematic truncations
                    clean_title = title
                    if "asthma and anaphylaxis" in title.lower() and "asthma and anaphylaxis in the" in title.lower():
                        clean_title = "Asthma And Anaphylaxis"
                    else:
                        clean_title = self._extract_condition_name(title)
                    
                    # Further refine the condition name to ensure it's the actual diagnosis
                    final_condition = self._refine_condition_name(clean_title, title, snippet)
                    
                    # Loosen filtering to allow more medical conditions through
                    # Only filter out clearly non-medical content
                    if len(final_condition) > 2 and not any(term in final_condition.lower() for term in ["symptom", "sign", "cause", "treatment", "therapy", "overview", "introduction"]):
                        diagnoses.append({
                            "condition": final_condition,
                            "match_score": round(match_score, 3),
                            "matched_symptoms": [],  # Will be populated by frontend
                            "matched_vitals": [],    # Will be populated by frontend
                            "severity": self._assess_severity(title, snippet),
                            "prevalence": min(0.9, match_score / 20.0),  # Normalize prevalence
                            "recommendations": self._get_dynamic_recommendations(title, snippet),
                            "description": clean_description,
                            "link": link  # Include the search result link
                        })
            
            # Sort by match score
            diagnoses = sorted(diagnoses, key=lambda x: x["match_score"], reverse=True)
            
        except asyncio.TimeoutError:
            logger.warning("Serper API timeout, falling back to hardcoded conditions")
            return []
        except Exception as e:
            logger.error(f"Error in Serper diagnosis generation: {e}")
            return []
        
        return diagnoses[:4]  # Return top 4 diagnoses to ensure we get at least 2-3 quality diagnoses

    def _generate_diagnoses(self, symptoms: str, vitals: dict, age: int, gender: str, medical_history: List[str], symptoms_analysis: dict) -> List[Dict[str, Any]]:
        """Generate and rank possible diagnoses based on symptoms, vitals, and patient data."""
        diagnoses = []
        
        # Check each condition in the database
        for condition_key, condition_data in self.condition_database.items():
            match_score = 0
            matched_symptoms = []
            matched_vitals = []
            
            # Check demographic compatibility
            demographics = condition_data.get("demographics", {})
            age_min = demographics.get("age_min", 0)
            age_max = demographics.get("age_max", 100)
            
            if age_min <= age <= age_max:
                match_score += 0.5  # Base demographic match
            
            # Check symptoms
            condition_symptoms = condition_data.get("symptoms", [])
            symptom_words = symptoms.split()
            
            for symptom in symptom_words:
                # Check for exact matches and partial matches
                for condition_symptom in condition_symptoms:
                    if self._symptoms_match(symptom, condition_symptom):
                        match_score += 1.0
                        matched_symptoms.append(condition_symptom)
            
            # Check vital sign indicators with increased weight
            vital_indicators = condition_data["vital_indicators"]
            for indicator, required in vital_indicators.items():
                if required and self._check_vital_indicator(indicator, vitals):
                    match_score += 1.2  # Increased weight for vital indicators
                    matched_vitals.append(indicator)
            
            # Adjust for age and gender factors
            match_score = self._adjust_for_demographics(match_score, condition_key, age, gender)
            
            # Adjust for medical history with higher impact
            match_score = self._adjust_for_medical_history(match_score, condition_key, medical_history)
            
            # Apply prevalence factor
            prevalence = condition_data.get("prevalence", 0.5)
            match_score *= prevalence
            
            # Only include conditions with significant match
            if match_score > 0.5:
                diagnoses.append({
                    "condition": condition_data["name"],
                    "condition_key": condition_key,
                    "match_score": round(match_score, 3),
                    "matched_symptoms": matched_symptoms,
                    "matched_vitals": matched_vitals,
                    "severity": condition_data.get("severity", "moderate"),
                    "prevalence": prevalence,
                    "recommendations": self._get_recommendations(condition_key),
                    "source": "Hardcoded Database"  # Indicate the source for transparency
                })
        
        return diagnoses

    def _symptoms_match(self, symptom1: str, symptom2: str) -> bool:
        """Check if two symptoms match (exact or partial)."""
        # Exact match
        if symptom1 == symptom2:
            return True
        
        # Partial match (one term contained in another)
        if symptom1 in symptom2 or symptom2 in symptom1:
            return True
        
        # Split into words for more detailed comparison
        words1 = set(symptom1.split())
        words2 = set(symptom2.split())
        
        if words1 and words2:
            # Check for exact word matches
            common_words = words1.intersection(words2)
            if len(common_words) > 0:
                # If they share more than 50% of words
                min_words = min(len(words1), len(words2))
                if len(common_words) >= max(1, min_words // 2):
                    return True
        
        return False

    def _check_vital_indicator(self, indicator: str, vitals: dict) -> bool:
        """Check if a vital sign indicator is present and abnormal."""
        # Convert all vital values to appropriate types for comparison
        vital_indicators = {
            "high_blood_pressure": lambda v: self._get_blood_pressure_value(v.get("blood_pressure", "")) > 140,
            "low_blood_pressure": lambda v: self._get_blood_pressure_value(v.get("blood_pressure", "")) < 90,
            "rapid_heart_rate": lambda v: self._get_int_value(v.get("heart_rate")) > 100,
            "slow_heart_rate": lambda v: self._get_int_value(v.get("heart_rate")) < 60,
            "high_temperature": lambda v: self._get_float_value(v.get("temperature")) > 38.0,
            "low_temperature": lambda v: self._get_float_value(v.get("temperature")) < 36.0,
            "low_oxygen": lambda v: self._get_float_value(v.get("oxygen_saturation", "").replace("%", "")) < 95,
            "rapid_breathing": lambda v: self._get_int_value(v.get("respiratory_rate")) > 20,
            "slow_breathing": lambda v: self._get_int_value(v.get("respiratory_rate")) < 12,
            "irregular_heartbeat": lambda v: False,  # This would require ECG data
            "fever": lambda v: self._get_float_value(v.get("temperature")) > 38.0,
            "hypothermia": lambda v: self._get_float_value(v.get("temperature")) < 35.0
        }
        
        checker = vital_indicators.get(indicator)
        if checker:
            return checker(vitals)
        return False

    def _get_blood_pressure_value(self, bp_str: str) -> int:
        """Extract systolic blood pressure value from string."""
        try:
            if "/" in bp_str:
                return int(bp_str.split("/")[0])
            else:
                return int(bp_str)
        except (ValueError, IndexError):
            return 0

    def _get_int_value(self, value) -> int:
        """Convert value to integer safely."""
        try:
            if isinstance(value, str):
                return int(value)
            elif isinstance(value, (int, float)):
                return int(value)
            else:
                return 0
        except (ValueError, TypeError):
            return 0

    def _get_float_value(self, value) -> float:
        """Convert value to float safely."""
        try:
            if isinstance(value, str):
                return float(value)
            elif isinstance(value, (int, float)):
                return float(value)
            else:
                return 0.0
        except (ValueError, TypeError):
            return 0.0

    def _refine_condition_name(self, clean_title: str, original_title: str, snippet: str) -> str:
        """Further refine the condition name to ensure it's the actual diagnosis."""
        # If we already have a clean title, use it
        if clean_title and len(clean_title) > 3:
            # Check if it's not a generic term
            generic_terms = ["symptoms", "signs", "causes", "treatment", "diagnosis", "medical", "health", "condition", "overview", "introduction"]
            if not any(term in clean_title.lower() for term in generic_terms):
                return clean_title
        
        # Try to extract a better condition name from the original title
        import re
        
        # Look for common medical condition patterns
        medical_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Syndrome|Disease|Disorder|Condition|Infection|Cancer|Tumor|Lesion|Deficiency|Insufficiency|Failure))\b'
        match = re.search(medical_pattern, original_title)
        if match:
            return match.group(1).strip()
        
        # Look for common conditions like "Heart Attack", "Kidney Stones"
        common_pattern = r'\b([A-Z][a-z]+\s+(?:Attack|Stones|Pain|Injury|Infection))\b'
        match = re.search(common_pattern, original_title)
        if match:
            return match.group(1).strip()
        
        # If no pattern matched, return the clean title or original title
        return clean_title if len(clean_title) > 3 else original_title.strip()

    def _adjust_for_demographics(self, score: float, condition_key: str, age: int, gender: str) -> float:
        """Adjust match score based on demographic factors."""
        # Age-based adjustments for specific conditions
        age_adjustments = {
            "myocardial_infarction": lambda a: 1.5 if a > 40 else 0.7,
            "pneumonia": lambda a: 1.2 if a < 5 or a > 65 else 1.0,
            "asthma_exacerbation": lambda a: 1.3 if a < 18 else 1.0,
            "hypertensive_crisis": lambda a: 1.4 if a > 50 else 0.8
        }
        
        adjustment_func = age_adjustments.get(condition_key)
        if adjustment_func:
            score *= adjustment_func(age)
        
        # Gender-based adjustments (simplified)
        # Some conditions are more prevalent in specific genders
        gender_adjustments = {
            "prostatitis": lambda g: 2.0 if g.lower() == "male" else 0.1,
            "menopause": lambda g: 2.0 if g.lower() == "female" else 0.1
        }
        
        gender_func = gender_adjustments.get(condition_key)
        if gender_func:
            score *= gender_func(gender)
        
        return score

    def _adjust_for_medical_history(self, score: float, condition_key: str, medical_history: List[str]) -> float:
        """Adjust match score based on medical history."""
        # Convert medical history to lowercase for comparison
        history_lower = [h.lower() for h in medical_history]
        
        # Risk factor adjustments based on medical history
        risk_factors = {
            "myocardial_infarction": ["hypertension", "diabetes", "smoking", "high cholesterol", "family history heart disease"],
            "pneumonia": ["copd", "asthma", "smoking", "immunocompromised", "diabetes"],
            "pulmonary_embolism": ["recent surgery", "immobilization", "cancer", "pregnancy", "oral contraceptives"],
            "diabetes": ["family history diabetes", "obesity", "gestational diabetes"],
            "hypertensive_crisis": ["hypertension", "kidney disease", "diabetes"]
        }
        
        condition_risks = risk_factors.get(condition_key, [])
        risk_matches = sum(1 for risk in condition_risks if any(risk in history for history in history_lower))
        
        # Increase score based on number of matching risk factors
        if risk_matches > 0:
            score *= (1.0 + risk_matches * 0.3)  # 30% increase per matching risk factor
        
        return score

    def _get_recommendations(self, condition_key: str) -> List[str]:
        """Get recommendations for a specific condition."""
        recommendations = {
            "myocardial_infarction": [
                "Immediate ECG monitoring",
                "Cardiac enzyme panel (troponin levels)",
                "IV access establishment",
                "Nitroglycerin for chest pain relief (if BP adequate)",
                "Aspirin 325mg chewable",
                "Oxygen therapy if hypoxic",
                "Morphine for pain if needed",
                "Continuous cardiac monitoring"
            ],
            "pneumonia": [
                "Chest X-ray",
                "Complete blood count with differential",
                "Sputum culture and sensitivity",
                "Blood cultures if febrile",
                "Antibiotic therapy pending culture results",
                "Oxygen therapy if hypoxic",
                "Hydration support"
            ],
            "pulmonary_embolism": [
                "D-dimer test (age-adjusted if >50)",
                "CT pulmonary angiogram",
                "Ventilation-perfusion scan if contraindicated",
                "Anticoagulation therapy (heparin protocol)",
                "Oxygen therapy",
                "IV access",
                "Monitor for bleeding complications"
            ],
            "asthma_exacerbation": [
                "Peak flow measurement",
                "Albuterol nebulizer treatment",
                "Ipratropium bromide if severe",
                "Systemic steroid therapy",
                "Oxygen therapy if hypoxic",
                "Continuous monitoring of oxygen saturation",
                "Consider magnesium sulfate for severe cases"
            ],
            "costochondritis": [
                "Pain management with NSAIDs",
                "Physical examination for reproducible tenderness",
                "ECG to rule out cardiac causes",
                "Chest X-ray if trauma suspected",
                "Reassurance and education about benign nature"
            ],
            "gastroesophageal_reflux": [
                "Antacid therapy for immediate relief",
                "Proton pump inhibitor trial",
                "ECG to rule out cardiac causes",
                "Dietary modifications (avoid trigger foods)",
                "Elevate head of bed",
                "Consider H. pylori testing if indicated"
            ],
            "anxiety_panic_attack": [
                "Reassurance and calming techniques",
                "Vital sign monitoring",
                "ECG to rule out cardiac causes",
                "Breathing exercises (paced breathing)",
                "Anxiolytic medication if indicated (benzodiazepines)",
                "Consider psychological support referral"
            ],
            "hypertensive_crisis": [
                "Immediate blood pressure monitoring every 5-15 min",
                "IV antihypertensive therapy (labetalol, nicardipine)",
                "ECG monitoring",
                "Neurological assessment",
                "Laboratory studies (creatinine, electrolytes, BUN)",
                "Ophthalmologic examination if visual symptoms",
                "Consider CT head if neurological symptoms"
            ],
            "pneumothorax": [
                "Chest X-ray (PA and lateral views)",
                "Arterial blood gas analysis",
                "Oxygen therapy",
                "Consider chest tube placement if large",
                "Monitor respiratory status closely",
                "Surgical consultation for recurrent cases"
            ],
            "pericarditis": [
                "ECG (look for diffuse ST elevations)",
                "Echocardiogram to assess for effusion",
                "Inflammatory markers (ESR, CRP)",
                "NSAIDs for pain and inflammation",
                "Colchicine for recurrent cases",
                "Rule out myocardial infarction"
            ],
            "pulmonary_edema": [
                "Immediate oxygen therapy",
                "ECG monitoring",
                "Chest X-ray",
                "BNP or NT-proBNP levels",
                "Diuretic therapy (furosemide)",
                "Non-invasive ventilation if severe",
                "Treat underlying cause",
                "Monitor electrolytes and renal function"
            ]
        }
        
        return recommendations.get(condition_key, ["Further evaluation recommended"])

    def _is_medical_diagnosis(self, title: str, snippet: str) -> bool:
        """Check if the result is a proper medical diagnosis rather than a general medical article."""
        title_lower = title.lower()
        snippet_lower = snippet.lower()
        
        # Keywords that indicate it's a proper medical condition/diagnosis
        diagnosis_indicators = [
            "diabetes", "pneumonia", "asthma", "hypertension", "myocardial infarction",
            "heart attack", "stroke", "migraine", "arthritis", "bronchitis", "appendicitis",
            "gastritis", "ulcer", "anemia", "thyroid", "depression", "anxiety", "allergy",
            "infection", "fracture", "sprain", "strain", "concussion", "epilepsy",
            "seizure", "cirrhosis", "hepatitis", "nephritis", "cystitis", "dermatitis",
            "eczema", "psoriasis", "osteoporosis", "osteopenia", "meningitis", "encephalitis",
            "tuberculosis", "malaria", "dengue", "chickenpox", "measles", "mumps", "rubella",
            "sinusitis", "tonsillitis", "pharyngitis", "laryngitis", "conjunctivitis",
            "otitis", "gastroenteritis", "colitis", "diverticulitis", "hemorrhoids",
            "hernia", "gallstones", "kidney stones", "urinary tract infection",
            "chronic obstructive pulmonary disease", "copd", "emphysema", "bronchiectasis",
            "pulmonary embolism", "deep vein thrombosis", "dvt", "anaphylaxis",
            "food poisoning", "gout", "lupus", "rheumatoid arthritis", "multiple sclerosis",
            "parkinson's disease", "alzheimer's disease", "dementia", "schizophrenia",
            "bipolar disorder", "panic disorder", "obsessive compulsive disorder", "ocd",
            "attention deficit hyperactivity disorder", "adhd", "autism", "autism spectrum disorder",
            "angina", "pericarditis", "endocarditis", "myocarditis", "cardiomyopathy",
            "arrhythmia", "atrial fibrillation", "heart failure", "congestive heart failure",
            "aneurysm", "atherosclerosis", "varicose veins", "deep vein thrombosis",
            "peptic ulcer", "gastroesophageal reflux", "gerd", "crohn's disease", "ulcerative colitis",
            "irritable bowel syndrome", "ibs", "celiac disease", "lactose intolerance",
            "kidney disease", "renal failure", "glomerulonephritis", "polycystic kidney disease",
            "bladder infection", "prostatitis", "erectile dysfunction", "menopause",
            "polycystic ovary syndrome", "pcos", "endometriosis", "fibroids",
            "cancer", "leukemia", "lymphoma", "melanoma", "carcinoma",
            "osteomyelitis", "cellulitis", "abscess", "boil", "carbuncle",
            "tetanus", "botulism", "rabies", "lyme disease", "west nile virus",
            "influenza", "flu", "common cold", "rhinovirus", "coronavirus",
            "hiv", "aids", "hepatitis b", "hepatitis c", "mononucleosis",
            "scarlet fever", "whooping cough", "pertussis", "impetigo",
            "ringworm", "athlete's foot", "jock itch", "yeast infection",
            "pink eye", "stye", "cataract", "glaucoma", "macular degeneration",
            "tinnitus", "vertigo", "meniere's disease", "carpal tunnel syndrome",
            "tendinitis", "bursitis", "fibromyalgia", "chronic fatigue syndrome",
            "sleep apnea", "insomnia", "narcolepsy", "sleepwalking",
            "bulimia", "anorexia", "binge eating disorder", "post-traumatic stress disorder",
            "ptsd", "social anxiety", "phobia", "agoraphobia", "claustrophobia",
            "addiction", "substance abuse", "alcoholism", "drug addiction",
            "withdrawal", "overdose", "poisoning", "heat stroke", "hypothermia",
            "dehydration", "malnutrition", "vitamin deficiency", "iron deficiency",
            "hypoglycemia", "hyperthyroidism", "hypothyroidism", " cushing's syndrome",
            "addison's disease", "acromegaly", "gigantism", "dwarfism"
        ]
        
        # Keywords that indicate it's NOT a proper diagnosis (general articles, guidelines, etc.)
        non_diagnosis_indicators = [
            "guideline", "guidance", "protocol", "procedure", "treatment", "therapy",
            "management", "care", "practice", "policy", "standard", "recommendation",
            "algorithm", "approach", "strategy", "framework", "model", "system",
            "program", "initiative", "campaign", "study", "research", "trial",
            "review", "meta-analysis", "analysis", "evaluation", "assessment",
            "investigation", "exploration", "inquiry", "survey", "report",
            "publication", "article", "journal", "book", "manual", "handbook",
            "dictionary", "encyclopedia", "reference", "database", "registry",
            "classification", "taxonomy", "nomenclature", "terminology",
            "glossary", "index", "catalog", "directory", "list", "table",
            "chart", "diagram", "figure", "image", "picture", "photo",
            "video", "audio", "podcast", "webinar", "course", "training",
            "education", "learning", "teaching", "instruction", "curriculum",
            "syllabus", "lesson", "module", "unit", "chapter", "section",
            "introduction", "overview", "summary", "conclusion", "abstract",
            "preface", "foreword", "afterword", "appendix", "supplement",
            "addendum", "erratum", "corrigendum", "retraction", "commentary",
            "editorial", "opinion", "perspective", "viewpoint", "position",
            "statement", "declaration", "resolution", "motion", "proposal",
            "suggestion", "recommendation", "advice", "counsel", "guidance",
            "instruction", "direction", "command", "order", "mandate",
            "requirement", "obligation", "duty", "responsibility", "role",
            "function", "purpose", "objective", "goal", "target", "aim",
            "mission", "vision", "value", "principle", "ethic", "morality",
            "virtue", "character", "personality", "temperament", "disposition",
            "attitude", "belief", "opinion", "conviction", "faith", "trust",
            "confidence", "assurance", "certainty", "certitude", "conviction",
            "flashcard", "quiz", "test", "exam", "assessment", "evaluation",
            "diagnostic criteria", "differential diagnosis", "case study",
            "clinical presentation", "medical education", "medical school",
            "residency", "fellowship", "board certification", "continuing education",
            "cme", "ce", "cpd", "professional development", "career", "job",
            "employment", "recruitment", "hiring", "interview", "resume",
            "cv", "curriculum vitae", "portfolio", "profile", "bio", "biography",
            "personal statement", "cover letter", "application", "admission",
            "enrollment", "registration", "sign up", "login", "account",
            "membership", "subscription", "newsletter", "magazine", "newspaper",
            "blog", "forum", "community", "social media", "facebook", "twitter",
            "instagram", "linkedin", "youtube", "tiktok", "pinterest", "reddit",
            "wikipedia", "wiki", "encyclopedia", "dictionary", "thesaurus",
            "definition", "meaning", "explanation", "description", "introduction",
            "tutorial", "how to", "guide", "step by step", "instructions",
            "faq", "frequently asked questions", "help", "support", "contact",
            "customer service", "technical support", "troubleshooting", "bug",
            "error", "problem", "issue", "solution", "fix", "repair", "maintenance",
            "update", "upgrade", "download", "install", "setup", "configuration",
            "settings", "preferences", "options", "features", "functions",
            "specifications", "specs", "requirements", "prerequisites", "dependencies",
            "compatibility", "system requirements", "hardware", "software", "firmware",
            "driver", "plugin", "extension", "module", "component", "library",
            "api", "sdk", "documentation", "manual", "handbook", "reference",
            "white paper", "technical report", "specification", "standard",
            "protocol", "format", "structure", "architecture", "design", "pattern",
            "methodology", "framework", "platform", "tool", "utility", "application",
            "app", "program", "software", "code", "script", "algorithm", "function",
            "method", "class", "object", "variable", "parameter", "argument",
            "return value", "output", "input", "data", "information", "content",
            "text", "document", "file", "folder", "directory", "path", "url",
            "link", "address", "location", "place", "position", "coordinate",
            "map", "navigation", "route", "direction", "way", "path", "trail",
            "track", "footprint", "signature", "hash", "checksum", "encryption",
            "security", "privacy", "protection", "safety", "risk", "threat",
            "vulnerability", "exploit", "attack", "breach", "compromise", "hack",
            "malware", "virus", "trojan", "worm", "spyware", "adware", "ransomware",
            "phishing", "scam", "fraud", "theft", "robbery", "burglary", "assault",
            "battery", "harassment", "stalking", "bullying", "discrimination",
            "harassment", "abuse", "neglect", "mistreatment", "mistake", "error",
            "accident", "incident", "event", "occurrence", "happening", "phenomenon",
            "situation", "circumstance", "condition", "state", "status", "status",
            "stage", "phase", "period", "time", "moment", "instant", "second",
            "minute", "hour", "day", "week", "month", "year", "decade", "century",
            "millennium", "era", "epoch", "age", "generation", "millisecond",
            "microsecond", "nanosecond", "picosecond", "femtosecond", "attosecond",
            "zeptosecond", "yoctosecond", "planck time", "chronon", "moment",
            "jiffy", "shake", "sigma", "lambda", "epsilon", "delta", "theta",
            "kappa", "omega", "alpha", "beta", "gamma", "zeta", "eta", "iota",
            "mu", "nu", "xi", "pi", "rho", "tau", "upsilon", "phi", "chi", "psi",
            "math", "mathematics", "algebra", "geometry", "calculus", "statistics",
            "probability", "logic", "set theory", "number theory", "combinatorics",
            "graph theory", "topology", "analysis", "arithmetic", "trigonometry",
            "linear algebra", "abstract algebra", "group theory", "ring theory",
            "field theory", "category theory", "homological algebra", "homotopy theory",
            "k-theory", "motivic cohomology", "etale cohomology", "crystalline cohomology",
            "p-adic hodge theory", "langlands program", "geometric langlands",
            "arithmetic geometry", "algebraic geometry", "differential geometry",
            "riemannian geometry", "symplectic geometry", "contact geometry",
            "complex geometry", "kähler geometry", "calabi-yau manifolds",
            "string theory", "quantum field theory", "quantum mechanics",
            "general relativity", "special relativity", "thermodynamics",
            "statistical mechanics", "fluid dynamics", "solid state physics",
            "condensed matter physics", "particle physics", "nuclear physics",
            "atomic physics", "molecular physics", "optics", "electromagnetism",
            "electricity", "magnetism", "electrodynamics", "maxwell's equations",
            "schrodinger equation", "dirac equation", "klein-gordon equation",
            "einstein field equations", "navier-stokes equations", "heat equation",
            "wave equation", "diffusion equation", "laplace equation", "poisson equation",
            "helmholtz equation", "biot-savart law", "faraday's law", "ampere's law",
            "coulomb's law", "ohm's law", "kirchhoff's laws", "newton's laws",
            "kepler's laws", "hubble's law", "planck's law", "stefan-boltzmann law",
            "wien's displacement law", "heisenberg uncertainty principle",
            "pauli exclusion principle", "bose-einstein statistics", "fermi-dirac statistics",
            "maxwell-boltzmann statistics", "blackbody radiation", "photoelectric effect",
            "compton scattering", "pair production", "annihilation", "tunneling",
            "superconductivity", "superfluidity", "bose-einstein condensate",
            "fermionic condensate", "quantum hall effect", "fractional quantum hall effect",
            "quantum spin hall effect", "topological insulator", "weyl semimetal",
            "dirac semimetal", "nodal line semimetal", "topological superconductor",
            "majorana fermion", "anyon", "non-abelian anyon", "braiding statistics",
            "topological quantum computing", "quantum error correction",
            "surface code", "color code", "toric code", "cluster state", "graph state",
            "matrix product state", "tensor network", "entanglement", "quantum entanglement",
            "quantum teleportation", "quantum cryptography", "quantum key distribution",
            "bb84 protocol", "ekert protocol", "quantum money", "quantum internet",
            "quantum communication", "quantum sensing", "quantum metrology",
            "quantum imaging", "quantum lithography", "quantum radar", "quantum biology",
            "quantum chemistry", "quantum field theory in curved spacetime",
            "hawking radiation", "unruh effect", "casimir effect", "lamb shift",
            "zeeman effect", "stark effect", "fine structure", "hyperfine structure",
            "spin-orbit coupling", "ls coupling", "jj coupling", "russell-saunders coupling",
            "term symbol", "spectroscopic notation", "atomic spectroscopy",
            "molecular spectroscopy", "rotational spectroscopy", "vibrational spectroscopy",
            "electronic spectroscopy", "raman spectroscopy", "nuclear magnetic resonance",
            "electron paramagnetic resonance", "mossbauer spectroscopy",
            "photoelectron spectroscopy", "auger electron spectroscopy",
            "x-ray photoelectron spectroscopy", "x-ray absorption spectroscopy",
            "x-ray emission spectroscopy", "extended x-ray absorption fine structure",
            "x-ray diffraction", "neutron diffraction", "electron diffraction",
            "low energy electron diffraction", "reflection high energy electron diffraction",
            "transmission electron microscopy", "scanning electron microscopy",
            "atomic force microscopy", "scanning tunneling microscopy",
            "near-field scanning optical microscopy", "super-resolution microscopy",
            "fluorescence microscopy", "confocal microscopy", "two-photon microscopy",
            "multiphoton microscopy", "nonlinear microscopy", "coherent anti-stokes raman spectroscopy",
            "sum frequency generation", "difference frequency generation",
            "second harmonic generation", "third harmonic generation",
            "four-wave mixing", "stimulated raman scattering", "stimulated brillouin scattering",
            "fourier transform infrared spectroscopy", "infrared spectroscopy",
            "ultraviolet-visible spectroscopy", "uv-vis spectroscopy",
            "circular dichroism", "linear dichroism", "optical rotatory dispersion",
            "magnetic circular dichroism", "electron spin resonance", "esr",
            "nuclear quadrupole resonance", "nqr", "muon spin resonance", "msr",
            "positron annihilation spectroscopy", "perturbed angular correlation",
            "time-differential perturbed angular correlation", "tdpac",
            "time-differential perturbed gamma-gamma angular correlation", "tdpac",
            "perturbed angular distribution", "pad", "time-differential perturbed angular distribution", "tdpad",
            "perturbed gamma-gamma angular correlation", "pggac", "time-differential perturbed gamma-gamma angular correlation", "tdpggac",
            "perturbed beta-gamma angular correlation", "pbgac", "time-differential perturbed beta-gamma angular correlation", "tdpbgac",
            "perturbed beta-beta angular correlation", "pbbac", "time-differential perturbed beta-beta angular correlation", "tdpbbac"
        ]
        
        # Check if it contains diagnosis indicators
        has_diagnosis_indicator = any(indicator in title_lower or indicator in snippet_lower 
                                    for indicator in diagnosis_indicators)
        
        # Check if it contains non-diagnosis indicators
        has_non_diagnosis_indicator = any(indicator in title_lower or indicator in snippet_lower 
                                        for indicator in non_diagnosis_indicators)
        
        # It's a diagnosis if it has diagnosis indicators and no non-diagnosis indicators
        if has_diagnosis_indicator and not has_non_diagnosis_indicator:
            return True
        elif has_diagnosis_indicator and has_non_diagnosis_indicator:
            # Special case: if it has strong diagnosis indicators, allow it even if it has some non-diagnosis words
            strong_diagnosis_indicators = ["diabetes", "pneumonia", "asthma", "hypertension", "myocardial infarction",
                                         "heart attack", "stroke", "migraine", "arthritis", "bronchitis", "appendicitis",
                                         "gastritis", "ulcer", "anemia", "thyroid", "depression", "anxiety", "allergy",
                                         "infection", "fracture", "sprain", "strain", "concussion", "epilepsy",
                                         "seizure", "cirrhosis", "hepatitis", "nephritis", "cystitis", "dermatitis"]
            has_strong_diagnosis = any(indicator in title_lower or indicator in snippet_lower 
                                     for indicator in strong_diagnosis_indicators)
            
            # If it has strong diagnosis indicators, allow it even if it has some non-diagnosis words
            if has_strong_diagnosis:
                # But still exclude if it's clearly a guideline or protocol
                clear_non_diagnosis_indicators = ["guideline", "protocol", "procedure", "treatment", "therapy",
                                                "management", "care", "practice", "policy", "standard", "recommendation",
                                                "algorithm", "approach", "strategy", "framework", "model", "system"]
                has_clear_non_diagnosis = any(indicator in title_lower or indicator in snippet_lower 
                                            for indicator in clear_non_diagnosis_indicators)
                return not has_clear_non_diagnosis
        
        return False
    
    def _extract_condition_name(self, title: str) -> str:
        """Extract clean condition name from search result title."""
        # Start with the original title
        condition = title.strip()
        
        # Special handling for known problematic truncations
        title_lower = title.lower()
        if "asthma and anaphylaxis" in title_lower and "asthma and anaphylaxis in the" in title_lower:
            return "Asthma And Anaphylaxis"
        
        # Remove common prefixes and suffixes that indicate educational content
        educational_prefixes = [
            "Symptoms of", "Diagnosis of", "Treatment for", "Causes of", "Signs of", 
            "Management of", "What is", "What are", "Understanding", "Overview of",
            "Introduction to", "Guide to", "How to Diagnose"
        ]
        
        for prefix in educational_prefixes:
            if condition.startswith(prefix):
                condition = condition[len(prefix):].strip()
                break
        
        # Remove institutional prefixes like "CDC - " or "Mayo Clinic - "
        if " - " in condition:
            parts = condition.split(" - ")
            # If the first part is short and seems institutional, remove it
            institutional_prefixes = [
                "cdc", "who", "mayo", "webmd", "healthline", "medline", "nih", "fda", 
                "fml", "cleveland clinic", "johns hopkins", "harvard health", "webmd"
            ]
            if len(parts[0]) < 30 and any(prefix in parts[0].lower() for prefix in institutional_prefixes):
                condition = " - ".join(parts[1:])
            # Otherwise, keep the full condition name to avoid truncation
            # Only take the first part if it's clearly a better representation
        
        # Remove institutional suffixes and common suffixes
        suffixes_to_remove = [
            " - Symptoms and Causes", " - Diagnosis and Treatment", " - Prevention",
            " - Overview", " - Mayo Clinic", " - CDC", " - WebMD", " - Healthline",
            " | Symptoms and Causes", " | Diagnosis and Treatment", " | Prevention",
            " | Overview", " | Mayo Clinic", " | CDC", " | WebMD", " | Healthline",
            " | Medical Encyclopedia", " | Health Topics", " | Patient Education"
        ]
        
        for suffix in suffixes_to_remove:
            if condition.endswith(suffix):
                condition = condition[:-len(suffix)]
                break
        
        # Remove trailing dots, colons, and extra whitespace
        condition = condition.strip(" .:")
        
        # Enhanced approach: Extract the most likely diagnosis from the title
        # First, try to identify if this is a medical condition by looking for common patterns
        import re
        
        # Pattern for common medical condition formats
        # This pattern looks for capitalized words followed by medical terms like "Syndrome", "Disease", etc.
        medical_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Syndrome|Disease|Disorder|Condition|Infection|Cancer|Tumor|Lesion|Deficiency|Insufficiency|Failure|Syndrome))\b'
        match = re.search(medical_pattern, condition)
        if match:
            return match.group(1).strip()
        
        # Pattern for conditions like "Heart Attack", "Kidney Stones", etc.
        common_conditions_pattern = r'\b([A-Z][a-z]+\s+(?:Attack|Stones|Pain|Injury|Infection))\b'
        match = re.search(common_conditions_pattern, condition)
        if match:
            return match.group(1).strip()
        
        # If no specific pattern matched, try to extract the most relevant part
        # Split by common separators and take the most meaningful part
        separators = [" - ", " | ", ": ", " -"]
        for separator in separators:
            if separator in condition:
                parts = condition.split(separator)
                # Take the first part that looks like a medical condition
                for part in parts:
                    part = part.strip()
                    # Skip parts that are clearly not medical conditions
                    non_medical_indicators = ["symptoms", "signs", "causes", "treatment", "diagnosis", "medical", "health", "overview", "introduction"]
                    if not any(indicator in part.lower() for indicator in non_medical_indicators):
                        # If part is long enough and doesn't contain non-medical words, use it
                        if len(part) > 3:
                            return part
        
        # Preserve complete medical terms by checking for common medical phrases
        medical_phrases = [
            "asthma and anaphylaxis",
            "asthma and anaphylaxis in the",
            "myocardial infarction",
            "chronic obstructive pulmonary disease",
            "deep vein thrombosis",
            "attention deficit hyperactivity disorder",
            "obsessive compulsive disorder",
            "autism spectrum disorder",
            "inflammatory bowel disease",
            "chronic kidney disease",
            "coronary artery disease",
            "acute respiratory distress syndrome",
            "chronic fatigue syndrome",
            "irritable bowel syndrome",
            "polycystic ovary syndrome",
            "post-traumatic stress disorder",
            "restless leg syndrome",
            "sleep apnea syndrome",
            "sudden infant death syndrome",
            "toxic shock syndrome"
        ]
        
        # If we have a partial match to a known medical phrase, use the full phrase
        condition_lower = condition.lower()
        for phrase in medical_phrases:
            # Check if the condition is a prefix of the phrase
            if phrase.startswith(condition_lower) and len(condition) >= 3:
                return phrase.title()  # Use proper title case
            # Check if the phrase is contained in the title and the condition is a part of it
            elif phrase in title_lower and condition_lower in phrase:
                return phrase.title()  # Use proper title case
        
        # If the condition is too generic or empty, return the original title
        if len(condition) < 3 or condition.lower() in ["symptoms", "signs", "causes", "treatment", "diagnosis", "medical"]:
            # Try to extract from the original title by removing common words
            words = title.split()
            # Filter out common non-medical words
            medical_words = [word for word in words if word.lower() not in [
                "the", "and", "or", "of", "in", "on", "at", "to", "for", "with", "by", 
                "a", "an", "is", "are", "was", "were", "be", "been", "have", "has", "had",
                "do", "does", "did", "will", "would", "could", "should", "may", "might", 
                "must", "can", "this", "that", "these", "those", "i", "you", "he", "she", 
                "it", "we", "they", "me", "him", "her", "us", "them"
            ]]
            if medical_words:
                # Return first few medical words that form a coherent condition name
                if len(medical_words) > 1:
                    # Try to form a proper medical term
                    combined = " ".join(medical_words[:4])  # Limit to first 4 words
                    # Check if it looks like a medical condition
                    if len(combined) > 3 and not any(word in combined.lower() for word in ["symptom", "sign", "cause", "treat", "diagnose", "medical", "health"]):
                        return combined
                return " ".join(medical_words[:7])  # Return first 7 medical words to capture longer terms
            else:
                return title.strip()
        
        return condition
    
    def _calculate_dynamic_match_score(self, symptoms: str, title: str, snippet: str) -> float:
        """Calculate match score for dynamic diagnoses based on symptom relevance."""
        score = 0.0
        symptoms_lower = symptoms.lower()
        title_lower = title.lower()
        snippet_lower = snippet.lower()
        
        # Split symptoms into words for matching
        symptom_words = set(symptoms_lower.split())
        
        # Score based on symptom word matches with higher weights for medical terms
        medical_symptom_indicators = [
            "pain", "fever", "cough", "nausea", "vomiting", "headache", "dizziness", "fatigue", 
            "swelling", "rash", "itching", "shortness", "breath", "chest", "abdominal", "joint", 
            "muscle", "thirst", "urination", "hunger", "weight", "loss", "gain", "sweating",
            "palpitations", "tingling", "numbness", "weakness", "stiffness", "cramping"
        ]
        
        for word in symptom_words:
            if len(word) > 2:  # Only consider words longer than 2 characters
                if word in title_lower:
                    # Higher weight if it's a recognized medical symptom
                    if any(med_symptom in word for med_symptom in medical_symptom_indicators):
                        score += 3.0
                    else:
                        score += 2.0
                if word in snippet_lower:
                    # Higher weight if it's a recognized medical symptom
                    if any(med_symptom in word for med_symptom in medical_symptom_indicators):
                        score += 1.5
                    else:
                        score += 1.0
        
        # Boost score for medical terms in title that indicate a proper diagnosis
        proper_diagnosis_indicators = [
            "diabetes", "pneumonia", "asthma", "hypertension", "myocardial infarction",
            "heart attack", "stroke", "migraine", "arthritis", "bronchitis", "appendicitis",
            "gastritis", "ulcer", "anemia", "thyroid", "depression", "anxiety", "allergy",
            "infection", "fracture", "sprain", "strain", "concussion", "migraine", "epilepsy",
            "seizure", "cirrhosis", "hepatitis", "nephritis", "cystitis", "dermatitis",
            "eczema", "psoriasis", "osteoporosis", "osteopenia", "meningitis", "encephalitis",
            "tuberculosis", "malaria", "dengue", "chickenpox", "measles", "mumps", "rubella",
            "sinusitis", "tonsillitis", "pharyngitis", "laryngitis", "conjunctivitis",
            "otitis", "gastroenteritis", "colitis", "diverticulitis", "hemorrhoids",
            "hernia", "gallstones", "kidney stones", "urinary tract infection",
            "chronic obstructive pulmonary disease", "copd", "emphysema", "bronchiectasis",
            "pulmonary embolism", "deep vein thrombosis", "dvt", "anaphylaxis",
            "food poisoning", "gout", "lupus", "rheumatoid arthritis", "multiple sclerosis",
            "parkinson's disease", "alzheimer's disease", "dementia", "schizophrenia",
            "bipolar disorder", "panic disorder", "obsessive compulsive disorder", "ocd",
            "attention deficit hyperactivity disorder", "adhd", "autism", "autism spectrum disorder"
        ]
        
        diagnosis_matches = 0
        for indicator in proper_diagnosis_indicators:
            if indicator in title_lower:
                score += 5.0  # High boost for proper diagnosis indicators
                diagnosis_matches += 1
            if indicator in snippet_lower:
                score += 2.5
                diagnosis_matches += 1
        
        # Penalize results that seem like guidelines or educational content
        non_diagnosis_indicators = [
            "guideline", "guidance", "protocol", "procedure", "treatment", "therapy",
            "management", "care", "practice", "policy", "standard", "recommendation",
            "algorithm", "approach", "strategy", "framework", "model", "system",
            "program", "initiative", "campaign", "study", "research", "trial",
            "review", "meta-analysis", "analysis", "evaluation", "assessment",
            "investigation", "exploration", "inquiry", "survey", "report",
            "publication", "article", "journal", "book", "manual", "handbook",
            "dictionary", "encyclopedia", "reference", "database", "registry",
            "flashcard", "quiz", "test", "exam", "assessment", "evaluation",
            "diagnostic criteria", "differential diagnosis", "case study",
            "clinical presentation", "medical education", "medical school"
        ]
        
        for indicator in non_diagnosis_indicators:
            if indicator in title_lower or indicator in snippet_lower:
                score -= 3.0  # Penalty for non-diagnosis content
        
        # Boost for multiple symptom matches
        symptom_matches = sum(1 for word in symptom_words if len(word) > 2 and (word in title_lower or word in snippet_lower))
        if symptom_matches > 2:
            score *= 1.5  # 50% boost for multiple matches
        elif symptom_matches > 1:
            score *= 1.2  # 20% boost for multiple matches
        
        # Additional boost if we have both symptom matches and diagnosis indicators
        if symptom_matches > 0 and diagnosis_matches > 0:
            score *= 1.3  # 30% boost for relevance
        
        return max(0.0, score)  # Ensure non-negative score
    
    def _assess_severity(self, title: str, snippet: str) -> str:
        """Assess severity based on title and snippet content."""
        title_lower = title.lower()
        snippet_lower = snippet.lower()
        
        # High severity indicators
        high_indicators = ["emergency", "critical", "severe", "life-threatening", "urgent"]
        for indicator in high_indicators:
            if indicator in title_lower or indicator in snippet_lower:
                return "high"
        
        # Moderate severity indicators
        moderate_indicators = ["moderate", "serious", "significant", "concern"]
        for indicator in moderate_indicators:
            if indicator in title_lower or indicator in snippet_lower:
                return "moderate"
        
        # Low severity indicators
        low_indicators = ["mild", "minor", "benign", "common"]
        for indicator in low_indicators:
            if indicator in title_lower or indicator in snippet_lower:
                return "low"
        
        # Default to moderate
        return "moderate"
    
    def _get_dynamic_recommendations(self, title: str, snippet: str) -> List[str]:
        """Generate dynamic recommendations based on the condition."""
        recommendations = []
        title_lower = title.lower()
        snippet_lower = snippet.lower()
        
        # General recommendations that apply to most conditions
        recommendations.extend([
            "Consult with a healthcare professional for proper evaluation",
            "Monitor symptoms and seek immediate care if they worsen"
        ])
        
        # Condition-specific recommendations based on keywords
        if "diabetes" in title_lower or "diabetes" in snippet_lower:
            recommendations.extend([
                "Check blood glucose levels regularly",
                "Follow a balanced diet with controlled carbohydrate intake"
            ])
        elif "heart" in title_lower or "cardiac" in title_lower:
            recommendations.extend([
                "Avoid strenuous activities until evaluated",
                "Monitor heart rate and blood pressure"
            ])
        elif "pneumonia" in title_lower or "respiratory" in title_lower or "lung" in title_lower:
            recommendations.extend([
                "Rest and stay hydrated",
                "Use a humidifier to ease breathing"
            ])
        elif "anxiety" in title_lower or "panic" in title_lower:
            recommendations.extend([
                "Practice deep breathing exercises",
                "Avoid caffeine and stimulants"
            ])
        
        return recommendations
    
    def _clean_description(self, snippet: str) -> str:
        """Clean and format description to avoid truncation issues."""
        if not snippet:
            return "No additional information available"
        
        # Limit to reasonable length but preserve sentence boundaries
        if len(snippet) > 400:  # Increased limit to reduce truncation
            # Try to find a natural break point
            truncated = snippet[:400]
            # Look for sentence ending punctuation
            last_punctuation = max(truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?'))
            if last_punctuation > 350:  # Only use if it's reasonably close to the end
                return truncated[:last_punctuation + 1].strip()
            else:
                # If no good punctuation break, look for word boundary
                last_space = truncated.rfind(' ')
                if last_space > 350:
                    return truncated[:last_space].strip() + "..."
                else:
                    return truncated.strip() + "..."
        
        return snippet.strip()
    
    def _generate_dynamic_diagnoses_nlm(self, symptoms: str, vitals: dict, age: int, gender: str, medical_history: List[str], symptoms_analysis: dict) -> List[Dict[str, Any]]:
        """Generate and rank possible diagnoses using NLM Conditions API for higher accuracy."""
        diagnoses = []
        
        try:
            # Import the NLM API function
            from ..utils.medical_apis import search_nlm_conditions
            
            # Search using NLM Conditions API
            nlm_result = search_nlm_conditions(symptoms)
            
            # Check if we got a valid response
            if not isinstance(nlm_result, dict) or nlm_result.get("status") != "success":
                logger.info("NLM Conditions API not available, falling back to Serper")
                return []
            
            search_results = nlm_result.get("results", [])
            
            # Process each search result to create a diagnosis
            for result in search_results:
                # Check if result is a dict (from NLM API it should be)
                if isinstance(result, dict):
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    match_score = result.get("match_score", 7.0)  # NLM provides high confidence scores
                else:
                    # Skip non-dict results
                    continue
                
                # Include results with high match scores from NLM
                if match_score > 6.0:  # High threshold for NLM results as they're more accurate
                    # Enhanced description handling to avoid truncation in the middle of sentences
                    clean_description = self._clean_description(snippet)
                    diagnoses.append({
                        "condition": title,  # NLM provides clean condition names, use directly
                        "match_score": round(match_score, 3),
                        "matched_symptoms": [],  # Will be populated by frontend
                        "matched_vitals": [],    # Will be populated by frontend
                        "severity": self._assess_severity(title, snippet),
                        "prevalence": min(0.95, match_score / 10.0),  # NLM results have higher prevalence
                        "recommendations": self._get_dynamic_recommendations(title, snippet),
                        "description": clean_description,
                        "source": "NLM Conditions API",  # Indicate the source for transparency
                        "link": result.get("link", "")  # Include the search result link if available
                    })
            
            # Sort by match score
            diagnoses = sorted(diagnoses, key=lambda x: x["match_score"], reverse=True)
            
        except Exception as e:
            logger.error(f"Error in NLM diagnosis generation: {e}")
            return []
        
        return diagnoses[:4]  # Return top 4 diagnoses
    
    def _generate_enhanced_diagnoses(self, symptoms: str, vitals: dict, age: int, gender: str, medical_history: List[str], symptoms_analysis: dict) -> List[Dict[str, Any]]:
        """Generate enhanced diagnoses by combining multiple data sources."""
        # Try NLM Conditions API first (highest accuracy)
        nlm_diagnoses = self._generate_dynamic_diagnoses_nlm(symptoms, vitals, age, gender, medical_history, symptoms_analysis)
        
        # If we have NLM diagnoses, use them (lower the threshold to prevent fallback)
        if nlm_diagnoses and len(nlm_diagnoses) > 0:
            logger.info(f"Using NLM diagnoses with {len(nlm_diagnoses)} results")
            return nlm_diagnoses[:4]
        
        # Fall back to Serper API
        serper_diagnoses = self._generate_dynamic_diagnoses_serper(symptoms, vitals, age, gender, medical_history, symptoms_analysis)
        
        # If we have Serper diagnoses, use them (lower the threshold to prevent fallback)
        if serper_diagnoses and len(serper_diagnoses) > 0:
            logger.info(f"Using Serper diagnoses with {len(serper_diagnoses)} results")
            return serper_diagnoses[:4]
        
        # Finally fall back to hardcoded conditions
        logger.info("Falling back to hardcoded conditions")
        return self._generate_diagnoses(symptoms, vitals, age, gender, medical_history, symptoms_analysis)
