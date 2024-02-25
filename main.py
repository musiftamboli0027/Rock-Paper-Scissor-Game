import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    imgScales = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScales = imgScales[:, 80:480]

    # find Hands
    hands, img = detector.findHands(imgScales)

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    imgAI = None
                    PlayerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        PlayerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        PlayerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        PlayerMove = 3

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # playerMove
                    if (PlayerMove == 1 and randomNumber == 3) or \
                            (PlayerMove == 2 and randomNumber == 1) or \
                            (PlayerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AIMove
                    if (PlayerMove == 3 and randomNumber == 1) or \
                            (PlayerMove == 1 and randomNumber == 2) or \
                            (PlayerMove == 2 and randomNumber == 3):
                        scores[0] += 1

    imgBG[234:654, 795:1195] = imgScales

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Scaled", imgScales)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
