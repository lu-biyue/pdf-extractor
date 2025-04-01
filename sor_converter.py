# import streamlit as st
# import pandas as pd
# import fitz  # PyMuPDF
# import re
# import textwrap
# import io

# def extract_items_from_pdf(file):
#     doc = fitz.open(stream=file.read(), filetype="pdf")
#     data = []
#     pattern = re.compile(r'\b(A\d{6})\b')

#     for page_num in range(len(doc)):
#         blocks = doc.load_page(page_num).get_text("blocks")
#         blocks = sorted(blocks, key=lambda b: b[1])

#         for block in blocks:
#             lines = block[4].split('\n')
#             for line in lines:
#                 line = line.strip()
#                 if not line:
#                     continue
#                 match = pattern.search(line)
#                 if match:
#                     item_no = match.group(1)
#                     desc = line.replace(item_no, '').strip()
#                     data.append({"Item No.": item_no, "Description": desc})
#                 elif data:
#                     data[-1]["Description"] += ' ' + line.strip()

#     if not data:
#         return pd.DataFrame(columns=["Item No.", "Description", "Unit", "Rate (S$)"])

#     for item in data:
#         words = item["Description"].split()
#         wrapped = textwrap.wrap(" ".join(words), width=90)
#         item["Description"] = "\n".join(wrapped)

#     df = pd.DataFrame(data)

#     unit_rate_pattern = re.compile(r'(Unit|No|Set|Each|Lot)?\s*[\$S]?([\d,]+\.\d{2})')
#     units, rates = [], []
#     for desc in df["Description"].str.replace('\n', ' '):
#         match = unit_rate_pattern.search(desc)
#         if match:
#             units.append(match.group(1) or '')
#             rates.append(match.group(2))
#         else:
#             units.append('')
#             rates.append('')
#     df["Unit"] = units
#     df["Rate (S$)"] = rates

#     return df

# st.title("PDF Item Extractor")
# st.markdown("Upload a PDF file with structured item data. The app will extract Item No, Description, Unit, and Rate, and allow you to download the results as an Excel file.")

# uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# if uploaded_file:
#     df = extract_items_from_pdf(uploaded_file)

#     if df.empty:
#         st.warning("No items were extracted from the uploaded PDF. Please check the format.")
#     else:
#         st.success("Extraction completed!")
#         st.dataframe(df)

#         buffer = io.BytesIO()
#         df.to_excel(buffer, index=False)
#         buffer.seek(0)

#         st.download_button(
#             label="Download as Excel",
#             data=buffer,
#             file_name="extracted_items.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

# sor_converter.py

import fitz  # PyMuPDF
import pandas as pd
import re

def extract_structured_items_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pattern_item = re.compile(r'\b([A-Z0-9]{6,})\b')
    pattern_rate = re.compile(r'(Unit|No|Set|Each|Lot|Sys|m|kg|pair|Pa|RT|kW|Job|Per Job)?\s*[\$S]?([\d,]+\.\d{2})')

    data = []
    current_header = ""
    capture_next_lines = False
    header_lines = []

    for page in doc:
        lines = page.get_text().split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Detect section headers like A110000
            if re.fullmatch(r'[A-Z]{1,3}\d{4}00', line):
                capture_next_lines = True
                header_lines = []
                continue

            if capture_next_lines:
                if len(header_lines) < 6:
                    header_lines.append(line)
                    continue
                else:
                    current_header = " ".join(header_lines).strip()
                    capture_next_lines = False
                    continue

            match = pattern_item.match(line)
            if match:
                item_no = match.group(1)
                remaining = line.replace(item_no, '').strip()

                unit, rate = '', ''
                match_rate = pattern_rate.search(line)
                if match_rate:
                    unit = match_rate.group(1) or ''
                    rate = match_rate.group(2)
                    remaining = remaining.replace(match_rate.group(0), '').strip()

                data.append({
                    "Item No.": item_no,
                    "Header": current_header,
                    "Description": remaining,
                    "Unit": unit,
                    "Rate (S$)": rate
                })

    return pd.DataFrame(data)
