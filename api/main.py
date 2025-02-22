from flask import Flask, request, jsonify, Response
from texttosign.text_recognition import TextToSign
from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT, VideoCapture
from camera.camera import camera_stream
from keras.models import load_model
from camera.detection import SignDetection
from flask_socketio import SocketIO,emit
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

sign_detection = None
video_capture = None
model = None

def open_camera():
    global video_capture
    if video_capture is None:
        video_capture = VideoCapture(0)
    return video_capture

@app.route('/api/texttosign', methods=['POST'])
def text_recognition():
    print("text recognition",request.json)
    # Request input validation
    if 'text' not in request.json:
        return jsonify({'error': 'No text field provided'})
    

        return jsonify({'error': 'No avatar field provided'})

    # Get the value of the text and avatar fields from the request
    text = request.json['text']
    avatar =  request.json['avatar']

    if isinstance(text, bytes):
        text = text.decode('utf-8')

    print(text,"text")
    text_sign = TextToSign(avatar)
    print(text_sign,"text_sign")
    frames_path,string_array = text_sign.text_recognition(text)

    # Return the processed text
    return jsonify({'frames_path': frames_path,'string_array':string_array})
    


def gen_frame():
    """Video streaming generator function."""
    global video_capture
    global sign_detection
    video_capture = open_camera() # 0 for web camera live stream
    print("gen_frame",video_capture.isOpened())

    while video_capture is not None and video_capture.isOpened():
        frame_array, frame = camera_stream(video_capture)

        if frame_array is None or frame is None:
            print("camera broke")
            break

        if (sign_detection is not None):
            sign_detection.add_frame_to_vid(frame = frame_array)

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concate frame one by one and show result



@app.route('/api/video_feed')
def video_feed():
    print("video feed")
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/release_camera')
def release_camera():
    print("release camera")
    global video_capture
    response = {
        "status": "error",
        "message": "Camera not released, because it is not in use"
    }
    if video_capture is not None:
        video_capture.release()
        print("released camera", video_capture.isOpened())
        video_capture = None
        response = {
        "status": "success",
        "message": "Camera released"
    }

    return jsonify(response)



@socketio.on("start_analyzing")
def connected(data):
    """event listener when client connects to the server"""
    global sign_detection
    global model

    print(request.sid,data)
    print("client has connected")
    sign_detection = SignDetection(model, socketio,10, 0.9)

    emit("connect",{"data":f"id: {request.sid} is connected"})

if __name__ == "__main__":
    model_path = os.path.join(os.getcwd(), 'model','mplstm_model_19WORDS_Run1__Date_Time_2024_05_20_15_16_33')
    print("model path: ",model_path)
    model = load_model(model_path)
    socketio.run(app, debug=True,port=5001)