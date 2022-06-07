import cv2 as cv
import numpy as np

# address = "http://192.168.1.102:4747/video"
# video.open(address)

def main():
    video=cv.VideoCapture(1)
    corners = np.array([[(5, 90), (225, 10), (425, 70), (405, 310), (235, 435),(45, 333)], ], dtype=np.int32)

    photo_index = 0

    while True:
        check, frame = video.read()
        frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
        frame = frame[60:-100, 20:-20]
        frame_copy = frame.copy()

        #Draw the cube contour
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
        cv.imshow("phone", frame_copy)

        if cv.waitKey(1) & 0xFF == ord('s'):
            cv.imwrite(f"samples/sample_{photo_index}.jpg", frame)
            photo_index += 1

        if cv.waitKey(1) & 0xFF == ord('k'):
            return frame

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()