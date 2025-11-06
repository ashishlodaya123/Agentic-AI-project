import logging
from typing import Dict, List, Any
from datetime import datetime

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
            
            # Generate differential diagnosis
            diagnosis_list = self._generate_diagnoses(combined_symptoms, vitals, age, gender, medical_history, symptoms_analysis)
            
            # Rank diagnoses based on match score
            ranked_diagnoses = sorted(diagnosis_list, key=lambda x: x["match_score"], reverse=True)
            
            # Limit to top 4 most relevant diagnoses
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
            
            logger.info(f"Generated {len(ranked_diagnoses)} differential diagnoses")
            return result
            
        except Exception as e:
            logger.error(f"Error in differential diagnosis generation: {e}")
            return {
                "differential_diagnosis": [],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
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
            if not (age_min <= age <= age_max):
                # Skip conditions not appropriate for patient's age
                continue
            
            # Check symptom matches - enhanced processing
            condition_symptoms = condition_data["symptoms"]
            
            # Method 1: Direct symptom matching from chief complaint with enhanced weighting
            symptom_words = set(symptoms.split())
            for symptom in condition_symptoms:
                # Exact match gets highest weight
                if symptom in symptoms:
                    match_score += 3.0
                    matched_symptoms.append(symptom)
                # Partial word match gets moderate weight
                elif any(word in symptom or symptom in word for word in symptom_words):
                    match_score += 1.5
                    matched_symptoms.append(symptom)
            
            # Method 2: Check symptoms from analysis if available
            if symptoms_analysis:
                # Check categorized symptoms with weighted matching
                categories = symptoms_analysis.get("symptom_categories", {})
                for category, category_symptoms in categories.items():
                    for symptom_dict in category_symptoms:
                        # Handle both string and dict formats
                        if isinstance(symptom_dict, str):
                            symptom_name = symptom_dict.lower()
                        else:
                            symptom_name = symptom_dict.get("name", "").lower()
                        
                        # Check if this symptom matches any condition symptom
                        for condition_symptom in condition_symptoms:
                            # Exact match
                            if condition_symptom == symptom_name:
                                if condition_symptom not in matched_symptoms:
                                    match_score += 2.5
                                    matched_symptoms.append(condition_symptom)
                            # Strong fuzzy match
                            elif self._fuzzy_match(condition_symptom, symptom_name):
                                if condition_symptom not in matched_symptoms:
                                    match_score += 2.0
                                    matched_symptoms.append(condition_symptom)
                            # Partial match
                            elif (condition_symptom in symptom_name or 
                                  symptom_name in condition_symptom):
                                if condition_symptom not in matched_symptoms:
                                    match_score += 1.0
                                    matched_symptoms.append(condition_symptom)
                
                # Check primary concerns with highest weight
                primary_concerns = symptoms_analysis.get("primary_concerns", [])
                for concern in primary_concerns:
                    concern_name = concern.get("name", concern.get("condition", "")).lower()
                    concern_significance = concern.get("significance", "").lower()
                    
                    # Check against condition symptoms
                    for condition_symptom in condition_symptoms:
                        # Exact match
                        if (condition_symptom == concern_name or 
                            condition_symptom == concern_significance):
                            if condition_symptom not in matched_symptoms:
                                match_score += 3.0
                                matched_symptoms.append(condition_symptom)
                        # Strong fuzzy match
                        elif (self._fuzzy_match(condition_symptom, concern_name) or
                              self._fuzzy_match(condition_symptom, concern_significance)):
                            if condition_symptom not in matched_symptoms:
                                match_score += 2.5
                                matched_symptoms.append(condition_symptom)
                        # Partial match
                        elif (condition_symptom in concern_name or 
                              condition_symptom in concern_significance or
                              concern_name in condition_symptom or
                              concern_significance in condition_symptom):
                            if condition_symptom not in matched_symptoms:
                                match_score += 1.5
                                matched_symptoms.append(condition_symptom)
                
                # Check detailed analysis for more symptoms
                detailed_analysis = symptoms_analysis.get("detailed_analysis", {})
                symptom_analysis = detailed_analysis.get("symptom_analysis", {})
                by_system = symptom_analysis.get("by_system", {})
                
                for system, system_symptoms in by_system.items():
                    for symptom in system_symptoms:
                        # Check if this symptom matches any condition symptom
                        for condition_symptom in condition_symptoms:
                            # Exact match
                            if condition_symptom.lower() == symptom.lower():
                                if condition_symptom not in matched_symptoms:
                                    match_score += 2.0
                                    matched_symptoms.append(condition_symptom)
                            # Strong fuzzy match
                            elif self._fuzzy_match(condition_symptom, symptom.lower()):
                                if condition_symptom not in matched_symptoms:
                                    match_score += 1.8
                                    matched_symptoms.append(condition_symptom)
                            # Partial match
                            elif (condition_symptom in symptom.lower() or 
                                  symptom.lower() in condition_symptom):
                                if condition_symptom not in matched_symptoms:
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
                    "severity": condition_data["severity"],
                    "prevalence": condition_data["prevalence"],
                    "recommendations": self._get_recommendations(condition_key)
                })
        
        return diagnoses
    
    def _check_vital_indicator(self, indicator: str, vitals: dict) -> bool:
        """Check if a vital sign indicator is present with enhanced accuracy."""
        if indicator == "fever":
            temp = vitals.get("temperature")
            if temp:
                try:
                    # Handle different temperature formats
                    if isinstance(temp, str):
                        temp = temp.replace("°C", "").replace("°F", "").strip()
                        temp_value = float(temp)
                        # Convert Fahrenheit to Celsius if needed
                        if temp_value > 100:  # Likely Fahrenheit
                            temp_value = (temp_value - 32) * 5/9
                    else:
                        temp_value = float(temp)
                    return temp_value > 38.0
                except (ValueError, TypeError):
                    return False
        elif indicator == "high_blood_pressure":
            bp = vitals.get("blood_pressure")
            if bp:
                try:
                    # Handle different BP formats
                    if isinstance(bp, str):
                        # Extract systolic value from formats like "120/80" or "120 mmHg"
                        systolic_str = bp.split("/")[0].split()[0]
                        systolic = int(systolic_str)
                    else:
                        systolic = int(bp)
                    return systolic > 140
                except (ValueError, IndexError, TypeError):
                    return False
        elif indicator == "rapid_heart_rate":
            hr = vitals.get("heart_rate")
            if hr:
                try:
                    # Handle different heart rate formats
                    if isinstance(hr, str):
                        hr = hr.replace("bpm", "").strip()
                    return int(hr) > 100
                except (ValueError, TypeError):
                    return False
        elif indicator == "rapid_breathing":
            rr = vitals.get("respiratory_rate")
            if rr:
                try:
                    # Handle different respiratory rate formats
                    if isinstance(rr, str):
                        rr = rr.replace("breaths/min", "").strip()
                    return int(rr) > 20
                except (ValueError, TypeError):
                    return False
        elif indicator == "low_oxygen":
            oxygen = vitals.get("oxygen_saturation")
            if oxygen:
                try:
                    # Handle different oxygen saturation formats
                    if isinstance(oxygen, str):
                        oxygen = oxygen.replace("%", "").replace("sat", "").strip()
                    return float(oxygen) < 95
                except (ValueError, TypeError):
                    return False
        
        return False
    
    def _adjust_for_demographics(self, score: float, condition_key: str, age: int, gender: str) -> float:
        """Adjust match score based on patient demographics."""
        adjusted_score = score
        
        # Age-related adjustments with more nuanced logic
        if age > 65:
            # Higher risk for cardiovascular conditions
            if condition_key in ["myocardial_infarction", "hypertensive_crisis", "pericarditis"]:
                adjusted_score += 0.7
            # Lower risk for certain conditions
            elif condition_key in ["pneumothorax", "anxiety_panic_attack"]:
                adjusted_score -= 0.3
        elif age < 18:
            # Lower risk for certain adult conditions
            if condition_key in ["hypertensive_crisis", "myocardial_infarction"]:
                adjusted_score -= 0.8
            # Higher risk for pediatric conditions
            elif condition_key in ["bronchitis", "asthma_exacerbation"]:
                adjusted_score += 0.5
        elif 30 <= age <= 50:
            # Higher risk for certain conditions in this age group
            if condition_key in ["anxiety_panic_attack", "gastroesophageal_reflux"]:
                adjusted_score += 0.4
        elif 18 <= age <= 30:
            # Higher risk for certain conditions
            if condition_key in ["pneumothorax"]:
                adjusted_score += 0.6
                
        # Gender-related adjustments
        if gender.lower() == "male":
            if condition_key == "myocardial_infarction":
                adjusted_score += 0.5
            elif condition_key == "anxiety_panic_attack":
                adjusted_score -= 0.2
        elif gender.lower() == "female":
            if condition_key == "anxiety_panic_attack":
                adjusted_score += 0.4
            elif condition_key == "myocardial_infarction":
                adjusted_score -= 0.3
                
        return adjusted_score
    
    def _adjust_for_medical_history(self, score: float, condition_key: str, medical_history: List[str]) -> float:
        """Adjust match score based on medical history."""
        adjusted_score = score
        
        for history_item in medical_history:
            history_lower = history_item.lower()
            
            if "hypertension" in history_lower and condition_key == "hypertensive_crisis":
                adjusted_score += 0.6
            elif "asthma" in history_lower and condition_key == "asthma_exacerbation":
                adjusted_score += 0.7
            elif "heart" in history_lower and condition_key == "myocardial_infarction":
                adjusted_score += 0.5
            elif "blood clot" in history_lower and condition_key == "pulmonary_embolism":
                adjusted_score += 0.6
            elif "copd" in history_lower and condition_key in ["pneumonia", "pulmonary_embolism"]:
                adjusted_score += 0.4
            elif "diabetes" in history_lower:
                # Diabetics are at higher risk for various complications
                adjusted_score += 0.2
                
        return adjusted_score
    
    def _fuzzy_match(self, term1: str, term2: str) -> bool:
        """Perform an enhanced fuzzy match between two terms."""
        # Convert to lowercase for case-insensitive comparison
        term1, term2 = term1.lower(), term2.lower()
        
        # Direct match
        if term1 == term2:
            return True
            
        # Partial match (one term contained in another)
        if term1 in term2 or term2 in term1:
            return True
            
        # Split into words for more detailed comparison
        words1 = set(term1.split())
        words2 = set(term2.split())
        
        if words1 and words2:
            # Check for exact word matches
            common_words = words1.intersection(words2)
            if len(common_words) > 0:
                # If they share more than 50% of words
                min_words = min(len(words1), len(words2))
                if len(common_words) >= max(1, min_words // 2):
                    return True
            
            # Check for similar words (partial matches within words)
            for word1 in words1:
                for word2 in words2:
                    if word1 in word2 or word2 in word1:
                        return True
                        
        # Special case for medical terms - check common medical term variations
        medical_variations = {
            "heart": ["cardiac", "cardio"],
            "lung": ["pulmonary", "respiratory"],
            "brain": ["neurological", "cerebral"],
            "stomach": ["gastric", "abdominal"],
            "chest": ["thoracic"],
            "blood": ["vascular", "circulatory"],
            "bone": ["skeletal", "orthopedic"],
            "kidney": ["renal"],
            "liver": ["hepatic"],
            "skin": ["dermatological"]
        }
        
        # Check for medical term variations
        for word1 in words1:
            if word1 in medical_variations:
                variations = medical_variations[word1]
                for variation in variations:
                    for word2 in words2:
                        if variation == word2 or variation in word2 or word2 in variation:
                            return True
            
        for word2 in words2:
            if word2 in medical_variations:
                variations = medical_variations[word2]
                for variation in variations:
                    for word1 in words1:
                        if variation == word1 or variation in word1 or word1 in variation:
                            return True
        
        return False
    
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