# utils/whisper_transcribe.py
import whisper

print("Loading Whisper model...")
# Using "base" is fast. "small" or "medium" are more accurate.
whisper_model = None
print("Whisper model loaded.")
def load_whisper_model():
    """
    This function loads the Whisper model into the global variable.
    It's designed to run only once, the first time it's needed.
    """
    global whisper_model
    if whisper_model is None:
        print("Whisper model is not loaded. Loading now... (This may take a moment)")
        # Using "base" is fast. "small" or "medium" are more accurate.
        whisper_model = whisper.load_model("base")
        print("Whisper model loaded successfully and will be reused.")

def transcribe_audio(file_path, language=None):
    """
    Transcribes the audio file using Whisper.
    Accepts an optional language code.
    Returns a dictionary with the transcription text and detected language.
    """
    load_whisper_model()
    print(f"Starting transcription for {file_path} with language '{language}'...")
    
    # Let Whisper auto-detect if language is 'auto' or not provided
    transcribe_options = {}
    if language and language != 'auto':
        transcribe_options['language'] = language

    result = whisper_model.transcribe(file_path, **transcribe_options)
    
    print(f"Transcription complete. Detected language: {result['language']}")
    
    # Return both the text and the language Whisper detected/used
    return {
        'text': result['text'],
        'language': result['language']
    }