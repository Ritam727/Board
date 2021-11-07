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

# does nothing but needed for Trackbar
def nothing(t):
    pass

def draw(event, x, y, flags, param):
    global drawing, brushColor, brushSize, ix, iy

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.line(img, (ix, iy), (x, y), tuple(brushColor), brushSize)
            ix, iy = x, y
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.line(img, (ix, iy), (x, y), tuple(brushColor), brushSize)

# setting up canvas to draw on
# background color is black
backgroundColor = [0,0,0]
img = np.zeros((height, width, 3), np.uint8)

cv.namedWindow('Controls')
# controls for color and brush size
cv.createTrackbar('R', 'Controls', 255, 255, nothing)
cv.createTrackbar('G', 'Controls', 255, 255, nothing)
cv.createTrackbar('B', 'Controls', 255, 255, nothing)
cv.createTrackbar('Background Color', 'Controls', 0, 255, nothing)
cv.createTrackbar('Brush Size', 'Controls', 5, 20, nothing)
cv.createTrackbar('Eraser Size', 'Controls', 10, 50, nothing)
# controls for window size
cv.createTrackbar('Height', 'Controls', height, screenDim[0]-205, nothing)
cv.createTrackbar('Width', 'Controls', width, screenDim[1], nothing)

cv.namedWindow("Paint")
cv.setMouseCallback('Paint', draw)

while True:
    bgcolornewValue = gtp("Background Color", "Controls")
    backgroundColorNew = [bgcolornewValue, bgcolornewValue, bgcolornewValue]

    if backgroundColorNew != backgroundColor:
        color_low=np.array([i-10 for i in backgroundColor])    # Define lower and uppper limits
        color_high=np.array([i+10 for i in backgroundColor])
        mask=cv.inRange(img, color_low, color_high)  # Mask image to only select previous color
        img[mask>0]= tuple(backgroundColorNew) # Change image to newColor where we found previous BackgroundColor
        backgroundColor = backgroundColorNew

    heightNew = gtp('Height', 'Controls')
    widthNew = gtp('Width', 'Controls')
    if heightNew!= height or widthNew!=width:
        if heightNew < min_height:
            heightNew = min_height
        if widthNew < min_width:
            widthNew = min_width

        if(heightNew > height or widthNew > width):
            imgNew = np.zeros((heightNew, widthNew, 3), np.uint8)
            imgNew[:height,:width] = img
            img = imgNew
        else:
            img = cv.resize(img , dsize = (widthNew, heightNew), interpolation = cv.INTER_CUBIC)
        height, width = heightNew, widthNew

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
        img = np.zeros((height, width, 3), np.uint8)
        backgroundColor = [0,0,0]

    if not mode:
        # when eraser mode on then brush color = background color
        brushColor = backgroundColor
        brushSize = 1 + gtp('Eraser Size', 'Controls')
    else:
        brushColor = [gtp('B', 'Controls'), gtp('G', 'Controls'), gtp('R', 'Controls')]
        brushSize = 1 + gtp('Brush Size', 'Controls')

    currentColorImg = np.zeros((200, 350, 3), np.uint8)
    cv.rectangle(currentColorImg, (0,0), (350, 200), tuple(brushColor), -1)
    cv.imshow("Controls", currentColorImg)

cv.destroyAllWindows()
