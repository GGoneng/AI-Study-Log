import json
import os
import shutil


def make_yolo_dataset(SAVE_PATH):
    PATH = r"F:/Fall_Detection_Data/Labeling_Data/Image/"
    json_path = []

    for dirpath, dirnames, filenames in os.walk(PATH):
        for filename in filenames:
            if filename.endswith('.json'):
                full_path = os.path.join(dirpath, filename)
                json_path.append(full_path)

    for json_file in json_path:
        with open(json_file, encoding = "utf-8") as f:
            data = json.load(f)
            
            x1, y1, x2, y2 = map(float, data["bboxdata"]["bbox_location"].split(','))
            w, h = map(int, data["metadata"]["scene_res"].split('x'))
            title = data["metadata"]["file_name"].split('.')[0]
            
            x_center = (x1 + x2) / 2 / w
            y_center = (y1 + y2) / 2 / h
            width = (x2 - x1) / w
            height = (y2 - y1) / h
            class_id = 0

            line = f"{class_id} {x_center} {y_center} {width} {height}"

            with open(SAVE_PATH + f"{title}.txt", "w") as f:
                f.write(line)
            f.close()


def move_image_data(SAVE_PATH):
    PATH = "F:/Fall_Detection_Data/Source_Data/Image/"

    for dirpath, _, filenames in os.walk(PATH):
        for filename in filenames:
            if filename.endswith((".jpg", ".JPG")):
                src_path = os.path.join(dirpath, filename)
                dst_path = os.path.join(SAVE_PATH, filename)
                shutil.move(src_path, dst_path)



if __name__ == "__main__":
    txt_save_path = r"./YOLO_Dataset/labels/train/"
    image_save_path = r"./YOLO_Dataset/images/train/"

    make_yolo_dataset(txt_save_path)
    move_image_data(image_save_path)
    
