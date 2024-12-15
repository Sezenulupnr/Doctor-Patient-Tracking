import streamlit as st

def patient_page():
    if st.button("Ana Sayfaya Dön"): 
        st.session_state.page = "home"

    st.title("🩺 Hasta Paneli")
    st.write("Hasta paneline hoşgeldiniz. Semptomlarınızı burada girebilirsiniz.") 

    tab1, tab2, tab3, tab4 = st.tabs(["Hasta Bilgileri", "Semptomlar", "Teşhisli Hastalıklar", "Doktor Bilgileri"])

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
        st.subheader("Teşhisli Hastalıklar")
        medical_history = st.text_area("Geçmiş Sağlık Durumu")
        st.session_state.medical_history = medical_history if medical_history else "-"

    with tab4:
        st.subheader("Doktor Bilgileri")

        hospital = st.text_input("Hastane")

        doctor_name = st.text_input("Doktor Adı")

        specialty_choices = [
            "Acil Tıp", "Kardiyoloji", "Anesteziyoloji", "Beyin Cerrahisi", "Cardiyoloji", "Dermatoloji", "Endokrinoloji", 
            "Gastroenteroloji", "Genetik", "Göğüs Hastalıkları", "Kadın Hastalıkları ve Doğum", 
            "Nöroloji", "Ortopedi", "Psikiyatri", "Radyoloji", "Romatoloji", "Genel Cerrahi", 
            "Kulak Burun Boğaz", "Beyin ve Sinir Cerrahisi"
        ]
        
        specialty = st.selectbox("Uzmanlık Alanı", specialty_choices)

        save_button = st.button("Doktor Bilgilerini Kaydet")
        
        if doctor_name and specialty and hospital :
            if save_button:
                st.session_state.hospital = hospital
                st.session_state.doctor_name = doctor_name
                st.session_state.specialty = specialty
                st.write(f"Hastane: {hospital}")
                st.write(f"Doktor Adı: {doctor_name}")
                st.write(f"Uzmanlık Alanı: {specialty}")
                st.success("Doktor Bilgileri Kaydedildi!")
        else:
            if save_button:
                st.warning("Lütfen tüm alanları doldurun.")

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
