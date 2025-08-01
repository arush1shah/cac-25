# routes/audio.py

# IMPORTANT: Add render_template to your imports
from flask import Blueprint, request, jsonify, render_template
from utils.whisper_transcribe import transcribe_audio
from utils.gpt_summarize import summarize_text
import os

# IMPORTANT: Tell the blueprint where to find the 'templates' folder
audio_bp = Blueprint(
    'audio', 
    __name__,
    template_folder='../templates'
)

# NEW: Route for the homepage. This is what was missing.
@audio_bp.route('/')
def index():
    # This tells Flask to find and show your index.html file.
    return render_template('index.html')

# MODIFIED: The route for processing audio
@audio_bp.route("/upload-audio", methods=["POST"])
def upload_audio_route():
    # Note: Your form sends 'audio', not 'file'. And 'language'.
    if "audio" not in request.files:
        return jsonify({"error": "No audio file part in request"}), 400
    
    file = request.files["audio"]
    language = request.form.get("language") # Get the selected language
    
    temp_path = "temp_audio.mp3"
    file.save(temp_path)
    print(f"File saved to {temp_path}, language selected: {language}")

    try:
        # 1. Transcribe and get both text and detected language
        transcription_data = transcribe_audio(temp_path, language=language)
        transcribed_text = transcription_data['text']
        detected_language = transcription_data['language']
        
        # 2. Summarize using the detected language for a better prompt
        summary = summarize_text(transcribed_text, language=detected_language)
        
        # 3. Clean up the temp file
        os.remove(temp_path)

        # 4. Return both transcription and summary
        return jsonify({
            "transcription": transcribed_text,
            "summary": summary
        })
    except Exception as e:
        # Clean up the file even if there's an error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"Error during file processing: {e}")
        return jsonify({"error": "Failed to process audio file"}), 500