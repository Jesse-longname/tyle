import numpy as np
import cv2
from sklearn.cluster import KMeans

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
    if avg[1]> 100:
        return "green"
    return "rainbow"

def kmeans(image):
    clt = KMeans(nclusters = 2)
    # reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    clt.fit(image)
    return clt.cluster_centers_



        
