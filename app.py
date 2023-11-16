from flask import Flask, render_template, request
from video_to_ascii import video_engine  # Adjust the import based on your module structure
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return render_template('index_video.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index_video.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index_video.html', error='No selected file')
 
    # Save the uploaded file
    video_path = 'static/uploads/' + file.filename
    file.save(video_path)

    # Call the function to convert video to ASCII
    ascii_output = convert_video_to_ascii(video_path)

    return render_template('result_video.html', video_path=video_path, ascii_output=ascii_output)

def convert_video_to_ascii(video_path):
    # Use the appropriate class or function for video to ASCII conversion
    video_engine = video_engine()  # Instantiate the class or use the function
    ascii_output = video_engine.convert_to_ascii(video_path)  # Adjust the method name
    return ascii_output

if __name__ == '__main__':
    app.run(debug=True)