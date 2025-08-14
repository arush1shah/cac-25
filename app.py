print("Starting Flask app...")

from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os
from openai import OpenAI
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

OPENAI_API_KEY = "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"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Initialize OpenAI client (make sure to set your API key as an environment variable before running)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", OPENAI_API_KEY))

def simplify_text(text):
    """Send extracted text to GPT for simplification."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use "gpt-4o" for higher quality
        messages=[
            {"role": "system", "content": "You are a helpful assistant that simplifies text for easy understanding."},
            {"role": "user", "content": f"Summarize this text with much fewer words:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # (OPTIONAL) Set path to tesseract binary if needed:
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # OCR: extract text from image
    image = Image.open(filepath)
    extracted_text = pytesseract.image_to_string(image)


    # GPT simplification
    simplified_text = simplify_text(extracted_text)

    print("Extracted text:", extracted_text)
    print("Simplified text:", simplified_text)

    return jsonify({
        'message': 'Image uploaded and processed',
        'extracted_text': extracted_text,
        'simplified_text': simplified_text
    }), 200

@app.route('/fidget-tools')
def fidget_tools():
    return render_template('fidget_tools.html')


if __name__ == '__main__':
    app.run(debug=True)