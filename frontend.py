import streamlit as st
import requests

st.set_page_config(page_title="LegalEase", layout="centered")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("image/Logo.png", use_container_width=True)

st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)

document_type = st.text_input("Document Type")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if st.button("Generate Document"):
    response = requests.post("http://localhost:8000/generate", json={
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates
    })
    generated_text = response.json()["document"]
    st.session_state["generated_text"] = generated_text