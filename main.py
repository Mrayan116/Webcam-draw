import cv2
import mediapipe as mp


# Open the computer's default webcam
camera = cv2.VideoCapture(0)

# Check if the webcam was opened successfully
if camera.isOpened() == False:
    print("Error: Could not open webcam.")
else:
    # Set up MediaPipe's hand tracking tools
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # Create the hand tracking model
    hands = mp_hands.Hands(
        static_image_mode=False,       # Track hands in a video
        max_num_hands=1,               # Detect only one hand
        min_detection_confidence=0.5,  # Minimum confidence for detecting a hand
        min_tracking_confidence=0.5    # Minimum confidence for tracking a hand
    )

    # Keep reading frames from the webcam
    while True:
        success, frame = camera.read()

        # Only process the frame if it was captured successfully
        if success == True:
            # Flip the frame so it acts like a mirror
            frame = cv2.flip(frame, 1)

            # Convert the frame from BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame to detect hand landmarks
            results = hands.process(rgb_frame)

            # Check if a hand was detected
            if results.multi_hand_landmarks:
                # Go through each detected hand
                for hand_landmarks in results.multi_hand_landmarks:

                    # Get the landmark for the tip of the index finger
                    index_finger = hand_landmarks.landmark[8]

                    # Get the height and width of the webcam frame
                    height, width, channels = frame.shape

                    # Convert the index finger's position from
                    # a value between 0 and 1 to pixel coordinates
                    x = int(index_finger.x * width)
                    y = int(index_finger.y * height)

                    # Draw a circle on the index finger
                    cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                    # Draw the hand landmarks and connections
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

            # Display the webcam frame
            cv2.imshow("Air Drawing Board", frame)

        # Check if a keyboard key was pressed
        key = cv2.waitKey(1)

        # Press 'q' to quit the program
        if key == ord('q'):
            break

    # Release the webcam
    camera.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()
