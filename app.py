print("Starting Flask app...")
from flask import Flask, render_template
from routes.audio import audio_bp
from routes.image import image_bp
from routes.adhd_tools import adhd_tools_bp
from flask import Flask, request, jsonify, render_template
from flask import Flask, send_from_directory



app = Flask(__name__)
app.register_blueprint(audio_bp)
app.register_blueprint(image_bp)
app.register_blueprint(adhd_tools_bp)


@app.route('/fidget-tools')
def fidget_tools():
    return render_template('fidget_tools.html')
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('uploads', filename)


if __name__ == '__main__':
    app.run(debug=True)


