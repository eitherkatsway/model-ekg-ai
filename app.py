import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Triage Jantung EKG", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load('model_ecg_angka.pkl')

model = load_model()

def sync_rr(): st.session_state.rr_num = st.session_state.rr_sld
def sync_rr_num(): st.session_state.rr_sld = st.session_state.rr_num
def sync_po(): st.session_state.po_num = st.session_state.po_sld
def sync_po_num(): st.session_state.po_sld = st.session_state.po_num
def sync_pe(): st.session_state.pe_num = st.session_state.pe_sld
def sync_pe_num(): st.session_state.pe_sld = st.session_state.pe_num
def sync_qo(): st.session_state.qo_num = st.session_state.qo_sld
def sync_qo_num(): st.session_state.qo_sld = st.session_state.qo_num
def sync_qe(): st.session_state.qe_num = st.session_state.qe_sld
def sync_qe_num(): st.session_state.qe_sld = st.session_state.qe_num
def sync_pa(): st.session_state.pa_num = st.session_state.pa_sld
def sync_pa_num(): st.session_state.pa_sld = st.session_state.pa_num
def sync_qa(): st.session_state.qa_num = st.session_state.qa_sld
def sync_qa_num(): st.session_state.qa_sld = st.session_state.qa_num
def sync_ta(): st.session_state.ta_num = st.session_state.ta_sld
def sync_ta_num(): st.session_state.ta_sld = st.session_state.ta_num

for key, val in [('rr_sld', 800), ('rr_num', 800), ('po_sld', 0), ('po_num', 0), ('pe_sld', 80), ('pe_num', 80), 
                 ('qo_sld', 0), ('qo_num', 0), ('qe_sld', 90), ('qe_num', 90), ('pa_sld', 60), ('pa_num', 60), 
                 ('qa_sld', 60), ('qa_num', 60), ('ta_sld', 45), ('ta_num', 45)]:
    if key not in st.session_state:
        st.session_state[key] = val

st.title("Sistem Deteksi Anomali Irama Jantung")
st.info("Catatan Transparansi Medis: Rentang nilai normal didasarkan pada teori anatomi standar. Pada praktiknya di dunia nyata, terdapat toleransi dinamis secara klinis.")

col_kiri, col_tengah, col_kanan = st.columns([1.1, 1.1, 1.4])

with col_kiri:
    st.subheader("Interval & Gelombang")
    
    c1, c2 = st.columns([3, 1])
    c1.slider("RR Interval", 300, 2000, key='rr_sld', on_change=sync_rr, help="Normal: 600 - 1000 ms.")
    c2.number_input("RR", 300, 2000, key='rr_num', on_change=sync_rr_num, label_visibility="collapsed")
    
    c1, c2 = st.columns([3, 1])
    c1.slider("P Onset (Awal P)", 0, 500, key='po_sld', on_change=sync_po)
    c2.number_input("P On", 0, 500, key='po_num', on_change=sync_po_num, label_visibility="collapsed")
    
    c1, c2 = st.columns([3, 1])
    c1.slider("P End (Akhir P)", 0, 500, key='pe_sld', on_change=sync_pe)
    c2.number_input("P End", 0, 500, key='pe_num', on_change=sync_pe_num, label_visibility="collapsed")
    
    c1, c2 = st.columns([3, 1])
    c1.slider("QRS Onset (Awal QRS)", 0, 500, key='qo_sld', on_change=sync_qo)
    c2.number_input("QRS On", 0, 500, key='qo_num', on_change=sync_qo_num, label_visibility="collapsed")
    
    c1, c2 = st.columns([3, 1])
    c1.slider("QRS End (Akhir QRS)", 0, 500, key='qe_sld', on_change=sync_qe)
    c2.number_input("QRS End", 0, 500, key='qe_num', on_change=sync_qe_num, label_visibility="collapsed")

