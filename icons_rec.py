import numpy as np
import cv2

def recoginze_icon(img):
    col = detect_color(img)
    if col == "green":
        return("spotify")
    elif col == "blue":
        return("word")
    else:
        return("chrome")

def detect_color(img):
    # define the list of boundaries
    def avg_col(img):
        average_color = [img[:, :, i].mean() for i in range(img.shape[-1])]
        return average_color
    avg = avg_col(img)
    if avg[0] > 150:
        return "blue"
    if avg[1]> 150:
        return "green"
    return "rainbow"

        
