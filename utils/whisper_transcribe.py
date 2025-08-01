import shutil
import whisper
import tempfile
import os
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin"

model = whisper.load_model("base")

def transcribe_audio(path):
    try:
        print(f"Processing file: {path}")
        if os.path.getsize(path) < 512:
            raise RuntimeError("Audio file is too small or invalid.")
        
        result = model.transcribe(path)
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {e}")
        raise RuntimeError("Failed to process audio file")
    finally:
         if os.path.exists(path):
            os.remove(path)


    