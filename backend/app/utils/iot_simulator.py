import random
import time
from typing import Dict, Any
import json
import os
from datetime import datetime

class IoTSimulator:
    """
    Simulates IoT medical device data for patient monitoring.
    This class generates realistic vital signs data that mimics
    what would be received from medical IoT devices.
    """
    
    def __init__(self):
        # Normal ranges for vital signs
        self.normal_ranges = {
            "heart_rate": {"min": 60, "max": 100, "unit": "bpm"},
            "blood_pressure_systolic": {"min": 90, "max": 120, "unit": "mmHg"},
            "blood_pressure_diastolic": {"min": 60, "max": 80, "unit": "mmHg"},
            "temperature": {"min": 36.1, "max": 37.2, "unit": "°C"},
            "oxygen_saturation": {"min": 95, "max": 100, "unit": "%"},
            "respiratory_rate": {"min": 12, "max": 20, "unit": "breaths/min"}
        }
        
        # Abnormal ranges for simulation of critical conditions
        self.abnormal_ranges = {
            "heart_rate": {"min": 40, "max": 140, "unit": "bpm"},
            "blood_pressure_systolic": {"min": 70, "max": 200, "unit": "mmHg"},
            "blood_pressure_diastolic": {"min": 40, "max": 120, "unit": "mmHg"},
            "temperature": {"min": 34.0, "max": 42.0, "unit": "°C"},
            "oxygen_saturation": {"min": 80, "max": 100, "unit": "%"},
            "respiratory_rate": {"min": 8, "max": 40, "unit": "breaths/min"}
        }
    
    def generate_normal_vitals(self) -> Dict[str, Any]:
        """Generate normal vital signs data."""
        vitals = {
            "heart_rate": str(random.randint(
                self.normal_ranges["heart_rate"]["min"],
                self.normal_ranges["heart_rate"]["max"]
            )),
            "blood_pressure": f"{random.randint(self.normal_ranges['blood_pressure_systolic']['min'], self.normal_ranges['blood_pressure_systolic']['max'])}/{random.randint(self.normal_ranges['blood_pressure_diastolic']['min'], self.normal_ranges['blood_pressure_diastolic']['max'])}",
            "temperature": str(round(random.uniform(
                self.normal_ranges["temperature"]["min"],
                self.normal_ranges["temperature"]["max"]
            ), 1)),
            "oxygen_saturation": str(random.randint(
                self.normal_ranges["oxygen_saturation"]["min"],
                self.normal_ranges["oxygen_saturation"]["max"]
            )),
            "respiratory_rate": str(random.randint(
                self.normal_ranges["respiratory_rate"]["min"],
                self.normal_ranges["respiratory_rate"]["max"]
            )),
            "timestamp": datetime.now().isoformat()
        }
        return vitals
    
    def generate_abnormal_vitals(self, condition: str = "moderate") -> Dict[str, Any]:
        """Generate abnormal vital signs data based on condition severity."""
        severity_multiplier = 1.0
        if condition == "severe":
            severity_multiplier = 1.5
        elif condition == "critical":
            severity_multiplier = 2.0
        
        vitals = {
            "heart_rate": str(random.randint(
                int(self.abnormal_ranges["heart_rate"]["min"] * (1 if severity_multiplier <= 1 else 0.7)),
                int(self.abnormal_ranges["heart_rate"]["max"] * severity_multiplier)
            )),
            "blood_pressure": f"{random.randint(int(self.abnormal_ranges['blood_pressure_systolic']['min'] * (1 if severity_multiplier <= 1 else 0.8)), int(self.abnormal_ranges['blood_pressure_systolic']['max'] * severity_multiplier))}/{random.randint(int(self.abnormal_ranges['blood_pressure_diastolic']['min'] * (1 if severity_multiplier <= 1 else 0.8)), int(self.abnormal_ranges['blood_pressure_diastolic']['max'] * severity_multiplier))}",
            "temperature": str(round(random.uniform(
                self.abnormal_ranges["temperature"]["min"] * (1 if severity_multiplier <= 1 else 0.95),
                self.abnormal_ranges["temperature"]["max"] * (1.05 if severity_multiplier <= 1 else severity_multiplier)
            ), 1)),
            "oxygen_saturation": str(random.randint(
                int(self.abnormal_ranges["oxygen_saturation"]["min"] * (1 if severity_multiplier <= 1 else 0.8)),
                self.abnormal_ranges["oxygen_saturation"]["max"]
            )),
            "respiratory_rate": str(random.randint(
                int(self.abnormal_ranges["respiratory_rate"]["min"] * (1 if severity_multiplier <= 1 else 0.7)),
                int(self.abnormal_ranges["respiratory_rate"]["max"] * severity_multiplier)
            )),
            "timestamp": datetime.now().isoformat()
        }
        return vitals
    
    def generate_vitals_for_condition(self, medical_condition: str) -> Dict[str, Any]:
        """Generate vital signs that are typical for specific medical conditions."""
        condition_map = {
            "chest_pain": {"heart_rate": (90, 130), "blood_pressure": "140/90-180/110", "oxygen_saturation": (90, 100)},
            "shortness_of_breath": {"respiratory_rate": (20, 40), "oxygen_saturation": (85, 95), "heart_rate": (90, 120)},
            "fever": {"temperature": (38.0, 40.0), "heart_rate": (80, 110)},
            "hypotension": {"blood_pressure": "80/50-90/60", "heart_rate": (100, 130)},
            "hypertension": {"blood_pressure": "140/90-200/120", "heart_rate": (70, 100)},
            "hypoxia": {"oxygen_saturation": (80, 90), "respiratory_rate": (20, 35)}
        }
        
        vitals = self.generate_normal_vitals()
        
        if medical_condition in condition_map:
            condition_data = condition_map[medical_condition]
            for key, value in condition_data.items():
                if key == "heart_rate" and isinstance(value, tuple):
                    vitals["heart_rate"] = str(random.randint(value[0], value[1]))
                elif key == "blood_pressure" and isinstance(value, str):
                    # For simplicity, we'll generate a random BP within the range
                    systolic = random.randint(120, 180)
                    diastolic = random.randint(70, 110)
                    vitals["blood_pressure"] = f"{systolic}/{diastolic}"
                elif key == "temperature" and isinstance(value, tuple):
                    vitals["temperature"] = str(round(random.uniform(value[0], value[1]), 1))
                elif key == "oxygen_saturation" and isinstance(value, tuple):
                    vitals["oxygen_saturation"] = str(random.randint(value[0], value[1]))
                elif key == "respiratory_rate" and isinstance(value, tuple):
                    vitals["respiratory_rate"] = str(random.randint(value[0], value[1]))
        
        vitals["timestamp"] = datetime.now().isoformat()
        return vitals
    
    def stream_vitals_data(self, duration_seconds: int = 60, interval_seconds: int = 5) -> list:
        """
        Simulate streaming vital signs data over time.
        Returns a list of vital signs readings over the specified duration.
        """
        readings = []
        num_readings = duration_seconds // interval_seconds
        
        for i in range(min(num_readings, 10)):  # Limit to 10 readings max for performance
            # Most readings are normal, occasional abnormal readings
            if random.random() < 0.85:  # 85% chance of normal reading
                vitals = self.generate_normal_vitals()
            else:  # 15% chance of abnormal reading
                condition = random.choice(["moderate", "severe", "critical"])
                vitals = self.generate_abnormal_vitals(condition)
            
            readings.append(vitals)
            # Remove the sleep for better performance in API calls
        
        return readings

# Global instance for easy access
iot_simulator = IoTSimulator()

def get_iot_vitals_data(condition: str | None = None) -> Dict[str, Any]:
    """
    Get simulated IoT vital signs data.
    
    Args:
        condition: Optional medical condition to simulate specific vital signs
        
    Returns:
        Dictionary containing vital signs data
    """
    if condition:
        return iot_simulator.generate_vitals_for_condition(condition)
    else:
        # 80% chance of normal vitals, 20% chance of abnormal
        if random.random() < 0.8:
            return iot_simulator.generate_normal_vitals()
        else:
            severity = random.choice(["moderate", "severe", "critical"])
            return iot_simulator.generate_abnormal_vitals(severity)

def stream_iot_vitals_data(duration_seconds: int = 60) -> list:
    """
    Stream simulated IoT vital signs data over time.
    
    Args:
        duration_seconds: How long to stream data (in seconds)
        
    Returns:
        List of vital signs readings
    """
    return iot_simulator.stream_vitals_data(duration_seconds)