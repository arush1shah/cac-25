from flask import Blueprint, request, jsonify
from PIL import Image
import pytesseract
import os
from openai import OpenAI
from utils.tts import speak_text  # <-- import your TTS function

image_bp = Blueprint('image', __name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def simplify_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that simplifies text."},
            {"role": "user", "content": f"Summarize the text from this image into a clear, concise paragraph:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

@image_bp.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    image = Image.open(filepath)
    extracted_text = pytesseract.image_to_string(image)
    simplified_text_result = simplify_text(extracted_text)

    # Optional TTS
    read_aloud = request.form.get('read_aloud', 'false').lower() == 'true'
    if read_aloud:
        speak_text(simplified_text_result)

    os.remove(filepath)  # cleanup

    return jsonify({
        'extracted_text': extracted_text,
        'simplified_text': simplified_text_result,
        'read_aloud': read_aloud
    })
