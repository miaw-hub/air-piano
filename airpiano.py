import cv2
import mediapipe as mp
import pygame
import numpy as np

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sounds
sounds = {
    "thumb_left": pygame.mixer.Sound("sounds/C4.wav"),
    "index_left": pygame.mixer.Sound("sounds/D4.wav"),
    "middle_left": pygame.mixer.Sound("sounds/E4.wav"),
    "ring_left": pygame.mixer.Sound("sounds/F4.wav"),
    "pinky_left": pygame.mixer.Sound("sounds/G4.wav"),

    "thumb_right": pygame.mixer.Sound("sounds/A4.wav"),
    "index_right": pygame.mixer.Sound("sounds/B4.wav"),
    "middle_right": pygame.mixer.Sound("sounds/C5.wav"),
    "ring_right": pygame.mixer.Sound("sounds/D5.wav"),
    "pinky_right": pygame.mixer.Sound("sounds/E5.wav")
}

# MediaPipe Hand Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Keep track of which fingers are currently pressed
finger_state = {key: False for key in sounds.keys()}

# Function to detect fingers (index, middle, ring, pinky)
def finger_up(landmarks, tip, pip, threshold=0.02):
    return landmarks[tip].y < landmarks[pip].y - threshold

# Function for thumb detection (depends on hand)
def thumb_up(landmarks, hand_label, threshold=0.02):
    if hand_label == "left":
        return landmarks[4].x < landmarks[3].x - threshold  # Left thumb
    else:
        return landmarks[4].x > landmarks[3].x + threshold  # Right thumb

while True:
    success, img = cap.read()
    if not success:
        break

    # Mirror the camera
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_id, handLms in enumerate(results.multi_hand_landmarks):
            landmarks = handLms.landmark
            hand_label = results.multi_handedness[hand_id].classification[0].label.lower()  # 'left' or 'right'

            # Check fingers
            fingers = {
                "thumb": thumb_up(landmarks, hand_label),
                "index": finger_up(landmarks, 8, 6),
                "middle": finger_up(landmarks, 12, 10),
                "ring": finger_up(landmarks, 16, 14),
                "pinky": finger_up(landmarks, 20, 18)
            }

            # Play sound only on finger press
            for finger_name, is_up in fingers.items():
                key = f"{finger_name}_{hand_label}"
                if is_up and not finger_state[key]:
                    sounds[key].play()
                    finger_state[key] = True
                elif not is_up and finger_state[key]:
                    finger_state[key] = False

            # Draw hand landmarks
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Air Piano", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()