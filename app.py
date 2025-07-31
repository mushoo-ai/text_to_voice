from flask import Flask, render_template, request, send_file
from gtts import gTTS
import edge_tts
import asyncio
import os

app = Flask(__name__)
AUDIO_PATH = "static/output.mp3"

@app.route('/')
def index():
    return render_template('text_to_voice.html')

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    lang = request.form['lang']

    if lang == 'ur':
        tts = gTTS(text=text, lang='ur')
        tts.save(AUDIO_PATH)
    elif lang == 'en':
        async def generate():
            communicate = edge_tts.Communicate(text=text, voice="en-US-GuyNeural")
            await communicate.save(AUDIO_PATH)
        asyncio.run(generate())

    return 'done'

@app.route('/audio')
def audio():
    if os.path.exists(AUDIO_PATH):
        return send_file(AUDIO_PATH, mimetype='audio/mpeg')
    else:
        return "Audio not found", 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)