with col_tengah:
    st.subheader("Aksis Kelistrikan (°)")
    
    c1, c2 = st.columns([3, 1])
    c1.slider("P Axis", -180, 180, key='pa_sld', on_change=sync_pa, help="Normal: 0° hingga 75°.")
    c2.number_input("P Ax", -180, 180, key='pa_num', on_change=sync_pa_num, label_visibility="collapsed")
    
    c1, c2 = st.columns([3, 1])
    c1.slider("QRS Axis", -180, 180, key='qa_sld', on_change=sync_qa, help="Normal: -30° hingga 90°.")
    c2.number_input("QRS Ax", -180, 180, key='qa_num', on_change=sync_qa_num, label_visibility="collapsed")
    
    c1, c2 = st.columns([3, 1])
    c1.slider("T Axis", -180, 180, key='ta_sld', on_change=sync_ta, help="Normal: -15° hingga 105°.")
    c2.number_input("T Ax", -180, 180, key='ta_num', on_change=sync_ta_num, label_visibility="collapsed")

    st.divider()
    st.subheader("Kalkulasi Durasi")
    p_duration = st.session_state.pe_num - st.session_state.po_num
    qrs_duration = st.session_state.qe_num - st.session_state.qo_num
    
    st.metric("P Duration (P End - P Onset)", f"{p_duration} ms")
    st.metric("QRS Duration (QRS End - QRS Onset)", f"{qrs_duration} ms")

input_data = pd.DataFrame({
    'rr_interval': [st.session_state.rr_num],
    'qrs_duration': [qrs_duration],
    'p_duration': [p_duration],
    'p_axis': [st.session_state.pa_num],
    'qrs_axis': [st.session_state.qa_num],
    't_axis': [st.session_state.ta_num]
})

probabilitas = model.predict_proba(input_data)[0]
persen_bahaya = probabilitas[1] * 100

with col_kanan:
    st.subheader("Hasil Triage AI")
    
    if persen_bahaya > 75:
        st.error("🚨 PRIORITAS 1 (KRITIS)")
    elif persen_bahaya > 40:
        st.warning("⚠️ PRIORITAS 2 (WASPADA)")
    else:
        st.success("✅ PRIORITAS 3 (AMAN)")
        
    st.markdown(
        f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 15px;'>Probabilitas Kritis: {persen_bahaya:.2f}%</div>", 
        unsafe_allow_html=True
    )
    
    st.markdown("**Analisis Keputusan Medis:**")
    
    if st.session_state.rr_num < 600:
        st.error(f"**RR ({st.session_state.rr_num} ms):** < 600 ms. Indikasi Takikardia.")
    elif st.session_state.rr_num > 1000:
        st.error(f"**RR ({st.session_state.rr_num} ms):** > 1000 ms. Indikasi Bradikardia.")
    else:
        st.success(f"**RR ({st.session_state.rr_num} ms):** Normal.")
        
    if qrs_duration > 120:
        st.error(f"**QRS ({qrs_duration} ms):** > 120 ms. Indikasi Bundle Branch Block.")
    elif qrs_duration < 0:
        st.error(f"**QRS ({qrs_duration} ms):** Input tidak valid.")
    else:
        st.success(f"**QRS ({qrs_duration} ms):** Normal.")
        
    if p_duration >= 120:
        st.error(f"**P Dur ({p_duration} ms):** >= 120 ms. Indikasi Atrial Enlargement.")
    elif p_duration < 0:
        st.error(f"**P Dur ({p_duration} ms):** Input tidak valid.")
    else:
        st.success(f"**P Dur ({p_duration} ms):** Normal.")
        
    if not (0 <= st.session_state.pa_num <= 75):
        st.error(f"**P Ax ({st.session_state.pa_num}°):** Di luar batas (0° s.d 75°).")
    else:
        st.success(f"**P Ax ({st.session_state.pa_num}°):** Normal.")

    if not (-30 <= st.session_state.qa_num <= 90):
        st.error(f"**QRS Ax ({st.session_state.qa_num}°):** Di luar batas (-30° s.d 90°).")
    else:
        st.success(f"**QRS Ax ({st.session_state.qa_num}°):** Normal.")

    if not (-15 <= st.session_state.ta_num <= 105):
        st.error(f"**T Ax ({st.session_state.ta_num}°):** Di luar batas (-15° s.d 105°).")
    else:
        st.success(f"**T Ax ({st.session_state.ta_num}°):** Normal.")
