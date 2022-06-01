import cubes.Cube as cube
import cubes.elements.CubeElements as els
import generator
import thistletwaite.construct_cube as construct
import thistletwaite.solve_cube as solve
from time import perf_counter


def main():
    batch_size = 10
    avg_time = 0
    for i in range(batch_size):
        start = perf_counter()
        faces = generator.generate()
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
        solution = solve.test(cube_state, True)
        print(f"{i}:::{len(solution)}  moves :::{solution} ")
        stop = perf_counter()
        print(stop - start)
        print("-------------------")
        avg_time += stop - start
    print(avg_time / batch_size)


if __name__ == "__main__":
    main()