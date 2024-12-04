from flask import Flask, request, send_file
from flask_cors import CORS
from pdf2docx import Converter
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (frontend -> backend)

@app.route('/')
def home():
    # This route is for testing if the backend is live
    return """
    <h1>Welcome to PDF to DOCX Converter</h1>
    <p>Use the <code>/convert</code> endpoint to upload a PDF and get a DOCX file.</p>
    """

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    try:
        # Check if file is uploaded
        if 'file' not in request.files:
            return "No file uploaded", 400

        pdf_file = request.files['file']

        # Validate file type
        if not pdf_file.filename.endswith('.pdf'):
            return "Invalid file type. Please upload a PDF.", 400

        # Save the uploaded file to /tmp (Render's writable directory)
        input_path = os.path.join('/tmp', pdf_file.filename)
        pdf_file.save(input_path)

        # Set output path for the converted file
        output_path = os.path.join('/tmp', 'converted.docx')

        # Convert PDF to DOCX
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()

        # Send the converted DOCX file back to the user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        # Log the error for debugging in Render logs
        print(f"Error during conversion: {e}")
        return f"Conversion failed: {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
