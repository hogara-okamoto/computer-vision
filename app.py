# app.py
import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import subprocess
from flask_cors import CORS
import json

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Define the folder where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define the route for file uploads
@app.route('/')
def index():
    return "Welcome to the Flask API!", 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    print("Upload request received")

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    print(f"File received: {file.filename}")

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File saved to: {filepath}")

        # Pass labels for object detection (or another appropriate label)
        process = subprocess.Popen(
            ['python', 'ObjectDetection.py', filepath, 'Lion', 'Elephant', 'Giraffe', 'Kangaroo', 'zebra', 'Panda', 'Tiger', 'cat', 'dog', 'person'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate(timeout=600)
        print(f"Subprocess output: {stdout}")
        print(f"Subprocess error: {stderr}")

        if process.returncode == 0:
            # Read and parse the output (assuming ObjectDetection.py outputs JSON)
            try:
                predictions = json.loads(stdout.strip())
                print("Parsed JSON:", predictions)
            except json.JSONDecodeError:
                return jsonify({"error": "Failed to parse detection results"}), 500

            detection_image = f"{os.path.splitext(filepath)[0]}_detection.png"
            print(f"File processed successfully. Detection image: {detection_image}")
            return jsonify({
                "message": "File processed successfully",
                "detection_image": detection_image,
                "predictions": predictions  # JSON data containing bounding boxes, labels, etc.
            }), 200
        else:
            print("Error in subprocess")
            return jsonify({"error": stderr}), 500
        
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
       
# Run Flask app on 0.0.0.0 so it's accessible from localhost in WSL
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)