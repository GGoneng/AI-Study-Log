from ultralytics import YOLO
import cv2
import time

# 사전학습된 YOLOv8 pose 모델 로드
model = YOLO("yolov8n-pose.pt")

# 이미지 또는 프레임 불러오기
frame = cv2.imread(r"./Dataset/images/00003_H_A_FY_C5_I006.jpg")
frame = cv2.resize(frame, dsize=(620, 420))
# 포즈 추론
t1 = time.time()
results = model.predict(source=frame, imgsz=320, classes = [0], conf=0.3)
t2 = time.time()
print(results[0].keypoints)
print(f"{t2 - t1:.4f}")
# 키포인트 시각화
annotated = results[0].plot()
cv2.imshow("Pose Detection", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
