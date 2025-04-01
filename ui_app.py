# upload_ui_app.py
import streamlit as st
import os
import pandas as pd
from datetime import datetime
from io import BytesIO
from structured_sor_extractor_v1 import extract_structured_items_from_pdf  # ✅ Import your function

# Setup
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
st.set_page_config(page_title="SOR PDF Uploader", layout="centered")

st.markdown("""
<style>
body { background-color: #8CB7F5; }
.upload-box {
    background-color: white;
    padding: 2rem;
    border-radius: 16px;
    width: 360px;
    margin: auto;
    box-shadow: 0 4px 24px rgba(0,0,0,0.1);
}
.upload-header {
    text-align: center;
    font-size: 14px;
    color: #999;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-box">', unsafe_allow_html=True)
st.markdown('<div class="upload-header">UPLOAD SOR PDF FILE</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Drop a PDF here or click to browse", type=["pdf"], label_visibility="collapsed")

if uploaded_file:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    save_path = os.path.join(UPLOAD_DIR, filename)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    # ✅ Use your converter function
    st.info("🔄 Extracting structured items from PDF...")
    df = extract_structured_items_from_pdf(save_path)

    st.success(f"✅ Extracted {len(df)} items.")
    st.dataframe(df, use_container_width=True)

    # 📥 Download Excel
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button("📥 Download Excel", data=buffer, file_name=f"{timestamp}_extracted.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("</div>", unsafe_allow_html=True)
