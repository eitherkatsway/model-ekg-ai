import streamlit as st

st.set_page_config(page_title="Triage Jantung EKG", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load('model_ecg_angka.pkl')

model = load_model()

st.title("Sistem Deteksi Anomali EKG Real-Time")
st.write("Geser slider di bawah ini untuk melihat prediksi sistem secara instan.")
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
    st.subheader("Hasil Analisis Triage")
    st.metric("Tingkat Probabilitas Kritis", f"{persen_bahaya:.2f}%")
    
    if persen_bahaya > 75:
        st.error("🚨 PRIORITAS 1 (KRITIS)")
    elif persen_bahaya > 40:
        st.warning("⚠️ PRIORITAS 2 (WASPADA)")
    else:
        st.success("✅ PRIORITAS 3 (AMAN)")

st.divider()
st.header("🔍 Explainable AI (Analisis Keputusan Medis)")

with st.expander("📖 Referensi Medis: Definisi & Nilai Normal"):
    st.markdown("""
    * **RR Interval (Jarak Antar Detak):** Mengukur kecepatan detak jantung. 
        * **Normal:** 600 - 1000 ms (setara 60-100 detak per menit).
        * *Bahaya:* < 600 ms (Takikardia/Terlalu Cepat) atau > 1000 ms (Bradikardia/Terlalu Lambat).
    * **QRS Duration (Durasi Bilik Jantung):** Waktu yang dibutuhkan bilik jantung untuk memompa darah.
        * **Normal:** 80 - 120 ms.
        * *Bahaya:* > 120 ms (Indikasi hambatan listrik/Bundle Branch Block).
    * **P Duration (Durasi Serambi Jantung):** Waktu kontraksi serambi jantung.
        * **Normal:** < 120 ms.
        * *Bahaya:* > 120 ms (Indikasi pembengkakan serambi/Atrial Enlargement).
    * **Aksis Kelistrikan (P, QRS, T Axis):** Arah rata-rata aliran listrik jantung.
        * **Normal QRS Axis:** -30° hingga 90°.
        * *Bahaya:* Di luar rentang tersebut mengindikasikan deviasi aksis (Left/Right Axis Deviation) yang sering terkait dengan kelainan anatomi jantung.
    """)

with st.expander("🧠 Mengapa AI memberikan persentase tersebut? (Klik untuk detail)"):
    alasan = []
    
    if rr_interval < 600:
        alasan.append(f"**RR Interval ({rr_interval} ms):** Terlalu rendah (Takikardia). Jantung berdetak terlalu cepat melebihi rentang normal (600-1000 ms).")
    elif rr_interval > 1000:
        alasan.append(f"**RR Interval ({rr_interval} ms):** Terlalu tinggi (Bradikardia). Jantung berdetak terlalu lambat dari rentang normal (600-1000 ms).")
    
    if qrs_duration > 120:
        alasan.append(f"**QRS Duration ({qrs_duration} ms):** Melebar. Durasi di atas normal (120 ms) menunjukkan kemungkinan adanya hambatan konduksi (seperti LBBB/RBBB).")
        
    if p_duration > 120:
        alasan.append(f"**P Duration ({p_duration} ms):** Memanjang. Mengindikasikan potensi pembesaran serambi jantung.")
        
    if not (-30 <= qrs_axis <= 90):
        alasan.append(f"**QRS Axis ({qrs_axis}°):** Deviasi Aksis. Arah aliran listrik jantung menyimpang dari kuadran normal (-30° hingga 90°).")
        
    if len(alasan) == 0:
        st.success("Semua metrik berada dalam batas toleransi normal. AI memprediksi risiko anomali yang rendah.")
    else:
        st.warning("AI mendeteksi beberapa metrik di luar rentang normal yang meningkatkan persentase bahaya:")
        for poin in alasan:
            st.markdown(f"- {poin}")
