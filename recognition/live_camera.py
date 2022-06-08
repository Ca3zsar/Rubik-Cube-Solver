import time
import cv2 as cv
import numpy as np

photo_index = 0

video=cv.VideoCapture(2, cv.CAP_DSHOW)

def take_photo(frame, image_index):
    cv.imwrite(f"./samples/frame_{image_index}.jpg", frame)

def show_camera(video, placement = True, show = True):
    global photo_index

    corners = np.array([[(5, 90), (225, 10), (425, 70), (405, 310), (235, 435),(45, 333)], ], dtype=np.int32)
    check, frame = video.read()

    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    frame = frame[60:-100, 20:-20]
    frame_copy = frame.copy()

    #Draw the cube contour
    if placement:
        frame_copy = cv.polylines(frame_copy, corners, True, (0, 0, 0), 3)

        #Draw the arms coverage
        frame_copy = cv.fillPoly(frame_copy, np.array([[
        (233,73),(215,81),(195,73),(191,0),(231,0)]], dtype=np.int32), (0, 0, 0))

        frame_copy = cv.fillPoly(frame_copy, np.array([[
            (109,249),(124,257),(130,278),(25,347),(7,307)
        ]], dtype=np.int32), (0, 0, 0))

        frame_copy = cv.fillPoly(frame_copy, np.array([[
            (328,236), (426,288), (420,324), (304,264)
        ]], dtype=np.int32), (0, 0, 0))

    #Show the camera
    if show:
        cv.imshow("phone", frame_copy)

    if cv.waitKey(1) & 0xFF == ord('s'):
        cv.imwrite(f"samples/sample_{photo_index}.jpg", frame)
        photo_index += 1

    return frame


def main(frame_index = 0, show_placement = True, show_image = True):
    global photo_index
    photo_index = 0
    
    if not video.isOpened():
        print("Could not open video")
        return

    while True:
        frame = show_camera(video, show_placement, show_image)
        
        if cv.waitKey(1) & 0xFF == ord('q') or not show_image:
            take_photo(frame, frame_index)
            break


if __name__ == "__main__":
    main()
    