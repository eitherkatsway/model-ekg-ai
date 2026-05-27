import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Triage Jantung EKG", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load('model_ecg_angka.pkl')

model = load_model()

# Fungsi Sinkronisasi Slider dan Kotak Angka
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

# Inisialisasi Nilai Awal
for key, val in [('rr_sld', 800), ('rr_num', 800), ('po_sld', 0), ('po_num', 0), ('pe_sld', 80), ('pe_num', 80), 
                 ('qo_sld', 0), ('qo_num', 0), ('qe_sld', 90), ('qe_num', 90), ('pa_sld', 60), ('pa_num', 60), 
                 ('qa_sld', 60), ('qa_num', 60), ('ta_sld', 45), ('ta_num', 45)]:
    if key not in st.session_state:
        st.session_state[key] = val

st.title("Sistem Deteksi Anomali Irama Jantung")
st.info("Catatan Transparansi Medis: Rentang nilai normal yang dicantumkan didasarkan pada teori anatomi standar. Pada praktiknya di dunia nyata, mesin EKG dan dokter ahli memiliki batas toleransi dinamis sebelum mengkategorikan kondisi sebagai anomali gawat darurat.")
st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Interval Waktu & Gelombang (ms)")
    
    # RR Interval dengan Hover Penjelasan
    c1, c2 = st.columns([3, 1])
    c1.slider("RR Interval", 300, 2000, key='rr_sld', on_change=sync_rr, 
              help="Jarak Antar Detak Jantung. Normal: 600 - 1000 ms.")
    c2.number_input("RR", 300, 2000, key='rr_num', on_change=sync_rr_num, label_visibility="collapsed")
    
    # P Onset
    c1, c2 = st.columns([3, 1])
    c1.slider("P Onset (Awal P)", 0, 500, key='po_sld', on_change=sync_po, 
              help="Titik waktu milidetik saat gelombang kontraksi serambi (atrium) dimulai.")
    c2.number_input("P On", 0, 500, key='po_num', on_change=sync_po_num, label_visibility="collapsed")
    
    # P End
    c1, c2 = st.columns([3, 1])
    c1.slider("P End (Akhir P)", 0, 500, key='pe_sld', on_change=sync_pe, 
              help="Titik waktu milidetik saat gelombang kontraksi serambi (atrium) berakhir.")
    c2.number_input("P End", 0, 500, key='pe_num', on_change=sync_pe_num, label_visibility="collapsed")
    
    # QRS Onset
    c1, c2 = st.columns([3, 1])
    c1.slider("QRS Onset (Awal QRS)", 0, 500, key='qo_sld', on_change=sync_qo, 
              help="Titik waktu milidetik saat bilik (ventrikel) mulai memompa.")
    c2.number_input("QRS On", 0, 500, key='qo_num', on_change=sync_qo_num, label_visibility="collapsed")
    
    # QRS End
    c1, c2 = st.columns([3, 1])
    c1.slider("QRS End (Akhir QRS)", 0, 500, key='qe_sld', on_change=sync_qe, 
              help="Titik waktu milidetik saat bilik (ventrikel) selesai memompa.")
    c2.number_input("QRS End", 0, 500, key='qe_num', on_change=sync_qe_num, label_visibility="collapsed")

with col_right:
    st.subheader("Aksis Kelistrikan (°)")
    
    # P Axis
    c1, c2 = st.columns([3, 1])
    c1.slider("P Axis", -180, 180, key='pa_sld', on_change=sync_pa, 
              help="Arah aliran listrik serambi (atrium) jantung. Normal: 0° hingga 75°.")
    c2.number_input("P Ax", -180, 180, key='pa_num', on_change=sync_pa_num, label_visibility="collapsed")
    
    # QRS Axis
    c1, c2 = st.columns([3, 1])
    c1.slider("QRS Axis", -180, 180, key='qa_sld', on_change=sync_qa, 
              help="Arah aliran listrik bilik (ventrikel) utama. Normal: -30° hingga 90°.")
    c2.number_input("QRS Ax", -180, 180, key='qa_num', on_change=sync_qa_num, label_visibility="collapsed")
    
    # T Axis
    c1, c2 = st.columns([3, 1])
    c1.slider("T Axis", -180, 180, key='ta_sld', on_change=sync_ta, 
              help="Arah repolarisasi (pemulihan) bilik jantung. Normal: -15° hingga 105°.")
    c2.number_input("T Ax", -180, 180, key='ta_num', on_change=sync_ta_num, label_visibility="collapsed")

# Kalkulasi Durasi (End - Onset)
p_duration = st.session_state.pe_num - st.session_state.po_num
qrs_duration = st.session_state.qe_num - st.session_state.qo_num

st.divider()
st.subheader("Kalkulasi Durasi")
st.caption("Nilainya merupakan selisih antara titik akhir (End) dan titik awal (Onset) dari gelombang yang dimasukkan di atas.")

