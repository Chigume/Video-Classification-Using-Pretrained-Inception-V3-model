from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        return "File has been uploaded."
    return render_template('index.html', form=form)

#model = load_model('C:/Users/Abgirl/Downloads/inceptionv3_pretrained.h5')

# Define a function to extract frames from a video
def extract_frames(video_path):
    frames = []
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (299, 299))
        frame = np.expand_dims(frame, axis=0)
        frames.append(frame)
    cap.release()
    return np.vstack(frames)

# Define a route to handle video classification
@app.route('/classify_video', methods=['POST'])
def classify_video():
    # Get the uploaded video file
    video_file = request.files['video']
    video_path = './uploads' + video_file.filename
    video_file.save(video_path)

    # Extract frames from the video
    frames = extract_frames(video_path)

    # Get predictions for each frame
    predictions = []
    for frame in frames:
        prediction = model.predict(frame)
        predictions.append(prediction)

    # Aggregate predictions to get final prediction
    predictions = np.vstack(predictions)
    final_prediction = np.argmax(np.bincount(predictions))

    # Return the final prediction as JSON response
    return jsonify({'activity': final_prediction})


if __name__ == '__main__':
    app.run(debug=True)