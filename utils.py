import numpy as np
import cv2
from sklearn.cluster import KMeans

colors = {
    'Word':         ((60,80,135),   (45,60,100)),
    'Chrome':       ((100,65,70),   (75,85,120)),
    'Spotify':      ((80,92,80),    (155,155,155)),
    'Dictation':    ((107,45,75),   (145,145,145)),
    'Search':       ((75,65,90),    (70,60,80)),
    'Play':         ((135,70,60),   (150,125,60)),
    'Black':        ((40,40,40),    (145,145,145))
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

def closest_colour(c1, c2):
    best_color = 'None'
    best_dist = float('inf')
    for name, color in colors.items():
        r1,g1,b1 = color[0]
        r2,g2,b2 = color[1]
        dist = 0
        dist += (r1 - c1[0]) ** 2
        dist += (g1 - c1[1]) ** 2
        dist += (b1 - c1[2]) ** 2
        dist += (r2 - c2[0]) ** 2
        dist += (g2 - c2[1]) ** 2
        dist += (b2 - c2[2]) ** 2
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