c_dur1, c_dur2, c_dur3 = st.columns(3)
c_dur1.metric("P Duration (P End - P Onset)", f"{p_duration} ms", 
              help="Durasi kontraksi serambi (atrium) jantung. Normal teori: < 120 ms.")
c_dur2.metric("QRS Duration (QRS End - QRS Onset)", f"{qrs_duration} ms", 
              help="Durasi kontraksi bilik (ventrikel) jantung. Normal teori: 80 - 120 ms.")

# Memasukkan ke Model untuk Prediksi
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

with c_dur3:
    if persen_bahaya > 75:
        st.error("🚨 PRIORITAS 1 (KRITIS)")
    elif persen_bahaya > 40:
        st.warning("⚠️ PRIORITAS 2 (WASPADA)")
    else:
        st.success("✅ PRIORITAS 3 (AMAN)")

    st.markdown(f"**Hasil Analisis Triage:** Probabilitas Kritis {persen_bahaya:.2f}%")
    
st.divider()

with st.expander("🧠 Mengapa AI memberikan persentase tersebut? (Klik untuk detail)"):
    
    if st.session_state.rr_num < 600:
        st.error(f"**RR Interval ({st.session_state.rr_num} ms) - Di Luar Batas (< 600 ms):** Secara teori, normal berkisar di 600 - 1000 ms. Angka ini terlalu cepat (Takikardia), namun mesin medis mungkin memiliki toleransi klinis tertentu.")
    elif st.session_state.rr_num > 1000:
        st.error(f"**RR Interval ({st.session_state.rr_num} ms) - Di Luar Batas (> 1000 ms):** Secara teori, normal berkisar di 600 - 1000 ms. Angka ini terlalu lambat (Bradikardia), namun bisa saja wajar pada atlet atau kasus non-akut.")
    else:
        st.success(f"**RR Interval ({st.session_state.rr_num} ms) - Normal:** Rentang teori dan batas aman berada di kisaran 600 - 1000 ms.")
        
    if qrs_duration > 120:
        st.error(f"**QRS Duration ({qrs_duration} ms) - Di Luar Batas (> 120 ms):** Normalnya secara teori berkisar di 80 - 120 ms. Angka ini merupakan indikasi hambatan listrik (Bundle Branch Block).")
    elif qrs_duration < 0:
        st.error(f"**QRS Duration ({qrs_duration} ms) - Input Tidak Valid:** Titik akhir (End) QRS tidak boleh lebih kecil dari titik awal (Onset).")
    else:
        st.success(f"**QRS Duration ({qrs_duration} ms) - Normal:** Waktu bilik memompa sesuai dengan rentang batas aman (< 120 ms).")
        
    if p_duration >= 120:
        st.error(f"**P Duration ({p_duration} ms) - Di Luar Batas (>= 120 ms):** Secara teori kisaran normal adalah < 120 ms. Angka ini merupakan indikasi pembengkakan serambi (Atrial Enlargement).")
    elif p_duration < 0:
        st.error(f"**P Duration ({p_duration} ms) - Input Tidak Valid:** Titik akhir (End) P tidak boleh lebih kecil dari titik awal (Onset).")
    else:
        st.success(f"**P Duration ({p_duration} ms) - Normal:** Waktu kontraksi serambi sesuai dengan rentang teori medis (< 120 ms).")
        
    if not (0 <= st.session_state.pa_num <= 75):
        st.error(f"**P Axis ({st.session_state.pa_num}°) - Di Luar Batas:** Secara teori berada di 0° hingga 75°. Menyimpang dari ini berpotensi mengindikasikan irama ektopik.")
    else:
        st.success(f"**P Axis ({st.session_state.pa_num}°) - Normal:** Aksis serambi berada dalam toleransi klinis (0° hingga 75°).")

    if not (-30 <= st.session_state.qa_num <= 90):
        st.error(f"**QRS Axis ({st.session_state.qa_num}°) - Di Luar Batas:** Secara teori berada di -30° hingga 90°. Deviasi dari angka ini dapat terkait dengan kelainan anatomi atau konduksi.")
    else:
        st.success(f"**QRS Axis ({st.session_state.qa_num}°) - Normal:** Aksis bilik utama berada dalam toleransi klinis (-30° hingga 90°).")

    if not (-15 <= st.session_state.ta_num <= 105):
        st.error(f"**T Axis ({st.session_state.ta_num}°) - Di Luar Batas:** Secara teori berada di -15° hingga 105°. Deviasi ini sering diwaspadai klinisi untuk potensi iskemia.")
    else:
        st.success(f"**T Axis ({st.session_state.ta_num}°) - Normal:** Aksis repolarisasi berada dalam batas toleransi (-15° hingga 105°).")
