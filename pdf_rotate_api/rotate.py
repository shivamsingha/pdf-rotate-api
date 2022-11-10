import json
from PyPDF2 import PdfReader, PdfWriter
from constants import UPLOAD_FOLDER


def rotate(filename, angle_of_rotation, page_number, file):
    reader = PdfReader(file)

    try:
        if page_number > len(reader.pages):
            with open(f"{UPLOAD_FOLDER}/output_{filename}.json", "w") as fp:
                fp.write(
                    json.dumps(
                        {
                            "error": "Invalid Input",
                            "message": "page_number exceeds number of pages in uploaded file.",
                        }
                    )
                )
                return

    except Exception as exc:
        with open(f"{UPLOAD_FOLDER}/output_{filename}.json", "w") as fp:
            fp.write(
                json.dumps(
                    {
                        "error": "Invalid PDF File",
                        "message": "Unable to read uploaded file.",
                    }
                )
            )
            return

    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.pages[page_number - 1].rotate(angle_of_rotation)

    with open(f"{UPLOAD_FOLDER}/output_{filename}", "wb") as fp:
        writer.write(fp)
