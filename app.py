print("Starting Flask app...")
from flask import Flask, render_template
from routes.audio import audio_bp


app = Flask(__name__)
app.register_blueprint(audio_bp)


@app.route('/fidget-tools')
def fidget_tools():
    return render_template('fidget_tools.html')


if __name__ == '__main__':
    app.run(debug=True)


