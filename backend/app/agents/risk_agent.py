import pickle
import os

class RiskStratificationAgent:
    """
    Agent to predict patient risk using a pre-trained model.
    """
    def __init__(self, model_path="app/models/risk_model.pkl"):
        # Load the pre-trained logistic regression model
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def run(self, patient_data: dict) -> float:
        """
        Predicts the risk score based on patient data.
        """
        # This is a dummy feature extraction.
        # In a real scenario, you would extract meaningful features from the patient data.
        age = patient_data.get("age", 50)
        hr = patient_data.get("vitals", {}).get("heart_rate", 80)

        features = [[age / 10, hr / 10]]

        # Predict the probability of the positive class (risk)
        risk_score = self.model.predict_proba(features)[0][1]

        return risk_score
