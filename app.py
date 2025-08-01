from flask import Flask
from routes.audio import audio_bp

app = Flask(__name__)
app.register_blueprint(audio_bp)

if __name__ == "__main__":
    app.run(debug=True)
