from collections import deque
import cv2
import mediapipe as mp
import numpy as np
import camera.utils as utils
from flask_socketio import emit

class SignDetection:
    def __init__(self, model, no_frames = 10):
        self.no_frames = no_frames
        self.signs_detected = []
        self.current_vid = deque(maxlen = self.no_frames)
        self.model = model
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic()
        self.final_sign = ''
        self.text_interpreted = ""
        emit("data",{'data':"shaghal"},broadcast=True)

    def extract_keypoints(self, results):
        # pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        # face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([lh, rh])

    def add_frame_to_vid(self, frame):
        self.current_vid.append(frame)
        if len(self.current_vid) == self.no_frames:
            sign = self.detect_sign(self.current_vid)
            if sign is None: return
            self.signs_detected.append(sign)
            print(self.signs_detected)
            if len(self.signs_detected) == 5:
                if len(np.unique(self.signs_detected)) == 1:
                    self.final_sign = self.signs_detected[0]
                    self.signs_detected = []
                    self.text_interpreted +=  " " + self.final_sign
                    emit("data",{'data':self.final_sign},broadcast=True)
                    # if len(self.text_interpreted.split(" "))>5:
                    #     tuned_text = chatGPT.detect(self.text_interpreted)
                    #     emit("data",{'data':tuned_text,"reset":"true"},broadcast=True)

    def detect_sign(self, vid):
        frames_queue = []
        word = None
        for frame in vid:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.holistic.process(image_rgb)
            keypoints = self.extract_keypoints(results)
            frames_queue.append(keypoints)

        if len(frames_queue) == utils.SEQUENCE_LENGTH:
                frames_array = np.array(frames_queue)
                frames_array = np.expand_dims(frames_array, axis=0)
                print(self.model)
                predicted_labels_probabilities = self.model.predict(frames_array)[0]
                predicted_label_indx = np.argmax(predicted_labels_probabilities)

                if 0 <= predicted_label_indx < len(utils.CLASSES_LIST):
                    predicted_class_name = utils.CLASSES_LIST[predicted_label_indx]
                    word = f"{utils.CLASSES_NAMES[predicted_label_indx]}"
                    
        return word
