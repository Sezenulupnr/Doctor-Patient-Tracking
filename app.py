import streamlit as st
from doctor import doctor_panel
from patient import patient_panel

st.set_page_config(page_title="Doktor-Hasta Takip", page_icon="🏥", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.title("🏥 Doktor-Hasta Takip Uygulaması")
    st.markdown("Lütfen girmek istediğiniz paneli seçiniz.")

    col = st.columns(1)  

    with col[0]:
        st.button("Hasta Sayfasına Git", key="patient_button", on_click=lambda: setattr(st.session_state, "page", "patient"))
        st.button("Doktor Sayfasına Git", key="doctor_button", on_click=lambda: setattr(st.session_state, "page", "doctor"))

elif st.session_state.page == "patient":
    patient_panel()

elif st.session_state.page == "doctor":
    doctor_panel()