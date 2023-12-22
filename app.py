from flask import Flask, render_template, request, send_file, jsonify, Response
import cv2
import numpy as np
import os
import base64
import convert


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])

def asciify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded video
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_video.mp4')
    file.save(video_path)


    # ASCII conversion with arguments
    os.system('python convert.py "uploads/input_video.mp4" "uploads/output.mp4"')

     # Set the response headers for streaming
    response = Response(generate_frames("uploads/output.mp4"), content_type='video/mp4')
    response.headers['Content-Disposition'] = 'inline; filename=output.mp4'

    # # Encode the ASCII video to base64
    # encoded_video = encode_video_to_base64("uploads/output.mp4")

    # # Return the base64 encoded video
    # return jsonify({'video': encoded_video})
    return response

def encode_video_to_base64(video_path):
    with open(video_path, 'rb') as video_file:
        encoded_video = base64.b64encode(video_file.read()).decode('utf-8')
    print(video_path +  " encoded!")
    return encoded_video

def generate_frames(video_path):
    with open(video_path, 'rb') as video_file:
        while True:
            chunk = video_file.read(1024)  # Adjust the chunk size as needed
            if not chunk:
                break
            yield chunk

if __name__ == '__main__':
    app.run(debug=True)

