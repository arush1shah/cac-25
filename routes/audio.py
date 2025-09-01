# routes/audio.py

from flask import Blueprint, request, jsonify, render_template
from utils.whisper_transcribe import transcribe_audio
from utils.gpt_summarize import summarize_text
import os
# --- CHANGE 1: Import secure_filename for safety ---
from werkzeug.utils import secure_filename

audio_bp = Blueprint(
    'audio', 
    __name__,
    template_folder='../templates'
)

@audio_bp.route('/')
def index():
    return render_template('index.html')

@audio_bp.route("/upload-audio", methods=["POST"])
def upload_audio_route():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file part in request"}), 400
    
    file = request.files["audio"]
    language = request.form.get("language")

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # --- CHANGE 2: Create a safe, temporary path with the ORIGINAL extension ---
    # This is the core of the fix.
    
    # Create an 'uploads' directory if it doesn't exist
    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)
    
    # Sanitize the filename for security and create the full path
    filename = secure_filename(file.filename)
    temp_path = os.path.join(upload_folder, filename)
    
    # Save the file with its correct name (e.g., "my_lecture.m4a")
    file.save(temp_path)
    # --- END OF CHANGES ---
    
    print(f"File saved to {temp_path}, language selected: {language}")

    try:
        # Now we pass the correctly named file to the transcriber
        transcription_data = transcribe_audio(temp_path, language=language)
        transcribed_text = transcription_data['text']
        detected_language = transcription_data['language']
        
        summary = summarize_text(transcribed_text, language=detected_language)
        
        os.remove(temp_path)

        return jsonify({
            "transcription": transcribed_text,
            "summary": summary
        })
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"Error during file processing: {e}")
        return jsonify({"error": "Failed to process audio file"}), 500