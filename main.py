##############################################################
# COVID-19 Safety Screening System
# Main Program
##############################################################

# import necessary modules
from asyncio import start_unix_server
import os
import cv2
import numpy as np
from lib import opencv_dnn, mask_detection_cnn
from util.bcolors import *

# disable debugging info
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# capture image from camera
try:
    vidcap = cv2.VideoCapture(-1)
    vidcap.set(3, 640)
    vidcap.set(4, 480)
    while vidcap.isOpened():
        ret, frame = vidcap.read()
        if ret:
            face_detection_results = opencv_dnn.detect_faces(frame)
            nearest_face = face_detection_results['nearest_face']
            nearest_face_rect_index = face_detection_results['nearest_face_rect_index']
            detected_faces_rect = face_detection_results['detected_faces_rect']
            prediction = None
            if (np.any(nearest_face)):
                image_to_predict = cv2.cvtColor(
                    nearest_face, cv2.COLOR_BGR2RGB)
                image_to_predict = cv2.resize(image_to_predict, (224, 224))
                image_to_predict = np.expand_dims(image_to_predict, axis=0)
                image_to_predict = image_to_predict.reshape(224, 224, 3)
                image_to_predict = image_to_predict / 256
                prediction = np.argmax(mask_detection_cnn.detect_mask(
                    image_to_predict.reshape(1, 224, 224, 3)))
            for index, detected_face_rect in enumerate(detected_faces_rect):
                startX = detected_face_rect['startX']
                startY = detected_face_rect['startY']
                endX = detected_face_rect['endX']
                endY = detected_face_rect['endY']
                if index == nearest_face_rect_index:
                    y = startY - 10 if startY - 10 > 10 else startY + 10

                    if (not prediction):
                        text = "Face Mask Detected"
                        cv2.rectangle(frame, (startX, startY), (
                            endX, endY), (0, 255, 0), 2)
                        cv2.putText(frame, text, (startX, y),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.45, (0, 255, 0), 1)
                    else:
                        text = "No Face Mask"
                        cv2.rectangle(frame, (startX, startY), (
                            endX, endY), (0, 0, 255), 2)
                        cv2.putText(frame, text, (startX, y),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.45, (0, 0, 255), 1)
                else:
                    cv2.rectangle(frame, (startX, startY), (
                        endX, endY), (255, 255, 0), 2)
            cv2.imshow('COVID-19 Safety Screening System', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
    else:
        print_error("[ERROR]: Unable to open camera")
except Exception as e:
    print_error('[ERROR]: ' + e)


# use image from file system
# try:
#     frame = cv2.imread('assets/sample_data_10.jpg')
#     if np.any(frame):
#         face_detection_results = opencv_dnn.detect_faces(frame)
#         nearest_face = face_detection_results['nearest_face']
#         nearest_face_rect_index = face_detection_results['nearest_face_rect_index']
#         detected_faces_rect = face_detection_results['detected_faces_rect']
#         prediction = None
#         if (np.any(nearest_face)):
#             image_to_predict = cv2.cvtColor(
#                 nearest_face, cv2.COLOR_BGR2RGB)
#             image_to_predict = cv2.resize(image_to_predict, (200, 200))
#             image_to_predict = np.expand_dims(image_to_predict, axis=0)
#             image_to_predict = image_to_predict.reshape(200, 200, 3)
#             image_to_predict = image_to_predict / 256
#             prediction = mask_detection_cnn.detect_mask(
#                 image_to_predict.reshape(1, 200, 200, 3))
#         for index, detected_face_rect in enumerate(detected_faces_rect):
#             startX = detected_face_rect['startX']
#             startY = detected_face_rect['startY']
#             endX = detected_face_rect['endX']
#             endY = detected_face_rect['endY']
#             if index == nearest_face_rect_index:
#                 y = startY - 10 if startY - 10 > 10 else startY + 10

#                 if (not prediction):
#                     text = "Face Mask Detected"
#                     cv2.rectangle(frame, (startX, startY), (
#                         endX, endY), (0, 255, 0), 2)
#                     cv2.putText(frame, text, (startX, y),
#                                 cv2.FONT_HERSHEY_DUPLEX, 0.45, (0, 255, 0), 1)
#                 else:
#                     text = "No Face Mask"
#                     cv2.rectangle(frame, (startX, startY), (
#                         endX, endY), (0, 0, 255), 2)
#                     cv2.putText(frame, text, (startX, y),
#                                 cv2.FONT_HERSHEY_DUPLEX, 0.45, (0, 0, 255), 1)
#             else:
#                 cv2.rectangle(frame, (startX, startY), (
#                     endX, endY), (255, 255, 0), 2)
#         while True:
#             cv2.imshow('COVID-19 Safety Screening System', frame)
#             key = cv2.waitKey(1)
#             if key == 27:
#                 break
# except Exception as e:
#     print_error('[ERROR]: ' + e)
