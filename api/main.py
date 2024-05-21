from flask import Flask, request, jsonify, Response
from texttosign.text_recognition import TextToSign
from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT
from camera.camera import camera_stream
from keras.models import load_model
from camera.detection import SignDetection

app = Flask(__name__)


@app.route('/api/texttosign', methods=['GET'])
def text_recognition():
    # Request input validation
    if 'text' not in request.json:
        return jsonify({'error': 'No text field provided'})
    
    if 'avatar' not in request.json:
        return jsonify({'error': 'No avatar field provided'})

    # Get the value of the text and avatar fields from the request
    text = request.json['text']
    avatar =  request.json['avatar']

    text_sign = TextToSign(avatar)
    frames_path = text_sign.text_recognition(text)

    # Return the processed text
    return jsonify({'frames_path': frames_path})
    

def gen_frame():
    """Video streaming generator function."""
    while True:
        frame_array, frame = camera_stream()
        sign_detection.add_frame_to_vid(frame = frame_array)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concate frame one by one and show result


@app.route('/api/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
    model_path = 'C:/Users/Jemmy/Desktop/aslrecognition/model/mplstm_model_4WORDS_Run1__Date_Time_2024_05_11_11_25_46'
    model = load_model(model_path)
    sign_detection = SignDetection(model, 20)