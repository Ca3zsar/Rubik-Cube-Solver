import cubes.Cube as cube
import cubes.elements.CubeElements as els
import generator
import thistletwaite.construct_cube as construct
import thistletwaite.solve_cube as solve
from time import perf_counter
import serial
import time

serial_comm = serial.Serial('COM6', 9600)
serial_comm.timeout = 0.1
time.sleep(2)
serial_comm.readline().decode()
def main():
    faces = generator.generate(moves=10)
    rubik = cube.RubikCube(faces)
    # rubik.make_rotation(els.FaceDirection.UP, True)

    print(rubik)
    print("---------end_cube----------")
    centers = [
        rubik.faces[0].face_color,
        rubik.faces[5].face_color,
        rubik.faces[2].face_color,
        rubik.faces[4].face_color,
        rubik.faces[1].face_color,
        rubik.faces[3].face_color,
    ]

    cube_state = construct.CubeRepresentation(centers, rubik)
    solution = solve.test(cube_state, True)
    print(f"{len(solution)}  moves :::{solution} ")
    print("-------------------")

    content = " ".join(map(str, solution))
    print(content+'\n')
    serial_comm.write((content + '\n').encode())
    time.sleep(1)
    print(serial_comm.readline().decode())


if __name__ == "__main__":
    main()
