from flask import Flask, jsonify

app = Flask(__name__)


# Initiate
is_playing = False


@app.route('/home', methods=['GET'])
def get_home():
    return jsonify(message="Home page is being shown"), 200


@app.route('/video-processing', methods=['GET'])
def get_video_processing():
    # subprocess.run(["python", "VideoPlayer.py"])
    return jsonify(message="video processing page is being shown"), 200


@app.route('/saved-data', methods=['GET'])
def get_saved_data():
    # subprocess.run(["python", "python-file-path-to-saved-data"])
    return jsonify(message="Saved data page is being shown"), 200


@app.route('/pause', methods=['POST'])
def pause():
    global is_playing
    is_playing = False
    return jsonify({'status': 'success', 'is_playing': is_playing})


@app.route('/play', methods=['POST'])
def play():
    global is_playing
    is_playing = True
    return jsonify({'status': 'success', 'is_playing': is_playing})


# wherever is using the api add, if status_code_variable_name == 200 then do, else do.
