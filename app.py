import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui

# Hand connections (index pairs)
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    running_mode=vision.RunningMode.IMAGE
)
detector = vision.HandLandmarker.create_from_options(options)

webcam = cv2.VideoCapture(0)

while True:
    _, image = webcam.read()
    if image is None:
        break

    h, w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            # Convert normalized coords to pixel coords
            points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]

            # Draw connections
            for start, end in HAND_CONNECTIONS:
                cv2.line(image, points[start], points[end], (0, 255, 0), 2)

            # Draw landmark dots
            for pt in points:
                cv2.circle(image, pt, 5, (0, 0, 255), -1)

    cv2.imshow("Hand Volume Control", image)

    if cv2.waitKey(10) == 27:  # ESC to quit
        break

webcam.release()
cv2.destroyAllWindows()