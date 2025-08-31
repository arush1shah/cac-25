print("Starting Flask app...")

from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os
from openai import OpenAI
from routes.audio import audio_bp
from routes.image import image_bp
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)
app.register_blueprint(audio_bp)
app.register_blueprint(image_bp)


if __name__ == '__main__':
    app.run(debug=True)
