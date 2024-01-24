import cv2 as c
import sys
import HandsTrackingModule

width, height = 600, 450

board = [[' ', ' ', ' '],
[' ', ' ', ' '],
[' ', ' ', ' ']]

def drawBoard(img, start, end, color):
    w = end[0] - start[0]
    h = end[1] - start[1]
    c.line(img, (start[0] + w//3, start[1]), (start[0] + w//3, end[1]), color, thickness=3)
    c.line(img, (start[0] + 2*(w//3), start[1]), (start[0] + 2*(w//3), end[1]), color, thickness=3)
    c.line(img, (start[0], start[1] + h//3), (end[0], start[1] + h//3), color, thickness=3)
    c.line(img, (start[0], start[1] + 2*(h//3)), (end[0], start[1] + 2*(h//3)), color, thickness=3)




def boardCheck(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == 'x':
            return 'x'
        
        elif board[i][0] == board[i][1] == board[i][2] == 'o':
            return 'o'

    for i in range(3):
        
        if board[0][i] == board[1][i] == board[2][i] == 'x':
            return 'x'

        elif board[0][i] == board[1][i] == board[2][i] == 'o':
            return 'o'

    if board[0][0] == board[1][1] == board[2][2] == 'x':
        return 'x'

    elif board[0][0] == board[1][1] == board[2][2] == 'o':
        return 'o'

    elif board[0][2] == board[1][1] == board[2][0] == 'x':
        return 'x'

    elif board[0][2] == board[1][1] == board[2][0] == 'o':
        return 'o'

    elif board[0][0] != ' ' and board[0][1] != ' ' and board[0][2] != ' ' and board[1][0] != ' ' and board[1][1] != ' ' and board[1][2] != ' ' and board[2][0] != ' ' and board[2][1] != ' ' and board[2][2] != ' ':
        return 'no one'




    

class Player:
    def __init__(self, x, y, w, h, type):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = (self.x + self.w//2, self.y + self.h//2)
        self.type = type
        self.isMoveable = True

    def update(self, img):
        self.center = (self.x + self.w//2, self.y + self.h//2)
        if self.type == 'o':
            c.circle(img, self.center, self.w//2, (0, 255, 0), thickness=5)
        elif self.type == 'x':
            c.line(img, (self.x, self.y), (self.x+self.w, self.y+self.h), (0, 0, 255), thickness=5)
            c.line(img, (self.x+self.w, self.y), (self.x, self.y+self.h), (0, 0, 255), thickness=5)

playerList = []
for i in range(5):
    playerList.append(Player(10, 10, 60, 60, 'x'))
    playerList.append(Player((width-110), 10, 60, 60, 'o'))

cap = c.VideoCapture(2)
cap.set(3, width)
cap.set(4, height)

detector = HandsTrackingModule.HandDetect()

quit = False
winner = None
start, end = (180, 80), (500, 400)
clickDist = 45
while not quit:
    success, img = cap.read()
    img = c.flip(img, 3)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:
        l, _, _ = detector.findDistance(8, 4, img)
        indexFinger = lmList[8]

        for player in playerList:
            cx = player.center[0]
            cy = player.center[1]
            w = end[0] - start[0]
            h = end[1] - start[1]
            
            if winner:
                player.isMoveable = False

            if cx > start[0] and cx < start[0] + w//3 and cy > start[1] and cy < start[1] + h//3 and l >= clickDist and board[0][0] == ' ':
                player.isMoveable = False
                board[0][0] = player.type
            elif cx > start[0] + w//3 and cx < start[0] + 2*(w//3) and cy > start[1] and cy < start[1] + h//3 and l >= clickDist and board[0][1] == ' ':
                player.isMoveable = False
                board[0][1] = player.type
            elif cx > start[0] + 2*(w//3) and cx < end[0] and cy > start[1] and cy < start[1] + h//3 and l >= clickDist and board[0][2] == ' ':
                player.isMoveable = False
                board[0][2] = player.type
            elif cx > start[0] and cx < start[0] + w//3 and cy > start[1] + h//3 and cy < start[1] + 2*(h//3) and l >= clickDist and board[1][0] == ' ':
                player.isMoveable = False
                board[1][0] = player.type
            elif cx > start[0] + w//3 and cx < start[0] + 2*(w//3) and cy > start[1] + h//3 and cy < start[1] + 2*(h//3) and l >= clickDist and board[1][1] == ' ':
                player.isMoveable = False
                board[1][1] = player.type
            elif cx > start[0] + 2*(w//3) and cx < end[0] and cy > start[1] + h//3 and cy < start[1] + 2*(h//3) and l >= clickDist and board[1][2] == ' ':
                player.isMoveable = False
                board[1][2] = player.type
            elif cx > start[0] and cx < start[0] + w//3 and cy > start[1] + 2*(h//3) and cy < end[1] and l >= clickDist and board[2][0] == ' ':
                player.isMoveable = False
                board[2][0] = player.type
            elif cx > start[0] + w//3 and cx < start[0] + 2*(w//3) and cy > start[1] + 2*(h//3) and cy < end[1] and l >= clickDist and board[2][1] == ' ':
                player.isMoveable = False
                board[2][1] = player.type
            elif cx > start[0] + 2*(w//3) and cx < end[0] and cy > start[1] + 2*(h//3) and cy < end[1] and l >= clickDist and board[2][2] == ' ':
                player.isMoveable = False
                board[2][2] = player.type

            if player.x < indexFinger[0] and player.x+player.w > indexFinger[0] and player.y < indexFinger[1] and player.y+player.h > indexFinger[1] and l < 35 and player.isMoveable:
                player.x = int(indexFinger[0] - player.w/2)
                player.y = int(indexFinger[1] - player.h/2)
                break

    # c.rectangle(img, (10, 10), (110, 110), (255, 0, 255), c.FILLED)
    for player in playerList:
        player.update(img)

    drawBoard(img, start, end, (0, 0, 0))
    winner = boardCheck(board)
    if winner:
        img = c.putText(img, f'{winner.upper()} is the winner', (160, 30), c.FONT_HERSHEY_COMPLEX, 1, (30, 0, 200), thickness = 2)

    img = c.resize(img, (1200, 900), interpolation=c.INTER_AREA)
    c.imshow('Image', img)
    if c.waitKey(1) == ord('q'):
        quit = True

c.destroyAllWindows()
sys.exit()