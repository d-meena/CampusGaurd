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


def filterPlate(plate_roi):
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
    plate_roi = cv2.cvtColor(np.asarray(con_pl), cv2.COLOR_RGB2BGR)

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
    vehicle_no = modify(vehicle_no)
    return vehicle_no

vehicle_class={'A' ,'B' ,'C' ,'D' ,'E' 'F' ,'G' ,'K' ,'R' ,'X'}
valid_state_code = {'AN', 'AP', 'AR', 'AS', 'BR', 'CG', 'CH', 'DD', 'DL', 'DN', 'GA', 'GJ', 'HP', 'HR', 'JH', 'JK', 'KA', 'KL',
                    'LA', 'LD', 'MH', 'ML', 'MN', 'MP', 'MZ', 'NL', 'OD', 'OR', 'OT', 'PB', 'PY', 'RJ', 'SK', 'TN', 'TR', 'TS', 'UA', 'UK', 'UP', 'WB'}

def convert_to_alpha(vehicle_no, i):
    if (vehicle_no[i] == '1'):
        return vehicle_no[:i]+'I'+vehicle_no[i+1:]
    if (vehicle_no[i] == '4'):
        return vehicle_no[:i]+'A'+vehicle_no[i+1:]
    elif (vehicle_no[i] == '5'):
        return vehicle_no[:i]+'S'+vehicle_no[i+1:]
    elif (vehicle_no[i] == '6'):
        return vehicle_no[:i]+'G'+vehicle_no[i+1:]
    elif (vehicle_no[i] == '7'):
        return vehicle_no[:i]+'Z'+vehicle_no[i+1:]
    elif (vehicle_no[i] == '8'):
        return vehicle_no[:i]+'B'+vehicle_no[i+1:]
    elif (vehicle_no[i] == '0'):
        return vehicle_no[:i]+'Q'+vehicle_no[i+1:]
    else:
        return vehicle_no


def convert_to_digit(vehicle_no, i):
    set_z = {'C', 'D', 'G', 'O', 'Q', 'U'}
    if (vehicle_no[i] == 'A'):
        return vehicle_no[:i]+'4'+vehicle_no[i+1:]
    elif (vehicle_no[i] == 'S'):
        return vehicle_no[:i]+'5'+vehicle_no[i+1:]
    elif (vehicle_no[i] == 'B'):
        return vehicle_no[:i]+'8'+vehicle_no[i+1:]
    elif vehicle_no[i] in {'O','Q','D'}:
        return vehicle_no[:i]+'0'+vehicle_no[i+1:]
    elif vehicle_no[i] == 'I' or vehicle_no[i] == 'J':
        return vehicle_no[:i]+'1'+vehicle_no[i+1:]
    elif (vehicle_no[i] == 'Z'):
        return vehicle_no[:i]+'2'+vehicle_no[i+1:]
    else:
        return vehicle_no


