import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
# Added confidence parameters for smoother tracking
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    # --- THE MIRROR FIX ---
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Drawing the skeleton
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Optional: Label the fingers to help with your piano logic later
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # Drawing a small circle on the index finger tip (ID 8)
                if id == 8:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

    cv2.imshow("Hand Test (Mirrored)", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()