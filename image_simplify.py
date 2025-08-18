from PIL import Image
from openai import OpenAI
import os
import pytesseract

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def simplify_text(text):
    """Send extracted text to GPT for simplification."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that simplifies text."},
            {"role": "user", "content": f"Summarize the text from this image into a clear, concise paragraph that keeps the main ideas but removes extra details.\n\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

# Path to your image file
image_path = "/Users/taratony/Downloads/letter.png"

# Open image and extract text
image = Image.open(image_path)
extracted_text = pytesseract.image_to_string(image)

# Simplify text
simplified_text = simplify_text(extracted_text)

print("Extracted text:")
print(extracted_text)
print("\nSimplified text:")
print(simplified_text)