def valid_number_plate(num):
    state_code = num[:2]  
    country_number="0"
    ind_country_num=0
    for ch in num:
        if(ch.isdigit()):
            ind_country_num+=1
            country_number+=ch
        else:
            break
    i=ind_country_num
    #private and commercial vehicles number plate format 
    if 12>len(num)>7 and num[0].isalpha() and num[1].isalpha() and state_code in valid_state_code and num[2].isdigit() and num[3].isdigit():
        # print("private vehicles")
        if (len(num)==11) and (num[4].isalpha() and num[5].isalpha() and num[6].isalpha()):
            if num[7].isdigit() and num[8].isdigit() and num[9].isdigit() and num[10].isdigit():
                return True
            else:
                return False
        elif (len(num)==10) and (num[4].isalpha() and num[5].isalpha()):
            if num[7].isdigit() and num[8].isdigit() and num[9].isdigit() and num[6].isdigit():
                return True
            else:
                return False
        elif (len(num)==9) and num[4].isalpha():
            if num[7].isdigit() and num[8].isdigit() and num[5].isdigit() and num[6].isdigit():
                return True
            else:
                return False
        elif (len(num)==8) and num[4].isdigit():
            if num[7].isdigit() and num[5].isdigit() and num[6].isdigit():
                return True
            else:
                return False
        else:
            return False
    
    #VA series vehicles number plate format
    elif len(num)==10 and state_code in valid_state_code and num[2]=='V' and num[3]=='A':
        # print("VA series vehicle ")
        if (len(num)==10) and (num[4].isalpha() and num[5].isalpha()):
            if num[7].isdigit() and num[8].isdigit() and num[9].isdigit() and num[6].isdigit():
                return True
            else:
                return False  
    
    #bharat series vehicles number plate format  
    elif 8<len(num)<11 and num[0].isdigit() and num[1].isdigit() and num[2]=='B' and num[3]=='H':
        # print("bharat series ")
        if (len(num)==9) and (num[7].isdigit() and num[4].isdigit() and num[5].isdigit() and num[6].isdigit()) and num[8].isalpha():
                return True
            
        elif len(num)==10 and (num[7].isdigit() and num[4].isdigit() and num[5].isdigit() and num[6].isdigit()) and num[8].isalpha() and num[9].isalpha():
                return True
        else:
            return False


    #foreign missons series vehicles number plate format  
    elif (len(num)>4 and len(num)<10) and 0<int(country_number)<161 and ((num[i]=='C' and num[i+1]=='D') or (num[i]=='C' and num[i+1]=='C') or (num[i]=='U' and num[i+1]=='N')) :
        # print("foreign mission series ")
        if (len(num)>4 and len(num)<10):
            i+=2
            if num[i]=='1' and num[i+1].isalpha() and len(num)==i+2:
                return True
            else:
                cnt = 0
                flag=0
                uniq_num=''
                for i in range(i, len(num)):
                    if num[i].isdigit():
                        cnt += 1
                        uniq_num+=num[i]
                    else:
                        flag=1
                        break
                if 1<int(uniq_num)<=9999 and not flag:
                    return True
                else:
                    return False
        

    #indian armed forces series vehicles number plate format  
    elif 10<len(num)<12 and num[0].isdigit() and num[1].isdigit() and num[2].isalpha() and num[2] in vehicle_class and num[3].isdigit():
        i=3
        uniq_num=''
        cnt=0
        # print("indian armed forces ")
        for i in range(i, len(num)):
            if num[i].isdigit():
                cnt += 1
                uniq_num+=num[i]
            else:
                flag=1
                break
        if(cnt==6) and i==len(num)-1 and num[i].isalpha():
            return True
        else:
            return False
  
    #temporary number plate vehicles number plate format  
    elif 11<len(num)<14 and num[0]=='T' and (num[1].isdigit() and num[2].isdigit() and num[3].isdigit() and num[4].isdigit()) and num[5].isalpha() and num[6].isalpha() and state_code in valid_state_code :
        if (len(num)==12) and (num[7].isdigit() and num[8].isdigit() and num[9].isdigit() and num[10].isdigit()) and num[11].isalpha():
                return True
            
        elif len(num)==13 and (num[7].isdigit() and num[8].isdigit() and num[9].isdigit() and num[10].isdigit()) and num[11].isalpha() and num[12].isalpha():
                return True
        else:
            return False
  

    else:
        # print("not any type of vehicle ")
        return False


