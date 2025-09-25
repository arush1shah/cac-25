from flask import Blueprint, request, jsonify, send_file, render_template
from PIL import Image
import pytesseract
import os
from openai import OpenAI
import traceback
from utils.tts import speak_text_to_file  # <-- import your TTS function

image_bp = Blueprint('image', __name__)

@image_bp.route('/get-audio', methods=['POST'])
def get_audio():
    data = request.get_json()
    simplified_text = data.get('simplified_text', '')

    if not simplified_text:
        return jsonify({'error': 'No text provided'}), 400

    # Generate audio file
    audio_file = 'output_audio.wav'
    speak_text_to_file(simplified_text, audio_file)

    # Serve the audio file
    return send_file(audio_file, as_attachment=True)

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
            return render_template('index.html', error='No image file uploaded.')

        file = request.files['image']
        if file.filename == '':
            return render_template('index.html', error='No file selected.')

        # Save file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Extract text from the image
        image = Image.open(filepath)
        extracted_text = pytesseract.image_to_string(image)

        # Simplify the extracted text
        simplified_text_result = simplify_text(extracted_text)

         # Generate audio file from simplified text
        audio_file_name = 'simplified_audio.wav'
        audio_file = os.path.join('uploads', audio_file_name)  # Full path for saving
        speak_text_to_file(simplified_text_result, audio_file)


        # Cleanup the uploaded file
        try:
            os.remove(filepath)
        except Exception as remove_error:
            print("Error removing file:", remove_error)

        # Render the template with the extracted and simplified text
        '''
        return render_template(
            'index.html',
            extracted_text=extracted_text,
            simplified_text=simplified_text_result,
            audio_file=audio_file_name
        )'''
        return jsonify({
        'extracted_text': extracted_text,
        'simplified_text': simplified_text_result
})

    except Exception as e:
        # Handle unexpected errors
        print("Unexpected error in upload_image:", e)
        traceback.print_exc()
        return render_template('index.html', error='An error occurred while processing the image.')