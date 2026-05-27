import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Triage Jantung EKG", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load('model_ecg_angka.pkl')

model = load_model()

st.title("Sistem Deteksi Anomali Irama Jantung")
st.write("Geser slider di bawah ini untuk melihat prediksi sistem secara instan. Arahkan kursor ke simbol (?) untuk info.")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Interval Waktu (ms)")
    rr_interval = st.slider("RR Interval", min_value=300, max_value=2000, value=800, step=10,
                            help="Jarak Antar Detak. Normal: 600 - 1000 ms.")
    qrs_duration = st.slider("QRS Duration", min_value=40, max_value=200, value=90, step=1,
                             help="Durasi bilik jantung memompa. Normal: 80 - 120 ms.")
    p_duration = st.slider("P Duration", min_value=20, max_value=150, value=80, step=1,
                           help="Durasi kontraksi serambi. Normal: < 120 ms.")

with col2:
    st.subheader("Aksis Kelistrikan (°)")
    p_axis = st.slider("P Axis", min_value=-180, max_value=180, value=60, step=1,
                       help="Arah aliran listrik serambi jantung. Normal: 0° hingga 75°.")
    qrs_axis = st.slider("QRS Axis", min_value=-180, max_value=180, value=60, step=1,
                         help="Arah aliran listrik bilik utama. Normal: -30° hingga 90°.")
    t_axis = st.slider("T Axis", min_value=-180, max_value=180, value=45, step=1,
                       help="Arah repolarisasi (pemulihan) bilik. Normal: -15° hingga 105°.")

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
    st.subheader("Hasil Analisis Triage")
    st.metric("Tingkat Probabilitas Kritis", f"{persen_bahaya:.2f}%")

    if persen_bahaya > 75:
        st.error("🚨 PRIORITAS 1 (KRITIS)")
    elif persen_bahaya > 40:
        st.warning("⚠️ PRIORITAS 2 (WASPADA)")
    else:
        st.success("✅ PRIORITAS 3 (AMAN)")

st.divider()

with st.expander("🧠 Mengapa AI memberikan persentase tersebut? (Klik untuk detail)"):

    if rr_interval < 600:
        st.error(f"**RR Interval ({rr_interval} ms) - Bahaya (< 600 ms):** Mengukur kecepatan detak jantung. Mengindikasikan Takikardia (Terlalu Cepat). Normal: 600 - 1000 ms.")
    elif rr_interval > 1000:
        st.error(f"**RR Interval ({rr_interval} ms) - Bahaya (> 1000 ms):** Mengukur kecepatan detak jantung. Mengindikasikan Bradikardia (Terlalu Lambat). Normal: 600 - 1000 ms.")
    else:
        st.success(f"**RR Interval ({rr_interval} ms) - Normal:** Mengukur kecepatan detak jantung. Berada di rentang normal 600 - 1000 ms.")

    if qrs_duration > 120:
        st.error(f"**QRS Duration ({qrs_duration} ms) - Bahaya (> 120 ms):** Waktu bilik jantung memompa. Indikasi hambatan listrik (Bundle Branch Block). Normal: 80 - 120 ms.")
    else:
        st.success(f"**QRS Duration ({qrs_duration} ms) - Normal:** Waktu bilik jantung memompa. Berada di rentang normal 80 - 120 ms.")

    if p_duration >= 120:
        st.error(f"**P Duration ({p_duration} ms) - Bahaya (> 120 ms):** Waktu kontraksi serambi. Indikasi pembengkakan serambi (Atrial Enlargement). Normal: < 120 ms.")
    else:
        st.success(f"**P Duration ({p_duration} ms) - Normal:** Waktu kontraksi serambi. Berada di rentang normal < 120 ms.")

    if not (0 <= p_axis <= 75):
        st.error(f"**P Axis ({p_axis}°) - Bahaya:** Arah aliran listrik serambi. Di luar normal (0° hingga 75°) mengindikasikan irama ektopik atau pembesaran atrium.")
    else:
        st.success(f"**P Axis ({p_axis}°) - Normal:** Arah aliran listrik serambi berada di rentang normal (0° hingga 75°).")

    if not (-30 <= qrs_axis <= 90):
        st.error(f"**QRS Axis ({qrs_axis}°) - Bahaya:** Arah aliran listrik bilik utama. Di luar normal (-30° hingga 90°) mengindikasikan deviasi aksis (kelainan anatomi/konduksi).")
    else:
        st.success(f"**QRS Axis ({qrs_axis}°) - Normal:** Arah aliran listrik bilik utama berada di rentang normal (-30° hingga 90°).")

    if not (-15 <= t_axis <= 105):
        st.error(f"**T Axis ({t_axis}°) - Bahaya:** Arah pemulihan (repolarisasi) jantung. Di luar normal (-15° hingga 105°) sering dikaitkan dengan iskemia atau hipertrofi bilik.")
    else:
        st.success(f"**T Axis ({t_axis}°) - Normal:** Arah pemulihan jantung berada di rentang normal (-15° hingga 105°).")
