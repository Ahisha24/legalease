import os
import requests
import streamlit as st
from io import BytesIO

# Optional libraries for DOCX and PDF
try:
    from docx import Document
except ImportError:
    Document = None

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

st.set_page_config(page_title="LegalEase", layout="centered")

# Logo & Header setup
col1, col2, col3 = st.columns([1, 2, 1])
logo_path = os.path.join(os.path.dirname(__file__), "image", "Logo.png")
if os.path.exists(logo_path):
    with col2:
        st.image(logo_path, use_container_width=True)

st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)

# Input Form
document_type = st.text_input("Document Type")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if st.button("Generate Document"):
    try:
        response = requests.post(
            "http://localhost:8000/generate",
            json={
                "document_type": document_type,
                "parties": parties,
                "terms": terms,
                "dates": dates
            }
        )

        if response.status_code == 200:
            res_json = response.json()
            generated_text = res_json.get("document", "No document found in response")
            st.session_state["generated_text"] = generated_text
            st.session_state["edited_text"] = generated_text
            st.success("Document Generated Successfully!")
        else:
            st.error(f"Server Error ({response.status_code}): {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI backend. Make sure uvicorn is running!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Generated Document Display, Edit & Download Section
if "generated_text" in st.session_state:
    st.markdown("---")
    st.subheader("Generated Document")
    
    # Display initial output
    st.write(st.session_state["generated_text"])

    # Edit Document State Toggle
    if "show_edit" not in st.session_state:
        st.session_state["show_edit"] = False

    if st.button("Click to Edit Document"):
        st.session_state["show_edit"] = not st.session_state["show_edit"]

    if st.session_state["show_edit"]:
        st.session_state["edited_text"] = st.text_area(
            "Edit Document Below:",
            value=st.session_state.get("edited_text", st.session_state["generated_text"]),
            height=250
        )

    final_document = st.session_state.get("edited_text", st.session_state["generated_text"])

    # Download Options Section
    st.markdown("### Downloading/ Saving the Generated Document")
    st.write("We can Download and save the documents in any of the following formats.")

    col_txt, col_docx, col_pdf = st.columns(3)

    # 1. Download as .TXT
    with col_txt:
        st.download_button(
            label="Download as .TXT",
            data=final_document,
            file_name="legal_document.txt",
            mime="text/plain"
        )

    # 2. Download as .DOCX
    with col_docx:
        if Document:
            doc = Document()
            doc.add_paragraph(final_document)
            docx_io = BytesIO()
            doc.save(docx_io)
            docx_io.seek(0)
            st.download_button(
                label="Download as .DOCX",
                data=docx_io,
                file_name="legal_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.download_button(
                label="Download as .DOCX",
                data=final_document.encode("utf-8"),
                file_name="legal_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    # 3. Download as .PDF
    with col_pdf:
        if FPDF:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=11)
            for line in final_document.split("\n"):
                pdf.multi_cell(0, 8, txt=line.encode('latin-1', 'replace').decode('latin-1'))
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="Download as .PDF",
                data=pdf_bytes,
                file_name="legal_document.pdf",
                mime="application/pdf"
            )
        else:
            st.download_button(
                label="Download as .PDF",
                data=final_document.encode("utf-8"),
                file_name="legal_document.pdf",
                mime="application/pdf"
            )