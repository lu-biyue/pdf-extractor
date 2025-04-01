import streamlit as st
import os
import pandas as pd
from datetime import datetime
from io import BytesIO
from sor_converter import extract_structured_items_from_pdf  # Make sure this file is in your project

# Streamlit setup
st.set_page_config(page_title="SOR PDF Extractor", layout="centered")
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Inject CSS
st.markdown("""
<style>
/* Hide default Streamlit elements */
#MainMenu, footer, header {visibility: hidden;}

/* Apply custom background to full page */
body {
    background-color: #2E3B4E;
    font-family: 'Segoe UI', sans-serif;

    --s: 200px;
    --c1: #1d1d1d;
    --c2: #4e4f51;
    --c3: #3c3c3c;
    background: repeating-conic-gradient(from 30deg, #0000 0 120deg, var(--c3) 0 180deg)
        calc(0.5 * var(--s)) calc(0.5 * var(--s) * 0.577),
      repeating-conic-gradient(from 30deg, var(--c1) 0 60deg, var(--c2) 0 120deg, var(--c3) 0 180deg);
    background-size: var(--s) calc(var(--s) * 0.577);
}

/* Upload card */
.upload-box {
    background-color: white;
    padding: 2.5rem 2rem;
    border-radius: 20px;
    width: 480px;
    margin: 5vh auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    text-align: center;
    position: relative;
    z-index: 10;
}

/* Heading */
.upload-title {
    font-size: 20px;
    font-weight: 600;
    color: #333;
    margin-bottom: 1.5rem;
}

/* Drag zone look */
.custom-upload {
    border: 2px dashed #7AAFE4;
    border-radius: 12px;
    background-color: #D0E8FF;
    padding: 2rem 1rem;
    margin-bottom: 1.5rem;
    color: #2E3B4E;
    font-weight: 500;
}

/* Buttons */
.download-button, .close-button {
    width: 100%;
    border: none;
    padding: 0.75rem;
    border-radius: 10px;
    font-weight: 600;
    font-size: 16px;
    margin-top: 1rem;
}

.download-button {
    background-color: #3498DB;
    color: white;
}

.download-button:hover {
    background-color: #2980B9;
}

.close-button {
    background-color: #FF5E5E;
    color: white;
}

.close-button:hover {
    background-color: #E04848;
}
</style>
""", unsafe_allow_html=True)

# ✅ Main UI block
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
st.markdown('<div class="upload-title">UPLOAD SOR PDF FILE</div>', unsafe_allow_html=True)

# Upload
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
st.markdown('<div class="custom-upload">Drag your PDF file here or click to browse</div>', unsafe_allow_html=True)

# Handle uploaded PDF
if uploaded_file:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    save_path = os.path.join(UPLOAD_DIR, filename)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully. Extracting content...")

    # Convert PDF → DataFrame
    df = extract_structured_items_from_pdf(save_path)
    st.dataframe(df, use_container_width=True)

    # Download Excel
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    st.download_button(
        label="📥 Download Excel",
        data=output,
        file_name=f"{timestamp}_SOR_Extracted.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_excel"
    )

    # Close (reload) button
    st.markdown(
        '<button class="close-button" onclick="window.location.reload();">Close</button>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)
