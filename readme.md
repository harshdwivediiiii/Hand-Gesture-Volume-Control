# ✋ Hand Gesture Volume Control

Control your system volume using just your hand gestures in real time using **Computer Vision**, **MediaPipe**, and **OpenCV**.

This project tracks the distance between your **thumb** and **index finger** through a webcam and maps it to your system volume level.

## 📸 Demo

### Live Hand Tracking

![Demo Image](public/demo/demo.png)

---

### Volume Gesture Detection

![Demo Image 2](public/demo/demo2.png)
---

## 🚀 Features

- 🎥 Real-time webcam hand tracking
- ✋ Thumb & index finger gesture detection
- 🔊 System volume control using gestures
- 📊 Smooth animated volume bar
- ⚡ Fast and responsive performance
- 🖥️ Works on Windows systems

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Pycaw
- Computer Vision

---

## 📦 Requirements

Create a `requirements.txt` file:

```txt
opencv-python
mediapipe
numpy
pycaw
comtypes
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```bash
Hand-Gesture-Volume-Control/
│
├── main.py
├── hand_landmarker.task
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Hand-Gesture-Volume-Control.git
```

### 2️⃣ Navigate to Project Folder

```bash
cd Hand-Gesture-Volume-Control
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Download MediaPipe Model

Download:

`hand_landmarker.task`

Place it inside the project folder.

---

## ▶️ Start the Project

```bash
python main.py
```

---

## 🎮 Controls

| Gesture | Action |
|----------|---------|
| 🤏 Fingers close | Volume Down |
| ✋ Fingers apart | Volume Up |
| ESC Key | Exit Program |

---

## 📸 How It Works

1. Webcam captures live video
2. MediaPipe detects hand landmarks
3. Distance between thumb & index finger is calculated
4. Distance maps to system volume
5. Volume updates smoothly in real time

---

## 🧠 Concepts Used

- Hand Landmark Detection
- Euclidean Distance
- Gesture Recognition
- Volume Mapping
- Real-Time Image Processing

---

## ⚡ Future Improvements

- 🖐️ Multi-hand support
- 🎵 Media controls (pause/play)
- 🌙 Dark futuristic UI
- 📱 Bluetooth phone camera support
- 🤖 AI gesture customization

---

## 🖥️ Output Preview

```text
Pinch = Volume Control
ESC = Quit
```

---

## 👨‍💻 Author

Harshvardhan Dwivedi

---

## ⭐ Support

If you liked this project:

- Star the repository
- Fork the project
- Share with friends

---

## 📜 License

This project is open-source and available under the MIT License.