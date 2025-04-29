import os
import random
import shutil

def split_val_data(IMAGE_PATH, VAL_IMAGE_PATH, LABEL_PATH, VAL_LABEL_PATH):
    file_num = len(os.listdir(IMAGE_PATH))
    random_idx = []

    image_filenames = [f for f in os.listdir(IMAGE_PATH) if f.lower().endswith(".jpg")]
    txt_filenames = [l for l in os.listdir(LABEL_PATH)]

    random_idx = random.sample(range(file_num), 3000)

    selected_images = [image_filenames[i] for i in random_idx]
    selected_labels = [txt_filenames[i] for i in random_idx]

    for filename in selected_images:
        # 이미지 이동
        img_src = os.path.join(IMAGE_PATH, filename)
        img_dst = os.path.join(VAL_IMAGE_PATH, filename)
        shutil.move(img_src, img_dst)


    for filename in selected_labels:
        label_src = os.path.join(LABEL_PATH, filename)
        label_dst = os.path.join(VAL_LABEL_PATH, filename)
        shutil.move(label_src, label_dst)

if __name__ == "__main__":
    label_save_path = r"C:/Users/PNC/Desktop/Coding/Python/Personal_Project/Graduate_Project/YOLO_Dataset/labels/train/"
    image_save_path = r"C:/Users/PNC/Desktop/Coding/Python/Personal_Project/Graduate_Project/YOLO_Dataset/images/train/"
    label_val_path = r"C:/Users/PNC/Desktop/Coding/Python/Personal_Project/Graduate_Project/YOLO_Dataset/labels/val/"
    image_val_path = r"C:/Users/PNC/Desktop/Coding/Python/Personal_Project/Graduate_Project/YOLO_Dataset/images/val/"

    split_val_data(image_save_path, image_val_path, label_save_path, label_val_path)