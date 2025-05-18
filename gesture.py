from enum import Enum
import math
import time

class GestureType(Enum):
    NONE = "none"
    DRAW = "draw"       # index + thumb pinch
    ERASE = "erase"     # open palm 
    SELECT = "select"   # index pointing
    CLEAR = "clear"     # fist with thumb out 

class GestureType(Enum):
    NONE = "none"
    DRAW = "draw"
    ERASE = "erase"
    SELECT = "select"
    CLEAR = "clear"

class GestureRecogniser:
    def __init__(self):
        self.pinch_threshold = 75
        self.current_gesture = GestureType.NONE
        self.clear_gesture_start = 0
        self.clear_hold_time = 3.0
        self.is_clear_gesture = False

    def recognise_gesture(self, landmark_list):
        if not landmark_list:
            self.is_clear_gesture = False
            self.clear_gesture_start = 0
            return GestureType.NONE
        
        landmarks = dict([(id, (x, y)) for id, x, y in landmark_list])
        fingers_extended = self._check_fingers_extended(landmarks)

        pinch_distance = self._calculate_distance(
            landmarks[4],
            landmarks[8]
        )

        print(f"Pinch distance: {pinch_distance}")
        print(f"Fingers extended: {fingers_extended}")

        if pinch_distance < self.pinch_threshold:
            return GestureType.DRAW

        if all(fingers_extended):
            return GestureType.ERASE

        if self._is_select_gesture(landmarks, fingers_extended):
            return GestureType.SELECT

        return GestureType.NONE

    def _check_fingers_extended(self, landmarks):
        fingers = []

        # Helper to determine if a finger is extended based on joint positions
        def is_extended(tip, pip, mcp):
            return landmarks[tip][1] < landmarks[pip][1] < landmarks[mcp][1]

        # Thumb (check X because it sticks out sideways)
        thumb_extended = landmarks[4][0] > landmarks[3][0]  # for right hand
        fingers.append(thumb_extended)

        # Index, Middle, Ring, Pinky
        fingers.append(is_extended(8, 6, 5))   # Index
        fingers.append(is_extended(12, 10, 9)) # Middle
        fingers.append(is_extended(16, 14, 13))# Ring
        fingers.append(is_extended(20, 18, 17))# Pinky

        return fingers

    def _is_select_gesture(self, landmarks, fingers_extended):
        index_extended = fingers_extended[1]
        other_fingers_curled = not any([fingers_extended[2], fingers_extended[3], fingers_extended[4]])

        index_tip = landmarks[8]
        index_pip = landmarks[6]
        
        dx = index_tip[0] - index_pip[0]
        dy = index_tip[1] - index_pip[1]
        angle = abs(math.degrees(math.atan2(dx, -dy)))

        is_vertical = angle < 30
        index_tip_y = landmarks[8][1]
        other_tips_y = [landmarks[i][1] for i in [12, 16, 20]]
        is_highest = all(index_tip_y < y for y in other_tips_y)

        return index_extended and other_fingers_curled and is_vertical and is_highest

    def _calculate_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
