##############################################################
# COVID-19 Safety Screening System
# Program for detecting masks on faces using custom CNN
##############################################################

import os
import pandas as pd
import numpy as np
import seaborn as sns
from util.bcolors import *
import matplotlib.pyplot as plt
from matplotlib.image import imread
from tensorflow.keras.models import load_model

print_normal('[INFO] Face Detector => Loading Model... ')
model = load_model('assets/face_mask_detection_mobilenetv2.h5')
print_success('Done')


def detect_mask(image):
    prediction = (model.predict(image) > 0.5).astype("int32")
    return prediction
