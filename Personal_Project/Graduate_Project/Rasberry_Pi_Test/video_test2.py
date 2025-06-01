import torch
import cv2
import mediapipe as mp
import time
import pandas as pd
import numpy as np
from collections import deque
import winsound
import threading

fall_detect_model = torch.jit.load("../Final_model/model_script.pt")

MAX_FRAMES_LEN = 300

lock = threading.Lock()

# MediaPipe Pose 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    smooth_landmarks=False
)
mp_drawing = mp.solutions.drawing_utils

# 중요 관절 인덱스
important_landmarks = [
    0, 11, 12, 13, 14, 15, 16,
    23, 24, 25, 26, 29, 30
]

window = deque(maxlen = ((MAX_FRAMES_LEN // 3) * len(important_landmarks)))

df_data = np.empty((MAX_FRAMES_LEN * len(important_landmarks), 5), dtype = np.float32)
df_data[:] = np.nan

row_index = 0
for frame in range(1, MAX_FRAMES_LEN + 1):
    for landmark in important_landmarks:
        df_data[row_index, 0] = frame
        df_data[row_index, 1] = landmark
        row_index += 1

test_df = pd.DataFrame(df_data, columns = ["frame", "landmark_id", "x", "y", "z"])

def pose_tracking():
    # 웹캠에서 영상 받기
    cap = cv2.VideoCapture(0)  # 기본 카메라 사용
    if not cap.isOpened():
        print("카메라 열기 실패")
        exit()

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽지 못했습니다.")
            break
        
        current_time = time.time()  
        elapsed = current_time - start_time

        if elapsed >= 0.1:
            start_time = current_time
            # MediaPipe에 넣기 위해 RGB로 변환
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                for idx in important_landmarks:
                    landmark = results.pose_landmarks.landmark[idx]
                    window.append((landmark.x, landmark.y, landmark.z))
                    
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        cv2.imshow('Real-Time Pose Landmarks', frame)

        # Q 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def fall_detecting():
    global output
    
    while True:
        time.sleep(5)

        with lock:
            if len(window) < 13 * 50:
                continue
    
        index_list = []
        j = 1

        for i in range(len(window)):
            index_list.append(j - 1)
            j += 1

            if j % 13 == 1:
                j += 26

        test_df.loc[index_list, ['x', 'y', 'z']] = window

        test_df2 = test_df.groupby("landmark_id").apply(lambda x : x.sort_values(by = ["frame", "landmark_id"]).interpolate().ffill().bfill()).reset_index(drop = True)
        test_df2 = test_df2.sort_values(by = ["frame", "landmark_id"]).reset_index(drop = True)


        # 피벗: (frame, source_index) 기준, landmark_id 별 x/y/z를 칼럼으로
        df_pivot = test_df2.pivot(index=["frame"], columns="landmark_id", values=["x", "y", "z"])

        # 다중 인덱스 컬럼을 단일 열로 변환: ex) ('x', 11.0) -> x_11
        df_pivot.columns = [f"{coord}_{int(lid)}" for coord, lid in df_pivot.columns]

        # 인덱스 복구
        df_pivot.reset_index(inplace=True)
                            
        # 다시 source_index 기준으로 묶고, 그 안에서 frame 오름차순 정렬 (보장용)
        df_pivot = df_pivot.sort_values(by=["frame"]).reset_index(drop=True)
        
        X_tensor = torch.tensor(df_pivot.values, dtype = torch.float32)
        X_tensor = X_tensor.unsqueeze(0)

        output = torch.sigmoid(fall_detect_model(X_tensor))
        output = (output > 0.5).int()
        
        if output == 1:
            winsound.Beep(440, 1000)
            break
        print(output)

pose_thread = threading.Thread(target = pose_tracking)
detect_thread = threading.Thread(target = fall_detecting)

pose_thread.start()
detect_thread.start()

pose_thread.join()
detect_thread.join()