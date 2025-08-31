import pyttsx3

def speak_text(text, volume=1.0, rate=140, voice_index=0):
    engine = pyttsx3.init()
    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')

    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    else:
        print("Invalid voice index. Using default.")

    # Add simple pauses for clarity
    text = text.replace(".", ".\n").replace(",", ",\n")
    engine.say(text)
    engine.runAndWait()