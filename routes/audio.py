from flask import Blueprint, request, jsonify
from utils.whisper_transcribe import transcribe_audio
from utils.gpt_summarize import summarize_text
import os;
import os

   
audio_bp = Blueprint('audio', __name__)

@audio_bp.route("/upload-audio", methods=["GET", "POST"])
def upload_audio():
    if request.method == "GET":
        return jsonify({"message": "Use POST to upload an audio file"}), 200
    
    if "file" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    file = request.files["file"]
    temp_path = "temp_audio.mp3"
    file.save(temp_path)
    print(f"File saved at: {temp_path}, size: {os.path.getsize(temp_path)} bytes")

    try:
        transcription = transcribe_audio(temp_path)
        summary = summarize_text(transcription)
        return jsonify({
        "transcript": transcription,
        "summary": summary
        })
    except Exception as e:
        print(f"Error during transcription: {e}")
        return jsonify({"error": "Failed to process audio file"}), 500
