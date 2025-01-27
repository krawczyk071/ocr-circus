import streamlit as st  
from app import runner

st.set_page_config(layout="wide", page_title="LLM Tool")
st.header("Upload file")
uploaded_file = st.file_uploader("Please upload your PDF document:", type= "pdf")
if uploaded_file is not None:

    col1, col2 = st.columns(2)
    with col1:
        start_page = st.number_input("Start Page", min_value=0)
    with col2:
        end_page = st.number_input("End Page", min_value=0)
    
    st.write("PDF loaded")
    # st.write(type(uploaded_file))

def download_file(filename):
    with open(filename, "rb") as file:
        btn = st.download_button(
            label="Download file",
            data=file,
            file_name='out.md',
            mime="application/octet-stream"
            )
        return btn

if st.button("Transform to MD"):
    with st.spinner("Generating answer"):

        # file_contents = uploaded_file.read()
        # Process action
        runner(uploaded_file, start_page, end_page) 
        
        answer = "md ready to download at"
        
        placeholder = st.empty()
        placeholder = st.write(answer)
        ph = download_file('../output/output.md')