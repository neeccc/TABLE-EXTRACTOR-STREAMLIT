import datetime
import os

PDF_FOLDER = "pdf/"


def save_file(file) -> str:
    if os.path.exists(PDF_FOLDER) == False:
        os.mkdir(PDF_FOLDER)
    filename = PDF_FOLDER + "tables-{date:%Y-%m-%d_%H:%M:%S}".format(
        date=datetime.datetime.now()
    )
    path = filename + ".pdf"
    with open(path, "wb") as f:
        f.write(file)
    return path
