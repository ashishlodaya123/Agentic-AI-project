import re

class SymptomsVitalsAgent:
    """
    Agent to process and analyze patient symptoms and vital signs using rule-based logic.
    Enhanced to better prioritize and categorize symptoms.
    """
    def __init__(self):
        # Common symptom categories for better organization
        self.symptom_categories = {
            "cardiovascular": ["chest pain", "heart palpitations", "rapid heart rate", "slow heart rate", 
                             "heart murmur", "irregular heartbeat", "high blood pressure", "low blood pressure"],
            "respiratory": ["shortness of breath", "difficulty breathing", "wheezing", "cough", "sputum", 
                          "chest tightness", "rapid breathing"],
            "neurological": ["headache", "dizziness", "fainting", "seizure", "numbness", "tingling", 
                           "confusion", "memory loss", "slurred speech"],
            "gastrointestinal": ["nausea", "vomiting", "diarrhea", "constipation", "abdominal pain", 
                               "bloating", "loss of appetite", "heartburn"],
            "musculoskeletal": ["joint pain", "muscle pain", "back pain", "stiffness", "swelling", 
                              "weakness", "cramps"],
            "constitutional": ["fever", "chills", "fatigue", "weight loss", "weight gain", 
                             "night sweats", "malaise"],
            "dermatological": ["rash", "itching", "redness", "swelling", "lesions", 
                             "dry skin", "excessive sweating"],
            "endocrine": ["excessive thirst", "frequent urination", "heat intolerance", "cold intolerance", 
                        "excessive hunger", "hair loss"],
            "genitourinary": ["painful urination", "frequent urination", "blood in urine", 
                            "lower back pain", "pelvic pain"],
            "psychiatric": ["anxiety", "depression", "insomnia", "mood swings", "panic attacks", 
                          "hallucinations", "delusions"]
        }

    def run(self, patient_data: dict) -> dict:
        """
        Analyzes symptoms and vitals to produce a structured summary.
        """
        symptoms = patient_data.get("symptoms", "")
        vitals = patient_data.get("vitals", {})
        age = patient_data.get("age", 0)
        gender = patient_data.get("gender", "")

        # Enhanced analysis with better symptom categorization
        analysis = self._analyze_patient_data(symptoms, vitals, age, gender)
        return analysis

    def _analyze_patient_data(self, symptoms: str, vitals: dict, age: int, gender: str) -> dict:
        """Perform an enhanced analysis of patient data with better symptom processing."""
        # Parse vitals
        vitals_dict = vitals
        
        # Generate analysis based on rules
        concerns = []
        primary_concerns = []
        
        # Check for high heart rate
        if "heart_rate" in vitals_dict:
            try:
                heart_rate = int(vitals_dict["heart_rate"])
                if heart_rate > 100:
                    concerns.append("elevated heart rate")
                    primary_concerns.append({
                        "name": "elevated heart rate",
                        "type": "vital_sign",
                        "value": heart_rate,
                        "normal_range": "60-100 bpm",
                        "severity": "moderate" if heart_rate <= 130 else "high"
                    })
            except (ValueError, TypeError):
                pass  # Invalid heart rate value
        
        # Check for fever
        if "temperature" in vitals_dict:
            try:
                temperature = float(vitals_dict["temperature"])
                if temperature > 38.0:
                    concerns.append("fever")
                    primary_concerns.append({
                        "name": "fever",
                        "type": "vital_sign",
                        "value": temperature,
                        "normal_range": "36.1-37.2°C",
                        "severity": "moderate" if temperature <= 39.0 else "high"
                    })
            except (ValueError, TypeError):
                pass  # Invalid temperature value
        
        # Enhanced symptom categorization
        categorized_symptoms = self._categorize_symptoms(symptoms)
        
        # Extract critical symptoms with higher priority
        critical_symptoms = ["chest pain", "shortness of breath", "severe headache", "difficulty breathing", 
                           "loss of consciousness", "severe abdominal pain", "high fever"]
        found_symptoms = [symptom for symptom in critical_symptoms if symptom in symptoms.lower()]
        
        # Add critical symptoms to primary concerns
        for symptom in found_symptoms:
            primary_concerns.append({
                "name": symptom,
                "type": "symptom",
                "severity": "high"
            })
        
        # Add categorized symptoms to concerns
        all_symptoms = []
        for category, symptom_list in categorized_symptoms.items():
            all_symptoms.extend(symptom_list)
            for symptom in symptom_list:
                if symptom not in [pc["name"] for pc in primary_concerns]:
                    primary_concerns.append({
                        "name": symptom,
                        "type": "symptom",
                        "category": category,
                        "severity": "moderate"
                    })
        
        # Generate summary with emphasis on symptoms
        if primary_concerns:
            symptom_concerns = [c for c in primary_concerns if c["type"] == "symptom"]
            vital_concerns = [c for c in primary_concerns if c["type"] == "vital_sign"]
            
            summary_parts = []
            if symptom_concerns:
                symptom_names = [c["name"] for c in symptom_concerns]
                summary_parts.append(f"symptoms: {', '.join(symptom_names)}")
            if vital_concerns:
                vital_names = [f"{c['name']} ({c['value']})" for c in vital_concerns]
                summary_parts.append(f"vital signs: {', '.join(vital_names)}")
            
            summary = f"Patient presents with {', and '.join(summary_parts)}."
            
            if any(c["severity"] == "high" for c in primary_concerns):
                summary += " This suggests a potentially serious condition requiring immediate attention."
            else:
                summary += " Further evaluation is recommended."
        else:
            summary = "The patient's symptoms and vitals do not indicate any immediately life-threatening conditions, but a thorough examination is recommended."

        return {
            "summary": summary,
            "primary_concerns": primary_concerns,
            "symptom_categories": categorized_symptoms,
            "vital_signs": self._process_vitals(vitals_dict),
            "demographics": {
                "age": age,
                "gender": gender
            },
            "detailed_analysis": {
                "symptom_analysis": {
                    "by_system": categorized_symptoms,
                    "severity_assessment": "High" if any(c["severity"] == "high" for c in primary_concerns) else "Moderate"
                },
                "vital_signs_analysis": self._analyze_vitals(vitals_dict)
            }
        }

    def _categorize_symptoms(self, symptoms: str) -> dict:
        """Categorize symptoms by body system."""
        categorized = {category: [] for category in self.symptom_categories.keys()}
        
        symptoms_lower = symptoms.lower()
        
        # Check each category for matching symptoms
        for category, category_symptoms in self.symptom_categories.items():
            for symptom in category_symptoms:
                if symptom in symptoms_lower:
                    categorized[category].append(symptom)
        
        # Remove empty categories
        categorized = {k: v for k, v in categorized.items() if v}
        
        return categorized

    def _process_vitals(self, vitals: dict) -> dict:
        """Process vital signs into structured format."""
        processed = {}
        
        # Heart rate
        if "heart_rate" in vitals:
            try:
                hr = int(vitals["heart_rate"])
                status = "normal" if 60 <= hr <= 100 else "abnormal"
                processed["heart_rate"] = {
                    "value": hr,
                    "unit": "bpm",
                    "normal_range": "60-100 bpm",
                    "interpretation": "Normal heart rate" if status == "normal" else "Abnormal heart rate",
                    "status": status
                }
            except (ValueError, TypeError):
                pass
        
        # Temperature
        if "temperature" in vitals:
            try:
                temp = float(vitals["temperature"])
                status = "normal" if 36.1 <= temp <= 37.2 else "abnormal"
                processed["temperature"] = {
                    "value": temp,
                    "unit": "°C",
                    "normal_range": "36.1-37.2 °C",
                    "interpretation": "Normal temperature" if status == "normal" else "Fever" if temp > 37.2 else "Hypothermia",
                    "status": status
                }
            except (ValueError, TypeError):
                pass
        
        # Blood pressure
        if "blood_pressure" in vitals:
            bp = vitals["blood_pressure"]
            if isinstance(bp, str):
                # Parse systolic/diastolic
                parts = bp.split("/")
                if len(parts) == 2:
                    try:
                        systolic = int(parts[0])
                        diastolic = int(parts[1])
                        # Simplified classification
                        if systolic >= 140 or diastolic >= 90:
                            bp_status = "hypertension"
                        elif systolic >= 120 or diastolic >= 80:
                            bp_status = "prehypertension"
                        else:
                            bp_status = "normal"
                        
                        processed["blood_pressure"] = {
                            "value": bp,
                            "systolic": systolic,
                            "diastolic": diastolic,
                            "unit": "mmHg",
                            "normal_range": "90/60-120/80 mmHg",
                            "interpretation": bp_status.capitalize(),
                            "status": "normal" if bp_status == "normal" else "abnormal"
                        }
                    except (ValueError, IndexError):
                        pass
        
        return processed

    def _analyze_vitals(self, vitals: dict) -> dict:
        """Analyze vital signs for clinical significance."""
        findings = []
        normal_values = []
        
        # Heart rate analysis
        if "heart_rate" in vitals:
            try:
                hr = int(vitals["heart_rate"])
                if hr > 100:
                    findings.append(f"Tachycardia: Heart rate {hr} bpm (normal: 60-100 bpm)")
                elif hr < 60:
                    findings.append(f"Bradycardia: Heart rate {hr} bpm (normal: 60-100 bpm)")
                else:
                    normal_values.append(f"Heart rate: {hr} bpm (normal)")
            except (ValueError, TypeError):
                pass
        
        # Temperature analysis
        if "temperature" in vitals:
            try:
                temp = float(vitals["temperature"])
                if temp > 38.0:
                    findings.append(f"Fever: Temperature {temp}°C (normal: 36.1-37.2°C)")
                elif temp < 36.1:
                    findings.append(f"Hypothermia: Temperature {temp}°C (normal: 36.1-37.2°C)")
                else:
                    normal_values.append(f"Temperature: {temp}°C (normal)")
            except (ValueError, TypeError):
                pass
        
        return {
            "findings": findings,
            "normal_values": normal_values
        }