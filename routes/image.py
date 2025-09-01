from flask import Blueprint, request, jsonify
from PIL import Image
import pytesseract
import os
from openai import OpenAI
import traceback
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
    try:
        # Check for file
        if 'image' not in request.files:
            return jsonify({'error': 'No image file'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Extract text
        image = Image.open(filepath)
        extracted_text = pytesseract.image_to_string(image)

        # Simplify text
        simplified_text_result = simplify_text(extracted_text)

        # Optional TTS
        read_aloud = request.form.get('read_aloud', 'false').lower() == 'true'
        if read_aloud:
            try:
                speak_text(simplified_text_result)  # play audio, but don’t block JSON response
            except Exception as tts_error:
                print("TTS error:", tts_error)
                traceback.print_exc()

        # Cleanup
        try:
            os.remove(filepath)
        except Exception as remove_error:
            print("Error removing file:", remove_error)

        # Always return JSON
        return jsonify({
            'extracted_text': extracted_text,
            'simplified_text': simplified_text_result,
            'read_aloud': read_aloud
        })

    except Exception as e:
        # Catch any unexpected error and return JSON (instead of HTML)
        print("Unexpected error in upload_image:", e)
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500