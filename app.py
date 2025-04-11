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
    




########### Streamlit Functions ##############
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
