print("Starting Flask app...")
from flask import Flask, render_template
from routes.audio import audio_bp
from routes.image import image_bp
from routes.adhd_tools import adhd_tools_bp
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)
app.register_blueprint(audio_bp)
app.register_blueprint(image_bp)
app.register_blueprint(adhd_tools_bp)


@app.route('/fidget-tools')
def fidget_tools():
    return render_template('fidget_tools.html')


if __name__ == '__main__':
    app.run(debug=True)


