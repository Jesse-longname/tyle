# import the necessary packages
import numpy as np
import cv2

def draw_box(img, tl, br):
    h, w, _ = img.shape
    x1 = int(tl[0]*w)
    x2 = int(br[0]*w)
    y1 = int(tl[1]*h)
    y2 = int(br[1]*h)
    contour = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
    cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)

def crop(img, tl, br):
    h, w, _ = img.shape
    x1 = int(tl[0]*w)
    x2 = int(br[0]*w)
    y1 = int(tl[1]*h)
    y2 = int(br[1]*h)
    return img[y1:y2, x1:x2, :]