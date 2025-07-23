import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import math


"""Global Variables"""
# Initialize if up gesture occurd
pointer_gesture_mem = 0
# Initializes Output
output = ''
PointerCounter = 0
PointerLock = False
# Initializes recording data frame: We add 5 lines of nothing to pad the loop.
gesture_data = pd.DataFrame(np.zeros((6, 5)), columns=['C1', 'C2', 'C3', 'C4', 'C5'])
gesture_data['Output'] = ''

"""CV Initiations"""
# Initialize Mediapipe Hands solution
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
# Initialize video capture
cap = cv2.VideoCapture(0)

"""Main"""
def get_angle(x1, y1, x2, y2):
    """Calculates the angle between two coordinates in degrees."""
    x_diff = x2 - x1
    y_diff = y2 - y1
    return math.degrees(math.atan2(y_diff, x_diff))
# Points out when a finger is extended.
def straight_finger(land):
    # PRE: Will read an array of 4 coordinates(finger and palm)
    # POST: Will return true if y1>Y2>y3>y4
    return land[4] > land[3] > land[2] > land[1] > land[0]
# Outputs "PointerLock" when pointer finger is raised for 5 or more frames
def lockPointer(f):
    global gesture_data
    global PointerCounter
    global output
    # Identifies when a finger is pointed.
    if (straight_finger([hand_mem[8][3], hand_mem[7][3], hand_mem[6][3], hand_mem[5][3], hand_mem[0][3]])):
        # print("pointer")
        cv2.putText(f, "pointer", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)
        if PointerCounter < 11:
            PointerCounter += 1
    elif PointerCounter > 0:
        PointerCounter -= 1
    if PointerCounter > 5:
        cv2.putText(f, "PointerLock", (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, 1)
        PointerLock = True
    else:
        PointerLock = False
    # Gesture Up
    if PointerLock:
        # Offers Output
        cv2.putText(f, "PointerLock", (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, 1)
        # Gesture up condition:Test this extra
        if [hand_mem[8][3]] - gesture_data['C1'].iloc[-4] > .2 and [hand_mem[7][3]] - gesture_data['C2'].iloc[
            -4] > .2 and [hand_mem[6][3]] - gesture_data['C3'].iloc[-4] > .2:
            # Appendage to the dataframe; we may want to expand on the appendage.
            output = 'Gesture Up'
        elif [hand_mem[8][3]] - gesture_data['C1'].iloc[-4] <= .2 and [hand_mem[7][3]] - \
                gesture_data['C2'].iloc[-4] <= .2 and [hand_mem[6][3]] - gesture_data['C3'].iloc[-4] <= .2:
            output = ''
        # Just in case we have repeats
        else:
            mem = 1
# Prepares the export log
def dataOutput(f):
    global output, gesture_data
    # Writes the landmaarks to a dataframe
    load_data = pd.DataFrame(
        {'C1': [hand_mem[8][3]],#PointerTip
         'C2': [hand_mem[7][3]],#PointerDip
         'C3': [hand_mem[6][3]],#PointerPip
         'C4': [hand_mem[5][3]],#PointerMCP
         'C5': [hand_mem[0][3]],#Wrist
         'Output': output})
    gesture_data = pd.concat([gesture_data, load_data])
    # Resets the output
    output = ''
    # Adds a row when a manual action is called.
    if cv2.waitKey(1) & 0xFF == ord('a'):
        message = "recall" + str(hand_mem[20][3]) + str(hand_mem[19][3]) + str(hand_mem[18][3]) + str(
            hand_mem[17][3]) + str(hand_mem[0][3])
        cv2.putText(f, message, (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)
        print(message)
# This function is for applying when the gesture is up.
def gesture_up(f):
    global gesture_data
    # Range that we determine how far we need to gesture for data to enter.
    threshold = .012
    for i in range(0, 4):
        if gesture_data.iloc[-1, i] - gesture_data.iloc[-2, i] > threshold:
            cv2.putText(f, "Gesture Up", (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, 1)
def gesture_up_2(f):
    #Intent:Instead of generating a CVout, this will generate a boolian
    #Pre:
    #Post:Output a boolian
    global gesture_data
    threshold = .012
    #Finger is within the top 20degreeze of an angle.
    angle_threshold = 10
    #Landmarks of pointer knuckle
    #If landmarks are rising above threshold and angle of the finger is 10 degreese verticle.
    if gesture_data.iloc[-1, 0] - gesture_data.iloc[-2, 0] > threshold \
        and gesture_data.iloc[-1, 1] - gesture_data.iloc[-2, 1] > threshold \
            and gesture_data.iloc[-1, 2] - gesture_data.iloc[-2, 2] > threshold \
                and get_angle(hand_mem[8][2], hand_mem[8][3], hand_mem[5][2],  hand_mem[5][3]) <= angle_threshold:
        # and gesture_data.iloc[-1, 3] - gesture_data.iloc[-2, 3] > threshold
        return True
    else:
        return False
# Secondary loop - could be renamed
def gesture_left(f):
    """"
    See gesture up(2) for requriements: Just need to jesture left
    Alterations:
    1) We will need to have a x-axis offset instead of a y axis change
    2) We will want to make sure to have a 'flat' angle/trajectory.
    """
    global gesture_data
    threshold = .012
    #if gesture_data.iloc[0]==1:
    #    print("TST")
    print(gesture_data.iloc[0])
#Do not work on this until you finish gesture left
def thumbTest(f):
    if (straight_finger([hand_mem[4][3], hand_mem[3][3], hand_mem[2][3], hand_mem[1][3], hand_mem[0][3]]))\
            and not straight_finger([hand_mem[8][3], hand_mem[7][3], hand_mem[6][3], hand_mem[5][3], hand_mem[0][3]]):
        cv2.putText(f, "Thumb", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)
    cv2.putText(f, str(hand_mem[4][3]), (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)
    cv2.putText(f, str(hand_mem[3][3]), (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)
    cv2.putText(f, str(hand_mem[2][3]), (100, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)
    cv2.putText(f, str(hand_mem[1][3]), (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)


    #Depressed Pointer


def placeholder(r, f):  # results, frame
    # Namechange: Eval Landmarks
    global PointerCounter
    global PointerLock
    global gesture_data
    global hand_mem
    global output
    # If a number of frams occur when the pointer finger is up, then we will lock the pointer.
    if r.multi_hand_landmarks:
        for hand_landmarks in r.multi_hand_landmarks:
            hand_mem = []
            for idx, landmark in enumerate(hand_landmarks.landmark):
                # Each landmark is an object with x, y, z attributes
                x = landmark.x
                y = landmark.y
                z = landmark.z
                # print(f"Landmark {idx}: x={x}, y={y}, z={z}")

                # You can use the coordinates (x, y) to draw or track the landmarks
                h, w, _ = f.shape
                x_pixel, y_pixel = int(x * w), int(y * h)

                # Draw a small circle at each landmark position
                cv2.circle(f, (x_pixel, y_pixel), 5, (0, 255, 0), -1)

                # Packs the landmark into memory
                hand_mem.append([idx, x, y, z])
            # Draw landmarks and connections
            mp_drawing.draw_landmarks(f, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Writes Output "PointerLock" if pointer is raised for 5 frames in a row.
            lockPointer(f)
            dataOutput(f)
            #Retired: Still good for testing
            #gesture_up(f)
            if gesture_up_2(f):
                cv2.putText(f, "G2", (500, 50), cv2.FONT_HERSHEY_SIMPLEX,1,  (255, 222, 110), 2)

            gesture_left(f)
            #thumbTest(f): Blocked until we fingish gesture right.
# Main loop: gets called and everyhitng else follows.
def primary():
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            # Flip the frame horizontally for a mirror-like effect
            frame = cv2.flip(frame, 1)
            # Convert the image to RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Process the image to detect hands
            results = hands.process(image_rgb)
            # Call the function that is being modulized
            placeholder(results, frame)
            # Display the frame
            cv2.imshow('Hand Landmarks', frame)
            # Gesture Up
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # np.savetxt('gesture_data.csv', gesture_data, delimiter=',')
                gesture_data.to_csv('gesture_data.csv', index=False)
                break
primary()
cap.release()
cv2.destroyAllWindows()
