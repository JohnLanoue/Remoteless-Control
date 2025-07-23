#Extended finger evaluations.  Plug into the main loop and these will let you now when a finger is raised.


# Identifies Extended Middle
if (straight_finger([hand_mem[12][3], hand_mem[11][3], hand_mem[10][3], hand_mem[9][3], hand_mem[0][3]])):
    print("Middle")
    cv2.putText(frame, "Middle", (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)
# Identifies Extended Ring Finger
if (straight_finger([hand_mem[16][3], hand_mem[15][3], hand_mem[14][3], hand_mem[13][3], hand_mem[0][3]])):
    print("Ring")
    cv2.putText(frame, "Ring", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)
# Identifies Extended Pinky
if (straight_finger([hand_mem[20][3], hand_mem[19][3], hand_mem[18][3], hand_mem[17][3], hand_mem[0][3]])):
    print("Pinky")
    cv2.putText(frame, "Pinky", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, 1)
if(straight_finger())
# Manual control on 'a' press: Output landmarks