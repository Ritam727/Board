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
brColor = [255, 255, 255]
brushSize = 2
mode = True
screenDim = (get_monitors()[0].height, get_monitors()[0].width)
ix, iy = -1, -1

# does nothing but needed for Trackbar
def nothing(t):
    pass

def draw(event, x, y, flags, param):
    global drawing, brColor, brushSize, ix, iy

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.line(img, (ix, iy), (x, y), tuple(brColor), brushSize)
            ix, iy = x, y
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.line(img, (ix, iy), (x, y), tuple(brColor), brushSize)

# setting up canvas to draw on
img = np.zeros((height, width, 3), np.uint8)

# controls for color and brush size
cv.namedWindow('Paint')
cv.createTrackbar('R', 'Paint', 255, 255, nothing)
cv.createTrackbar('G', 'Paint', 255, 255, nothing)
cv.createTrackbar('B', 'Paint', 255, 255, nothing)
cv.createTrackbar('Brush Size', 'Paint', 2, 20, nothing)

# controls for window size
cv.namedWindow("Controls")
cv.createTrackbar('Height', 'Controls', height, screenDim[0]-205, nothing)
cv.createTrackbar('Width', 'Controls', width, screenDim[1], nothing)
cv.setMouseCallback('Paint', draw)

while True:

    heightn = gtp('Height', 'Controls')
    widthn = gtp('Width', 'Controls')
    if heightn!= height or widthn!=width:
        if heightn > min_height:
            height = heightn
        if widthn > min_width:
            width = widthn
        img = cv.resize(img , dsize = (width, height), interpolation = cv.INTER_CUBIC)

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

    if not mode:
        # when eraser mode on then brush color = background color
        brColor = [0, 0, 0]
        brushSize = gtp('Brush Size', 'Paint')*10
    else:
        brColor = [gtp('B', 'Paint'), gtp('G', 'Paint'), gtp('R', 'Paint')]
        brushSize = gtp('Brush Size', 'Paint')

    cv.rectangle(img, (screenDim[1]-60, 0), (screenDim[1], 60), tuple(brColor), -1)

cv.destroyAllWindows()
