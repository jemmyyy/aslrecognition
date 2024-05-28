from collections import deque
import cv2
import mediapipe as mp
import numpy as np
import camera.utils as utils
from flask_socketio import emit

class SignDetection:
    def __init__(self, model, app, no_frames = 20, confidence_level = 0.9):
        self.no_frames = no_frames
        self.signs_detected = []
        self.current_vid = deque(maxlen = self.no_frames)
        self.model = model
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic()
        self.text_interpreted = ""
        self.confidence_level = confidence_level
        self.app = app
        self.app.emit("data", {'data': "shaghal"})

    def extract_keypoints(self, results):
        # pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        # face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([lh, rh])

    def add_frame_to_vid(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(image_rgb)
        keypoints = self.extract_keypoints(results)
        self.current_vid.append(keypoints)
        if len(self.current_vid) == self.no_frames:
            sign = self.detect_sign(self.current_vid)
            if sign is None: return
            self.signs_detected.append(sign)
            print(self.signs_detected)
            if len(self.signs_detected) == 5:
                if len(np.unique(self.signs_detected)) == 1 and self.signs_detected[0] != 'None':
                    final_sign = self.signs_detected[0]
                    self.text_interpreted +=  " " + final_sign
                    self.app.emit("data",{'data':final_sign})
                    # if len(self.text_interpreted.split(" "))>5:
                    #     tuned_text = chatGPT.detect(self.text_interpreted)
                    #     self.app.emit("data",{'data':tuned_text,"reset":"true"})
                self.signs_detected = []

    def detect_sign(self, vid):
        frames_to_get = [x for x in range(0, len(vid), int(len(vid)/10)) ]
        frames = [vid[n] for n in frames_to_get]
        # frames = vid[frames_to_get]
        frames_array = np.array(frames)
        frames_array = np.expand_dims(frames_array, axis=0)
        predicted_labels_probabilities = self.model.predict(frames_array)[0]
        if max(predicted_labels_probabilities) >= self.confidence_level:
            predicted_label_indx = np.argmax(predicted_labels_probabilities)

            if 0 <= predicted_label_indx < len(utils.CLASSES_LIST):
                predicted_class_name = utils.CLASSES_LIST[predicted_label_indx]
                word = f"{utils.CLASSES_NAMES[predicted_label_indx]}"
        else:
            word = 'None'
                    
        return word
