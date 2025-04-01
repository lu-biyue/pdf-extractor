import streamlit as st
import os
import pandas as pd
from datetime import datetime
from io import BytesIO
from sor_converter import extract_structured_items_from_pdf

# Setup
st.set_page_config(page_title="SOR PDF Extractor", layout="centered")
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Inject CSS for appearance
st.markdown("""
    <style>
    section[data-testid="stFileUploader"] > div:first-child {
        background-color: #D0E8FF;
        border: 2px dashed #7AAFE4;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    body {
        background-color: #2E3B4E;
        font-family: 'Arial', sans-serif;
    }
    .upload-box {
        background-color: #3498DB;
        padding: 2rem;
        border-radius: 20px;
        width: 500px;
        margin: auto;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        color: white;
    }
    .upload-header {
        font-size: 20px;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
    }
    .drag-hint {
        background-color: #A9D6F2;
        border: 2px dashed white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        font-size: 16px;
        color: #2E3B4E;
        margin-bottom: 1.5rem;
    }
    .uploaded-info {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        color: #333;
    }
    .progress-bar {
        background-color: #4CAF50;
        height: 8px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .close-btn {
        background-color: #F56C6C;
        color: white;
        padding: 0.7rem 1.5rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        width: 100%;
        margin-top: 2rem;
    }
    .close-btn:hover {
        background-color: #FF4C4C;
    }
    </style>
""", unsafe_allow_html=True)

# Upload Box
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
st.markdown('<div class="upload-header">UPLOAD SOR PDF FILE</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag your file here or browse", 
    type=["pdf"], 
    label_visibility="collapsed"
)

# Simulate drag box
# st.markdown('<div class="drag-hint">Drag your PDF file here or click to browse</div>', unsafe_allow_html=True)

# Handle file upload and conversion
if uploaded_file:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    save_path = os.path.join(UPLOAD_DIR, filename)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    # Simulate loading/progress
    st.info("🔄 Processing your PDF...")
    progress = st.progress(0)
    for i in range(0, 101, 20):
        progress.progress(i)

    df = extract_structured_items_from_pdf(save_path)

    st.success(f"✅ Extracted {len(df)} items.")
    st.markdown('<div class="uploaded-info">Preview of extracted data:</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    # Download Excel
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    st.download_button(
        "📥 Download Excel",
        data=output,
        file_name=f"{timestamp}_SOR_Extracted.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Close (reload) button
    st.markdown("""
        <button class="close-btn" onclick="window.location.reload();">CLOSE</button>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
