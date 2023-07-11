from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    text = request.json.get('text', '')
    if text:
        subprocess.run(["./run_piper.sh", text], check=True)
        return 'Text to speech conversion successful', 200
    else:
        return 'No text provided', 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
