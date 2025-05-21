import os
import cv2
import mediapipe as mp
import csv

def extract_path(PATH):
    path_list = []

    for dirpath, _, filenames in os.walk(PATH):
        for filename in filenames:
            if filename.endswith((".mp4", ".MP4")):
                path_list.append(os.path.join(dirpath, filename))

    return path_list

def extract_csv(path_list):


    # MediaPipe Pose 초기화
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
        smooth_landmarks=True
    )

    # 중요 관절 인덱스
    important_landmarks = [
        0, 11, 12, 13, 14, 15, 16,
        23, 24, 25, 26, 29, 30
    ]

    for i, path in enumerate(path_list):
        cap = cv2.VideoCapture(path)
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        skip_interval = max(1, round(original_fps / 10))


        with open(f'./10fps_Dataset/pose_landmark_{2272 + i:04d}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['frame', 'landmark_id', 'x', 'y', 'z'])

            frame_count = 0
            processed_frame = 1

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % skip_interval == 0:
                    
                    frame = cv2.resize(frame, (1920, 1280))
                    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = pose.process(image_rgb)

                    if results.pose_landmarks:
                        for idx in important_landmarks:
                            landmark = results.pose_landmarks.landmark[idx]
                            writer.writerow([processed_frame, idx, landmark.x, landmark.y, landmark.z])

                        # for idx in important_landmarks:
                        #     landmark = results.pose_landmarks.landmark[idx]
                        #     x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                        #     cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                    
                    processed_frame += 3

                    # cv2.imshow('Pose with Important Landmarks', frame)
                    # if cv2.waitKey(1) & 0xFF == ord('q'):
                    #     break

                frame_count += 1

        cap.release()
        cv2.destroyAllWindows()
        print("CSV 파일과 비디오 파일로 저장 완료.")


if __name__ == "__main__":
    PATH = r"D:/041.낙상사고 위험동작 영상-센서 쌍 데이터/3.개방데이터/1.데이터/Training/01.원천데이터/TS/영상/N/N/"
    # PATH = r"./Test_Dataset/"
    # PATH = r"F:/Fall_Detection_Data/Source_Data/Video/"
    path_list = extract_path(PATH)

    print(path_list)
    extract_csv(path_list)