from flask import Flask, request, send_file
from flask_cors import CORS
from pdf2docx import Converter
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (useful for frontend communication)

# Home route to check if the server is running
@app.route('/')
def home():
    return "Welcome to the PDF to DOCX Converter API!"

# File conversion route
@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            return "No file uploaded", 400

        pdf_file = request.files['file']

        # Validate file type
        if not pdf_file.filename.endswith('.pdf'):
            return "Invalid file type. Please upload a PDF file.", 400

        # Save the uploaded file to /tmp (Render's writable directory)
        input_path = os.path.join('/tmp', pdf_file.filename)
        pdf_file.save(input_path)

        # Set output file path in /tmp
        output_path = os.path.join('/tmp', 'converted.docx')

        # Convert PDF to DOCX
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()

        # Return the converted file as a response
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        # Log error to Render's logs and return error response
        print(f"Error during conversion: {e}")
        return f"Conversion failed: {e}", 500

if __name__ == "__main__":
    # Run the app locally for testing
    app.run(host="0.0.0.0", port=5000, debug=True)
