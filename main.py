import numpy as np
import cv2 as cv
from screeninfo import get_monitors
from cv2 import getTrackbarPos as gtp
import sys

# defaults to not save the image
save_image = False
# if there is an argument called save
# it will change it to True
if len(sys.argv) == 2 and sys.argv[1] == "save":
    save_image = True

drawing = False
brColor = [255, 255, 255]
brushSize = 2
mode = True
screenDim = (get_monitors()[0].height, get_monitors()[0].width)
ix, iy = -1, -1

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

img = np.zeros((screenDim[0]-200, screenDim[1], 3), np.uint8)
cv.namedWindow('Paint')
cv.createTrackbar('R', 'Paint', 255, 255, nothing)
cv.createTrackbar('G', 'Paint', 255, 255, nothing)
cv.createTrackbar('B', 'Paint', 255, 255, nothing)
cv.createTrackbar('Brush Size', 'Paint', 2, 20, nothing)
cv.setMouseCallback('Paint', draw)
prev = brColor

while True:
    cv.imshow('Paint', img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        if save_image:
            cv.imwrite("painting.jpg", img)
        break
    elif k == ord('e'):
        mode = not mode

    if not mode:
        brColor = [0, 0, 0]
        brushSize = gtp('Brush Size', 'Paint')*10
    else:
        brColor = [gtp('B', 'Paint'), gtp('G', 'Paint'), gtp('R', 'Paint')]
        brushSize = gtp('Brush Size', 'Paint')

    cv.rectangle(img, (screenDim[1]-60, 0), (screenDim[1], 60), tuple(brColor), -1)

cv.destroyAllWindows()
