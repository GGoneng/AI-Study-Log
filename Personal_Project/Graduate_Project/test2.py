import cv2
import mediapipe as mp

# MediaPipe Pose 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,    # 매 프레임마다 새로 검출
    model_complexity=0,         # 가장 간단한 모델 사용
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# 중요 관절의 인덱스 (MediaPipe Pose의 landmarks에서)
important_landmarks = [
    0,
    11, 12,
    13, 14,
    15, 16,
    23, 24,
    25, 26,
    27, 28,
    29, 30,
    31, 32
]

# 비디오 파일 열기
cap = cv2.VideoCapture(r"F:/Fall_Detection_Data/Source_Data/Video/Y/BY/00074_H_A_BY_C2/00074_H_A_BY_C2.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1024, 860))  # 입력 해상도 줄이기 (필수)

    # MediaPipe Pose로 관절 검출
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    # 관절이 검출되었을 때
    if results.pose_landmarks:
        # 중요 관절만 그리기
        for idx in important_landmarks:
            landmark = results.pose_landmarks.landmark[idx]
            # 각 관절의 (x, y) 좌표
            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            # 해당 위치에 원 그리기
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # 초록색 점으로 표시

    # 결과 이미지 출력
    cv2.imshow('Pose with Important Landmarks', frame)

    # 'q'를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
