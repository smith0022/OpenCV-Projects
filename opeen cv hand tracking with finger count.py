import cv2 as c
import pygame as py
import mediapipe as mp
import time, sys

width, height = 1200, 600

py.init()
screen = py.display.set_mode((width, height))
clock = py.time.Clock()

cap = c.VideoCapture(0)
ctime = 0
ptime = 0

cap.set(c.CAP_PROP_FRAME_WIDTH, width)
cap.set(c.CAP_PROP_FRAME_HEIGHT, height)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands(max_num_hands = 1)

# =============================================================
bg = py.image.load('background.jpeg')
# bg = py.transform.rotozoom(bg, 0, 2)
quit = False
while not quit:
    screen.fill((47,79,79))

    success, img = cap.read()
    img = c.flip(img, 1)

    imgRGB = c.cvtColor(img, c.COLOR_BGR2RGB)

    result = hands.process(imgRGB)
    fingerCount = 0
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            if handLms.landmark[4].x <  handLms.landmark[2].x:
                fingerCount += 1
            if handLms.landmark[8].y <  handLms.landmark[6].y:
                fingerCount += 1
            if handLms.landmark[12].y <  handLms.landmark[10].y:
                fingerCount += 1
            if handLms.landmark[16].y <  handLms.landmark[14].y:
                fingerCount += 1
            if handLms.landmark[20].y <  handLms.landmark[18].y:
                fingerCount += 1
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * width), int(lm.y * height)
                py.draw.ellipse(screen, 'purple', (cx, cy, 15, 15))

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    c.putText(img, str(int(fps)), (10, 70), c.FONT_HERSHEY_PLAIN, 3, (200, 0, 0), 3)
    c.putText(img, str(fingerCount), (10, 140), c.FONT_HERSHEY_PLAIN, 3, (0, 200, 0), 3)

    c.imshow("Image", img)

    if c.waitKey(1) == ord('q'):
        quit = True

# ============================================================================================


    py.display.update()
    py.display.set_caption(str(clock.get_fps()))
    clock.tick(60)

cap.release()
c.destroyAllWindows()
py.quit()
sys.exit()