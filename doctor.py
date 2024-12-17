import streamlit as st
import google.generativeai as genai
from database import DOCTOR_DATABASE
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_ANAHTARI = os.getenv("GEMINI_ANAHTARI")

genai.configure(api_key=GEMINI_ANAHTARI)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_possible_conditions(symptoms, medical_history):
    prompt = f"""
    Aşağıdaki semptomlar ve geçmiş sağlık durumu göz önünde bulundurularak olası hastalıklar listesini ver:

    Semptomlar: {symptoms}
    Geçmiş Sağlık Durumu: {medical_history}
    """
    return model.generate_content(prompt).text

def get_advice(conditions, risk_level):
    prompt = f"""
    Aşağıdaki semptomlar ve geçmiş sağlık durumu göz önüne alındığında, olası hastalıklar hakkında bir tavsiye oluşturun:

    Olası Hastalıklar: {conditions}
    Risk Durumu: {risk_level}

    Lütfen, hastalıklarla ilgili önerilen tedavi ve dikkat edilmesi gereken noktalar hakkında tavsiye verin.
    """
    return model.generate_content(prompt).text

def doctor_panel():
    if st.button("Ana Sayfaya Dön", key="doctor_to_home"): 
        st.session_state.page = "home"

    if not st.session_state.get("doctor_authenticated", False):
        st.title("🔐 Doktor Girişi")
        
        doctor_name = st.text_input("Adınız-Soyadınız")
        hospital = st.text_input("Çalıştığınız Hastane")
        specialty = st.text_input("Uzmanlık Alanınız")
        password = st.text_input("Şifreniz", type="password")
        
        if st.button("Giriş Yap", key="doctor_button"):
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
        return 

    st.title("👩‍⚕️ Doktor Paneli")
    st.write("Doktor paneline hoşgeldiniz. Hasta bilgilerini burada görüntüleyebilirsiniz.") 
     
    assigned_patients = [
        {
            "patient_name": st.session_state.patient_name,
            "gender": st.session_state.gender,
            "age": st.session_state.age,
            "symptoms": st.session_state.symptoms,
            "medical_history": st.session_state.medical_history,
        }
        for patient in [st.session_state]
        if (
        patient.get("assigned_doctor", {}).get("name") == st.session_state.doctor_name and
        patient.get("assigned_doctor", {}).get("hospital") == st.session_state.hospital and
        patient.get("assigned_doctor", {}).get("specialty") == st.session_state.specialty
    )
    ]

    if not assigned_patients:
        st.warning("🔍 Hasta verisi eksik veya size atanmış bir hasta yok.")
        return

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([ 
        "Hasta Bilgileri", "Semptomlar", "Geçmiş Sağlık Durumu", "Olası Hastalıklar", "Risk Durumu", "Tavsiye"
    ])

    with tab1:
        st.subheader("Hasta Bilgileri")
        st.text_input("Ad", value=st.session_state.get('patient_name', 'N/A'))
        st.text_input("Cinsiyet", value=st.session_state.get('gender', 'N/A'))
        st.text_input("Yaş", value=st.session_state.get('age', 'N/A'))

    with tab2:
        st.subheader("Semptomlar")
        st.text_area("Semptomlar", value=st.session_state.get('symptoms', 'N/A'))

    with tab3:
        st.subheader("Geçmiş Sağlık Durumu")
        st.text_area("Geçmiş Sağlık Durumu", value=st.session_state.get('medical_history', 'N/A'))

    with tab4:
        st.subheader("Olası Hastalıklar")
        if st.session_state.get("symptoms") and st.session_state.get("medical_history"):
            symptoms = st.session_state.symptoms
            medical_history = st.session_state.medical_history

            conditions = get_possible_conditions(symptoms, medical_history)
            st.write("Semptomlar ve geçmiş sağlık durumu göz önüne alındığında olası hastalıklar:")
            st.session_state.conditions = conditions
            st.write(conditions)

        else:
            st.write("Lütfen semptomları alınız.")

    with tab5:
        st.subheader("Risk Durumu")
        if st.session_state.get("conditions"):
            conditions = st.session_state.conditions
            risk_level = st.radio(
                "Risk Durumu Belirleyiniz",
                ["Düşük", "Orta", "Yüksek"],
                index=0,
                key="risk_level_radio"
            )

            if st.button("Risk Durumunu Gönder"):
                if risk_level == "Düşük":
                    st.success(f"Risk durumu '{risk_level}' olarak kaydedildi!", icon="✅")
                    st.session_state.risk_level = "Düşük"
                elif risk_level == "Orta":
                    st.success(f"Risk durumu '{risk_level}' olarak kaydedildi!", icon="⚠️")
                    st.session_state.risk_level = "Orta"
                elif risk_level == "Yüksek":
                    st.success(f"Risk durumu '{risk_level}' olarak kaydedildi!", icon="🚨")
                    st.session_state.risk_level = "Yüksek"
        else:
            st.info("Lütfen önce olası hastalıkları alınız.")

    with tab6:
        st.subheader("Tavsiye")
        if st.session_state.get("conditions") and st.session_state.get("risk_level"):
            conditions = st.session_state.conditions
            risk_level = st.session_state.risk_level

            advice = get_advice(conditions, risk_level)
            st.write(advice)

            if st.button("Tavsiyeyi Gönder"):
                st.success("Tavsiye hasta paneline gönderildi!")
                st.session_state.advice = advice

        else:
            st.info("Lütfen önce olası hastalıkları ve risk durumunu alınız.")

if "doctor_authenticated" not in st.session_state:
    st.session_state.doctor_authenticated = False
