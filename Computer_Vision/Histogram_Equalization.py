"""
05.
Student ID : 21920141
Name       : 이민하
Subject    : Computer Vision
Function   : Histogram Eqaulize to Y Channel and Recovery YCbCr Image to RGB Image
"""

# Import Modules
import numpy as np
import cv2 as cv
import time
import math

# Create a function that sets the Image
def set_path(file_name):
    # Set a File Path
    FILE_PATH = "./Data/"
    imgfile = FILE_PATH + file_name

    # Read a Image File
    img = cv.imread(imgfile, cv.IMREAD_COLOR)

    return img


# Create a function that shows the image
def show_image(img_file):
    # Resize the Image Window
    img = cv.resize(img_file, dsize = (500, 300))

    # Show the Image Window
    cv.imshow("img_file", img_file)

    # To maintain the window opened
    cv.waitKey(0)


# Create a function that transform RGB to YCbCr (SDTV Version)
def transform_rgb_to_ycbcr_sdtv(rgb_img_file):
    # Make a empty numpy array
    ycbcr = np.zeros(rgb_img_file.shape, dtype = np.uint8)

    # Transform the Image RGB to YCbCr
    for i, y in enumerate(rgb_img_file):
        for j, x in enumerate(y):
            red, green, blue = x

            # (SDTV Version Formula)
            y601 = 0.299 * red + 0.587 * green + 0.114 * blue 
            cb = -0.172 * red + -0.339 * green + 0.511 * blue + 128
            cr = 0.511 * red + -0.428 * green + -0.083 * blue + 128

            # Input YCbCr to empty array
            ycbcr[i][j] = [y601, cb, cr]

    return ycbcr

# Create a function that transform YCbCr to RGB (SDTV Version)
def transform_ycbcr_to_rgb_sdtv(ycbcr_img_file):
    # Make a empty numpy array
    rgb = np.zeros(ycbcr_img_file.shape, dtype = np.uint8)

    # Transform the Image YCbCr to RGB
    for i, y in enumerate(ycbcr_img_file):
        for j, x in enumerate(y):
            y601, cb, cr = x

            # (SDTV Version Formula)
            red = y601 + 1.371 * (cr - 128)
            green = y601 - 0.698 * (cr - 128) - 0.336 * (cb - 128)
            blue = y601 + 1.732 * (cb - 128)

            # Input RGB to empty array
            rgb[i][j] = [red, green, blue]

    return rgb

# Create a function that transform RGB to YCbCr (HDTV Version)
def transform_rgb_to_ycbcr_hdtv(rgb_img_file):
    # Make a empty numpy array
    ycbcr = np.zeros(rgb_img_file.shape, dtype = np.uint8)

    # Transform the Image RGB to YCbCr
    for i, y in enumerate(rgb_img_file):
        for j, x in enumerate(y):
            red, green, blue = x

            # (HDTV Version Formula)
            y709 = 0.213 * red + 0.715 * green + 0.072 * blue 
            cb = -0.117 * red + -0.394 * green + 0.511 * blue + 128
            cr = 0.511 * red + -0.464 * green + -0.047 * blue + 128

            # Input YCbCr to empty array
            ycbcr[i][j] = [y709, cb, cr]

    return ycbcr


# Create a function that transform YCbCr to RGB (HDTV Version)
def transform_ycbcr_to_rgb_hdtv(ycbcr_img_file):
    # Make a empty numpy array
    rgb = np.zeros(ycbcr_img_file.shape, dtype = np.uint8)

    # Transform the Image YCbCr to RGB
    for i, y in enumerate(ycbcr_img_file):
        for j, x in enumerate(y):
            y709, cb, cr = x

            # (HDTV Version Formula)
            red = y709 + 1.54 * (cr - 128)
            green = y709 - 0.459 * (cr - 128) - 0.183 * (cb - 128)
            blue = y709 + 1.816 * (cb - 128)

            # Input RGB to empty array
            rgb[i][j] = [red, green, blue]

    return rgb


