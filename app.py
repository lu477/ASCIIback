from flask import Flask, render_template, request, send_file, jsonify
import cv2
import numpy as np
import os
import base64
# from test import convert_ascii
# import argparse
import convert


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])

def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded video
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_video.mp4')
    file.save(video_path)


    # Perform video to ASCII conversion
    os.system('python convert.py "uploads/input_video.mp4" "uploads/output.mp4"')

    # Encode the ASCII video to base64
    encoded_video = encode_video_to_base64("uploads/output.mp4")

    # Return the base64 encoded video
    return jsonify({'video': encoded_video})
    

def encode_video_to_base64(video_path):
    with open(video_path, 'rb') as video_file:
        encoded_video = base64.b64encode(video_file.read()).decode('utf-8')
    print(video_path +  " encoded!")
    return encoded_video

if __name__ == '__main__':
    app.run(debug=True)

