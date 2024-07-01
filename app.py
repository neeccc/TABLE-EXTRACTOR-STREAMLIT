import streamlit as st
from streamlit_navigation_bar import st_navbar
from scan_table import pdf_to_excel
from pathlib import Path

from store_file import save_file

f = ""

st.title("WIRATEK AI ")

uploaded_file = st.file_uploader("Choose a file", type="pdf")

if st.button("PROCCESS FILE"):
    with st.spinner("Proccessing file......."):
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            path = save_file(bytes_data)
            xls = pdf_to_excel(path=path)
            with open(xls, "rb") as f:
                st.success("File Proccessed")
                st.download_button("Download", f, Path(xls).name)

        else:
            st.error("No file selected!")
