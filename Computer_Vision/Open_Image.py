"""
01.
Student ID : 21920141
Name       : 이민하
Subject    : Computer Vision
Function   : Show jpg file through openCV
"""

# Import Modules
import numpy as np
import cv2 as cv

# Set a File Path
FILE_PATH = "./Data/"
imgfile = FILE_PATH + "window.jpg"

# Read a Image File
img = cv.imread(imgfile, cv.IMREAD_COLOR)

# Resize the Image Window
img = cv.resize(img, dsize = (500, 300))

# Show the Image Window
cv.imshow("img", img)

# To maintain the window opened
cv.waitKey(0)

