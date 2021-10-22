import numpy as np
import cv2 as cv
from cv2 import getTrackbarPos as gtp

drawing = False
brColor = [255, 255, 255]
brushSize = 2
mode = True

def nothing(t):
    pass

def draw(event, x, y, flags, param):
    global drawing, brColor, brushSize

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.circle(img, (x, y), brushSize, tuple(brColor), -1)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.circle(img, (x, y), brushSize, tuple(brColor), -1)

img = np.zeros((720, 1280, 3), np.uint8)
cv.namedWindow('Paint')
cv.createTrackbar('B', 'Paint', 255, 255, nothing)
cv.createTrackbar('G', 'Paint', 255, 255, nothing)
cv.createTrackbar('R', 'Paint', 255, 255, nothing)
cv.createTrackbar('Brush Size', 'Paint', 2, 20, nothing)
cv.setMouseCallback('Paint', draw)
prev = brColor

while True:
    cv.imshow('Paint', img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    elif k == ord('e'):
        mode = not mode

    if not mode:
        brColor = [0, 0, 0]
    else:
        brColor = [gtp('R', 'Paint'), gtp('G', 'Paint'), gtp('B', 'Paint')]
    brushSize = gtp('Brush Size', 'Paint')

    cv.rectangle(img, (1260, 0), (1280, 20), tuple(brColor), -1)

cv.destroyAllWindows()
