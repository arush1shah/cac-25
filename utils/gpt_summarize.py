# utils/gpt_summarize.py
import openai
from dotenv import load_dotenv

load_dotenv()

try:
    client = openai.OpenAI()
    print("OpenAI client initialized.")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

def summarize_text(text, language='en'):
    if not client:
        return "OpenAI client not initialized. Check your API key."

    language_map = {
        'en': 'English', 'es': 'Spanish', 'fr': 'French',
        'de': 'German', 'it': 'Italian', 'ja': 'Japanese',
        'ko': 'Korean', 'pt': 'Portuguese'
    }
    language_name = language_map.get(language, language.capitalize())

    # --- REPLACE THE PROMPT HERE ---
    # This is the new, more detailed prompt (Option 2)
    prompt_message = f"""
    You are an expert university teaching assistant. Your task is to summarize a lecture for a student who missed the class. The lecture is in {language_name}.

    Your notes must be clear, intuitive, and capture the most important points.

    Please structure your output as follows:

    **1. The Big Picture (Main Idea):**
    Start with a short, easy-to-understand paragraph explaining the overall topic of the lecture.

    **2. Key Concepts & Explanations:**
    List the main concepts discussed. For each concept, provide a simple explanation. Define all important terms. Crucially, **you must include the professor's helpful analogies and informal terms (like 'doomed space' or 'death space')**, as they are key to understanding the material.

    **3. How It All Connects:**
    Explain how the different concepts build on each other. For example, how do the simple 2D rotations relate to the more complex 3D and 4D ones? Why are these rotation matrices important for things like computer graphics or data science?

    **4. Final Takeaway:**
    End with the single most important idea the student should remember from this lecture.

    Write the entire summary in {language_name}.
    """
    # --- END OF PROMPT REPLACEMENT ---
    
    print(f"Sending text to GPT-4 with the new, improved prompt...")
    try:
        response = client.chat.completions.create(
            model="gpt-4", # Or gpt-4o for even better results
            messages=[
                # The 'system' role is perfect for this kind of detailed instruction
                {"role": "system", "content": prompt_message},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return f"Error during summarization: {e}"