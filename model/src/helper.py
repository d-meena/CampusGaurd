import cv2
import numpy as np
import os
from skimage.segmentation import clear_border
import pytesseract
import imutils
import argparse
from PIL import ImageEnhance
from PIL import Image
from collections import Counter

def find_licensePlate(plate_roi):
    # Convert to grayscale
    gray_image = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray_image, (0, 0), sigmaX=3)

    # Increase sharpness
    sharp = cv2.addWeighted(gray_image, 1.5, blurred, -0.5, 0)

    # Convert to PIL Image
    plate_roi_pil = Image.fromarray(cv2.cvtColor(plate_roi, cv2.COLOR_BGR2RGB))

    # Enhance sharpness
    pl = ImageEnhance.Sharpness(plate_roi_pil)
    enhan_pl = pl.enhance(2.5)

    # Enhance contrast
    con_pl = ImageEnhance.Contrast(enhan_pl)
    con_pl = con_pl.enhance(0.5)

    # Convert back to OpenCV format
    plate_roi = cv2.cvtColor(np.array(con_pl), cv2.COLOR_RGB2BGR)

    return plate_roi

def read_image(plate_roi, psm=7):
    lptext = None
    alphnum = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    options = "-c tessedit_char_whitelist={}".format(alphnum)
    options += " --psm {}".format(psm)
    lptext = pytesseract.image_to_string(plate_roi, config=options)
    return lptext

def modify_no(vehicle_no):
    vehicle_no = ''.join(c for c in vehicle_no if c.isalnum())
    vehicle_no = vehicle_no.upper()

    length = len(vehicle_no)
    if length < 9 or length > 10:
        return "NULL"
    else:
        if vehicle_no[0].isdigit():
            vehicle_no = convert_to_alpha(vehicle_no, 0)
        if vehicle_no[1].isdigit():
            vehicle_no = convert_to_alpha(vehicle_no, 1)
        if vehicle_no[2].isalpha():
            vehicle_no = convert_to_digit(vehicle_no, 2)
        if vehicle_no[3].isalpha():
            vehicle_no = convert_to_digit(vehicle_no, 3)
        if vehicle_no[4].isdigit():
            vehicle_no = convert_to_alpha(vehicle_no, 4)
        i = 5
        if length == 10:
            i = i+1
            if vehicle_no[5].isdigit():
                vehicle_no = convert_to_alpha(vehicle_no, 5)
        if vehicle_no[i].isalpha():
            vehicle_no = convert_to_digit(vehicle_no, i)
        if vehicle_no[i+1].isalpha():
            vehicle_no = convert_to_digit(vehicle_no, i+1)
        if vehicle_no[i+2].isalpha():
            vehicle_no = convert_to_digit(vehicle_no, i+2)
        if vehicle_no[i+3].isalpha():
            vehicle_no = convert_to_digit(vehicle_no, i+3)
    return vehicle_no




def convert_to_alpha(vehicle_no, i):
    if (vehicle_no[i] == '4'):
        return vehicle_no[:i]+'A'+vehicle_no[i+1:]
        # vehicle_no[i] = '4'
    elif (vehicle_no[i] == '6'):
        return vehicle_no[:i]+'G'+vehicle_no[i+1:]
    elif (vehicle_no[i] == '8'):
        return vehicle_no[:i]+'B'+vehicle_no[i+1:]
        # vehicle_no[i] = '8'
    elif (vehicle_no[i] == '0'):
        return vehicle_no[:i]+'O'+vehicle_no[i+1:]
    else:
        return vehicle_no

def convert_to_digit(vehicle_no, i):
    set_z = {'C', 'D', 'G', 'O', 'Q', 'U'}
    if (vehicle_no[i] == 'A'):
        return vehicle_no[:i]+'4'+vehicle_no[i+1:]
        # vehicle_no[i] = '4'
    elif (vehicle_no[i] == 'B'):
        return vehicle_no[:i]+'8'+vehicle_no[i+1:]
        # vehicle_no[i] = '8'
    elif vehicle_no[i] in {'O','Q','G', 'D  '}:
        return vehicle_no[:i]+'0'+vehicle_no[i+1:]
        # vehicle_no[i] = '0'
    elif vehicle_no[i] == 'I' or vehicle_no[i] == 'J':
        return vehicle_no[:i]+'1'+vehicle_no[i+1:]
        # vehicle_no[i] = '1'
    else:
        return vehicle_no


valid_state_code = {'AN', 'AP', 'AR', 'AS', 'BR', 'CG', 'CH', 'DD', 'DL', 'DN', 'GA', 'GJ', 'HP', 'HR', 'JH', 'JK', 'KA', 'KL',
                    'LA', 'LD', 'MH', 'ML', 'MN', 'MP', 'MZ', 'NL', 'OD', 'OR', 'OT', 'PB', 'PY', 'RJ', 'SK', 'TN', 'TR', 'TS', 'UA', 'UK', 'UP', 'WB'}


def valid_number_plate(num):
    if 9 > len(num) or len(num) > 10:
        return False
    else:
        state_code = num[:2]
        if state_code in valid_state_code:
            if num[0] == 'D' and num[1] == 'L':
                return True
            elif num[0].isalpha() and num[1].isalpha() and num[2].isdigit() and num[3].isdigit() and num[4].isalpha():
                return True
            else:
                return False

def resizeFrame(frame, fixed_height):
    # Calculate the aspect ratio
    aspect_ratio = frame.shape[1] / frame.shape[0]
    
    # Calculate the corresponding width to maintain the aspect ratio
    fixed_width = int(fixed_height * aspect_ratio)
    
    # Resize the frame
    resized_frame = cv2.resize(frame, (fixed_width, fixed_height))
    
    return resized_frame

def calculate_frequency(vector):
    sorted_vector = sorted(vector, key=lambda x: x[0], reverse=True)
    numbers = [pair[1] for pair in sorted_vector]

    freq10 = 0
    filtered_vector = []
    for plate in numbers:
        if len(plate) == 10:
            freq10 = freq10 + 1
    if freq10 >= 0.5*len(numbers):
        filtered_vector = [plate for plate in numbers if len(plate) != 9]
    else:
        filtered_vector = [plate for plate in numbers if len(plate) != 10]    
    
    return filtered_vector

def  select_number(plates):
    mp = [{} for _ in range(10)]
    n = len(plates)
    res = ""
    for i in range(len(plates[0])):
        mx = 0
        ch = '*'
        for j in range(n):
            mp[i][plates[j][i]] = mp[i].get(plates[j][i], 0) + 1
            if mx < mp[i][plates[j][i]]:
                mx = mp[i][plates[j][i]]
                ch = plates[j][i]
        res += ch
    return res

def make_excel(wb):
    temp_file = 'temp.xls'
    wb.save(temp_file)

    existing_file = 'xlwt example.xls'
    if os.path.exists(existing_file):
        os.remove(existing_file)

    os.rename(temp_file, existing_file)

        