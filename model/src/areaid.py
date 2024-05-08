import cv2
import numpy as np
from skimage.segmentation import clear_border
import argparse
from PIL import ImageEnhance
from PIL import Image
from track import *
from helper import find_licensePlate, read_image, modify_no, resizeFrame, calculate_frequency, rec
# 
fixed_height = 600  # Set your desired height
id_tracker = EuclideanDistTracker()
plates_map = {}

plat_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")

fileName = 'data11.mp4'
video = cv2.VideoCapture('../Data/' + fileName)


if (video.isOpened() == False):
    print('Error Reading Video')

frameCount=0
while True:
    isreading, frame = video.read()
    frameCount = frameCount+1
    # if (frameCount % 3 != 0):
    #     continue
    if isreading == False:
        print('vedio completed or error in reading frame')
        break

    gray_video = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    plate_coordinates = plat_detector.detectMultiScale(
        gray_video, scaleFactor=1.2, minNeighbors=5, minSize=(25, 25))
    boxes_ids = []
    detections = []
    for (x, y, w, h) in plate_coordinates:

        plate_roi = frame[y:y+h, x:x+w]
        cv2.imshow('plate', plate_roi)
        lisence_plate = find_licensePlate(plate_roi)

        # results = reader.readtext(plate_roi, paragraph='False')
        number = read_image(lisence_plate, psm=7)
        # try:
        if number is not None and number.strip() != "":
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # veh_number = number.strip()
            veh_number = modify_no(number)
            print(number.strip(), " ", number)
            cv2.putText(frame, text=veh_number, org=(
                x-3, y-3), fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 255), thickness=2, fontScale=2)

            detections.append([x, y, x+w, y+h, veh_number])

    ids_to_insert = id_tracker.update(detections) 

    plates_map = id_tracker.plates_map
    # print(plates_map)
    
    


    resized_frame = resizeFrame(frame, fixed_height)

    cv2.imshow('frame', resized_frame)
    
    if len(plates_map)!=0:
        print(plates_map, "this is the map")
    for id in ids_to_insert:
        print("ID:", id)
        if id in plates_map:
            # Check if the value associated with 'id' is empty or not
            if plates_map[id]:
                # Access the value
                vector = plates_map[id]
                # Calculate frequency of numbers in the sorted vector for the first 70% of elements
                sorted_plates = calculate_frequency(vector)
                print(sorted_plates, "sorted_plates")
                final_plate=rec(sorted_plates)
                print(final_plate, " final Plate ")
                # Print the frequency of each number
                
                # Your further code here
            else:
                print("The value associated with id is not detected.")
            del plates_map[id]
        else:
            print("The id does not exist in plates_map.")

        
       
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()



