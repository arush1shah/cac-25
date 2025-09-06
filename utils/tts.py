'''import pyttsx3
import os

# Create engine once at import time
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 140)

def speak_text_to_file(text, output_file, voice_index=0):
    voices = engine.getProperty('voices')
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    else:
        print("Invalid voice index. Using default.")

    # Save the audio to a file
    engine.save_to_file(text, output_file)
    engine.runAndWait()
'''
from gtts import gTTS
# import pyttsx3

# # Create engine once at import time
# engine = pyttsx3.init()
# engine.setProperty('volume', 1.0)
# engine.setProperty('rate', 140)

# voices = engine.getProperty('voices')

def speak_text_to_file(text, output_file):
    try:
        # Create a gTTS object
        tts = gTTS(text=text, lang='en')
        
        # Save the audio as a .wav file
        tts.save(output_file)
        print(f"Audio file generated: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

