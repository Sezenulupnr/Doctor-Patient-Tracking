import streamlit as st
import google.generativeai as genai

GEMINI_ANAHTARI = "AIzaSyC5_ActnFp7AW2P2r05nZVwHEP7wa8JN5A"
genai.configure(api_key=GEMINI_ANAHTARI)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_possible_conditions(symptoms, medical_history):
    prompt = f"""
    Aşağıdaki semptomlar ve geçmiş sağlık durumu göz önünde bulundurularak olası hastalıklar listesini ver:

    Semptomlar: {symptoms}
    Geçmiş Sağlık Durumu: {medical_history}
    """
    return model.generate_content(prompt).text

def doctor_page():

    if st.button("Ana Sayfaya Dön"): 
        st.session_state.page = "home"

    st.title("🏥 Doktor Paneli")
    st.write("Doktor paneline hoşgeldiniz. Hasta bilgilerini burada girebilirsiniz.") 

    tab1, tab2, tab3, tab4 = st.tabs(["Hasta Bilgileri", "Semptomlar", "Geçmiş Sağlık Durumu", "Olası Hastalıklar"])

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
        
        if st.button("Kaydet"):
            st.session_state.medical_history = medical_history
            st.write("Geçmiş sağlık durumu kaydedildi!")

    with tab4:
        st.subheader("Olası Hastalıklar")
        if st.button("Olası Hastalıkları Al"):
            symptoms = st.session_state.get('symptoms', "")
            medical_history = st.session_state.get('medical_history', "")
            if symptoms:
                conditions = get_possible_conditions(symptoms, medical_history)
                st.write("Semptomlar ve geçmiş sağlık durumu göz önüne alındığında olası hastalıklar:")
                st.write(conditions)
            else:
                st.write("Lütfen semptomlar giriniz.")

    st.sidebar.title("Kayıtlı Hasta Bilgileri")

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
          
