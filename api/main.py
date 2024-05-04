from flask import Flask, request
from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT
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
    

if __name__ == "__main__":
    app.run(debug=True)
    model = load_model()