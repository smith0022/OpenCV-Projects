import numpy as np
import math
from random import randint as rn
import HandsTrackingModule as hdt
import cv2 as c
import time
from subprocess import call
#from ctypes import cast, POINTER
#rom comtypes import CLSCTX_ALL
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
wCam,hCam= 720,640
cap = c.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
ctime = 0
ptime = 0
HDT=hdt.HandDetect(detectC=0.7)

# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# #volume.GetMute()
# #volume.GetMasterVolumeLevel()
# volrange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-5.0, None)
while True:
    success, img = cap.read()
    img = HDT.findhands(img,False)#put false fr noy showing the lines
    lmlist =  HDT.findPosition(img)#false for not shoing dots as well
    if len(lmlist) != 0:
        finger = HDT.FingersUp()

        #print(lmlist[4],lmlist[8])
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx,cy=(x1+x2)/2,(y1+y2)/2
        #print(cx,cy)
        k=(200,20,200)
        c.circle(img,(x1,y1),15,k,c.FILLED)
        c.circle(img,(x2,y2),15,k,c.FILLED)
        c.circle(img,(int(cx),int(cy)),15,k,c.FILLED)
        c.line(img,(x1,y1),(x2,y2),k,3)
        length = math.hypot(x2-x1,y2-y1)
        print(length)
        if length <50:
            c.circle(img, (int(cx),int(cy)), 15, (255,0,0), c.FILLED)
        if length > 370:
            c.circle(img, (int(cx), int(cy)), 15, (0, 0, 255), c.FILLED)
        valid = False
        if finger == [0, 1, 1, 1, 0] or finger == [1, 1, 1, 1, 0]:
            break
        while not valid:
            volume = (length/300)*100

            try:
                volume = int(volume)

                if (volume <= 100) and (volume >= 0):
                    call(["amixer", "-D", "pulse", "sset", "Master", str(volume) + "%"])
                    valid = True
                if finger == [0, 1, 1, 1, 0] or finger == [1, 1, 1, 1, 0]:
                    break

            except ValueError:
                pass

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    c.putText(img, f'FPS: {str(int(fps))}', (10, 20), c.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    c.imshow("Image", img)
    key = c.waitKey(1)
    if key==83 or key ==113:
        break
