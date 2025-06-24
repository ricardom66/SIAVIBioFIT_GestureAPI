import cv2
import mediapipe as mp
from utils.pose_utils import count_repetitions_arm_lift
import requests

BACKEND_URL = "https://siavibiofit-backend.onrender.com/api/gesture/submit"

def send_reps_to_backend(exercise, reps):
    try:
        requests.post(BACKEND_URL, json={
            "exercise": exercise,
            "repetitions": reps
        })
    except Exception as e:
        print(f"Error sending reps to backend: {e}")

cap = cv2.VideoCapture(0)
counter = 0
stage = None  # "up" or "down"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame, counter, stage = count_repetitions_arm_lift(frame, counter, stage)

    send_reps_to_backend("weights_lift", counter)

    cv2.putText(frame, f'Reps: {counter}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Weights Lift Counter', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
