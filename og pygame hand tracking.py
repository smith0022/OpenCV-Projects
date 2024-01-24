import cv2 as c
import pygame as py
import mediapipe as mp
import time, sys

width = 1200
height = 400
py.init()
width, height = 1200, 600
screen = py.display.set_mode((width, height))
clock = py.time.Clock()
fps = 60

# ======================================================

cap = c.VideoCapture(1)
ctime = 0
ptime = 0

cap.set(3, 2400)
cap.set(4, 1200)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands(max_num_hands = 1)

# =======================================================
quit = False
while not quit:
    screen.fill((100, 100, 100))
    for event in py.event.get():
        if event.type == py.QUIT:
            quit = True

    box = py.Rect(200, 200, 50, 50)
    

# =================================================================================

    success, img = cap.read()
    img = c.flip(img, 1)

    imgRGB = c.cvtColor(img, c.COLOR_BGR2RGB)

    result = hands.process(imgRGB)
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * width), int(lm.y * height)
                py.draw.ellipse(screen, 'green', (cx, cy, 20, 20))

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    # ctime = time.time()
    # fps = 1/(ctime-ptime)
    # ptime = ctime
    # c.putText(img, str(int(fps)), (10, 70), c.FONT_HERSHEY_PLAIN, 3, (200, 0, 0), 3)

    c.imshow("Image", img)

    if c.waitKey(1) == ord('q'):
        quit = True

# ============================================================================================


    py.draw.rect(screen, 'red', box)

    clock.tick(fps)
    py.display.set_caption(str(clock))
    py.display.update()

cap.release()
c.destroyAllWindows()
py.quit()
sys.exit()