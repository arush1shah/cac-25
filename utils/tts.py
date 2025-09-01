import pyttsx3

# Create engine once at import time
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 140)

def speak_text(text, voice_index=0):
    voices = engine.getProperty('voices')
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    else:
        print("Invalid voice index. Using default.")

    text = text.replace(".", ".\n").replace(",", ",\n")
    engine.say(text)
    engine.runAndWait()
