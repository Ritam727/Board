import numpy as np
import cv2 as cv
from screeninfo import get_monitors
from cv2 import getTrackbarPos as gtp
from datetime import datetime
import subprocess as sb
import os

drawing = False
min_width = 300
min_height = 300
height = 500
width = 700
brushColor = [255, 255, 255]
brushSize = 2
mode = True
screenDim = (get_monitors()[0].height, get_monitors()[0].width)
ix, iy = -1, -1
changes = []
# redoList = []
startIndexOfChange = 0
oneTimeChange = []
backgroundColor = [0,0,0]

# does nothing but needed for Trackbar
def nothing(t):
    pass

def draw(event, x, y, flags, param):
    global startIndexOfChange,drawing, brushColor, brushSize, ix, iy

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        startIndexOfChange = len(changes)
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            changes.append([(ix,iy),(x,y),tuple(brushColor),brushSize])
            ix, iy = x, y
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        changes.append([(ix, iy), (x, y), tuple(brushColor), brushSize])
        endIndexOfChange = len(changes)
        oneTimeChange.append((startIndexOfChange, endIndexOfChange))

def drawChanges(img, changes):
    for i in changes:
        cv.line(img, i[0], i[1],i[2], i[3])
    return img


cv.namedWindow('Controls')
# controls for color and brush size
cv.createTrackbar('R', 'Controls', 0, 255, nothing)
cv.createTrackbar('G', 'Controls', 0, 255, nothing)
cv.createTrackbar('B', 'Controls', 0, 255, nothing)
cv.createTrackbar('Background Color', 'Controls', 255, 255, nothing)
cv.createTrackbar('Brush Size', 'Controls', 5, 20, nothing)
cv.createTrackbar('Eraser Size', 'Controls', 10, 50, nothing)
# controls for window size
cv.createTrackbar('Height', 'Controls', height, screenDim[0]-105, nothing)
cv.createTrackbar('Width', 'Controls', width, screenDim[1], nothing)

cv.namedWindow("Paint")
cv.setMouseCallback('Paint', draw)

while True:
    temp = gtp('Background Color', 'Controls')
    backgroundColor = [temp,temp,temp]
    height = max(300,gtp('Height', 'Controls'))
    width = max(300,gtp('Width', 'Controls'))

    img = np.zeros((height, width, 3), np.uint8)
    cv.rectangle(img, (0,0), (width, height), tuple(backgroundColor), -1)
    img = drawChanges(img, changes)
    cv.imshow('Paint', img)

    k = cv.waitKey(1) & 0xFF
    if k == 27:
        # 27 is for escape key
        break
    elif k == ord('s'):
        print("Saving...")
        exists = sb.run("ls | grep savedImages", shell = True, capture_output = True)
        if exists.stdout.decode("utf-8") == "":
            os.system("mkdir savedImages")
        curr = str(datetime.now()).split()
        cv.imwrite("./savedImages/BoardDrawing_"+curr[0]+"_"+curr[1]+".png", img[:, :img.shape[1]-60])
    elif k == ord('e'):
        # eraser mode toggle
        mode = not mode
    elif k == ord('n'):
        # erase everything and start new board
        changes = []
    elif k == ord('z'):
        otc = oneTimeChange[len(oneTimeChange)-1]
        
        # for redo , not complete yet
        # for i in changes[otc[0]:otc[1]]:
        #     redoList.append(i)
        
        changes = changes[:otc[0]]
        oneTimeChange = oneTimeChange[:len(oneTimeChange)-1]


    if mode == False:
        # when eraser mode on then brush color = background color
        brushColor = backgroundColor
        brushSize = max(1,gtp('Eraser Size', 'Controls'))
    else:
        brushColor = [gtp('B', 'Controls'), gtp('G', 'Controls'), gtp('R', 'Controls')]
        brushSize = max(1,gtp('Brush Size', 'Controls'))

    currentColorImg = np.zeros((200, 350, 3), np.uint8)
    cv.rectangle(currentColorImg, (0,0), (350, 200), tuple(brushColor), -1)
    cv.imshow("Controls", currentColorImg)

cv.destroyAllWindows()
