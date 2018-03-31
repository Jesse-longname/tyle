# import the necessary packages
import numpy as np
import cv2

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