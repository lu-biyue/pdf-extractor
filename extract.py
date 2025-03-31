import fitz  # PyMuPDF
import pandas as pd
import re
import os
from pathlib import Path
import textwrap

def extract_items_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    data = []
    pattern = re.compile(r'\b(A\d{6})\b')

    for page_num in range(len(doc)):
        blocks = doc.load_page(page_num).get_text("blocks")
        blocks = sorted(blocks, key=lambda b: b[1])  # Sort top-down

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

    # Wrap description to approx 15 words per line (based on character width)
    for item in data:
        words = item["Description"].split()
        wrapped = textwrap.wrap(" ".join(words), width=15 * 6)  # Approx 90 characters
        item["Description"] = "\n".join(wrapped)

    df = pd.DataFrame(data)

    # Optional: attempt to extract 'Unit' and 'Rate' from description
    unit_rate_pattern = re.compile(r'(Unit|No|Set|Each|Lot)?\s*[\$S]?([\d,]+\.\d{2})')
    units, rates = [], []
    for desc in df["Description"]:
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

def save_to_excel(df, output_path):
    df.to_excel(output_path, index=False)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract Item No, Description, Unit, Rate from PDF")
    parser.add_argument("pdf_path", help="Path to input PDF file")
    parser.add_argument("--output", help="Output Excel path", default="output.xlsx")
    args = parser.parse_args()

    if not Path(args.pdf_path).exists():
        print(f"File not found: {args.pdf_path}")
        exit(1)

    print(f"Extracting from {args.pdf_path}...")
    df = extract_items_from_pdf(args.pdf_path)
    save_to_excel(df, args.output)
    print(f"Done! Extracted data saved to {args.output}")

# Usage:
# python3 extract.py sor_copy.pdf --output output3.xlsx