def modify(number):
    country_number="0"
    ind_country_num=0
    for ch in number:
        if(ch.isdigit()):
            ind_country_num+=1
            country_number+=ch
        else:
            break
    i=ind_country_num

    #indian armed force
    if len(number) == 10 and number[0].isdigit() and number[1].isdigit() and number[9].isalpha() and number[8].isdigit():
        if number[2].isdigit():
            number = convert_to_alpha(number, 2)
        if number[3].isalpha():
            number = convert_to_digit(number, 3)
        if number[4].isalpha():
            number = convert_to_digit(number, 4)
        if number[5].isalpha():
            number = convert_to_digit(number, 5)
        if number[6].isalpha():
            number = convert_to_digit(number, 6)
        if number[7].isalpha():
            number = convert_to_digit(number, 7)
        return number
    #bh series
    elif len(number) == 10 and ((number[9].isalpha() and number[8].isalpha() and number[3] == 'H') 
                              or (number[7].isdigit() and number[4].isdigit() and number[5].isdigit() and number[6].isdigit())):
        if number[0].isalpha():
            number = convert_to_digit(number, 0)
        if number[1].isalpha():
            number = convert_to_digit(number, 1)
        if number[2].isdigit():
            number = convert_to_alpha(number, 2)
        if number[4].isalpha():
            number = convert_to_digit(number, 4)
        if number[5].isalpha():
            number = convert_to_digit(number, 5)
        if number[6].isalpha():
            number = convert_to_digit(number, 6)
        if number[7].isalpha():
            number = convert_to_digit(number, 7)
        if number[8].isdigit():
            number = convert_to_alpha(number, 8)
        if number[7].isdigit():
            number = convert_to_alpha(number, 7)
        return number
    #va series   
    elif len(number)==10 and number[2]=='V' and number[3]=='A':
        if number[0].isdigit():
            number = convert_to_alpha(number, 0)
        if number[1].isdigit():
            number = convert_to_alpha(number,1)
        if number[4].isdigit():
            number = convert_to_alpha(number,4)
        if number[5].isdigit():
            number = convert_to_alpha(number,5)
        return number
    # for temporaray number plate vehicles
    elif 11<len(number)<14 and number[0]=='T':
        if number[1].isalpha():
            number = convert_to_digit(number, 1)
        if number[2].isalpha():
            number = convert_to_digit(number, 2)
        if number[3].isalpha():
            number = convert_to_digit(number, 3)
        if number[4].isalpha():
            number = convert_to_digit(number, 4)
        
        if number[5].isdigit():
            number = convert_to_alpha(number, 5)
        if number[6].isdigit():
            number = convert_to_alpha(number, 6)

        if number[7].isalpha():
            number = convert_to_digit(number, 7)
        if number[8].isalpha():
            number = convert_to_digit(number, 8)
        if number[9].isalpha():
            number = convert_to_digit(number, 9)
        if number[10].isalpha():
            number = convert_to_digit(number, 10)

        if number[11].isdigit():
            number = convert_to_digit(number, 11)
        if len(number)==13 and number[12].isdigit():
            number = convert_to_digit(number, 12)
        return number

    elif len(number)==10 and number[0]!='D' and number[1]!='L':
        # print("private ")
        if number[0].isdigit():
            number = convert_to_alpha(number, 0)
        if number[1].isdigit():
            number = convert_to_alpha(number,1)
        if number[2].isalpha():
            number = convert_to_digit(number,2)
        if number[3].isalpha():
            number = convert_to_digit(number,3)
        if number[4].isdigit():
            number = convert_to_alpha(number,4)
        if number[5].isdigit():
            number = convert_to_alpha(number,5)
        if number[6].isalpha():
            number = convert_to_digit(number,6)
        if number[7].isalpha():
            number = convert_to_digit(number,7)
        if number[8].isalpha():
            number = convert_to_digit(number,8)
        if number[9].isalpha():
            number = convert_to_digit(number,9)
        return number
    elif len(number)==10 and number[0]=='D' and number[1]=='L':
        if number[0].isdigit():
            number = convert_to_alpha(number, 0)
        if number[1].isdigit():
            number = convert_to_alpha(number,1)
        if number[2].isalpha():
            number = convert_to_digit(number,2)
        if number[4].isdigit():
            number = convert_to_alpha(number,4)
        if number[5].isdigit():
            number = convert_to_alpha(number,5)
        if number[6].isalpha():
            number = convert_to_digit(number,6)
        if number[7].isalpha():
            number = convert_to_digit(number,7)
        if number[8].isalpha():
            number = convert_to_digit(number,8)
        if number[9].isalpha():
            number = convert_to_digit(number,9)
        return number
    
    elif len(number)==9 and number[0]!='D' and number[1]!='L':
        if number[0].isdigit():
            number = convert_to_alpha(number, 0)
        if number[1].isdigit():
            number = convert_to_alpha(number,1)
        if number[2].isalpha():
            number = convert_to_digit(number,2)
        if number[3].isalpha():
            number = convert_to_digit(number,3)
        if number[4].isdigit():
            number = convert_to_alpha(number,4)
        if number[6].isalpha():
            number = convert_to_digit(number,6)
        if number[7].isalpha():
            number = convert_to_digit(number,7)
        if number[8].isalpha():
            number = convert_to_digit(number,8)
        if number[5].isalpha():
            number = convert_to_digit(number,5)
        return number
    elif len(number)==9 and number[0]=='D' and number[1]=='L':
        if number[0].isdigit():
            number = convert_to_alpha(number, 0)
        if number[1].isdigit():
            number = convert_to_alpha(number,1)
        if number[2].isalpha():
            number = convert_to_digit(number,2)
        if number[4].isdigit():
            number = convert_to_alpha(number,4)
        if number[6].isalpha():
            number = convert_to_digit(number,6)
        if number[7].isalpha():
            number = convert_to_digit(number,7)
        if number[8].isalpha():
            number = convert_to_digit(number,8)
        if number[5].isalpha():
            number = convert_to_digit(number,5)
        return number
    else: 
        return number


