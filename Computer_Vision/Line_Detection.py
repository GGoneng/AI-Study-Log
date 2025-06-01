"""
07.
Student ID : 21920141
Name       : 이민하
Subject    : Computer Vision
Function   : Line Detecting using Canny Edge Detection and Hough Line Detection
"""

# Import Modules
import cv2
import numpy as np
import math

def capture_video(video_path): # Video Capture Function
    cap = cv2.VideoCapture(video_path) # Capture the video
    
    # Make empty lists
    y_frames = []
    frame_copy = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        frame = cv2.resize(frame, (640, 480))
        frame_copy.append(frame.copy())
        # Change frame RGB channel to YCrCb channel
        ycbcr = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)

        # Extract Y channel
        y_frames.append(ycbcr[:, :, 0])
    
    cap.release()
    return y_frames, frame_copy

def show_video(video): # Video Show function
    for frame in video:
        # Open video window
        cv2.imshow("Line Detecting", frame)
        
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()

def detect_canny_line(y_frames): # Canny line detect function
    # Make a empty canny frames' list 
    canny_frames = []

    for frame in y_frames:
        # Detect the Canny line
        edges = cv2.Canny(frame, 200, 250, None, 3)
        canny_frames.append(edges)

    return canny_frames

def detect_hough_line(canny_frames, frame_copy): # Hough line detect function
    # Make a empty hough frames' list
    hough_lines = []

    for idx, frame in enumerate(canny_frames):
        # Detect the Hough line
        lines = cv2.HoughLines(frame, 1, np.pi / 180, 80, None, 0, 0)

        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                # Restrict degree to detect lanes
                if not ((np.pi / 6 < theta < 1.3 * np.pi / 6) or (4.7 * np.pi / 6 < theta < 5 * np.pi / 6)):
                    continue

                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                # Draw the Hough line
                cv2.line(frame_copy[idx], pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

        hough_lines.append(frame_copy[idx])
    
    return hough_lines
        
if __name__ == "__main__": # Main Function  
    # Set a Data Path
    DATA_PATH = r"./Data/test_video.mp4"

    y_frames, frame_copy = capture_video(DATA_PATH)
    canny_frames = detect_canny_line(y_frames)
    hough_lines = detect_hough_line(canny_frames, frame_copy)
    show_video(hough_lines)