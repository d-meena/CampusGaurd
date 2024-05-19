import cv2
import numpy as np
import time
import xlwt 
from xlwt import Workbook 
import os
from skimage.segmentation import clear_border
import argparse
from PIL import ImageEnhance
from PIL import Image
import easyocr
from findid import *
from helper import filterPlate, read_image, modify_no, resizeFrame, calculate_frequency, select_number, make_excel,save_frame_to_folder


def check_ids(ids_to_insert):
    global row, plates_map, first_detection, last_detection, sheet1

    for id in ids_to_insert:
        # print("ID:", id)
        if id in plates_map:
            # Check if the value associated with 'id' is empty or not
            if plates_map[id]:  

                direction = ""
                if first_detection[id] > last_detection[id]:
                    direction = "OUT"
                else:
                    direction = "IN"

                vector = plates_map[id] 
                vector = calculate_frequency(vector)

                
                if len(plates_map[id])!=0:
                    print(plates_map[id], "this is the map")

                final_plate=select_number(vector)
                print("Final number ", final_plate, "ENTRY = ", direction)

                max_length = max(len(plate) for plate in vector)
                sheet1.col(0).width = 1000*max_length
                sheet1.col(1).width = 2000
                # Join elements of sorted_plates with commas
                formatted_plates = ', '.join(vector)
                # Write formatted_plates to the cell
                sheet1.write(row, 0, formatted_plates)
                sheet1.write(row, 1, final_plate) 
                sheet1.write(row, 2, direction) 
                row += 1
            # else:
                # print("The value associated with id is not detected.")
            del plates_map[id]
            del first_detection[id]
            del last_detection[id]
        # else:
            # print("The id does not exist in plates_map.") 
        window_name = "Plate " + str(id)
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) != 0:
            cv2.destroyWindow(window_name)
       


if __name__ == "__main__":
    start_time = time.time()

    fixed_height = 600  # Set your desired height
    id_tracker = IdTracker()

    plat_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")
    # plat_detector = cv2.CascadeClassifier('./indian_license_plate.xml')

    # reader = easyocr.Reader(['en'])

    fileName = 'try7.mp4'
    video = cv2.VideoCapture('../Data/' + fileName)


    if (video.isOpened() == False):
        print('Error Reading Video')

    frameCount=0
    plates_map = {}
    first_detection = {}
    last_detection = {}
    saved_frames = {}
    wb = Workbook() 
    row = 0
    # add_sheet is used to create sheet. 
    sheet1 = wb.add_sheet('Sheet 1') 

    FrameHeight = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        isreading, frame = video.read()
        frameCount = frameCount+1
        if (frameCount % 2 != 0):
            continue
        if isreading == False:
            print('vedio completed or error in reading frame')
            break

        gray_video = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # plate_coordinates = plat_detector.detectMultiScale(
        #     gray_video, scaleFactor=1.2, minNeighbors=5, minSize=(25, 25))
        plate_coordinates = plat_detector.detectMultiScale(
            gray_video, scaleFactor=1.2, minNeighbors=4, minSize=(25, 25))

        frame_height, frame_width = frame.shape[:2]
        # plate_coordinates = plat_detector.detectMultiScale(
        #     gray_video, scaleFactor=1.2, minNeighbors=7)
        
        curr_centers = {}
        for (x, y, w, h) in plate_coordinates:

            # if y < frame_height/3:
            #     continue
            

            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            id = id_tracker.getId(cx, cy, 2*w)
            if id not in first_detection:
                first_detection[id] = y
                last_detection[id] = y
            else:
                last_detection[id] = y

            # ***TO CROP THE PLATE PROPERLY***
            # a,b = (int(0.02*img.shape[0]), int(0.025*img.shape[1])) #parameter tuning
            # plate_roi = plate_img[y+a:y+h-a, x+b:x+w-b, :]

            plate_roi = frame[y:y+h, x:x+w]   
            window_y = int(id % 4) * 100 
            cv2.imshow('Plate ' + str(id), plate_roi)        
            cv2.moveWindow("Plate " + str(id), 0, window_y)

            veh_x = x - 2*w
            veh_y = y - 7*h
            veh_w = int(5*w)
            veh_h = 12*h

            veh_x = max(0, min(veh_x, frame_width))
            veh_y = max(0, min(veh_y, frame_height))
            veh_w = min(veh_w, frame_width - veh_x)
            veh_h = min(veh_h, frame_height - veh_y)

            car_roi = frame[veh_y: veh_y+veh_h, veh_x: veh_x+veh_w]

            # cv2.imshow('car' + str(id), car_roi)
            # cv2.moveWindow('car' + str(id), 200, window_y*2)


            lisence_plate = filterPlate(plate_roi)

            # for using tesseract
            number = read_image(lisence_plate, psm=7)


            # for using easyocr
            # text_results = reader.readtext(lisence_plate)
            # number = ""
            # if text_results:
            #     number = text_results[0][1]

            curr_centers[id] = (cx, cy)
            veh_number = modify_no(number)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.rectangle(frame, (veh_x, veh_y), (veh_x+veh_w, veh_y+veh_h), (255, 0, 0), 3)
            
            if(len(veh_number)>3 and id not in saved_frames):
                save_frame_to_folder(fileName[:(len(fileName)-4)], car_roi, veh_number + ".jpg")
                saved_frames[id] = 1

            
            if(valid_number_plate(veh_number)):
                cv2.putText(frame, text=veh_number, org=(
                    x-3, y-3), fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 255), thickness=2, fontScale=2)
                # print("i am valid", veh_number)
                if saved_frames[id] == 1:
                    save_frame_to_folder(fileName[:(len(fileName)-4)], car_roi, veh_number + ".jpg")
                    saved_frames[id] = 2
                
                if id in plates_map:
                    # Key exists, append to the existing list
                    plates_map[id].append((veh_number))
                    # saved_frames[id]
                else:
                    # Key doesn't exist, create a new list with the value
                    plates_map[id] = [(veh_number)]


        resized_frame = resizeFrame(frame, fixed_height)
        # print("this is map = ", plates_map)
        
        # ***TO TAKE IDEA OF PIXELS IN VEDIO***
        # cv2.rectangle(resized_frame, (50, 400), (180, 1050), (255, 0, 0), 2)

        cv2.imshow('frame', resized_frame)

        prev_centers = id_tracker.center_points
        ids_to_insert = set(prev_centers.keys()) - set(curr_centers.keys())

        check_ids(ids_to_insert)
        id_tracker.center_points = curr_centers
        
        # if len(plates_map)!=0:
            # print(plates_map, "this is the map")
        
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()

    make_excel(wb,fileName[:(len(fileName)-4)])



    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print("Time taken = ", elapsed_time)