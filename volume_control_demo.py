from utils.hand_detector import HandDetector
import cv2
import numpy as np
import math
# from volume_control import VolumeControl

hand_detector = HandDetector(min_detection_confidence=0.7)

webcamFeed = cv2.VideoCapture(0)

# Volume Control
# vol_ctrl = VolumeControl()


def draw_slider(handLandmarks, image, idx=0):
    if(len(handLandmarks) != 0):
        # for volume control we need 4th and 8th landmark
        # details: https://google.github.io/mediapipe/solutions/hands
        x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
        x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
        length = math.hypot(x2-x1, y2-y1)
        print(length)

        # Hand range(length): 50-250
        # Volume Range: (0, 100)

        # coverting length to proportionate to volume range
        volumeValue = np.interp(length, [30, 200], [0, 100])
        # volume.SetMasterVolumeLevel(volumeValue, None)
        # vol_ctrl.set_volume(volumeValue)

        if idx == 0:
            org = (50, 50)
            color = (255, 0, 0)
        elif idx == 1:
            org = (250, 50)
            color = (255, 255, 0)
        elif idx == 2:
            org = (450, 50)
            color = (255, 0, 255)
        elif idx == 3:
            org = (650, 50)
            color = (0, 0, 0)
        else:
            org = (25, 25)
            color = (0, 0, 255)

        cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.putText(image, "{}".format(volumeValue), org=org, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=color, thickness=2)
    
    return image


while True:
    status, image = webcamFeed.read()
    handsLandmarks = hand_detector.infer_hand_landmarks(image=image, draw=True)

    if handsLandmarks == [] :
        print("No Hands Detected")
    else:
        print("{} Hands Detected".format(len(handsLandmarks)))
        for idx, ihand in enumerate(handsLandmarks):
            draw_slider(ihand, image, idx)

    cv2.imshow("Volume", image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
webcamFeed.release()


