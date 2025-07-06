from ultralytics import YOLO
import cv2

# YOLOv5 모델 로드
model = YOLO('yolo11n-pose.pt')  # 처음 실행 시 자동 다운로드됨

# confidence threshold 및 사람 클래스만 감지 설정
model.conf = 0.4  # 이건 내부에 적용 안 되므로, 아래 predict 함수에서 직접 설정
classes_to_detect = [0]  # COCO 기준으로 0번은 사람

# 영상 열기
video_path = r"./Source_Data/Video/N/N/00047_H_A_N_C2/00047_H_A_N_C2.mp4"
cap = cv2.VideoCapture(video_path)

# 저장용 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_with_people.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

if not out.isOpened():
    print("Error: VideoWriter not opened!")
    exit()

frame_skip = 5  # 20프레임마다 추론 진행
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 일정 간격마다 추론 진행
    if frame_count % frame_skip == 0:
        # 프레임 감지 수행 (사람 클래스만, confidence threshold 직접 지정)
        results = model.predict(frame, conf=0.4, classes=classes_to_detect, verbose=False)
        print(results)
        # 감지된 결과 프레임 렌더링
        annotated_frame = results[0].plot()  # 첫 번째 결과에 대한 시각화 프레임

        # 결과 저장
        out.write(annotated_frame)

    frame_count += 1
    print(f"Processing frame {frame_count}...")

cap.release()
out.release()
cv2.destroyAllWindows()
