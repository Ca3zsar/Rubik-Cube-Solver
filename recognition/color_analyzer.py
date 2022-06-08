from operator import index
from matplotlib.pyplot import hsv
import numpy as np
import cv2 as cv
import sys

GREEN = (0, 255, 0)
LIME = (0, 128, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
GRAY = (128,128,128)

indexes = {
    WHITE : 2,
    YELLOW : 4,
    ORANGE : 5,
    GREEN : 3,
    BLUE : 1,
    RED : 0,
}

faces_config = []

def apply_kmeans(image):
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER + cv.TERM_CRITERIA_COUNT, 10, 1.0)
    K = 7
    ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_PP_CENTERS,np.array([(70, 70), (210, 70), (350, 70), (70, 210), (210, 210), (350, 210), (70, 350), (210, 350), (350, 350)]))
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(image.shape)

    return res2

def crop_image(image, crop_img = False):
    if crop_img:
        image = image[60:-100, 20:-20]
    mask = np.zeros(image.shape, dtype=np.uint8)

    roi_corners = np.array([[(5, 90), (225, 10), (425, 70), (405, 310), (235, 435),(45, 333)], ], dtype=np.int32)

    channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
    cv.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image

def get_face(image, corners, color):
    mask = np.zeros(image.shape, dtype=np.uint8)
    
    channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
    cv.fillPoly(mask, corners, ignore_mask_color)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image

def compute_color(color_array):
    min_dist = np.inf
    best_color = None
    colors = [WHITE, YELLOW, ORANGE, GREEN, BLUE, RED, LIME, GRAY]

    for color in colors:
        dist = np.linalg.norm(np.array(color_array) - np.array(color))
        if dist < min_dist:
            min_dist = dist
            best_color = color

    hsv_color = cv.cvtColor(np.uint8([[color_array[::-1]]]), cv.COLOR_BGR2HSV)[0][0]
    # print(hsv_color)

    second_color = None #[ 20 180 242]

    if (hsv_color[0] <= 11 or hsv_color[0] >= 170) and hsv_color[1] > 5:
        second_color = RED
    elif hsv_color[0] > 11 and hsv_color[0] <= 20 and hsv_color[1] > 150:
        second_color = ORANGE
    elif hsv_color[0] >= 18 and hsv_color[0] <= 32 and hsv_color[1] > 150 and hsv_color[2] > 10:
        second_color = YELLOW
    elif hsv_color[0] > 32 and hsv_color[0] <= 65 and hsv_color[1] > 30:
        second_color = GREEN
    elif hsv_color[0] > 65 and hsv_color[1] > 55 and hsv_color[2] >= 65 and\
            hsv_color[0] <= 120:
        second_color = BLUE
    elif hsv_color[0] <= 25 and hsv_color[0] > 15 and hsv_color[1] < 78:
        second_color = WHITE
    
    # print(second_color, best_color)
    if second_color:
        return second_color
    else:
        if best_color == GRAY:
            best_color = WHITE
        if best_color == LIME:
            best_color = GREEN
        return best_color

def increase_brightness(img, value=30):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img

def draw_grid(image, face):
    global faces_config
    boundaries = {
        'left' : [(0,0), (0.3, 0.33), (0.66, 0.7), (1, 1)],
        'right' : [(0,0), (0.33, 0.33), (0.7, 0.7), (1, 1)],
        'up' : [(0,0), (0.33, 0.26), (0.7, 0.63), (1, 1)],
    }

    for i in range(3):
        for j in range(3):
            up_left = (int(boundaries[face][j][0] * image.shape[1]), int(boundaries[face][i][1] * image.shape[0]))
            up_right = (int(boundaries[face][j+1][0] * image.shape[1]), int(boundaries[face][i][1] * image.shape[0]))
            down_left = (int(boundaries[face][j][0] * image.shape[1]), int(boundaries[face][i+1][1] * image.shape[0]))
            down_right = (int(boundaries[face][j+1][0] * image.shape[1]), int(boundaries[face][i+1][1] * image.shape[0]))

            cubie = image[up_left[1]+10:down_left[1]-10, up_left[0]+10:up_right[0]-10]

            # mean_color = np.array([0,0,0])
            # colors_number = 0
            # for row in cubie:
            #     for color in row:
            #         if color[0] != 0 or color[1] != 0 or color[2] != 0:
            #             mean_color[0] += color[0]
            #             mean_color[1] += color[1]
            #             mean_color[2] += color[2]
            #             colors_number += 1

            # mean_color = mean_color / colors_number

            cubie = cubie[np.where((cubie[:,:,0] != 0) | (cubie[:,:,1] != 0) | (cubie[:,:,2] != 0))]
            mean_color = np.mean(cubie, axis=0)
            # print(faces_config)
            cv.fillPoly(image, np.array([[up_left, up_right, down_right, down_left]], dtype=np.int32), mean_color)
            color = compute_color(mean_color[::-1])
            
            faces_config.append(indexes[color])
            
            # print(f"{i} {j} {mean_color[::-1]}")
    #         print(f"{i} {j} {color}")
    #         print("------")
    # print("-----------------------------------------------------")
    return image
    
