from flask import Flask, render_template, request, send_file
from gtts import gTTS
import edge_tts
import asyncio
import os

app = Flask(__name__)

# Use absolute path in PythonAnywhere
AUDIO_PATH = os.path.expanduser("~/static/output.mp3")

# Ensure directory exists
os.makedirs(os.path.dirname(AUDIO_PATH), exist_ok=True)

@app.route('/')
def index():
    return render_template('text_to_voice.html')

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    lang = request.form['lang']

    try:
        if lang == 'ur':
            tts = gTTS(text=text, lang='ur')
            tts.save(AUDIO_PATH)
        elif lang == 'en':
            async def generate():
                communicate = edge_tts.Communicate(text=text, voice="en-US-GuyNeural")
                await communicate.save(AUDIO_PATH)
            asyncio.run(generate())
        
        return 'done'
    except Exception as e:
        return str(e), 500

@app.route('/audio')
def audio():
    try:
        if os.path.exists(AUDIO_PATH):
            return send_file(AUDIO_PATH, mimetype='audio/mpeg')
        else:
            return "Audio not found", 404
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)