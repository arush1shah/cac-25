# utils/dalle_image_generator.py

import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image_from_prompt(prompt_text):
    """
    Uses DALL-E 3 to generate an image from a given text prompt.
    Returns the URL of the generated image.
    """
    if not prompt_text:
        return None

    print(f"Sending prompt to DALL-E 3: '{prompt_text}'")
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image with DALL-E 3: {e}")
        return None