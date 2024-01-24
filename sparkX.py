import cv2 as c
import sys, random
import pygame as py

py.init()
width, height = 1200, 400
screen = py.display.set_mode((width, height))
clock = py.time.Clock()
fps = 30

# =================================================

face_cas = c.CascadeClassifier(c.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
eye_cas = c.CascadeClassifier(c.data.haarcascades + 'haarcascade_eye.xml')

cap = c.VideoCapture(0)

cap.set(3, width)
cap.set(4, height)

x = 0
y = 0
w = 0
h = 0


class snowBall():
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = py.Rect(self.x, self.y, self.w, self.h)
        self.acc = 1
        self.yvel = 5

    def draw(self, surf):
        py.draw.ellipse(surf, 'white', self.rect)


snowBall_list = []
snowBall_radius = 30

for i in range(10):
    snowBall_list.append(snowBall(random.randint(0, width - snowBall_radius),
                                  random.randint(-height - snowBall_radius, -snowBall_radius), snowBall_radius,
                                  snowBall_radius))

quit = False
bg_image = py.image.load("/home/smith/Downloads/background_for_sparkx.png")

while not quit:
    screen.fill('gray')
    screen.blit(bg_image,[0,0])

    for event in py.event.get():
        if event.type == py.QUIT:
            quit = True

    boo, frm = cap.read()
    frm = c.flip(frm, 1)
    bw = c.cvtColor(frm, c.COLOR_BGR2GRAY)
    face = face_cas.detectMultiScale(bw, scaleFactor=1.5, minNeighbors=4)
    eye = eye_cas.detectMultiScale(bw, scaleFactor = 1.5, minNeighbors = 4)

    for x, y, w, h in face:
        c.rectangle(frm, (x, y), (x + w, y + h), (43, 194, 42), 3)
        break
    for x, y, w, h in eye:
        c.rectangle(frm, (x, y), (x + w, y + h), (35, 145, 65), 2)
    c.imshow('Facee', frm)
    c.imwrite('Fa.png', frm)
    if (c.waitKey(1) & 0xFF) == 27:
        quit = True

    py.draw.rect(screen, 'blue', (x + w / 2, y + h / 2, 20, 20))

    for i in snowBall_list:
        i.rect.y += i.yvel
        i.yvel += i.acc
        if i.rect.y > height:
            i.rect.y = random.randint(-height, -20)
            i.rect.x = random.randint(0, width - 20)
            i.yvel = 3
        i.draw(screen)
        if i.rect.colliderect((x,y,w,h)):
            break

    clock.tick(fps)
    py.display.set_caption(f'Gaim {clock}')
    py.display.update()

cap.release()
c.destroyAllWindows()
sys.exit()
