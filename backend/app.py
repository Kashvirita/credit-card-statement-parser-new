import fitz
import re
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from parser import UniversalCCParser

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all routes, allowing requests from any origin
CORS(app) 

# --- No other changes needed for the backend ---
# The /parse route and parser logic remain the same.

@app.route('/parse', methods=['POST'])
def parse_pdf():
    if 'statement' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['statement']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            pdf_bytes = file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = "".join(page.get_text() for page in doc)
            doc.close()

            parser_obj = UniversalCCParser(text)
            extracted_data = parser_obj.extract_all_data()

            return jsonify(extracted_data)
        except Exception as e:
            return jsonify({"error": f"An error occurred during parsing: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type, please upload a PDF"}), 400

if __name__ == '__main__':
    # Flask will run on its default port 5000
    app.run(debug=True)

