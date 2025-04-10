import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import shutil
from final import main, color_check_cells, copy_sheet

# Page configuration
st.set_page_config(
    page_title="PDF to Excel Converter",
    layout="wide",
    page_icon="📄",
)

st.image("https://cdn-icons-png.flaticon.com/512/124/124837.png", width=78)

st.write(
    """
    # SOR Rate Comparison
    """
)

st.info(
    """
    Compare SOR with a single click!
    """,
    icon="🎯",
)

with st.expander("ℹ️ How to use this app"):
    st.markdown("""
    **Step 1:** Upload your Excel file using the file uploader above.  
    **Step 2:** Wait for the app to process and extract the data.  
    **Step 3:** Preview the extracted or compared data on the screen.  
    **Step 4:** Click the download button to save the final Excel output.  
    """)

# with st.expander("📺 Watch a video tutorial here!"):
#     st.markdown("Here’s a quick walkthrough video:")
#     try:
#         video_bytes = open("demo.mp4", "rb").read() 
#         st.video(video_bytes)
#     except FileNotFoundError:
#         st.error("❌ demo.mov not found in the repo.")
    
st.divider()

# Upload Section
uploaded_file = st.file_uploader("📤 Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    status_msg = st.empty()  # Create a placeholder for status updates
    status_msg.success("✅ File uploaded. Running comparison...")

    # Set output path
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    date = datetime.today().strftime('%d_%b_%y')
    input_path = f"input_{timestamp}.xlsx"
    output_path = f"ACMV_{date}.xlsx"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        main(input_path, output_path)
        color_check_cells(output_path)
        copy_sheet(input_path, output_path)
        # st.success("✅ Excel comparison completed!")
        status_msg.success("✅ Excel comparison completed!")

        # Load and display results
        df = pd.read_excel("output.xlsx", sheet_name="ACMV")
        st.dataframe(df, use_container_width=True)

        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 Download Result File",
                data=file,
                file_name=output_path,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")

else:
    st.info("Please upload an Excel to begin.")
    
# uploaded_file = st.file_uploader("📤 Upload your Excel file", type=["xlsx", "xls"])
# if uploaded_file:
#     st.success("File uploaded. Running comparison...")

# # Save file before processing
# timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
# filename = f"{timestamp}_{uploaded_file.name}"

# with open(filename, "wb") as f:
#     f.write(uploaded_file.read())

# try:
#     main()
#     color_check_cells()
#     st.success("✅ Excel comparison completed!")

#     # Load final sheet from output file
#     df = pd.read_excel("output.xlsx", sheet_name="ACMV")
#     st.dataframe(df, use_container_width=True)

#     with open("output.xlsx", "rb") as file:
#         st.download_button(
#             label="📥 Download Result File",
#             data=file,
#             file_name="output.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

# except Exception as e:
#     st.error(f"⚠️ An error occurred: {e}")
    
        
    # # Process file
    # with st.spinner("🔍 Extracting data..."):
    #     df = extract_structured_items_from_pdf(filename)

    # # Preview
    # st.subheader("📋 Preview Extracted Data")
    # st.dataframe(df, use_container_width=True)

    # # Download
    # buffer = BytesIO()
    # df.to_excel(buffer, index=False)
    # buffer.seek(0)

    # st.download_button(
    #     label="📥 Download Excel File",
    #     data=buffer,
    #     file_name=f"{timestamp}_output.xlsx",
    #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # )
    
# import streamlit as st
# import os
# import pandas as pd
# from datetime import datetime
# from io import BytesIO
# from sor_converter import extract_structured_items_from_pdf  # Make sure this file is in your project

# # Streamlit setup
# st.set_page_config(page_title="SOR PDF Extractor", layout="centered")
# UPLOAD_DIR = "uploaded_files"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # ✅ Inject CSS
# st.markdown("""
# <style>
# /* Hide default Streamlit elements */
# #MainMenu, footer, header {visibility: hidden;}

# /* Apply custom background to full page */
# body {
#     background-color: #2E3B4E;
#     font-family: 'Segoe UI', sans-serif;

#     --s: 200px;
#     --c1: #1d1d1d;
#     --c2: #4e4f51;
#     --c3: #3c3c3c;
#     background: repeating-conic-gradient(from 30deg, #0000 0 120deg, var(--c3) 0 180deg)
#         calc(0.5 * var(--s)) calc(0.5 * var(--s) * 0.577),
#       repeating-conic-gradient(from 30deg, var(--c1) 0 60deg, var(--c2) 0 120deg, var(--c3) 0 180deg);
#     background-size: var(--s) calc(var(--s) * 0.577);
# }

# /* Upload card styling */
# .upload-box {
#     background-color: white;
#     padding: 2.5rem 2rem;
#     border-radius: 20px;
#     width: 480px;
#     margin: 5vh auto;
#     box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
#     text-align: center;
#     position: relative;
#     z-index: 10;
# }

# /* Heading */
# .upload-title {
#     font-size: 20px;
#     font-weight: 600;
#     color: #333;
#     margin-bottom: 1.5rem;
# }

# /* Buttons */
# .download-button, .close-button {
#     width: 100%;
#     border: none;
#     padding: 0.75rem;
#     border-radius: 10px;
#     font-weight: 600;
#     font-size: 16px;
#     margin-top: 1rem;
# }

# .download-button {
#     background-color: #3498DB;
#     color: white;
# }

# .download-button:hover {
#     background-color: #2980B9;
# }

# .close-button {
#     background-color: #FF5E5E;
#     color: white;
# }

# .close-button:hover {
#     background-color: #E04848;
# }
# </style>
# """, unsafe_allow_html=True)

# # ✅ Main UI block
# st.markdown('<div class="upload-box">', unsafe_allow_html=True)
# st.markdown('<div class="upload-title">UPLOAD SOR PDF FILE</div>', unsafe_allow_html=True)

# # Upload
# uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

# # Handle uploaded PDF
# if uploaded_file:
#     timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
#     filename = f"{timestamp}_{uploaded_file.name}"
#     save_path = os.path.join(UPLOAD_DIR, filename)

#     with open(save_path, "wb") as f:
#         f.write(uploaded_file.read())

#     st.success("✅ File uploaded successfully. Extracting content...")

#     # Convert PDF → DataFrame
#     df = extract_structured_items_from_pdf(save_path)
#     st.dataframe(df, use_container_width=True)

#     # Download Excel
#     output = BytesIO()
#     df.to_excel(output, index=False)
#     output.seek(0)

#     st.download_button(
#         label="📥 Download Excel",
#         data=output,
#         file_name=f"{timestamp}_SOR_Extracted.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         key="download_excel"
#     )

#     # Close (reload) button
#     st.markdown(
#         '<button class="close-button" onclick="window.location.reload();">Close</button>',
#         unsafe_allow_html=True
#     )

# st.markdown('</div>', unsafe_allow_html=True)

# import streamlit as st
# import pandas as pd
# from io import BytesIO
# from datetime import datetime

# # Sample data
# data = pd.DataFrame({
#     "Name": ["Alice", "Bob"],
#     "Score": [85, 92]
# })

# # File for download simulation
# download_content = BytesIO()
# download_content.write(b"Hello from your download!")
# download_content.seek(0)

# # Page setup
# st.set_page_config(page_title="Streamlit UI Showcase", layout="centered")

# # Streamlit-style hierarchy
# st.title("My title")
# st.header("My header")
# st.subheader("My sub")

# st.markdown("_Markdown_")
# st.text("Fixed width text")
# st.caption("Balloons. Hundreds of them...")
# st.latex(r"e^{i\pi} + 1 = 0")
# st.write("Most objects")
# st.write(["st", "is <", 3])
# st.code("for i in range(8): foo()")

# st.divider()

# # Input widgets
# st.button("Hit me")
# st.checkbox("Check me out")
# st.radio("Pick one:", ["nose", "ear"])
# st.selectbox("Select", [1, 2, 3])
# st.multiselect("Multiselect", [1, 2, 3])
# st.slider("Slide me", min_value=0, max_value=10)
# st.select_slider("Slide to select", options=[1, "2"])
# st.text_input("Enter some text")
# st.number_input("Enter a number")
# st.text_area("Area for textual entry")
# st.date_input("Date input")
# st.time_input("Time entry")
# st.file_uploader("File uploader")
# st.camera_input("一二三,茄子!")
# st.color_picker("Pick a color")

# st.download_button(
#     label="On the dl",
#     data=download_content,
#     file_name="demo.txt",
#     mime="text/plain"
# )
