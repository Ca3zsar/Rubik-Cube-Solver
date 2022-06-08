from cubes.elements.CubeElements import Color
from recognition import live_camera
from recognition import color_analyzer as analyzer

import serial
import time
# Start the program

inverses = {
    1:3,
    3:1,
    2:4,
    4:2,
    0:5,
    5:0
}

faces = [-1] * 54
serial_comm = serial.Serial('COM6', 9600)
serial_comm.timeout = 0.1
time.sleep(0.5)

def set_faces(result, index):
    if index == 0:
        for i in range(9):
            faces[i] = result[i+18]
            faces[18+i] = result[i]
            faces[27+i] = result[9+i]
    elif index == 1:
        #0 - up, 9 - left, 18 - front, 27 - right, 36 - back, 45 - down
        for i in range(3):
            faces[36 + i] = result[i]
            faces[9 + i] = result[9 + i]
    elif index == 2:
        for i in range(3):
            faces[9 + i + 6] = result[9 + i + 6]
            faces[36 + i + 6] = result[i + 6]
    elif index == 3:
        for i in range(3):
            faces[45 + i] = result[18 + 8 - i]
        faces[9 + 5] = result[9 + 3]
    elif index == 4:
        for i in range(3):
            faces[45 + i + 6] = result[18 + 2 - i]
        faces[9 + 3] = result[9 + 5]
    elif index == 5:
        faces[36 + 5] = result[3]
        faces[45 + 3] = result[18 + 3]
    elif index == 6:
        faces [36 + 3] = result[5]
        faces[45 + 5] = result[18 + 5]


def execute_step(rotation_index, step_index):
    print(f"Step {step_index}")

    command = f"{rotation_index}\n"
    print(command)
    serial_comm.write(command.encode())
    while not (message := serial_comm.readline().decode()):
        pass
    print(message)

    live_camera.main(frame_index=step_index,show_placement = False, show_image = False)
    result = analyzer.apply_operations(
        show = False,
        crop = False,
        rotate = False,
        image_name = f"samples/sample_{step_index}.jpg",
        return_data = True
    )

    set_faces(result, step_index)
    while serial_comm.in_waiting:
        pass
    serial_comm.write(command.encode())
    while not (message := serial_comm.readline().decode()):
        pass
    print(message)

def main():
    # Place the cube in the right position and take the first photo 
    live_camera.main(frame_index=0,show_placement = True, show_image = True)
    
    result = analyzer.apply_operations(
        show = False,
        crop = False,
        rotate = False,
        image_name = "samples/sample_0.jpg",
        return_data = True
    )

    set_faces(result, 0)

    for i in range(6):
        execute_step(i * 3 + 1, i + 1)
    
    faces[9 + 4] = inverses[faces[27 + 4]]
    faces[36 + 4] = inverses[faces[18 + 4]]
    faces[45 + 4] = inverses[faces[0 + 4]]
    for i in range(0,54,9):
        print(faces[i:i+9])

    with open("cube.txt", "w") as file:
        file.write(",".join(map(str, faces)))
    
    live_camera.video.release()

if __name__ == "__main__":

    main()