# Create a function that transform RGB to YCbCr (OpenCV Version)
def transform_rgb_to_ycbcr_cv(rgb_img_file):
    ycbcr = cv.cvtColor(rgb_img_file, cv.COLOR_RGB2YCrCb)

    return ycbcr

# Create a function that transform YCbCr to RGB (OpenCV Version)
def transform_ycbcr_to_rgb_cv(ycbcr_img_file):
    rgb = cv.cvtColor(ycbcr_img_file, cv.COLOR_YCrCb2RGB)

    return rgb

# Create a function that extract Y Channel (= Gray Scale)
def extract_y_channel(ycbcr_img):
    # Make a empty numpy array
    y_channel = np.zeros(ycbcr_img.shape[:-1], dtype = np.uint8)

    # Extract Y Channel and Input Y to empty array
    for i, y in enumerate(ycbcr_img):
        for j, x in enumerate(y):   
            y601, cb, cr = x
            y_channel[i][j] = y601

    return y_channel

# Create a function that extract Mean Squared Error
def getMSE(rgb_img_file1, rgb_img_file2):
    # Make a MSE variable
    redMSE = 0
    greenMSE = 0
    blueMSE = 0

    # Get MSE by each pixel
    for i, y in enumerate(rgb_img_file1):
        for j, x in enumerate(y):
            red_1, green_1, blue_1 = x

            red_2 = rgb_img_file2[i][j][0]
            green_2 = rgb_img_file2[i][j][1]
            blue_2 = rgb_img_file2[i][j][2]

            redMSE += (np.float64(red_1) - np.float64(red_2)) ** 2
            greenMSE += (np.float64(green_1) - np.float64(green_2)) ** 2
            blueMSE += (np.float64(blue_1) - np.float64(blue_2)) ** 2
    
    N = rgb_img_file1.shape[0] * rgb_img_file1.shape[1]
    
    totalMSE = (redMSE + greenMSE + blueMSE) / (3 * N)

    return totalMSE

# Create a function that extract PSNR
def getPSNR(totalMSE):
    # Define a MAX (RGB = 255 * 3)
    MAX = 255

    # Get PSNR
    PSNR = 10 * math.log10(MAX ** 2 / totalMSE)

    return PSNR

# Create a function that count Pixel Num
def count_pixel_num(y_img):
    # Define a Max Value (0 ~ 255)
    MAX_VALUE = 255

    # Make a Empty Array to Save the Pixel Num
    pixel_num = np.zeros(MAX_VALUE + 1, dtype = np.uint8)

    # Count the Pixel Num into the Array
    for arr in y_img:
        for pixel in arr:
            pixel_num[pixel] += 1

    return pixel_num

# Create a function that histogram equalize (Method 1)
def histogram_equalize_1(y_img, pixel_num):
    # Define a Max Value (0 ~ 255)
    MAX_VALUE = 255

    # Make a Empty Array to Save Equalization List
    equalization_y = np.zeros(y_img.shape, dtype = np.uint8)
    equalization_list = np.zeros(MAX_VALUE + 1, dtype = np.uint8)

    # Get each Equalization Numbers (Method 1)
    for i in range(len(equalization_list)):
        pixel_sum = sum(pixel_num[:i + 1])
        equalization_list[i] = (MAX_VALUE + 1) / sum(pixel_num) * pixel_sum - 1

    # Change a Y Channel to the Equalization Numbers
    for i, arr in enumerate(y_img):
        for j, pixel in enumerate(arr):
            equalization_y[i][j] = equalization_list[pixel]

    return equalization_y

