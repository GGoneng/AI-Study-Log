import torch
import cv2

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Windows/System32/yolov5/runs/train/fall_yolov5n/weights/best.pt')
model.conf = 0.4

# 영상 열기
cap = cv2.VideoCapture(r"F:/Fall_Detection_Data/Source_Data/Video/Y/BY/00074_H_A_BY_C2/00074_H_A_BY_C2.mp4")
out = cv2.VideoWriter('output_YOLOv5s_01.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 60.0,
                      (int(cap.get(3)), int(cap.get(4))))

frame_skip = 3  # N프레임마다 한 번 추론
frame_count = 0
annotated_frame = None  # 초기화

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_skip == 0:
        results = model(frame)
        annotated_frame = results.render()[0]
    # 추론 안 했으면 이전 결과 프레임 사용
    out.write(annotated_frame)
    cv2.imshow("YOLOv5 Result", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
out.release()
cv2.destroyAllWindows()
