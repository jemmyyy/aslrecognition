import cv2

video_capture = cv2.VideoCapture(0)  # 0 for web camera live stream
#  for cctv camera'rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
#  example of cctv or rtsp: 'rtsp://mamun:123456@101.134.16.117:554/user=mamun_password=123456_channel=1_stream=0.sdp'


def camera_stream():
     # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame_array = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_LINEAR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # # Display the resulting frame in browser
    return frame_array, cv2.imencode('.jpg', frame)[1].tobytes()