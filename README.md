# 📊 SOR Rate Comparison Tool

A simple and efficient Streamlit app that allows users to compare rates across multiple SOR documents — extract, match, and validate with ease.

---

## 🚀 Features
- Upload Excel files with multiple SORs
- Automatically extract and compare rates
- Highlight price discrepancies and match scores
- Download a color-coded comparison Excel file

---

## 🖥️ How to Run the App Locally

### 1. Make sure the following files are in your main project folder:

	1.	app.py         # The main Streamlit interface
	2.	final.py       # Contains processing and Excel formatting logic
	3.	requirements.txt

### 2. Install the required libraries:
(We recommend using a virtual environment)

```bash
pip install -r requirements.txt

streamlit run app.py    # Run the Streamlit app

## 🧪 Testing the System

To ensure your input Excel file works correctly, follow these guidelines:

### ✅ Required Sheet Structure

- **Base SOR Sheet**  
  Include a sheet named:  
INPUT 1 (ACMV)
This should contain the main SOR data you want to compare from (e.g. MOE ACMV).

- **Comparison SOR Sheets**  
Add one or more sheets to compare against.  
Name them using this format:  
SOR 1 (Name), SOR 2 (Name), etc.

- **Header Comparison Sheet**  
Include a sheet that matches the column headers between ACMV and each SOR.  
Make sure the column names exactly match the sheet names used (e.g. "SOR 1 (Name)").

### 📄 Reference Template

Use the file below as a reference for formatting and structure:
Cleaned_Input_Files final.xlsx

### ✅ Output Example

If everything is set up correctly, the tool will generate a structured output file named:
ACMV_10_Apr_25.xlsx
This file will include all comparison results, rate differences, and color-coded highlights.
