# routes/image.py

from flask import Blueprint, request, jsonify
from PIL import Image
import pytesseract
import os
from openai import OpenAI

# --- Blueprint Setup ---
image_bp = Blueprint('image', __name__)

# --- Initialization ---
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Helper Function ---
def simplify_text(text):
    """Send extracted text to GPT for simplification."""
    if not text.strip():
        return "No text was extracted from the image to simplify."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that simplifies complex text into clear, easy-to-understand language."},
            {"role": "user", "content": f"Please simplify this text:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

# --- Route ---
@image_bp.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        image = Image.open(filepath)
        extracted_text = pytesseract.image_to_string(image)
        simplified_text = simplify_text(extracted_text)
        
        # Clean up the uploaded file
        os.remove(filepath)

        return jsonify({
            'message': 'Image processed successfully',
            'extracted_text': extracted_text,
            'simplified_text': simplified_text
        }), 200
    except Exception as e:
        # Clean up the file on error too
        if os.path.exists(filepath):
            os.remove(filepath)
        print(f"Error processing image: {e}")
        return jsonify({'error': 'Failed to process image'}), 500