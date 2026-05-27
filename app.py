import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Triage Jantung EKG", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load('model_ecg_angka.pkl')

model = load_model()

st.title("Sistem Deteksi Anomali EKG Real-Time")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Interval Waktu (ms)")
    rr_interval = st.slider("RR Interval", min_value=300, max_value=2000, value=800, step=10)
    qrs_duration = st.slider("QRS Duration", min_value=40, max_value=200, value=90, step=1)
    p_duration = st.slider("P Duration", min_value=20, max_value=150, value=80, step=1)

with col2:
    st.subheader("Aksis Kelistrikan (°)")
    p_axis = st.slider("P Axis", min_value=-180, max_value=180, value=60, step=1)
    qrs_axis = st.slider("QRS Axis", min_value=-180, max_value=180, value=60, step=1)
    t_axis = st.slider("T Axis", min_value=-180, max_value=180, value=45, step=1)

input_data = pd.DataFrame({
    'rr_interval': [rr_interval],
    'qrs_duration': [qrs_duration],
    'p_duration': [p_duration],
    'p_axis': [p_axis],
    'qrs_axis': [qrs_axis],
    't_axis': [t_axis]
})

probabilitas = model.predict_proba(input_data)[0]
persen_bahaya = probabilitas[1] * 100

with col3:
    st.subheader("Hasil Analisis")
    st.metric("Probabilitas Kritis", f"{persen_bahaya:.2f}%")

    if persen_bahaya > 75:
        st.error("PRIORITAS 1 (KRITIS)")
    elif persen_bahaya > 40:
        st.warning("PRIORITAS 2 (WASPADA)")
    else:
        st.success("PRIORITAS 3 (AMAN)")