def resizeFrame(frame, fixed_height):
    # Calculate the aspect ratio
    aspect_ratio = frame.shape[1] / frame.shape[0]
    
    # Calculate the corresponding width to maintain the aspect ratio
    fixed_width = int(fixed_height * aspect_ratio)
    
    # Resize the frame
    resized_frame = cv2.resize(frame, (fixed_width, fixed_height))
    
    return resized_frame


def calculate_frequency(vector):
    freq10 = 0
    filtered_vector = []
    for plate in vector:
        if len(plate) == 10:
            freq10 = freq10 + 1
    if freq10 >= 0.5*len(vector):
        filtered_vector = [plate for plate in vector if len(plate) != 9]
    else:
        filtered_vector = [plate for plate in vector if len(plate) != 10]    
    
    return filtered_vector


def  select_number(plates):
    mp = [{} for _ in range(10)]
    n = len(plates)
    res = ""
    for i in range(len(plates[0])):
        mx = 0
        ch = '*'
        st={''}
        for j in range(n):
            if i < len(plates[j]):
                st.add(plates[j][i])
                mp[i][plates[j][i]] = mp[i].get(plates[j][i], 0) + 1
                if mx <= mp[i][plates[j][i]]:
                    mx = mp[i][plates[j][i]]
                    ch = plates[j][i]
        ch=choose(mp[i],st,ch)
        if ch != '*':
            res += ch
    return res

# def getchar(mp):
#     ch = '*'
#     mx = 0
#     for key, value in mp.items():
#         if value > mx:
#             mx = value
#             ch = key
#     return ch

# def select_number(plates):
#     final_plate = ""
#     vec = []
#     for number in plates:
#         for j, digit in enumerate(number):
#             if j >= len(vec):
#                 vec.append({})
#             vec[j][digit] = vec[j].get(digit, 0) + 1
#     for mp in vec:
#         final_plate += getchar(mp)
#     return final_plate

def choose(mp,st,ch):
    if ('5' in st)and '3' in st:
        return '9'
    if ('Q' in st or 'O' in st) and 'D' in st:
        return 'D'
    
    if 'H' in st and 'M' in st:
        return 'M'
    if 'H' in st and ('N' in st):
        if mp['H']>mp['N']:
            return 'M'
        else:
            return 'N'
    if 'H' in st and 'A' in st:
        return 'H'
    if 'U' in st and 'J' in st:
        return 'U'
    return ch


def make_excel(wb, filename):
    destination_path = 'excel_files'
    
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    temp_file = os.path.join(destination_path, 'temp.xls')
    wb.save(temp_file)

    existing_file = os.path.join(destination_path, filename + '.xls')
    if os.path.exists(existing_file):
        os.remove(existing_file) 

    os.rename(temp_file, existing_file)


def save_frame_to_folder(folder_name, frame, frame_name):
    # Create the folder if it doesn't exist
    folder_path = os.path.join('saved_images', folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Save the frame to the target folder
    filename = os.path.join(folder_path, frame_name)
    cv2.imwrite(filename, frame)