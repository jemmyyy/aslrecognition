from flask import Flask, request, jsonify, Response
from texttosign.text_recognition import TextToSign
from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT
from camera.camera import camera_stream
from keras.models import load_model
from camera.detection import SignDetection
from flask_socketio import SocketIO,emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

sign_detection = None

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
        if (sign_detection is not None):
            sign_detection.add_frame_to_vid(frame = frame_array)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concate frame one by one and show result


@app.route('/api/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    sign_detection = SignDetection(model, 20)

    emit("connect",{"data":f"id: {request.sid} is connected"})

if __name__ == "__main__":
    socketio.run(app, debug=True,port=5001)
    model_path = 'C:/Users/Jemmy/Desktop/aslrecognition/model/mplstm_model_4WORDS_Run1__Date_Time_2024_05_11_11_25_46'
    model = load_model(model_path)