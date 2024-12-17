import streamlit as st
from database import DOCTOR_DATABASE

def patient_panel():
    if st.button("Ana Sayfaya Dön"): 
        st.session_state.page = "home"

    st.title("🩺 Hasta Paneli")
    st.write("Hasta paneline hoşgeldiniz. Semptomlarınızı burada girebilirsiniz.") 

    tab1, tab2, tab3, tab4 = st.tabs(["Hasta Bilgileri", "Semptomlar", "Geçmiş Sağlık Durumu", "Doktor Bilgileri"])

    with tab1:
        st.subheader("Hasta Bilgileri")
        patient_name = st.text_input("Hasta Adı")
        gender = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Diğer"])
        age = st.number_input("Yaş", min_value=1, max_value=120)
        
        if patient_name:
            st.session_state.patient_name = patient_name
            st.session_state.gender = gender
            st.session_state.age = age

    with tab2:
        st.subheader("Semptomlar")
        
        symptom_choices = [
            "Ateş", "Baş Ağrısı", "Yorgunluk", "Öksürük", "Boğaz Ağrısı", "Nefes Darlığı", "Bulantı", "Karın Ağrısı"
        ]
        
        symptoms = st.multiselect("Semptomlar Seçiniz", symptom_choices)
        
        other_symptom = st.text_input("Diğer semptomlar (Varsa)", value="")
        
        if symptoms or other_symptom:
            symptoms_str = ", ".join(symptoms)
            if other_symptom:
                symptoms_str += f", {other_symptom}"    
            
            st.session_state.symptoms = symptoms_str

    with tab3:
        st.subheader("Geçmiş Sağlık Durumu")
        medical_history = st.text_area("Geçmiş Sağlık Durumu")
        st.session_state.medical_history = medical_history if medical_history else "Hastalık Geçmişi Yok"

    with tab4:
        st.subheader("Doktor Bilgileri")

        doctor_name = [doc["name"] for doc in DOCTOR_DATABASE]
        hospital = [doc["hospital"] for doc in DOCTOR_DATABASE]
        specialty = [doc["specialty"] for doc in DOCTOR_DATABASE]
        
        selected_doctor_name = st.selectbox("Doktor Adı", options=["Seçiniz"] + doctor_name)
        selected_hospital = st.selectbox("Hastane", options=["Seçiniz"] + hospital)
        selected_specialty = st.selectbox("Uzmanlık Alanı", options=["Seçiniz"] + specialty)
        
        if (
            selected_doctor_name != "Seçiniz"
            and selected_hospital != "Seçiniz"
            and selected_specialty != "Seçiniz"
        ):
            st.session_state.selected_doctor = {
                "name": selected_doctor_name,
                "hospital": selected_hospital,
                "specialty": selected_specialty,
            }

        if st.button("Bilgileri Gönder"):
            if "selected_doctor" in st.session_state:
                st.session_state.assigned_doctor = st.session_state.selected_doctor
                st.success("Bilgileriniz doktorunuza gönderildi!")
            else:
                st.error("Lütfen bir doktor seçiniz!")

    st.sidebar.title("Kayıtlı Bilgilerim")

    if "patient_name" in st.session_state:
        st.sidebar.subheader("Hasta Bilgileri")
        st.sidebar.write(f"Ad: {st.session_state.patient_name}")
        st.sidebar.write(f"Cinsiyet: {st.session_state.gender}")
        st.sidebar.write(f"Yaş: {st.session_state.age}")

    if "symptoms" in st.session_state:
        st.sidebar.subheader("Semptomlar")
        st.sidebar.write(st.session_state.symptoms)

    if "medical_history" in st.session_state:
        st.sidebar.subheader("Geçmiş Sağlık Durumu")
        st.sidebar.write(st.session_state.medical_history)

    if "doctor_name" in st.session_state:
        st.sidebar.subheader("Doktor Bilgileri")
        st.sidebar.write(f"Hastane: {st.session_state.hospital}")
        st.sidebar.write(f"Doktor Adı: {st.session_state.doctor_name}")
        st.sidebar.write(f"Uzmanlık Alanı: {st.session_state.specialty}")

    if "risk_level" in st.session_state:
        st.sidebar.subheader("Risk Seviyesi")
        st.sidebar.write(f"{st.session_state.risk_level}")

    if "advice" in st.session_state:
        st.sidebar.subheader("Tavsiye")
        st.sidebar.write(f"{st.session_state.advice}")
