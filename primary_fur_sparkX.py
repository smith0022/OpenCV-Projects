import cv2 as c
import time
import os
import math
import HandsTrackingModule as htm
import pygame as py
width, height = 1200, 600
screen = py.display.set_mode((width, height))
folderpath  = "/home/smith/sparkX_project_file"#change the directory
mylist = os.listdir(folderpath)
overlaylist=[]
xp,yp=0,0
for imPath in mylist:
    image = c.imread(f'{folderpath}/{imPath}')
    overlaylist.append(image)
header = overlaylist[0]
wCam,hCam= 1200,600
cap = c.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detect = htm.HandDetect(detectC=0.85)
bg_image = py.image.load("/home/smith/sparkX_project_file/primary_bg.jpg")
finger=[0,0,0,0,0]
detonation=5
#position sunmode=((121 240)
# snow mode (470,240)
# dungeon mode (850 240)
while True:
    success, img = cap.read()
    screen.blit(bg_image, [0, 0])
    img = c.flip(img,1)
    img=detect.findhands(img,False)
    lmlist=detect.findPosition(img,draw=False)
    if len(lmlist) != 0:
        x1,y1=lmlist[8][1],lmlist[8][2]
        x2, y2 = lmlist[12][1], lmlist[12][2]
        x3, y3 = lmlist[16][1], lmlist[16][2]
        finger = detect.FingersUp()
        length = math.hypot(x2 - x1, y2 - y1)
        if (finger==[0,1,1,0,0] or finger==[1,1,1,0,0]) and length<50:
            c.circle(img, (x1, y1), 20, (0,0,0),c.FILLED)
            c.circle(img, (x2, y2), 20, (0,0,0),c.FILLED)
            #print(x1,y1)
            if 25<y1<60:#do the coordinates this are wrong :(
                if 200<x1<280:
                    print("sunny mode")
                    cap.release()
                    c.destroyAllWindows()
                    import sparkX
                    break
                    #the game should stop when they show to fingers bascially write if finger==[0,1,1,0,0] or finger==[1,1,1,0,0]: game break
            elif 28<y1<70:
                if 285<x1<333:
                    print("snow mode")

            elif 30<y1<80:
                if 360<x1<411:
                    print("throne mode")

        # if finger==[0,1,0,0,0] or finger==[1,1,0,0,0] :
        #     # c.circle(img, (x1, y1), 20, (0,0,0), c.FILLED)
        if (finger==[0,1,1,1,0] or finger==[1,1,1,1,0]):
            c.circle(img, (x1, y1), 20, (0,0,255), c.FILLED)
            c.circle(img, (x2, y2), 20, (0, 0, 255), c.FILLED)
            c.circle(img, (x3, y3), 20, (0, 0, 255), c.FILLED)
            break
    c.imshow("Image",img)
    py.display.update()
    c.waitKey(1)
