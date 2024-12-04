from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from pdf2docx import Converter
import os

app = Flask(__name__, template_folder="templates")
CORS(app)  # Allow frontend to communicate with backend

# Serve the homepage
@app.route('/')
def home():
    return render_template('index.html')

# File conversion route
@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    pdf_file = request.files['file']

    if not pdf_file.filename.endswith('.pdf'):
        return "Invalid file type. Please upload a PDF.", 400

    # Save the uploaded file temporarily
    input_path = os.path.join('temp', pdf_file.filename)
    os.makedirs('temp', exist_ok=True)  # Create temp directory if it doesn't exist
    pdf_file.save(input_path)

    # Convert PDF to DOCX
    output_path = os.path.join('temp', 'converted.docx')
    try:
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()
    except Exception as e:
        return f"Conversion failed: {e}", 500

    # Return the converted DOCX file
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
