import json
import os
import math
import cv2 as cv
import matplotlib.pyplot as plt

DATA_PATH = r"F:\Data\Validation\Source_Data\VS\08_085504_221103\sensor_raw_data\camera\\"
JSON_PATH = r"F:\Data\Validation\Labeling_Data\VL\3D\08_085504_221103\sensor_raw_data\camera\\"

file_list = os.listdir(JSON_PATH)
class_type = []

big_vehicle = ["bus", "schoolBus", "ambulance", "truck"]            

for file in file_list:
    with open(JSON_PATH + file, 'r', encoding = "utf-8") as f:
        data = json.load(f)
        for annotations in data["annotations"]:
            if "bbox" in annotations:
                class_name = annotations["class"]
                yaw = annotations["yaw"]

                if yaw != None:
                    if (class_name in ["vehicle", "pedestrian", "twoWheeler"]):
                        type_name = annotations["attribute"]["type"]
                        if type_name in big_vehicle:
                            class_name = "big_vehicle"
                    
                        if (-math.pi / 4 <= yaw and yaw < math.pi / 4):
                            class_name = class_name + "_F"
                        
                        elif (math.pi / 4 <= yaw and yaw < math.pi * 3 / 4):
                            class_name = class_name + "_R"
                        
                        elif ((math.pi * 3 / 4 <= yaw and yaw < math.pi) or (-math.pi * 3 / 4 > yaw and -math.pi <= yaw)):
                            class_name = class_name + "_B"
                        
                        else:
                            class_name = class_name + "_L"

                        class_type.append(class_name)

print(class_type)

with open(JSON_PATH + "08_085504_221103_01.json", 'r', encoding = "utf-8") as f:
    data = json.load(f)

image_path = data["information"]["filename"]
IMAGE_FILE = DATA_PATH + "08_085504_221103_01.jpg"
image = cv.imread(IMAGE_FILE)  # 이미지 파일이 있어야 함
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)  # OpenCV는 BGR로 읽으므로 RGB 변환

# Bounding Box 그리기
for annotation in data["annotations"]:
    if "bbox" in annotation:
        x1, y1, x2, y2 = annotation["bbox"]
        class_name = annotation["class"]
        track_id = annotation["attribute"]["track_id"]
        yaw = annotation["yaw"]
 
        if yaw != None:
            
            # BBox 그리기
            cv.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
        
            # 라벨(객체 유형 및 ID) 추가
            label = f"{class_name} (ID: {track_id})"
            cv.putText(image, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
# 시각화
plt.figure(figsize=(10, 6))
plt.imshow(image)
plt.axis("off")
plt.title("Bounding Box Visualization")
plt.show()

# for annotations in data["annotations"]:
#     if "bbox" in annotations:
#         class_name = annotations["class"]
#         yaw = annotations["yaw"]

#         if yaw != None:
#             if (class_name in ["vehicle", "pedestrian", "twoWheeler"]):
#                 type_name = annotations["attribute"]["type"]
#                 if type_name in big_vehicle:
#                     class_name = "big_vehicle"
            
#                 if (-math.pi / 4 <= yaw and yaw < math.pi / 4):
#                     class_name = class_name + "_F"
                
#                 elif (math.pi / 4 <= yaw and yaw < math.pi * 3 / 4):
#                     class_name = class_name + "_L"
                
#                 elif ((math.pi * 3 / 4 <= yaw and yaw < math.pi) or (-math.pi * 3 / 4 > yaw and -math.pi <= yaw)):
#                     class_name = class_name + "_B"
                
#                 else:
#                     class_name = class_name + "_R"

#                 print(class_name)