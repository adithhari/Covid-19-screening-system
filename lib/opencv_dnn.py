##############################################################
# COVID-19 Safety Screening System
# Program for detecting faces using OpenCV DNN.
##############################################################

# module imports
import numpy as np
import matplotlib.pyplot as plt
import cv2
from util.bcolors import *

# arguments for the model to work
args = {
    'prototxt':  'assets/deploy.prototxt.txt',
    'model': 'assets/res10_300x300_ssd_iter_140000.caffemodel',
    'confidence': 0.7
}

# function to find the largest image


def find_largest_image(images):
    if (len(images) > 0):
        max_image = images[0]
        max_image_index = 0
        for index, image in enumerate(images):
            if (max_image.size < image.size):
                max_image = image
                max_image_index = index
        return max_image, max_image_index
    return None, None

# function to detect faces in a given image


def detect_faces(image):
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(
        image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    detected_faces = []
    detected_faces_rect = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args['confidence']:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            detected_face = image[startY:endY, startX:endX]
            detected_face_rect = {
                'startX': startX,
                'startY': startY,
                'endX': endX,
                'endY': endY
            }
            detected_faces.append(detected_face)
            detected_faces_rect.append(detected_face_rect)

    detected_image = image
    largest_image = None
    largest_image_index = None
    if (len(detected_faces)):
        largest_image, largest_image_index = find_largest_image(detected_faces)
    return {'image': detected_image, 'faces': detected_faces, 'nearest_face': largest_image, 'detected_faces_rect': detected_faces_rect, 'nearest_face_rect_index': largest_image_index}


# load model
print_normal("[INFO] OpenCV DNN => Initializing... ", False)
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
print_success('Done')
