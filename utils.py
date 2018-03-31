# import the necessary packages
import numpy as np
import cv2
import webcolors
from sklearn.cluster import KMeans

def draw_box(img, tl, br, color = (255, 0, 0)):
    h, w = img.shape[:2]
    x1 = int(tl[0]*w)
    x2 = int(br[0]*w)
    y1 = int(tl[1]*h)
    y2 = int(br[1]*h)
    contour = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
    cv2.drawContours(img, [contour], -1, color, 3)

def draw_point(img, p, color = (255, 0, 0)):
    h, w = img.shape[:2]
    x = int(w*p[0])
    y = int(h*p[1])
    cv2.circle(img, (x,y), 2, color, 2)

def convert_point(img, p):
    h, w = img.shape[:2]
    x = int(w*p[0])
    y = int(h*p[1])
    return (x,y)

def get_pixel(img, p):
    h, w = img.shape[:2]
    x = int(w*p[0])
    y = int(h*p[1])
    return img[y,x]

def crop(img, tl, br):
    h, w = img.shape[:2]
    x1 = int(tl[0]*w)
    x2 = int(br[0]*w)
    y1 = int(tl[1]*h)
    y2 = int(br[1]*h)
    return img[y1:y2, x1:x2, :]

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def kmeans(pixel_list):
    clt = KMeans(n_clusters = 2)
    clt.fit(pixel_list)
    return clt.cluster_centers_
