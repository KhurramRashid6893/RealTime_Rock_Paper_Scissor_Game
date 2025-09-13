# 🖐️ Rock Paper Scissors with Hand Gestures

This project implements a real-time Rock-Paper-Scissors game using hand gestures and computer vision. It detects user hand gestures (Rock, Paper, or Scissors) via webcam and plays the game against a computer opponent.   

## 📁 Project Structure

```
RPS_Game/
├── config.py              # Configuration parameters
├── gesture.py             # Gesture classification logic
├── hand_tracker.py        # Hand tracking using Mediapipe
├── rps.py                 # Main game loop and UI
└── assets/
    ├── rock.png           # Image representing rock 
    ├── paper.png          # Image representing paper
    └── scissors.png       # Image representing scissors
```

---

## 🧠 How It Works

### 1. **Hand Tracking**

* Uses **MediaPipe Hands** to track hand landmarks in real-time.
* Detects which fingers are up using landmark positions.

### 2. **Gesture Recognition**

* Defines logic to classify gestures:

  * **Rock**: All fingers down.
  * **Paper**: All fingers up.
  * **Scissors**: Only index and middle fingers up.
* Logic implemented in `gesture.py`.

### 3. **Gameplay**

* Run the main game loop in `rps.py`.
* Captures user input from webcam.
* Randomly selects a computer move.
* Displays both moves visually with images and determines the winner.

---

## 🛠️ Requirements

Install required libraries using:

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ How to Run

```bash
python rps.py
```

Make sure your webcam is enabled.

---

## ⚙️ Files Explained

### `rps.py`

* Main entry point of the application.
* Manages webcam input, game rounds, visual rendering.

### `hand_tracker.py`

* Uses MediaPipe to detect and track hands.
* Returns landmark positions and bounding boxes.

### `gesture.py`

* Contains logic for interpreting hand gestures.
* Maps landmark patterns to Rock/Paper/Scissors.

### `config.py`

* Stores parameters like frame dimensions, thresholds.

### `assets/`

* Contains images used to display each gesture move.

---

## 🎮 Example Gameplay

When run, the app:

* Opens webcam.
* Detects your gesture.
* Picks a random move for the computer.
* Shows the result on screen.

---

## 📌 Notes

* Ensure good lighting for accurate gesture recognition.
* Use a high-resolution webcam for best performance.
* Extendable to include additional gestures or multiplayer modes.

---
