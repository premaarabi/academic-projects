from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# Routes for rendering the main page
@app.route('/')
def index():
    return render_template('index.html')

# API for video detection
@app.route('/video', methods=['POST'])
def video():
    try:
        # Call the video detection script
        subprocess.run(['python', 'video_detection.py'])
        return jsonify({"message": "Video detection executed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# API for image text detection
@app.route('/image', methods=['POST'])
def image():
    try:
        # Call the image OCR script
        subprocess.run(['python', 'image_text_detection.py'])
        return jsonify({"message": "Image text detection executed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# API for route navigation
@app.route('/route', methods=['POST'])
def route():
    try:
        # Call the route navigation script
        subprocess.run(['python', 'route_navigation.py'])
        return jsonify({"message": "Route navigation executed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# API for voice command handling
@app.route('/voice', methods=['POST'])
def voice():
    try:
        # Call the voice command processing script
        subprocess.run(['python', 'voice_command.py'])
        return jsonify({"message": "Voice command executed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
