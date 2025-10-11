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
            You will be given text extracted from an image. Your task is to rewrite it so that it is:

            1. **Simple:** Use short, clear sentences and everyday words. Avoid technical terms unless necessary, and explain them when used.  
            2. **Organized:** Break the information into short paragraphs or bullet points if it improves clarity.  
            3. **Accurate:** Preserve the original meaning and key ideas — do not remove important details.  
            4. **Accessible:** Write at about a 6th–8th grade reading level. Avoid idioms, slang, or overly complex grammar.  
            5. **Engaging and supportive:** Maintain a calm, friendly tone that encourages understanding.  

            **Formatting Rules:**
            - Highlight key terms or main ideas by wrapping them in `_highlight_term_here_highlight_` markers.  
            - If the text contains steps, dates, or instructions, number them clearly.  
            - If the original text is confusing or incomplete, infer missing context **only** if necessary to make it understandable.  
            - If the text seems like a story or description, summarize it clearly while keeping important emotional or factual details.  

            Finally, output the simplified version in the following format:

            **Simplified Text:**  
            (Your rewritten and simplified version here)

            **Summary (1–2 sentences):**  
            (A short summary of the main idea for quick understanding)

            Here is the text to simplify:

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