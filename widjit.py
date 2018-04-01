import cv2
import numpy as np
import quad
import utils
import controls
import time
import ocr

cap = cv2.VideoCapture(1)
screenCnt = None
k_thresh = 125 # adjust for lighting

# track when paper has stabilized
counter = 0
counter_thresh = 6
gap_counter = 0
gap_thresh = 3
bg_thresh = None
ppr_quad = None

# density represent grid of samples from paper area
border = 0.01
density = [30, 30]
d_tot = density[0] * density[1]
ref_white = [128, 128, 128]
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

cur_app = ''
tiles = {}
old_tiles = {}

# convert point from density coordinates to fractional coordinates
def dpt2fpt(p):
    x, y = p
    return ((x+1)/(density[0]+1), (y+1)/(density[1]+1))

# get average pixel color sampled over the paper
def get_white():
    ppr_img = ppr_quad.transform(img)
    out = np.array([0, 0, 0])
    for x in range(density[0]):
        for y in range(density[1]):
            p = (x,y)
            out += utils.get_pixel(ppr_img, dpt2fpt(p))
    return (out / d_tot).astype(int)

def handle_tile_start(name, p):
    print('Start: %s' % name)
    global cur_app
    if name in controls.apps:
        if name != cur_app:
            controls.open_app(controls.apps[name])
            cur_app = name
        # apps = list(controls.app_names.intersection(tiles.keys()))
        # if len(apps) == 2:
        #     app1, app2 = sorted(apps, key=lambda x: tiles[x][0])[:2]
        #     controls.open_app(controls.apps[app1])
        #     controls.align_left()
        #     time.sleep(0.1)
        #     controls.open_app(controls.apps[app2])
        #     controls.align_right()
        #     time.sleep(0.1)
        #     controls.open_app(controls.apps[cur_app])
    elif name == 'Play':
        controls.play()
    if name == 'Text':
        query = ocr.read_text(ppr_img)
        if query is not None:
            print(query)
            controls.open_chrome_site(query)
    elif name == 'Dictation':
        controls.dictation()

def handle_tile_end(name):
    global ppr_img
    print('End: %s' % name)
    if name == 'Dictation':
        controls.dictation()

def handle_tile_constant(name, p):
    if name == 'Black':
        controls.change_volume(np.clip(int((p[1]-0.1)/0.75*16),0,16))

while(True):
    ret,img = cap.read()
    img = cv2.flip(img,1)
    img = cv2.flip(img,0)
    orig = img.copy()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, k_thresh, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(thresh, 50, 200)
    (_, contours, _) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        # found paper
        if len(approx) == 4 and peri > 1500 and area > 50000:
            counter += 1
            gap_counter = 0
            if counter >= counter_thresh:
                counter = 0
                screenCnt = approx
                bg_thresh = np.zeros(thresh.shape, dtype=np.uint8)
                ppr_quad = quad.Quad(map(lambda x: x[0], screenCnt))
                ref_white = get_white()
                cv2.fillConvexPoly(bg_thresh, ppr_quad.points, 255)
                cv2.polylines(bg_thresh, [ppr_quad.points], True, 0, 5)
            break

    # allow for brief losses in tracking the paper
    gap_counter += 1
    if gap_counter >= gap_thresh:
        counter = 0

    # if paper is detected
    if bg_thresh is not None:
        ppr_img = ppr_quad.transform(img)
        h, w = ppr_img.shape[:2]

        # get contours for the icons
        area = (ppr_img.shape[0] * ppr_img.shape[1])
        gray = cv2.cvtColor(ppr_img,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, k_thresh, 255, cv2.THRESH_BINARY)[1]
        edges = cv2.Canny(thresh, 50, 200)
        p1 = utils.convert_point(edges, (border,border))
        p2 = utils.convert_point(edges, (1-border,1-border))
        (_, contours, _) = cv2.findContours(edges[p1[1]:p2[1],p1[0]:p2[0]], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = list(filter(lambda x: cv2.contourArea(x, True) > area / 80, map(lambda x: x+p1, contours)))

        # draw icon contours
        cv2.drawContours(ppr_img, cnts, -1, BLUE, 3)

        tiles = {}
        # get center of contours
        for cnt in cnts:
            w_size = 50
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            pixel_list = []
            for dx in range(-w_size,w_size,10):
                for dy in range(-w_size,w_size,10):
                    if dx*dx + dy*dy < 2500:
                        x,y = (cX - dx,cY - dy)
                        pixel_list.append(ppr_img[y,x])
            out = utils.kmeans_noisy(pixel_list)
            # cv2.circle(ppr_img, (cX,cY), 10, out, 20)
            # cv2.circle(ppr_img, (cX,cY), 20, BLACK, 3)    
            # cv2.putText(ppr_img, "(%d,%d,%d)" % ((out[0], out[1], out[2])), (cX-55, cY+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
            name = utils.closest_colour((out[2], out[1], out[0]))
            text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 2)[0]
            # cv2.putText(ppr_img, "%s" % name, (cX-int(text_size[0]/2), cY+int(text_size[1]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, WHITE, 2)
            
            tiles[name] = (cX/w, 1-cY/h)

        for name in tiles.keys() - old_tiles.keys():
            handle_tile_start(name, tiles[name])
        for name in old_tiles.keys() - tiles.keys():
            handle_tile_end(name)
        for name in set(tiles.keys()).intersection(old_tiles.keys()):
            handle_tile_constant(name, tiles[name])
        old_tiles = tiles

        cv2.imshow('Frame', ppr_img)
    else:
        cv2.drawContours(img, cnts, -1, BLUE, 3)
        cv2.imshow('Frame', img)

    if cv2.waitKey(1) &0xFF == ord('q'):
        break
