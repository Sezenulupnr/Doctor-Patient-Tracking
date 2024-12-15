import streamlit as st

DOCTOR_DATABASE = [
    {"name": "Sezen Ulupınar", "hospital": "Acıbadem", "specialty": "Kardiyoloji", "password": "12345"},
    {"name": "Seray Taşlı", "hospital": "Medipol", "specialty": "Dermatoloji", "password": "67890"},
]

def doctor_login():

    if st.button("Ana Sayfaya Dön", key="doctor_to_home"): 
        st.session_state.page = "home"

    st.title("🔐 Doktor Girişi")
    
    doctor_name = st.text_input("Adınız-Soyadınız")
    hospital = st.text_input("Çalıştığınız Hastane")
    specialty = st.text_input("Uzmanlık Alanınız")
    password = st.text_input("Şifreniz", type="password")

    if st.button("Giriş Yap"):
        for doctor in DOCTOR_DATABASE:
            if (doctor["name"] == doctor_name and 
                doctor["hospital"] == hospital and 
                doctor["specialty"] == specialty and 
                doctor["password"] == password):
                st.success(f"Hoş geldiniz, {doctor_name}!")
                st.session_state.doctor_authenticated = True
                st.session_state.doctor_name = doctor_name
                st.session_state.hospital = hospital
                st.session_state.specialty = specialty
                return
        st.error("Giriş bilgileri hatalı! Lütfen tekrar deneyiniz.")
