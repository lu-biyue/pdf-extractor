import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
import textwrap
import io

def extract_items_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    data = []
    pattern = re.compile(r'\b(A\d{6})\b')

    for page_num in range(len(doc)):
        blocks = doc.load_page(page_num).get_text("blocks")
        blocks = sorted(blocks, key=lambda b: b[1])

        for block in blocks:
            lines = block[4].split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                match = pattern.search(line)
                if match:
                    item_no = match.group(1)
                    desc = line.replace(item_no, '').strip()
                    data.append({"Item No.": item_no, "Description": desc})
                elif data:
                    data[-1]["Description"] += ' ' + line.strip()

    if not data:
        return pd.DataFrame(columns=["Item No.", "Description", "Unit", "Rate (S$)"])

    for item in data:
        words = item["Description"].split()
        wrapped = textwrap.wrap(" ".join(words), width=90)
        item["Description"] = "\n".join(wrapped)

    df = pd.DataFrame(data)

    unit_rate_pattern = re.compile(r'(Unit|No|Set|Each|Lot)?\s*[\$S]?([\d,]+\.\d{2})')
    units, rates = [], []
    for desc in df["Description"].str.replace('\n', ' '):
        match = unit_rate_pattern.search(desc)
        if match:
            units.append(match.group(1) or '')
            rates.append(match.group(2))
        else:
            units.append('')
            rates.append('')
    df["Unit"] = units
    df["Rate (S$)"] = rates

    return df

st.title("PDF Item Extractor")
st.markdown("Upload a PDF file with structured item data. The app will extract Item No, Description, Unit, and Rate, and allow you to download the results as an Excel file.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    df = extract_items_from_pdf(uploaded_file)

    if df.empty:
        st.warning("No items were extracted from the uploaded PDF. Please check the format.")
    else:
        st.success("Extraction completed!")
        st.dataframe(df)

        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            label="Download as Excel",
            data=buffer,
            file_name="extracted_items.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
