from img2table.ocr import TesseractOCR
from img2table.document import PDF
import os

XLS_FOLDER = "xls/"


def pdf_to_excel(path) -> str:
    if os.path.exists(XLS_FOLDER) == False:
        os.mkdir(XLS_FOLDER)
    pdf = PDF(src=path)
    ocr = TesseractOCR(
        lang="eng+jpn",
    )
    filename = os.path.basename(path)
    xlsPath = XLS_FOLDER + os.path.splitext(filename)[0] + ".xlsx"
    pdf.to_xlsx(
        xlsPath,
        ocr=ocr,
        borderless_tables=True,
        implicit_rows=True,
        min_confidence=90,
    )
    return xlsPath
