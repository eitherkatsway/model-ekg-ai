# AI-Driven ECG Triage System

An intelligent clinical decision support system designed to assist medical professionals in prioritizing ECG readings. This system utilizes an XGBoost model to classify cardiac anomalies and incorporates Explainable AI (SHAP) to provide diagnostic transparency.

## Clinical Value
- **Intelligent Triage:** Classifies ECG data into *Normal*, *Caution*, and *Critical* based on data-driven thresholds (K-Means Clustering).
- **Explainable AI:** Uses SHAP to provide local feature importance, allowing clinicians to validate AI reasoning against clinical guidelines.
- **System Guardrails:**
  - **Input Validation:** Restricts input data to physiological ranges to prevent processing of sensor artifacts.
  - **Logical Clipping:** Applies medical constraints (e.g., RR-interval limits) to ensure model inputs are medically sound.
  - **Transparency Layer:** Prevents "black-box" decision-making by making the system to output feature-level justifications for every triage result.

## Data Source
This project utilizes the **MIMIC-IV Clinical Database**. All data processing is performed in compliance with clinical privacy standards, and the system is designed to handle de-identified data in secure hospital environments.

## Architecture
1. **Feature Engineering:** Derived clinical metrics (P-duration, QRS-duration) from raw ECG signals.
2. **Predictive Engine:** XGBoost Classifier (0.83 Recall).
3. **Thresholding:** K-Means driven triage boundaries (24.73% & 67.71%).
4. **Dashboard:** Real-time assessment via Streamlit.

## How to Run

### Option 1: Live Demo (Recommended)
Access the application directly via Streamlit Cloud: 
https://model-ai-electrocardiogram-anomalityprediction.streamlit.app/

### Option 2: Run Locally
If you wish to run the system on your local machine, follow these steps:
1. **Clone this repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Launch the application**: `streamlit run app.py`

## Ethical Statement
This system functions strictly as a **Decision Support System (DSS)**. It is intended to assist, not replace, clinical judgment. The final authority in patient diagnosis remains exclusively with the healthcare professional.
