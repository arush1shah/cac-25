import pyttsx3

def list_voices(engine):
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        gender = "Female" if "female" in voice.name.lower() else "Male"
        print(f"{i}: {voice.name} ({gender})")
    return voices

def speak_text(text, volume=1.0, rate=150, voice_index=0):
    engine = pyttsx3.init()

    # Set properties
    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')

    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    else:
        print("Invalid voice index. Using default.")

    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    engine = pyttsx3.init()
    voices = list_voices(engine)

    # Get user input
    user_text = input("\nType the text you'd like to hear:\n> ")

    try:
        user_volume = float(input("\nEnter volume (0.0 to 1.0, default 1.0):\n> ") or "1.0")
        user_rate = int(input("\nEnter speed (e.g., 100 slow, 150 normal, 200 fast):\n> ") or "150")
        voice_index = int(input("\nChoose voice number from the list above (default 0):\n> ") or "0")
    except ValueError:
        print("Invalid input. Using defaults.")
        user_volume, user_rate, voice_index = 1.0, 150, 0

    speak_text(user_text, user_volume, user_rate, voice_index)