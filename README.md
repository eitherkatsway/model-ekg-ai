# AI-Driven ECG Triage System

An intelligent clinical decision support system designed to assist medical professionals in prioritizing ECG readings. This system utilizes an XGBoost model to classify cardiac anomalies and incorporates Explainable AI (SHAP) to provide diagnostic transparency.

## Key Features
- **Intelligent Triage:** Classifies ECG data into *Normal*, *Caution*, and *Critical* based on data-driven thresholds (K-Means Clustering).
- **Explainable AI:** Uses SHAP to provide local feature importance, allowing clinicians to validate AI reasoning.
- **Guardrails:** Integrated input validation and physiological constraints to ensure reliable and medically sound inferences.
- **Web Interface:** Deployed using Streamlit for real-time clinical assessment.

## Architecture
1. **Feature Engineering:** Derived clinical metrics (P-duration, QRS-duration) from raw ECG time-series.
2. **Model:** XGBoost Classifier (0.83 Recall).
3. **Thresholding:** K-Means driven triage boundaries (24.73% & 67.71%).
4. **Explanation:** SHAP TreeExplainer.

## How to Run
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`

## Ethical Considerations
This system acts as a **Decision Support System**. All clinical decisions remain the responsibility of the medical professional.
