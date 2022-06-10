import sys
import cubes.Cube as cube
import cubes.elements.CubeElements as els
import generator
import thistletwaite.construct_cube as construct
import thistletwaite.solve_cube as solve
from time import perf_counter

def read_cube():
    with open("cube.txt", "r") as file:
        cube_string = file.read()
    
    cube_string = cube_string.split(",")
    numbers = list(map(int, cube_string))
    faces = [els.Color(number) for number in numbers]
    return faces

def main():
    existent = "-file" in sys.argv

    start = perf_counter()
    if not existent:
        faces = generator.generate()
    else:
        faces = read_cube()
    rubik = cube.RubikCube(faces)

    centers = [
        rubik.faces[0].face_color,
        rubik.faces[5].face_color,
        rubik.faces[2].face_color,
        rubik.faces[4].face_color,
        rubik.faces[1].face_color,
        rubik.faces[3].face_color,
    ]

    cube_state = construct.CubeRepresentation(centers, rubik)
    solution = solve.test(cube_state, False)
    print(f"{len(solution)}  moves :::{solution} ")
    stop = perf_counter()
    print(stop - start)
    print("-------------------")


if __name__ == "__main__":
    main()