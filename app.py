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

# Inject CSS for design
st.markdown("""
<style>
body {
    background-color: #F3F6FA;
}
.upload-box {
    background-color: white;
    padding: 2rem;
    border-radius: 20px;
    width: 450px;
    margin: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}
.upload-title {
    text-align: center;
    font-size: 16px;
    color: #888;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-box">', unsafe_allow_html=True)
st.markdown('<div class="upload-title">UPLOAD SOR PDF FILE</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Drag and drop or browse PDF", type=["pdf"], label_visibility="collapsed")

if uploaded_file:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    save_path = os.path.join(UPLOAD_DIR, filename)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    # Process and display
    st.info("🔍 Extracting items...")
    df = extract_structured_items_from_pdf(save_path)

    st.success(f"✅ {len(df)} items extracted.")
    st.dataframe(df, use_container_width=True)

    # Excel download button
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    st.download_button("📥 Download Excel", buffer,
                       file_name=f"{timestamp}_SOR_Extracted.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("</div>", unsafe_allow_html=True)
