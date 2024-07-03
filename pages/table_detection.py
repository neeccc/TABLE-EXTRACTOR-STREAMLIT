import io
import streamlit as st
from scan_table import pdf_to_excel
from pathlib import Path

from store_file import save_image
from PIL import Image

import numpy as np
import pandas as pd

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

import pytesseract
from pytesseract import Output

from ultralyticsplus import YOLO, render_result
from img2table.document import Image as ImageDoc
from img2table.ocr import TesseractOCR


def render_image(path):
    st.divider()
    st.image(path)
    img = Image.open(path)

    st.divider()
    # load model
    model = YOLO("keremberke/yolov8m-table-extraction")

    # set model parameters
    model.overrides["conf"] = 0.25  # NMS confidence threshold
    model.overrides["iou"] = 0.45  # NMS IoU threshold
    model.overrides["agnostic_nms"] = False  # NMS class-agnostic
    model.overrides["max_det"] = 1000  # maximum number of detections per image
    results = model.predict(img)

    # observe results
    st.write("Boxes: ", results[0].boxes)
    render = render_result(model=model, image=img, result=results[0])
    render

    st.divider()

    cuda_tensor = results[0].boxes

    # Move the CUDA tensor to CPU
    cpu_tensor = cuda_tensor.cpu()

    # Convert to NumPy array
    numpy_array = cpu_tensor.data.numpy()

    # Then proceed with your tuple unpacking
    x1, y1, x2, y2, _, _ = tuple(int(item) for item in numpy_array[0])
    img = np.array(img)
    # cropping
    cropped_image = img[y1:y2, x1:x2]
    cropped_image = Image.fromarray(cropped_image)
    cropped_image.save("test.png", "png")

    ext_df = pytesseract.image_to_data(
        cropped_image,
        output_type=Output.DATAFRAME,
        config="--psm 6 --oem 3",
        lang="eng+jpn",
    )
    st.write(ext_df)

    # Instantiation of OCR
    ocr = TesseractOCR(n_threads=1, lang="eng")

    # Instantiation of document, either an image or a PDF
    doc = ImageDoc("test.png")

    # Table extraction
    extracted_tables = doc.to_xlsx(
        "output.xlsx",
        ocr=ocr,
        implicit_rows=True,
        borderless_tables=True,
    )
    with open("output.xlsx", "rb") as b:
        st.download_button("Download Excel", b, "output.xlsx")


uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg"])

if st.button("Procces Image"):
    with st.spinner("Proccessing Image...."):
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            path = save_image(bytes_data)
            render_image(path)

        else:
            st.error("No file selected!")
