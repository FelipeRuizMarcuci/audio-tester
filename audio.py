from flask import Flask, render_template, request, jsonify
from pydub import AudioSegment
from pydub.playback import play
import threading

app = Flask(__name__)

def play_audio(direction):
    sound = AudioSegment.from_file("snap-sound.mp3")
    if direction == "left":
        left_only = sound.pan(-1.0)
        play(left_only)
    elif direction == "right":
        right_only = sound.pan(1.0)
        play(right_only)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play-audio", methods=["POST"])
def play_audio_route():
    data = request.json
    direction = data.get("direction")
    try:
        # Play the audio in a separate thread to avoid blocking
        threading.Thread(target=play_audio, args=(direction,)).start()
        return jsonify({"status": "success", "message": f"Playing audio to the {direction}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
