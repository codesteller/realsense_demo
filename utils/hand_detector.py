from mediapipe.python.solutions.hands import HandLandmark
import cv2
import math
import numpy as np
import mediapipe as mdp


# Global Variables
mdp_hands = mdp.solutions.mediapipe.python.solutions.hands
mdp_draw = mdp.solutions.mediapipe.python.solutions.drawing_utils


class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = mdp_hands.Hands(max_num_hands=max_num_hands,
                                     min_detection_confidence=min_detection_confidence,
                                     min_tracking_confidence=min_tracking_confidence)

    def infer_hand_landmarks(self, image, draw=False):
        _image = image.copy()
        # Convert image to RGB as Opencv reads images in BGR
        _image = cv2.cvtColor(_image, cv2.COLOR_BGR2RGB)

        # Inference
        _image.flags.writeable = False
        detection_output = self.hands.process(_image)
        _image.flags.writeable = True

        # Post Process the results
        hands_landmarks = list()

        if detection_output.multi_hand_landmarks is None:
            pass
        else:
            # The multi_hand_landmarks returns landMarks for all the hands
            # However we are interested in just one hand
            for ihand in range(0, len(detection_output.multi_hand_landmarks)):
                hand = detection_output.multi_hand_landmarks[ihand]
                landmark_list = list()
                for id, landMark in enumerate(hand.landmark):
                    # landMark holds x,y,z ratios of single landmark
                    imgH, imgW, imgC = image.shape  # height, width, channel for image
                    xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                    landmark_list.append([id, xPos, yPos])

                if draw:
                    mdp_draw.draw_landmarks(
                        image, hand, mdp_hands.HAND_CONNECTIONS)

                hands_landmarks.append(landmark_list)

        if hands_landmarks == [] :
            print("No Hands Detected")
        else:
            print("{} Hands Detected".format(len(hands_landmarks)))
            if draw:
                for idx, ihand in enumerate(hands_landmarks):
                    self.draw_slider(ihand, image, idx)

        return hands_landmarks
        
    @staticmethod
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


