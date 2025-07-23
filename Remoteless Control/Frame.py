import cv2
import mediapipe as mp

# Initialize Mediapipe Hands solution
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)

# Create a hands object to detect hands
with mp_hands.Hands(static_image_mode=False,
                    max_num_hands=2,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Flip the frame horizontally for a mirror-like effect
        frame = cv2.flip(frame, 1)

        # Convert the image color space from BGR to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the RGB image to detect hands
        results = hands.process(image_rgb)

        # Get image dimensions
        h, w, _ = frame.shape

        # If hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the bounding box around the hand
                x_min = w
                y_min = h
                x_max = 0
                y_max = 0

                # Iterate through all the hand landmarks to calculate the bounding box
                for lm in hand_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    x_min = min(x_min, x)
                    y_min = min(y_min, y)
                    x_max = max(x_max, x)
                    y_max = max(y_max, y)

                # Draw the bounding box (ROI) around the detected hand
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                # Optionally, you can draw hand landmarks (Mediapipe feature)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the frame with ROI
        cv2.imshow('Hand Detection with ROI', frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
