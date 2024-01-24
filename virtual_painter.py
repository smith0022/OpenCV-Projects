import cv2 as c
import numpy as np
import time
import os
import math
import HandsTrackingModule as htm
folderpath  = "/home/smith/Da Painter"
mylist = os.listdir(folderpath)
mylist = mylist[:-1]
#print(mylist)
overlaylist=[]
drawcolor = (0,0,0)
brushthicc=7
imgcan=np.zeros((480,640,3),np.uint8)
xp,yp=0,0
for imPath in mylist:
    image = c.imread(f'{folderpath}/{imPath}')
    overlaylist.append(image)
#print(len(overlaylist))
header = overlaylist[0]
wCam,hCam= 480,640
cap = c.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detect = htm.HandDetect(detectC=0.85)
while True:
    success, img = cap.read()
    img = c.flip(img,1)
    img=detect.findhands(img,False)
    lmlist=detect.findPosition(img,draw=False)
    if len(lmlist) != 0:
        x1,y1=lmlist[8][1],lmlist[8][2]
        x2, y2 = lmlist[12][1], lmlist[12][2]
        finger = detect.FingersUp()
        length = math.hypot(x2 - x1, y2 - y1)
        #print(length)
        #print(finger)
        if (finger==[0,1,1,0,0] or finger==[1,1,1,0,0]) and length<50:
            #c.circle(img, (x1, y1), 20, (0,0,0),c.FILLED)
            #c.circle(img, (x2, y2), 20, (0,0,0),c.FILLED)
            #print("selectioon mode")
            if 90<y1:
                header=overlaylist[0]
            elif 25<y1<60:
                if 200<x1<280:
                    header=overlaylist[2]
                    brushthicc = 7
                    drawcolor = (255, 0, 0)
            elif 28<y1<70:
                if 285<x1<333:
                    brushthicc = 7
                    header=overlaylist[3]
                    drawcolor = (0, 0, 255)

            elif 30<y1<80:
                if 360<x1<411:
                    header=overlaylist[1]
                    brushthicc = 7
                    drawcolor = (0, 255, 255)
            if 30<y1<80:
                if 444<x1<500:
                    header = overlaylist[0]
                    brushthicc=25
                    drawcolor=(0,0,0)
            print(drawcolor)
            c.rectangle(img, (x1, y1), (x2, y2),drawcolor, c.FILLED)

        if finger==[0,1,0,0,0] or finger==[1,1,0,0,0] :
            c.circle(img, (x1, y1), 20, (0,0,0), c.FILLED)
            print("drawing mode mode")
            if xp==0 and yp==0:
                xp,yp=x1,y1
            #c.line(imgcan,(xp,yp),(x1,y1),drawcolor,brushthicc)
            c.circle(imgcan, (x1, y1), brushthicc,drawcolor, c.FILLED)
            c.line(img,(xp,yp),(x1,y1),drawcolor,brushthicc)
            xp, yp = x1, y1
        if finger == [0, 1, 1, 1, 0] or finger == [1, 1, 1, 1, 0]:
            break



    imggray=c.cvtColor(imgcan,c.COLOR_BGR2GRAY)
    _,imgInv=c.threshold(imggray,50,255,c.THRESH_BINARY_INV)
    imgInv=c.cvtColor(imgInv,c.COLOR_GRAY2BGR)
    img=c.bitwise_and(img,imgInv)
    img=c.bitwise_or(img,imgcan)

    img[0:105,80:560] = header
    img = c.addWeighted(img,0.5,imgcan,0.5,0)
    c.imshow("Image",img)
    #c.imshow("draw",imgcan)
    c.waitKey(1)