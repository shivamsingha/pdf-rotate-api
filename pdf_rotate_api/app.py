import json
import os
import hashlib
from pathlib import Path
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import safe_join
from constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from rotate import rotate

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 32 * 1000 * 1000


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    angle_of_rotation = request.form["angle_of_rotation"]
    page_number = request.form["page_number"]

    if angle_of_rotation not in ["90", "180", "270"]:
        return json.dumps(
            {"error": "Invalid Input", "message": "Only 90, 180, 270 degrees allowed."}
        )

    if page_number != "" and not page_number.isnumeric():
        return json.dumps(
            {
                "error": "Invalid Input",
                "message": "page_number should be a number between 1 and n (n is the number of pages in the pdf file).",
            }
        )

    angle_of_rotation = int(angle_of_rotation)
    page_number = int(page_number)

    if file and allowed_file(file.filename):
        digest = hashlib.file_digest(file, "sha256")
        filename = digest.hexdigest() + secure_filename(file.filename)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        rotate(filename, angle_of_rotation, page_number, file)

        return json.dumps(
            {"status": "processing", "downloadURL": f"/output_{filename}"}
        )


@app.route("/<path:filename>", methods=["GET"])
def download(filename):
    filepath = safe_join(app.config["UPLOAD_FOLDER"], filename)
    path = Path(filepath)
    if path.is_file():
        return send_from_directory(
            app.config["UPLOAD_FOLDER"], filename, as_attachment=True
        )

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".json")


app.run()
