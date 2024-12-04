from flask import Flask, request, send_file, render_template
from flask_cors import CORS
import os
from pdf2docx import Converter

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (useful for frontend-backend interaction)

# Serve the frontend page
@app.route('/')
def home():
    return render_template('index.html')  # Renders index.html from the templates directory

# File conversion endpoint
@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            return "No file uploaded", 400

        pdf_file = request.files['file']

        # Validate the file type
        if not pdf_file.filename.endswith('.pdf'):
            return "Invalid file type. Please upload a PDF.", 400

        # Save the uploaded file in the /tmp directory (Render's writable directory)
        input_path = os.path.join('/tmp', pdf_file.filename)
        pdf_file.save(input_path)

        # Set the output file path
        output_path = os.path.join('/tmp', 'converted.docx')

        # Convert the PDF to DOCX
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()

        # Send the converted file to the user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        # Log the error and return an error response
        print(f"Error during conversion: {e}")
        return f"Conversion failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
