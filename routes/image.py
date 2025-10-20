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
        messages = [
    {
        "role": "system",
        "content": (
            "You are an expert language simplifier and accessibility assistant. "
            "Your goal is to make complex written text easy to understand for readers with learning disabilities or lower reading proficiency. "
            "You must keep the meaning accurate while improving readability, organization, and comprehension."
        )
    },
    {
        "role": "user",
        "content": f"""
            You are an expert university teaching assistant. Your task is to create clear and structured notes from text extracted from an image. This could include textbook pages, slides, diagrams, or handwritten notes.

            Your notes must be clear, intuitive, and capture the most important points, making them easy for a student who missed the class to understand.

            Please structure your output as follows:

            **1. The Big Picture (Main Idea):**
            Start with a short, easy-to-understand paragraph explaining the overall topic of the passage.

            **2. Key Concepts & Explanations:**
            Break down the passage into structured notes, focusing on key topics and terms. For each concept, provide a simple explanation that is detailed enough for a student to understand. Define all important terms, using your own knowledge if necessary. VERY CRUCIAL: Use bullet points rather than large headings for individual terms or ideas. Don't make headings within this section.

            **3. How It All Connects:**
            Explain how the different concepts build on each other. For example, how do the simple 2D rotations relate to the more complex 3D and 4D ones? Why are these rotation matrices important for things like computer graphics or data science?

            **4. Final Takeaway:**
            End with the single most important idea the student should remember from this passage.

            {text}
            """
                }
            ]
    )
    return response.choices[0].message.content.strip()

@image_bp.route('/upload-image', methods=['POST'])
def upload_image():
    try:
        # Check for file
        if 'image' not in request.files:
            return jsonify({'error': 'No image file uploaded.'}), 400

        file = request.files['image']
        if file.filename.lower().endswith('.heic'):
            print("⚠️ HEIC images are not supported yet.")
            return jsonify({'error': 'HEIC images are not supported. Please upload a JPG or PNG file instead.'}), 400

        if file.filename == '':
            return jsonify({'error': 'No file selected.'}), 400

        # Save file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Extract text from the image
        image = Image.open(filepath)
        extracted_text = pytesseract.image_to_string(image)

        # Simplify the extracted text
        simplified_text_result = simplify_text(extracted_text)

         # Generate audio file from simplified text
        audio_file_name = f'simplified_{os.path.splitext(file.filename)}_{os.getpid()}.wav'
        audio_file_path = os.path.join('uploads', audio_file_name)
        speak_text_to_file(simplified_text_result, audio_file_path)


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
        'simplified_text': simplified_text_result,
        'audio_file': audio_file_name
})

    except Exception as e:
        # Handle unexpected errors
        print("Unexpected error in upload_image:", e)
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while processing the image.'}), 500