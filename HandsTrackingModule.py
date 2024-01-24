import cv2 as c
import mediapipe as mp
import time


class HandDetect() :
    def __init__(self, mode=False, maxhands=2, detectC=0.5, trackC=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detectC = detectC
        self.trackC = trackC
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxhands, self.detectC, self.trackC)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]
    def findhands(self,img,draw = True):
        Rgb = c.cvtColor(img, c.COLOR_BGR2RGB)
        self.result = self.hands.process(Rgb)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for HandsLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, HandsLms, self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self,img,handNo=0,draw=True):
        self.lmlist = []
        if self.result.multi_hand_landmarks:
            myhand=self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                # print(id,lm)
                h, w, cen = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                self.lmlist.append([id,cx, cy])
                #if id in (4, 8, 16, 12, 20) and draw==True:
                    #c.circle(img, (cx, cy), 15, (255, 0, 255), c.FILLED)return
        return self.lmlist
    def FingersUp(self):
        finger = []
        if self.lmlist[self.tipIds[0]][1] <  self.lmlist[self.tipIds[0]-1][1]:
            finger.append(1)
        else:
            finger.append(0)
        for id in range(1,5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id]-2][2]:
                finger.append(1)
            else:
                finger.append(0)
        return finger
def main():#to write from this everytime for usuage
    cap = c.VideoCapture(0)
    ctime = 0
    ptime = 0
    HDT=HandDetect()
    while True:
        success, img = cap.read()
        img = HDT.findhands(img,False)#put false fr noy showing the lines
        HDT.findPosition(img)#false for not shoing dots as well
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        c.putText(img, str(int(fps)), (10, 70), c.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        c.imshow("Image", img)
        c.waitKey(1)
if __name__ == "__main__":
    main()