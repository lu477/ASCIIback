from flask import Flask, render_template, request, send_file, jsonify
import cv2
import numpy as np
import os
import base64

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
    ascii_video_path = convert_video_to_ascii(video_path)

    # Encode the ASCII video to base64
    encoded_video = encode_video_to_base64(ascii_video_path)

    # Return the base64 encoded video
    return jsonify({'video': encoded_video})

def convert_video_to_ascii(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    ascii_video_path = "uploads/ascii_video.mp4"
    out = cv2.VideoWriter(ascii_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize the frame to a smaller size for better ASCII representation
        resized_frame = cv2.resize(gray_frame, (80, 60))

        # Convert each pixel intensity to ASCII character
        ascii_frame = np.zeros_like(resized_frame, dtype=np.dtype('U1'))
        ascii_frame[:,:] = ' '
        ascii_frame[resized_frame < 50] = '@'
        ascii_frame[resized_frame > 200] = '.'

        # Write the ASCII frame to the output video
        out.write(cv2.cvtColor(cv2.resize(cv2.putText(frame.copy(), ''.join(ascii_frame.flatten()), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2), (width, height)), cv2.COLOR_BGR2RGB))

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return ascii_video_path

def encode_video_to_base64(video_path):
    with open(video_path, 'rb') as video_file:
        encoded_video = base64.b64encode(video_file.read()).decode('utf-8')
    return encoded_video

if __name__ == '__main__':
    app.run(debug=True)