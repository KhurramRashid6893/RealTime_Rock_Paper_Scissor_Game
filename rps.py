#importing the modules
import cv2
import random
import time
import numpy as np
from PIL import Image
from hand_tracker import HandTracker 
from gesture import GestureRecogniser

class RPSGame: 
    def __init__(self, user_name):
        self.user_name = user_name
        self.tracker = HandTracker()
        self.gesture_recogniser = GestureRecogniser()
        self.choices = ["ROCK", "PAPER", "SCISSORS"]
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        self.round_delay = 2.0
        self.last_round_time = 0
        self.score = {"user": 0, "computer": 0, "draws": 0}
        self.countdown_active = False
        self.countdown_value = 3
        self.countdown_start_time = 0
        self.game_over = False

        self.emoji_images = {
            "ROCK": Image.open("assets/rock.png").convert("RGBA"),
            "PAPER": Image.open("assets/paper.png").convert("RGBA"),
            "SCISSORS": Image.open("assets/scissors.png").convert("RGBA")
        }

    def recognise_rps_gesture(self, landmark_list):
        if not landmark_list:
            print("No landmarks detected.")
            return None
        landmarks = dict([(id, (x, y)) for id, x, y in landmark_list])
        fingers = self.gesture_recogniser._check_fingers_extended(landmarks)

        print("Detected Finger States [Thumb, Index, Middle, Ring, Pinky]:", fingers)

        if not any(fingers[1:]):
            print("🪨 Gesture Detected: ROCK")
            return "ROCK"
        elif all(fingers[1:]):
            print("📄 Gesture Detected: PAPER")
            return "PAPER"
        elif fingers[1] and fingers[2] and not (fingers[3] or fingers[4]):
            print("✌️ Gesture Detected: SCISSORS")
            return "SCISSORS"
        else:
            print("❓ Unknown or unclear gesture.")
        return None


    def start_countdown(self):
        self.countdown_active = True
        self.countdown_value = 3
        self.countdown_start_time = time.time()

    def update_countdown(self):
        if not self.countdown_active:
            return False
        elapsed = time.time() - self.countdown_start_time
        if elapsed >= 1:
            self.countdown_value -= 1
            self.countdown_start_time = time.time()
            if self.countdown_value <= 0:
                self.countdown_active = False
                return True
        return False

    def play_round(self, player_choice):
        self.player_choice = player_choice
        self.computer_choice = random.choice(self.choices)
        self.last_round_time = time.time()

        if self.player_choice == self.computer_choice:
            self.result = "DRAW"
            self.score["draws"] += 1
        elif (self.player_choice == "ROCK" and self.computer_choice == "SCISSORS") or \
             (self.player_choice == "PAPER" and self.computer_choice == "ROCK") or \
             (self.player_choice == "SCISSORS" and self.computer_choice == "PAPER"):
            self.result = f"{self.user_name.upper()} WINS THIS ROUND!"
            self.score["user"] += 1
        else:
            self.result = "COMPUTER WINS THIS ROUND!"
            self.score["computer"] += 1

        if self.score["user"] == 5 or self.score["computer"] == 5:
            self.game_over = True

    def overlay_image(self, frame, emoji_img, position):
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert("RGBA")
        frame_pil.paste(emoji_img, position, emoji_img)
        return cv2.cvtColor(np.array(frame_pil.convert("RGB")), cv2.COLOR_RGB2BGR)

    def draw_game_ui(self, frame):
        # Draw score on top
        cv2.putText(frame,
                    f"{self.user_name}: {self.score['user']}  Computer: {self.score['computer']}  Draws: {self.score['draws']}",
                    (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        if self.countdown_active:
            cv2.putText(frame, str(self.countdown_value),
                        (frame.shape[1] // 2 - 30, frame.shape[0] // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 10)
            return frame

        if self.player_choice:
            # Draw player choice left
            frame = self.overlay_image(frame, self.emoji_images[self.player_choice], (100, 120))
            cv2.putText(frame, self.user_name.upper(), (100, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Draw computer choice right
            frame = self.overlay_image(frame, self.emoji_images[self.computer_choice], (frame.shape[1]-250, 120))
            cv2.putText(frame, "COMPUTER", (frame.shape[1]-250, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if self.result and (time.time() - self.last_round_time < self.round_delay):
            cv2.putText(frame, self.result, (frame.shape[1]//2 - 200, 350),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        if self.game_over:
            winner = self.user_name.upper() if self.score["user"] == 5 else "COMPUTER"
            msg = f"{winner} WINS THE GAME!"
            cv2.putText(frame, msg, (frame.shape[1]//2 - 250, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 4)

        return frame

def main():
    user_name = input("Enter your name: ").strip()
    if not user_name:
        user_name = "PLAYER"

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    game = RPSGame(user_name)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = game.tracker.find_hands(frame, draw=True)
        landmarks = game.tracker.get_hand_position(frame)

        if not game.countdown_active and (time.time() - game.last_round_time > game.round_delay) and not game.game_over:
            gesture = game.recognise_rps_gesture(landmarks)
            if gesture:
                game.start_countdown()

        if game.update_countdown():
            gesture = game.recognise_rps_gesture(landmarks)
            if gesture:
                game.play_round(gesture)

        frame = game.draw_game_ui(frame)
        cv2.imshow("Rock-Paper-Scissors", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or game.game_over:
            time.sleep(5)
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
