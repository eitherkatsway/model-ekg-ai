import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="ECG Heart Triage", layout="wide")

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

st.title("Heart Rhythm Anomaly Detection System")
st.info("Medical Transparency Note: Normal value ranges are based on standard anatomical theory. In real-world clinical practice, dynamic tolerances are applied before categorizing a condition as an emergency.")

col_left, col_center, col_right = st.columns([1.1, 1.1, 1.4])

with col_left:
    st.subheader("Intervals & Waves (ms)")

    # RR Interval
    c1, c2 = st.columns([3, 1])
    c1.slider("RR Interval", 300, 2000, key='rr_sld', on_change=sync_rr,
              help="Distance between heartbeats. Normal: 600 - 1000 ms.")
    c2.number_input("RR", 300, 2000, key='rr_num', on_change=sync_rr_num, label_visibility="collapsed")

    # P Onset
    c1, c2 = st.columns([3, 1])
    c1.slider("P Onset", 0, 500, key='po_sld', on_change=sync_po,
              help="Time point in milliseconds when the atrial contraction wave begins.")
    c2.number_input("P On", 0, 500, key='po_num', on_change=sync_po_num, label_visibility="collapsed")

    # P End
    c1, c2 = st.columns([3, 1])
    c1.slider("P End", 0, 500, key='pe_sld', on_change=sync_pe,
              help="Time point in milliseconds when the atrial contraction wave ends.")
    c2.number_input("P End", 0, 500, key='pe_num', on_change=sync_pe_num, label_visibility="collapsed")

    # QRS Onset
    c1, c2 = st.columns([3, 1])
    c1.slider("QRS Onset", 0, 500, key='qo_sld', on_change=sync_qo,
              help="Time point in milliseconds when the ventricles begin to contract.")
    c2.number_input("QRS On", 0, 500, key='qo_num', on_change=sync_qo_num, label_visibility="collapsed")

    # QRS End
    c1, c2 = st.columns([3, 1])
    c1.slider("QRS End", 0, 500, key='qe_sld', on_change=sync_qe,
              help="Time point in milliseconds when the ventricles finish contracting.")
    c2.number_input("QRS End", 0, 500, key='qe_num', on_change=sync_qe_num, label_visibility="collapsed")

with col_center:
    st.subheader("Electrical Axis (°)")

    c1, c2 = st.columns([3, 1])
    c1.slider("P Axis", -180, 180, key='pa_sld', on_change=sync_pa, help="Normal: 0° to 75°.")
    c2.number_input("P Ax", -180, 180, key='pa_num', on_change=sync_pa_num, label_visibility="collapsed")

    c1, c2 = st.columns([3, 1])
    c1.slider("QRS Axis", -180, 180, key='qa_sld', on_change=sync_qa, help="Normal: -30° to 90°.")
    c2.number_input("QRS Ax", -180, 180, key='qa_num', on_change=sync_qa_num, label_visibility="collapsed")

    c1, c2 = st.columns([3, 1])
    c1.slider("T Axis", -180, 180, key='ta_sld', on_change=sync_ta, help="Normal: -15° to 105°.")
    c2.number_input("T Ax", -180, 180, key='ta_num', on_change=sync_ta_num, label_visibility="collapsed")

    st.divider()
    st.subheader("Duration Calculation")
    p_duration = st.session_state.pe_num - st.session_state.po_num
    qrs_duration = st.session_state.qe_num - st.session_state.qo_num

    st.metric("P Duration (P End - P Onset)", f"{p_duration} ms",
             help="Duration of atrial contraction. Theoretical normal: < 120 ms.")
    st.metric("QRS Duration (QRS End - QRS Onset)", f"{qrs_duration} ms",
              help="Duration of ventricular contraction. Theoretical normal: 80 - 120 ms.")

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

with col_right:
    st.subheader("AI Triage Results")

    if persen_bahaya > 75:
        st.error("🚨 PRIORITY 1 (CRITICAL)")
    elif persen_bahaya > 40:
        st.warning("⚠️ PRIORITY 2 (WARNING)")
    else:
        st.success("✅ PRIORITY 3 (SAFE)")

    st.markdown(
        f"<div style='font-size: 30px; font-weight: bold; margin-bottom: 15px;'>Critical Probability: {persen_bahaya:.2f}%</div>",
        unsafe_allow_html=True
    )

    with st.expander("🧠 Why did the AI give this percentage? (Click for details)"):

        if st.session_state.rr_num < 600:
            st.error(f"**RR Interval ({st.session_state.rr_num} ms) - Out of Bounds (< 600 ms):** Theoretically, normal ranges from 600 - 1000 ms. This rate is too fast, possibly indicating Tachycardia.")
        elif st.session_state.rr_num > 1000:
            st.error(f"**RR Interval ({st.session_state.rr_num} ms) - Out of Bounds (> 1000 ms):** Theoretically, normal ranges from 600 - 1000 ms. This rate is too slow, possibly indicating Bradycardia.")
        else:
            st.success(f"**RR Interval ({st.session_state.rr_num} ms) - Normal:** Falls within the theoretical and safe range of 600 - 1000 ms.")

        if qrs_duration > 120:
            st.error(f"**QRS Duration ({qrs_duration} ms) - Out of Bounds (> 120 ms):** Theoretical normal ranges from 80 - 120 ms. This value indicates a possible electrical conduction block (Bundle Branch Block).")
        elif qrs_duration < 0:
            st.error(f"**QRS Duration ({qrs_duration} ms) - Invalid Input:** QRS End cannot be smaller than QRS Onset.")
        else:
            st.success(f"**QRS Duration ({qrs_duration} ms) - Normal:** Ventricular pumping time is within safe limits (< 120 ms).")

        if p_duration >= 120:
            st.error(f"**P Duration ({p_duration} ms) - Out of Bounds (>= 120 ms):** Theoretical normal range is < 120 ms. This value indicates possible Atrial Enlargement.")
        elif p_duration < 0:
            st.error(f"**P Duration ({p_duration} ms) - Invalid Input:** P End cannot be smaller than P Onset.")
        else:
            st.success(f"**P Duration ({p_duration} ms) - Normal:** Atrial contraction time matches theoretical medical ranges (< 120 ms).")

        if not (0 <= st.session_state.pa_num <= 75):
            st.error(f"**P Axis ({st.session_state.pa_num}°) - Out of Bounds:** Theoretically falls between 0° and 75°. Deviation from this may indicate an ectopic rhythm.")
        else:
            st.success(f"**P Axis ({st.session_state.pa_num}°) - Normal:** Atrial axis is within clinical tolerance (0° to 75°).")

        if not (-30 <= st.session_state.qa_num <= 90):
            st.error(f"**QRS Axis ({st.session_state.qa_num}°) - Out of Bounds:** Theoretically falls between -30° and 90°. Deviation may be related to anatomical or conduction abnormalities.")
        else:
            st.success(f"**QRS Axis ({st.session_state.qa_num}°) - Normal:** Main ventricular axis is within clinical tolerance (-30° to 90°).")

        if not (-15 <= st.session_state.ta_num <= 105):
            st.error(f"**T Axis ({st.session_state.ta_num}°) - Out of Bounds:** Theoretically falls between -15° and 105°. This deviation is often monitored by clinicians for potential ischemia.")
        else:
            st.success(f"**T Axis ({st.session_state.ta_num}°) - Normal:** Repolarization axis is within tolerance limits (-15° to 105°).")
