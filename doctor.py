import streamlit as st
import google.generativeai as genai

# Google Generative AI API anahtarını ayarla
GEMINI_ANAHTARI = "AIzaSyC5_ActnFp7AW2P2r05nZVwHEP7wa8JN5A"
genai.configure(api_key=GEMINI_ANAHTARI)
model = genai.GenerativeModel('gemini-1.5-flash')

# Olası hastalıkları getiren fonksiyon
def get_possible_conditions(symptoms, medical_history):
    prompt = f"""
    Aşağıdaki semptomlar ve geçmiş sağlık durumu göz önünde bulundurularak olası hastalıklar listesini ver:

    Semptomlar: {symptoms}
    Geçmiş Sağlık Durumu: {medical_history}
    """
    return model.generate_content(prompt).text

# Tavsiye almak için fonksiyon
def get_advice(conditions, risk_level):
    prompt = f"""
    Aşağıdaki semptomlar ve geçmiş sağlık durumu göz önüne alındığında, olası hastalıklar hakkında bir tavsiye oluşturun:

    Olası Hastalıklar: {conditions}
    Risk Durumu: {risk_level}

    Lütfen, hastalıklarla ilgili önerilen tedavi ve dikkat edilmesi gereken noktalar hakkında tavsiye verin.
    """
    return model.generate_content(prompt).text

# Doktor paneli
def doctor_page():
    if st.button("Ana Sayfaya Dön"): 
        st.session_state.page = "home"

    st.title("👩‍⚕️ Doktor Paneli")
    st.write("Doktor paneline hoşgeldiniz. Hasta bilgilerini burada girebilirsiniz.") 

    # Hasta bilgisi kontrolü
    patient_name = st.session_state.get("patient_name")
    gender = st.session_state.get("gender")
    age = st.session_state.get("age")
    symptoms = st.session_state.get("symptoms")
    medical_history= st.session_state.get("medical_history")

    if not all([patient_name, gender, age, symptoms, medical_history]):
        st.warning("Hasta bilgileri eksik kaydedilmiş. Lütfen hasta panelinden bilgileri eksiksiz doldurun.")
        return

    # Sekmeler
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([ 
        "Hasta Bilgileri", "Semptomlar", "Geçmiş Sağlık Durumu", "Olası Hastalıklar", "Risk Durumu", "Tavsiye"
    ])

    with tab1:
        st.subheader("Hasta Bilgileri")
        patient_name = st.text_input(
            "Hasta Adı", 
            value=st.session_state.get("patient_name", "")
        )
        gender = st.selectbox(
            "Cinsiyet", 
            ["Erkek", "Kadın", "Diğer"], 
            index=["Erkek", "Kadın", "Diğer"].index(st.session_state.get("gender", "Erkek"))
        )
        age = st.number_input(
            "Yaş", 
            min_value=1, 
            max_value=120, 
            value=st.session_state.get("age", 1)
        )
        
        if patient_name:
            st.session_state.patient_name = patient_name
            st.session_state.gender = gender
            st.session_state.age = age

    with tab2:
        st.subheader("Semptomlar")
        symptom_choices = [
            "Ateş", "Baş Ağrısı", "Yorgunluk", "Öksürük", "Boğaz Ağrısı", "Nefes Darlığı", "Bulantı", "Karın Ağrısı"
        ]
        
        symptoms = st.multiselect(
            "Semptomlar Seçiniz", 
            symptom_choices, 
            default=[ 
                symptom for symptom in st.session_state.get("symptoms", "").split(", ") 
                if symptom in symptom_choices 
            ]
        )
        
        other_symptom = st.text_input(
            "Diğer semptomlar (Varsa)", 
            value=st.session_state.get("other_symptom", "")
        )
        
        if symptoms or other_symptom:
            symptoms_str = ", ".join(symptoms)
            if other_symptom:
                symptoms_str += f", {other_symptom}"
            
            st.session_state.symptoms = symptoms_str
            st.session_state.other_symptom = other_symptom

    with tab3:
        st.subheader("Geçmiş Sağlık Durumu")
        medical_history = st.text_area(
            "Geçmiş Sağlık Durumu", 
            value=st.session_state.get("medical_history", "")
        )

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
                index=0
            )
            if st.button("Risk Durumunu Gönder"):
                st.success(f"Risk durumu '{risk_level}' olarak kaydedildi!")
                st.session_state.risk_level = risk_level
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
