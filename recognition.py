import numpy as np
import cv2 as cv
import sys

GREEN = (0, 128, 0)
LIME = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)

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


def crop_image(image):
    image = image[60:-100, 20:-20]
    mask = np.zeros(image.shape, dtype=np.uint8)

    roi_corners = np.array([[(5, 90), (225, 10), (425, 70), (405, 310), (235, 435),(45, 333)], ], dtype=np.int32)

    channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
    cv.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image


def get_face(image, corners, color):
    mask = np.zeros(image.shape, dtype=np.uint8)
    
    channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
    cv.fillPoly(mask, corners, ignore_mask_color)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image


def compute_color(color_array):
    # if color_array[0] > 200 and color_array[1] > 200 and color_array[2] > 200:
    #     return "WHITE"
    # elif color_array[0] > 200 and color_array[1] > 200 and color_array[2] < 200:
    #     return "YELLOW"
    # elif color_array[0] > 200 and color_array[1] < 200 and color_array[2] > 200:
    #     return "ORANGE"
    # elif color_array[0] < 200 and color_array[1] > 200 and color_array[2] > 200:
    #     return "GREEN"
    # elif color_array[0] > 200 and color_array[1] < 200 and color_array[2] < 200:
    #     return "BLUE"
    # elif color_array[0] < 200 and color_array[1] < 200 and color_array[2] > 200:
    #     return "RED"
    # else:
    #     return "UNKNOWN"
    
    min_dist = np.inf
    best_color = None
    colors = [WHITE, YELLOW, ORANGE, GREEN, BLUE, RED, LIME]

    for color in colors:
        dist = np.linalg.norm(np.array(color_array) - np.array(color))
        if dist < min_dist:
            min_dist = dist
            best_color = color
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
    boundaries = {
        'left' : [(0,0), (0.3, 0.33), (0.66, 0.7), (1, 1)],
        'right' : [(0,0), (0.33, 0.33), (0.7, 0.7), (1, 1)],
        'up' : [(0,0), (0.33, 0.26), (0.7, 0.63), (1, 1)],
    }

    centers = {
        'left' : [(0.66, 0), (0.95, 0.9)],
        'right' : [(0, 0), (0.33, 0.95)],
        'up' : [(0, 0),(0.33, 0.95)]
    }

    colors = [
        ['','',''],
        ['','',''],
        ['','',''],
    ]

    for i in range(3):
        for j in range(3):
            up_left = (int(boundaries[face][i][0] * image.shape[1]), int(boundaries[face][j][1] * image.shape[0]))
            up_right = (int(boundaries[face][i+1][0] * image.shape[1]), int(boundaries[face][j][1] * image.shape[0]))
            down_left = (int(boundaries[face][i][0] * image.shape[1]), int(boundaries[face][j+1][1] * image.shape[0]))
            down_right = (int(boundaries[face][i+1][0] * image.shape[1]), int(boundaries[face][j+1][1] * image.shape[0]))

            # mean_color = np.mean(image[up_left[1]+5:down_left[1]-5, up_left[0]+5:up_right[0]-5],axis=(0, 1))
            # std = np.std(image[up_left[1]+5:down_left[1]-5, up_left[0]+5:up_right[0]-5],axis=(0, 1))

            

            # print(f"{face}  {i} {j}:::{mean_color[::-1]}")
            # new_mean = np.array([0,0,0], dtype=np.int32)
            # numbers = 0
            # for line in image[up_left[1]+5:down_left[1]-5]:
            #     for point in line[ up_left[0]+5:up_right[0]-5]:
            #         if point[0] > mean_color[0] - 2*std[0] and point[0] < mean_color[0] + 2*std[0] and \
            #             point[1] > mean_color[1] - 2*std[1] and point[1] < mean_color[1] + 2*std[1] and \
            #                 point[2] > mean_color[2] - 2*std[2] and point[2] < mean_color[2] + 2*std[2]:

            #             new_mean[0] += point[0]
            #             new_mean[1] += point[1]
            #             new_mean[2] += point[2]
            #             numbers += 1

            # new_mean //= numbers
            # new_mean = (int(new_mean[0]), int(new_mean[1]), int(new_mean[2]))

            # print(f"{face}  {i} {j}:::{new_mean[::-1]}")
            

            # cv.fillPoly(image, np.array([[up_left, up_right, down_right, down_left]], dtype=np.int32), tuple(new_mean))
            # color = compute_color(new_mean[::-1])
            # print(color)
            # colors[j][i] = color
            print("------")

    # print(f"{face}  {colors}")
    return image
    

def warp_cube(image):
    #Get the faces
    left_corners = np.array([[(5, 90),(45, 333),(235, 435),(225, 170)],],dtype=np.int32)
    right_corners = np.array([[(225, 165),(235, 435),(400, 310),(425, 70)],],dtype=np.int32)
    up_corners = np.array([[(5,90), (225, 160),(430, 70), (225, 10)]], dtype=np.int32)

    new_corners = np.array([[(0,0),(0,420),(420,420),(420,0)]],dtype=np.int32)

    left_face = get_face(img, left_corners, (0, 255, 0))
    M = cv.getPerspectiveTransform(np.float32(left_corners), np.float32(new_corners))
    left_warped = cv.warpPerspective(left_face,M,(420,420))[5:-5,5:-5]

    right_face = get_face(img, right_corners, (255, 0, 0))
    M = cv.getPerspectiveTransform(np.float32(right_corners), np.float32(new_corners))
    right_warped = cv.warpPerspective(right_face,M,(420,420))[5:-5,5:-5]

    up_face = get_face(img, up_corners, (0, 0, 255))
    M = cv.getPerspectiveTransform(np.float32(up_corners), np.float32(new_corners))
    up_warped = cv.warpPerspective(up_face,M,(420,420), flags=cv.INTER_LINEAR)[5:-5,5:-5]

    return left_warped, right_warped, up_warped


img = cv.imread(cv.samples.findFile("third.jpg"))
if img is None:
    sys.exit("Could not read the image.")

img = crop_image(img)
# img = cv.bilateralFilter(img,9,75,75)

img = increase_brightness(img, 30)
left_warped, right_warped, up_warped = warp_cube(img)


#Apply K-Means
# image = apply_kmeans(img)

# left_warped = cv.bilateralFilter(left_warped,9,75,75)
# right_warped = cv.bilateralFilter(right_warped,9,75,75)
# up_warped = cv.bilateralFilter(up_warped,9,75,75)

# left_warped = cv.GaussianBlur(left_warped,(5,5),0)
# right_warped = cv.GaussianBlur(right_warped,(5,5),0)
# up_warped = cv.GaussianBlur(up_warped,(5,5),0)

# left_warped = cv.medianBlur(left_warped,15)
# right_warped = cv.medianBlur(right_warped,15)
# up_warped = cv.medianBlur(up_warped,15)

left_warped = draw_grid(left_warped, "left")
right_warped = draw_grid(right_warped, "right")
up_warped = draw_grid(up_warped, "up")

# cv.imshow("left", apply_kmeans(left_warped))
# cv.imshow("right", apply_kmeans(right_warped))
# cv.imshow("up", apply_kmeans(up_warped))

cv.imshow("left", left_warped)
cv.imshow("right", right_warped)
cv.imshow("up", up_warped)

cv.imwrite("left.jpg", left_warped)
cv.imwrite("right.jpg", right_warped)
cv.imwrite("up.jpg", up_warped)

cv.imshow("original", img)

k = cv.waitKey(0)
cv.destroyAllWindows()
