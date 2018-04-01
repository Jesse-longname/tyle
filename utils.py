# import the necessary packages
import numpy as np
import cv2
from sklearn.cluster import KMeans

colors = {
    'Word': (60,80,130),
    'Chrome': (100, 30, 25),
    'Spotify': (31, 55, 50), #(66,91,82),
    'Dictation': (90,20,55),
    'Text': (50,35,70),
    'Play': (140,60,35),
    'Black': (15,15,15)
}

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
    best_color = 'None'
    best_dist = float('inf')
    for name, color in colors.items():
        r_c, g_c, b_c, = color
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        dist = rd + gd + bd
        if dist < best_dist:
            best_color = name
            best_dist = dist
    return best_color

def kmeans(pixel_list):
    clt = KMeans(n_clusters = 2)
    clt.fit(pixel_list)
    labels = clt.labels_
    if sum(labels)/len(labels) > 0.5:
        return clt.cluster_centers_[1]
    return clt.cluster_centers_[0]

def kmeans_noisy(pixel_list):
    k = 3
    clt = KMeans(n_clusters = k, n_init=1, max_iter=5, tol=1e-2, precompute_distances=True)
    clt.fit(pixel_list)
    labels = list(clt.labels_)
    counts = [labels.count(i) for i in range(0,k)]
    x = np.argmax(counts)
    return clt.cluster_centers_[x]
