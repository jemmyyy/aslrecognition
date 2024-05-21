from flask import Flask, request, jsonify, Response
from texttosign.text_recognition import TextToSign
from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT
from camera.camera import camera_stream
from keras.models import load_model

app = Flask(__name__)


@app.route('/api/signtotext/', methods = ['GET'])
def signToText():
    video = request.data
    vidcap = VideoCapture(video)
    total_frames = vidcap.get(CAP_PROP_FRAME_COUNT)
    print(total_frames)
    n = 10
    frames_step = total_frames//n
    frames = []
    for i in range(n):
        #here, we set the parameter 1 which is the frame number to the frame (i*frames_step)
        vidcap.set(1,i*frames_step)
        success,image = vidcap.read()  
        frames.append(image)

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
        frame = camera_stream()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concate frame one by one and show result


@app.route('/api/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
    model = load_model()