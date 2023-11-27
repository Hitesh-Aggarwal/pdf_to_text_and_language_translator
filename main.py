from flask import (
    Flask,
    request,
    send_file,
    render_template,
    send_from_directory,
    jsonify,
)
from googletrans import Translator

from PyPDF2 import PdfReader
import os

app = Flask(__name__)


@app.route("/")
def index_get():
    return render_template("index.html")


@app.route("/bootstrap-5.3.1-dist/<path:filename>")
def serve_static(filename):
    return send_from_directory("bootstrap-5.3.1-dist", filename)


@app.route("/images/<path:filename>")
def serve_images(filename):
    return send_from_directory("images", filename)


@app.route("/language_translator")
def language_translator():
    return render_template("language_translator.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/convert_pdf", methods=["POST"])
def convert_pdf():
    print("Received request to convert PDF")
    if "file" not in request.files:
        return "No file part", 400

    pdf_file = request.files["file"]

    if pdf_file.filename == "":
        return "No selected file", 400

    if pdf_file:
        file_path = os.path.join("uploads", pdf_file.filename)
        pdf_file.save(file_path)

        output_path = file_path.replace(".pdf", ".txt")
        output_text = ""

        reader = PdfReader(file_path)
        for page in reader.pages:
            output_text += page.extract_text()

        with open(output_path, "w") as txt_file:
            txt_file.write(output_text)

        return send_file(output_path, as_attachment=True)


@app.route("/translate", methods=["POST"])
def translate():
    # Get the selected languages from the front end
    from_language = request.form.get("from_language")
    to_language = request.form.get("to_language")

    # Get the text to be translated from the front end
    text_to_translate = request.form.get("text_to_translate")

    # Perform translation
    translator = Translator()
    translated_text = translator.translate(
        text_to_translate, src=from_language, dest=to_language
    ).text

    # Return translated text to the front end
    return jsonify({"translated_text": translated_text})


if __name__ == "__main__":
    app.run(debug=True)
