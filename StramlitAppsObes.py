import streamlit as st
import requests

st.set_page_config(page_title="Prediksi Obesitas", layout="centered")
st.title("🧠 Prediksi Klasifikasi Obesitas")

st.markdown("Silakan isi form berikut untuk mengetahui klasifikasi berat badan berdasarkan gaya hidup dan kebiasaan.")

with st.form("obesity_form"):
    Gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
    Age = st.slider("Usia", 5.0, 100.0, step=1.0)
    Height_in_m = st.slider("Tinggi Badan (meter)", 1.0, 2.5, step=0.01)
    Weight_in_kg = st.slider("Berat Badan (kg)", 20.0, 200.0, step=0.5)
    family_history_with_overweight = st.selectbox("Riwayat Keluarga dengan Overweight", ["yes", "no"])
    High_calorie_diet = st.selectbox("Konsumsi Makanan Tinggi Kalori", ["yes", "no"])
    Frequency_vegetable_consumption = st.slider("Frekuensi Konsumsi Sayur per Minggu", 0.0, 7.0)
    main_course_per_day = st.slider("Jumlah Makan Utama per Hari", 1.0, 5.0)
    Food_consumption_interval = st.selectbox("Pola Makan", ["no", "Sometimes", "Frequently"])
    Smoking = st.selectbox("Merokok", ["yes", "no"])
    Daily_water_intake = st.slider("Asupan Air Harian (liter)", 0.0, 5.0)
    Count_Calorie_intake = st.selectbox("Menghitung Asupan Kalori?", ["yes", "no"])
    Physical_activity_frequency = st.slider("Aktivitas Fisik (jam/minggu)", 0.0, 20.0)
    Time_spent_on_tech = st.slider("Waktu dengan Teknologi (jam/hari)", 0.0, 24.0)
    Alcohol_Consumption_Frequency = st.selectbox("Frekuensi Konsumsi Alkohol", ["no", "Sometimes", "Frequently"])
    Main_Transportation = st.selectbox("Transportasi Utama", ["Walking", "Bike", "Public_Transportation", "Automobile", "Motorbike"])

    submitted = st.form_submit_button("🔍 Prediksi")

if submitted:
    with st.spinner("Mengirim data ke model..."):
        payload = {
            "Gender": Gender,
            "Age": Age,
            "Height_in_m": Height_in_m,
            "Weight_in_kg": Weight_in_kg,
            "family_history_with_overweight": family_history_with_overweight,
            "High_calorie_diet": High_calorie_diet,
            "Frequency_vegetable_consumption": Frequency_vegetable_consumption,
            "main_course_per_day": main_course_per_day,
            "Food_consumption_interval": Food_consumption_interval,
            "Smoking": Smoking,
            "Daily_water_intake": Daily_water_intake,
            "Count_Calorie_intake": Count_Calorie_intake,
            "Physical_activity_frequency": Physical_activity_frequency,
            "Time_spent_on_tech": Time_spent_on_tech,
            "Alcohol_Consumption_Frequency": Alcohol_Consumption_Frequency,
            "Main_Transportation": Main_Transportation
        }

        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=payload)
            result = response.json()

            if response.status_code == 200:
                st.success(f"Hasil Prediksi: **{result['prediction_label']}** (kelas {result['prediction_class']})")
            else:
                st.error(f"Terjadi kesalahan: {result.get('detail', 'Tidak diketahui')}")

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Gagal menghubungi API: {e}")
