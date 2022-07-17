
from cv2 import *
from cv2 import imshow
from cv2 import waitKey
from cv2 import VideoCapture
from cv2 import cvtColor
from cv2 import inRange
from cv2 import COLOR_BGR2HSV
import cv2
import numpy as np

# for red colors

lower = np.array([8, 100, 20])
upper = np.array([25, 255, 255])

# get feed from webcam, 0 means default webcam
video = VideoCapture(0)

# for continuosly getting images frames from video
while True:

    # if success state and image frames
    success, img = video.read()

    # converting our frame to hsv from rgb
    image = cvtColor(img, COLOR_BGR2HSV)

    # creating a mask layer for capturing colors only in our range
    mask = inRange(image, lower, upper)
                                         

    # creating window for shoing our outputs images continuosly as a video
    imshow("mask", mask)
    imshow("webcam", img)

    # waits 1 millisecond before destroying a frame or until the specified key is pressed
    if waitKey(1) == ord('q'):
        break

    