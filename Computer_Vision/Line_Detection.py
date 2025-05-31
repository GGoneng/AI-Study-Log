"""
07.
Student ID : 21920141
Name       : 이민하
Subject    : Computer Vision
Function   : Line Detecting using Canny Edge Detection and Hough Line Detection
"""

import cv2
import numpy as np
import math

def capture_video(video_path):
    cap = cv2.VideoCapture(video_path)
    y_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error!")
            break
        if frame is None:
            print("Error!")
            break

        frame = cv2.resize(frame, (640, 480))
        ycbcr = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)

        y_frames.append(ycbcr[:, :, 0])
    
    cap.release()
    return y_frames

def show_video(video):
    for frame in video:
        cv2.imshow("Line Detecting", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()

def detect_canny_line(y_frames):
    canny_frames = []

    for frame in y_frames:
        edges = cv2.Canny(frame, 50, 200, None, 3)
        canny_frames.append(edges)

    return canny_frames

def detect_hough_line(canny_frames, y_frames):
    hough_lines = []

    for idx, frame in enumerate(canny_frames):
        lines = cv2.HoughLines(frame, 1, np.pi / 180, 150, None, 0, 0)
    
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                hough_lines.append(cv2.line(y_frames[idx], pt1, pt2, (0,0,255), 3, cv2.LINE_AA))
    
    return hough_lines
        
        # linesP = cv2.HoughLinesP(frame, 1, np.pi / 180, 50, None, 50, 10)
        
        # if linesP is not None:
        #     for i in range(0, len(linesP)):
        #         l = linesP[i][0]
        #         cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

if __name__ == "__main__":
    DATA_PATH = r"./Data/test_video.mp4"

    y_frames = capture_video(DATA_PATH)
    canny_frames = detect_canny_line(y_frames)
    hough_lines = detect_hough_line(canny_frames, y_frames)
    show_video(hough_lines)