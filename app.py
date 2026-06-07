import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

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

    c1, c2 = st.columns([3, 1])
    c1.slider("RR Interval", 300, 2000, key='rr_sld', on_change=sync_rr, help="Distance between heartbeats. Normal: 600 - 1000 ms.")
    c2.number_input("RR", 300, 2000, key='rr_num', on_change=sync_rr_num, label_visibility="collapsed")

    c1, c2 = st.columns([3, 1])
    c1.slider("P Onset", 0, 500, key='po_sld', on_change=sync_po, help="Time point in milliseconds when the atrial contraction wave begins.")
    c2.number_input("P On", 0, 500, key='po_num', on_change=sync_po_num, label_visibility="collapsed")

    c1, c2 = st.columns([3, 1])
    c1.slider("P End", 0, 500, key='pe_sld', on_change=sync_pe, help="Time point in milliseconds when the atrial contraction wave ends.")
    c2.number_input("P End", 0, 500, key='pe_num', on_change=sync_pe_num, label_visibility="collapsed")

    c1, c2 = st.columns([3, 1])
    c1.slider("QRS Onset", 0, 500, key='qo_sld', on_change=sync_qo, help="Time point in milliseconds when the ventricles begin to contract.")
    c2.number_input("QRS On", 0, 500, key='qo_num', on_change=sync_qo_num, label_visibility="collapsed")

    c1, c2 = st.columns([3, 1])
    c1.slider("QRS End", 0, 500, key='qe_sld', on_change=sync_qe, help="Time point in milliseconds when the ventricles finish contracting.")
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

    st.metric("P Duration (P End - P Onset)", f"{p_duration} ms", help="Duration of atrial contraction. Theoretical normal: < 120 ms.")
    st.metric("QRS Duration (QRS End - QRS Onset)", f"{qrs_duration} ms", help="Duration of ventricular contraction. Theoretical normal: 80 - 120 ms.")

input_data = pd.DataFrame({
    'rr_interval': [st.session_state.rr_num],
    'p_axis': [st.session_state.pa_num],
    'qrs_axis': [st.session_state.qa_num],
    't_axis': [st.session_state.ta_num],
    'p_duration': [p_duration],
    'qrs_duration': [qrs_duration]
})

probabilitas = model.predict_proba(input_data)[0]
persen_bahaya = probabilitas[1] * 100

with col_right:
    st.subheader("AI Triage Results")

    # --- PERUBAHAN THRESHOLD BERDASARKAN HASIL CLUSTERING K-MEANS ---
    if persen_bahaya > 67.71:
        st.error("🚨 PRIORITY 1 (CRITICAL)")
    elif persen_bahaya >= 24.73:
        st.warning("⚠️ PRIORITY 2 (CAUTION)")
    else:
        st.success("✅ PRIORITY 3 (NORMAL)")

    st.markdown(
        f"<div style='font-size: 30px; font-weight: bold; margin-bottom: 15px;'>Critical Probability: {persen_bahaya:.2f}%</div>",
        unsafe_allow_html=True
    )

    with st.expander("🧠 Explainable AI: Feature Impact Analysis"):
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(input_data)

        if isinstance(shap_vals, list):
            shap_vals_anomaly = shap_vals[1][0]
        elif len(shap_vals.shape) == 3:
            shap_vals_anomaly = shap_vals[0, :, 1]
        else:
            shap_vals_anomaly = shap_vals[0]

        shap_df = pd.DataFrame({
            'Feature': input_data.columns,
            'SHAP Value': shap_vals_anomaly,
            'Actual Value': input_data.iloc[0].values
        })

        shap_df['Original_Index'] = shap_df.index
        shap_df['Abs_SHAP'] = shap_df['SHAP Value'].abs()

        def categorize_impact(val):
            if val > 0.01:
                return 1
            elif val < -0.01:
                return 2
            else:
                return 3

        shap_df['Impact_Category'] = shap_df['SHAP Value'].apply(categorize_impact)

        if (shap_df['Impact_Category'] == 1).any():
            shap_df = shap_df.sort_values(by=['Impact_Category', 'Abs_SHAP'], ascending=[True, False])
        else:
            shap_df = shap_df.sort_values(by='Original_Index')

        st.markdown("### Top Factors Driving This Prediction")

        for index, row in shap_df.iterrows():
            feature = row['Feature']
            shap_val = row['SHAP Value']
            actual_val = row['Actual Value']

            if shap_val > 0.01:
                st.error(f"⬆️ **{feature}** (Value: {actual_val}): Increased the probability of anomaly.")
            elif shap_val < -0.01:
                st.success(f"⬇️ **{feature}** (Value: {actual_val}): Decreased the probability of anomaly.")
            else:
                st.info(f"➖ **{feature}** (Value: {actual_val}): Neutral impact on this specific prediction.")

        fig, ax = plt.subplots(figsize=(6, 4))

        shap_df_plot = shap_df.sort_values(by='Abs_SHAP', ascending=True)

        colors = ['#ff4b4b' if x > 0 else '#00cc96' for x in shap_df_plot['SHAP Value']]

        ax.barh(shap_df_plot['Feature'], shap_df_plot['SHAP Value'], color=colors)

        ax.set_xlabel("Impact on Risk Probability (SHAP Value)")
        ax.set_title("Local Feature Importance")
        ax.axvline(0, color='black', linewidth=0.8)

        st.pyplot(fig)