def warp_cube(image):
    #Get the faces
    left_corners = np.array([[(5, 90),(45, 333),(235, 435),(225, 170)],],dtype=np.int32)
    right_corners = np.array([[(225, 165),(235, 435),(400, 310),(425, 70)],],dtype=np.int32)
    up_corners = np.array([[(5,90), (225, 160),(430, 70), (225, 10)]], dtype=np.int32)

    new_corners = np.array([[(0,0),(0,420),(420,420),(420,0)]],dtype=np.int32)

    left_face = get_face(image, left_corners, (0, 255, 0))
    M = cv.getPerspectiveTransform(np.float32(left_corners), np.float32(new_corners))
    left_warped = cv.warpPerspective(left_face,M,(420,420))[5:-5,5:-5]

    right_face = get_face(image, right_corners, (255, 0, 0))
    M = cv.getPerspectiveTransform(np.float32(right_corners), np.float32(new_corners))
    right_warped = cv.warpPerspective(right_face,M,(420,420))[5:-5,5:-5]

    up_face = get_face(image, up_corners, (0, 0, 255))
    M = cv.getPerspectiveTransform(np.float32(up_corners), np.float32(new_corners))
    up_warped = cv.warpPerspective(up_face,M,(420,420), flags=cv.INTER_LINEAR)[5:-5,5:-5]
    up_warped = cv.rotate(up_warped, cv.ROTATE_90_COUNTERCLOCKWISE)

    return left_warped, right_warped, up_warped

def apply_operations(**options):
    global faces_config
    faces_config = []

    show = options.get('show', False)
    crop = options.get('crop', False)
    rotate = options.get('rotate', False)
    image_name = options.get('image_name', '')
    return_data = options.get('return_data', False)

    img = cv.imread(cv.samples.findFile(image_name))
    if img is None:
        sys.exit("Could not read the image.")

    if rotate:
        img = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)

    img = crop_image(img, crop)
    cv.imwrite("cropped.jpg", img)

    #Cover the arms
    img = cv.fillPoly(img, np.array([[
        (233,73),(215,81),(195,73),(191,0),(231,0)]], dtype=np.int32), (0, 0, 0))

    img = cv.fillPoly(img, np.array([[
        (109,249),(124,257),(130,278),(25,347),(7,307)
    ]], dtype=np.int32), (0, 0, 0))

    img = cv.fillPoly(img, np.array([[
        (328,236), (426,288), (420,324), (304,264)
    ]], dtype=np.int32), (0, 0, 0))

    #Cover the reflection
    # img = cv.fillPoly(img, np.array([[
    #     (199,187),(202,120),(229,119),(227,186)
    # ]], dtype=np.int32), (0, 0, 0))

    # gamma = 0.9
    # lookUpTable = np.empty((1,256), np.uint8)
    # for i in range(256):
    #     lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    # img = cv.LUT(img, lookUpTable)

    # img = increase_brightness(img, 30)
    #[222.52667984 140.43135705  83.17977602]
    left_warped, right_warped, up_warped = warp_cube(img)
    # left_warped = cv.GaussianBlur(left_warped, (5,5), sigmaX=50, sigmaY=50)
    # right_warped = cv.GaussianBlur(right_warped, (5,5), sigmaX=50, sigmaY=50)
    # up_warped = cv.GaussianBlur(up_warped, (5,5), sigmaX=50, sigmaY=50)

    #Apply K-Means
    # image = apply_kmeans(img)

    # left_warped = apply_kmeans(left_warped)
    # right_warped = apply_kmeans(right_warped)
    # up_warped = apply_kmeans(up_warped)

    left_warped = draw_grid(left_warped, "left")
    right_warped = draw_grid(right_warped, "right")
    up_warped = draw_grid(up_warped, "up")
    if show:
        cv.imshow("left", left_warped)
        cv.imshow("right", right_warped)
        cv.imshow("up", up_warped)

        cv.imwrite("left.jpg", left_warped)
        cv.imwrite("right.jpg", right_warped)
        cv.imwrite("up.jpg", up_warped)

        cv.imshow("original", img)

        cv.waitKey(0)
    cv.destroyAllWindows()
    if return_data:
        return faces_config
    

def main():
    show = True
    crop = "-c" in sys.argv
    rotate = "-r" in sys.argv
    image_name = sys.argv[1]
    apply_operations(show=show, crop=crop, rotate=rotate, image_name=image_name)


if __name__ == "__main__":
    main()