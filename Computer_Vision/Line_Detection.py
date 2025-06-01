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
    frame_copy = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        frame = cv2.resize(frame, (640, 480))
        frame_copy.append(frame.copy())
        ycbcr = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)

        y_frames.append(ycbcr[:, :, 0])
    
    cap.release()
    return y_frames, frame_copy

def show_video(video):
    for frame in video:
        cv2.imshow("Line Detecting", frame)
        
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()

def detect_canny_line(y_frames):
    canny_frames = []

    for frame in y_frames:
        edges = cv2.Canny(frame, 50, 200, None, 3)
        canny_frames.append(edges)

    return canny_frames

def detect_hough_line(canny_frames, frame_copy):
    hough_lines = []

    for idx, frame in enumerate(canny_frames):
        lines = cv2.HoughLines(frame, 1, np.pi / 180, 120, None, 0, 0)

        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]

                if ((theta > np.pi / 3) and (theta <  2 * np.pi / 3)):
                    continue

                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(frame_copy[idx], pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

        hough_lines.append(frame_copy[idx])
    
    return hough_lines
        
if __name__ == "__main__":
    DATA_PATH = r"./Data/test_video.mp4"

    y_frames, frame_copy = capture_video(DATA_PATH)
    canny_frames = detect_canny_line(y_frames)
    hough_lines = detect_hough_line(canny_frames, frame_copy)
    show_video(hough_lines)