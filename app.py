import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import math

# ─── Volume Setup (Windows) ───────────────────────────────────────────────────
devices = AudioUtilities.GetSpeakers()
interface = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_ctrl = cast(interface, POINTER(IAudioEndpointVolume))

vol_min, vol_max = volume_ctrl.GetVolumeRange()[:2]  # typically -65.25 to 0.0 dB

# ─── Hand Connections ─────────────────────────────────────────────────────────
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

THUMB_TIP    = 4
INDEX_TIP    = 8

# ─── MediaPipe Setup ──────────────────────────────────────────────────────────
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    running_mode=vision.RunningMode.IMAGE
)
detector = vision.HandLandmarker.create_from_options(options)

# ─── Helpers ──────────────────────────────────────────────────────────────────
def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def draw_volume_bar(img, vol_pct):
    """Draw a vertical volume bar on the right side of the frame."""
    h, w = img.shape[:2]
    bar_x       = w - 60
    bar_top     = 100
    bar_bottom  = h - 100
    bar_height  = bar_bottom - bar_top

    # Background bar
    cv2.rectangle(img, (bar_x, bar_top), (bar_x + 30, bar_bottom), (50, 50, 50), -1)

    # Filled level
    fill_y = int(bar_bottom - (vol_pct / 100) * bar_height)
    color  = (0, 255, 100) if vol_pct > 10 else (0, 80, 255)
    cv2.rectangle(img, (bar_x, fill_y), (bar_x + 30, bar_bottom), color, -1)

    # Border
    cv2.rectangle(img, (bar_x, bar_top), (bar_x + 30, bar_bottom), (200, 200, 200), 2)

    # Percentage label
    cv2.putText(img, f"{int(vol_pct)}%", (bar_x - 10, bar_bottom + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img, "VOL", (bar_x, bar_top - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

def draw_hand(img, points):
    for start, end in HAND_CONNECTIONS:
        cv2.line(img, points[start], points[end], (0, 220, 255), 2)
    for i, pt in enumerate(points):
        color = (0, 0, 255) if i in (THUMB_TIP, INDEX_TIP) else (255, 255, 255)
        radius = 8 if i in (THUMB_TIP, INDEX_TIP) else 4
        cv2.circle(img, pt, radius, color, -1)

# ─── Smoothing ────────────────────────────────────────────────────────────────
smoothed_vol = volume_ctrl.GetMasterVolumeLevelScalar() * 100
SMOOTH       = 0.15          # lower = smoother but slower

# ─── Gesture distance range (pixels) → maps to 0–100% volume ─────────────────
DIST_MIN = 30    # fingers touching  → 0%
DIST_MAX = 220   # fingers fully apart → 100%

# ─── Main Loop ────────────────────────────────────────────────────────────────
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Running — pinch thumb & index finger to control volume. ESC to quit.")

while True:
    ret, image = webcam.read()
    if not ret or image is None:
        break

    image = cv2.flip(image, 1)          # mirror so it feels natural
    h, w  = image.shape[:2]

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image  = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
    result    = detector.detect(mp_image)

    if result.hand_landmarks:
        hand_landmarks = result.hand_landmarks[0]   # first hand only
        points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]

        draw_hand(image, points)

        thumb = points[THUMB_TIP]
        index = points[INDEX_TIP]
        dist  = distance(thumb, index)

        # Map distance → volume percentage
        vol_pct = np.interp(dist, [DIST_MIN, DIST_MAX], [0, 100])
        vol_pct = float(np.clip(vol_pct, 0, 100))

        # Smooth it
        smoothed_vol += SMOOTH * (vol_pct - smoothed_vol)

        # Set system volume
        volume_ctrl.SetMasterVolumeLevelScalar(smoothed_vol / 100, None)

        # Draw line between thumb & index with distance indicator
        mid = ((thumb[0] + index[0]) // 2, (thumb[1] + index[1]) // 2)
        cv2.line(image, thumb, index, (255, 200, 0), 2)
        cv2.circle(image, mid, 6, (255, 200, 0), -1)
        cv2.putText(image, f"{int(dist)}px", (mid[0] + 10, mid[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)

        draw_volume_bar(image, smoothed_vol)

        # Pinch indicator
        if dist < DIST_MIN + 15:
            cv2.putText(image, "PINCH", (mid[0] - 30, mid[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 80, 255), 2)
    else:
        # No hand — still show current volume bar
        current_vol = volume_ctrl.GetMasterVolumeLevelScalar() * 100
        draw_volume_bar(image, current_vol)
        cv2.putText(image, "Show your hand", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 255), 2)

    # HUD
    cv2.putText(image, "Pinch = Volume | ESC = Quit", (20, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    cv2.imshow("Hand Gesture Volume Control", image)
    if cv2.waitKey(10) == 27:
        break

webcam.release()
cv2.destroyAllWindows()