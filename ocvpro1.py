import cv2 as c
import mediapipe as mp
import time
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
cap = c.VideoCapture(0)
ctime=0
ptime=0
key=c.waitKey(1)
while True:
    success, img = cap.read()
    Rgb = c.cvtColor(img, c.COLOR_BGR2RGB)
    result = hands.process(Rgb)
    #print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        for HandsLms in result.multi_hand_landmarks:
            for id , lm in enumerate(HandsLms.landmark):
                #print(id,lm)
                h,w,cen = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)
                if id in (4,8,16,12,20):
                    c.circle(img, (cx,cy),15,(255,0,255),c.FILLED)
            mpDraw.draw_landmarks(img, HandsLms, mpHands.HAND_CONNECTIONS)

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    c.putText(img, str(int(fps)),(10,70), c.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    c.imshow("Image", img)
    key = c.waitKey(1)
    if key==81 or key==113:
        break
