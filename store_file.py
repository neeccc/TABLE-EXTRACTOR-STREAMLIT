import datetime
import os

PDF_FOLDER = "pdf/"
IMG_FOLDER = "img/"


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


def save_image(file) -> str:
    if os.path.exists(IMG_FOLDER) == False:
        os.mkdir(IMG_FOLDER)
    filename = IMG_FOLDER + "tables-{date:%Y-%m-%d_%H:%M:%S}".format(
        date=datetime.datetime.now()
    )
    path = filename + ".png"
    with open(path, "wb") as f:
        f.write(file)
    return path
