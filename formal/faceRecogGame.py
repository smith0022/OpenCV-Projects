import cv2 as c
import pygame as py
import time, sys, random

width, height = 1200, 600

py.init()
screen = py.display.set_mode((width, height))
clock = py.time.Clock()

faceCascade = c.CascadeClassifier(c.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

cap = c.VideoCapture(0)
ctime = 0
ptime = 0

cap.set(c.CAP_PROP_FRAME_WIDTH, width)
cap.set(c.CAP_PROP_FRAME_HEIGHT, height)

class Snowball:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = py.Rect(random.randint(0, width - self.w), -random.randint(0, height), self.w, self.h)
        self.yvel = 0
        self.yacc = 1

    def update(self, surf):
        self.rect.y += self.yvel
        self.yvel += self.yacc

        py.draw.ellipse(surf, 'white', self.rect)

        if self.rect.y > height:
            self.rect.y =-random.randint(0, height)
            self.yvel = 0

snowballList = []
for i in range(10):
    snowballList.append(Snowball(0, 0, 20, 20))

# =============================================================

bg = py.image.load('background.jpeg')
player = py.image.load('player.PNG')
# bg = py.transform.rotozoom(bg, 0, 2)
x, y, w, h = (0, 0, 0, 0)
quit = False
while not quit:
    screen.fill((47,79,79))
    for event in py.event.get():
        if event.type == py.QUIT:
            quit = True

    success, img = cap.read()
    img = c.flip(img, 1)
    imgGRAY = c.cvtColor(img, c.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGRAY, scaleFactor=1.5, minNeighbors=5)
    if len(faces) != 0:
        x, y, w, h = faces[0]
    screen.blit(player, (x + w/2, y + h/2))

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    c.putText(img, str(int(fps)), (10, 70), c.FONT_HERSHEY_PLAIN, 3, (200, 0, 0), 3)

    c.imshow("Image", img)

    if c.waitKey(1) & 0xFF == ord('q'):
        quit = True

# ============================================================================================

    for snowball in snowballList:
        snowball.update(screen)
    py.display.set_caption(str(clock.get_fps()))
    py.display.update()
    clock.tick(60)

cap.release()
c.destroyAllWindows()
py.quit()
sys.exit()