# Create a function that histogram equalize (Method 2)
def histogram_equalize_2(y_img, pixel_num):
    # Define a Max Value (0 ~ 255)
    MAX_VALUE = 255

    # Make a Empty Array to Save Equalization List
    equalization_y = np.zeros(y_img.shape, dtype = np.uint8)
    equalization_list = np.zeros(MAX_VALUE + 1, dtype = np.uint8)

    # Get each Equalization Numbers (Method 2)
    for i in range(len(equalization_list)):
        pixel_sum = sum(pixel_num[:i + 1])
        equalization_list[i] = round((MAX_VALUE + 1) / sum(pixel_num) * pixel_sum)

    # Change a Y Channel to the Equalization Numbers
    for i, arr in enumerate(y_img):
        for j, pixel in enumerate(arr):
            equalization_y[i][j] = equalization_list[pixel]

    return equalization_y

# Create a function that histogram equalize (OpenCV)
def histogram_equalize_cv(y_img):
    # Get a Equalization Y Channel
    equalization_list = cv.equalizeHist(y_img)

    return equalization_list

# Create a function that Change the Old YCbCr Image to Histogram Equalized YCbCr image
def change_y_channel(y_img, ycbcr_img):
    # Copy the Old YCbCr Image
    img = ycbcr_img 

    # Change the Old Y Channel to New Y Channel
    for i, y in enumerate(img):
        for j, x in enumerate(y):   
            x[0] = y_img[i][j]
    
    return img

# Main Funciton
if __name__ == "__main__":

    # Set a File Path
    rgb_img = set_path("test.jpg")   

    # Transform the Image file (OpenCV Version)
    cv_ycbcr_img = transform_rgb_to_ycbcr_cv(rgb_img)
    cv_y_img = extract_y_channel(cv_ycbcr_img)
    cv_rgb_img = transform_ycbcr_to_rgb_cv(cv_ycbcr_img)

    # Histogram Equalize the Image (Method 1)
    t1 = time.time()
    equalized_y_img1 = histogram_equalize_1(cv_y_img, count_pixel_num(cv_y_img))
    t2 = time.time()

    manual_time1 = t2 - t1

    # Histogram Equalize the Image (Method 2)
    t1 = time.time()
    equalized_y_img2 = histogram_equalize_2(cv_y_img, count_pixel_num(cv_y_img))
    t2 = time.time()

    manual_time2 = t2 - t1

    # Histogram Equalize the Image (OpenCV)
    t1 = time.time()
    equalized_y_img_cv = histogram_equalize_cv(cv_y_img)
    t2 = time.time()

    opencv_time = t2 - t1

    # Recovery the YCbCr Image to the RGB Image
    rgb_img1 = transform_ycbcr_to_rgb_cv(change_y_channel(equalized_y_img1, cv_ycbcr_img))
    rgb_img2 = transform_ycbcr_to_rgb_cv(change_y_channel(equalized_y_img2, cv_ycbcr_img)) 
    rgb_img3 = transform_ycbcr_to_rgb_cv(change_y_channel(equalized_y_img_cv, cv_ycbcr_img))

    # Get the PSNR about Equalized and Non Equalized
    psnr1 = cv.PSNR(rgb_img, rgb_img1)
    psnr2 = cv.PSNR(rgb_img, rgb_img2)
    psnr3 = cv.PSNR(rgb_img, rgb_img3)
    vanilla_psnr = cv.PSNR(rgb_img, cv_rgb_img)

    print(f"PSNR implement : {vanilla_psnr:.4f}")
    print(f"PSNR equalized implement (Method 1) : {psnr1:.4f}")
    print(f"PSNR equalized implement (Method 2) : {psnr2:.4f}")
    print(f"PSNR equalized implement (OpenCV) : {psnr3:.4f}")

    print(f"\n\nopencv_time = {opencv_time:.4f}")
    print(f"manual_time1 = {manual_time1:.4f}")
    print(f"manual_time2 = {manual_time2:.4f}")

    show_image(cv_rgb_img)
    show_image(rgb_img1)
    show_image(rgb_img2)
    show_image(rgb_img3)