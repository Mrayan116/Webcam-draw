import cv2
import mediapipe as mp


camera = cv2.VideoCapture(0)

if camera.isOpened() == False:
    print("Error: Could not open webcam.")
else:
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    while True:
        success, frame = camera.read()

        if success == True:
            frame = cv2.flip(frame, 1)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    index_finger = hand_landmarks.landmark[8]

                    height, width, channels = frame.shape

                    x = int(index_finger.x * width)
                    y = int(index_finger.y * height)

                    cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

            cv2.imshow("Air Drawing Board", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()