import utils
from time import perf_counter
from LayerByLayer import BeginnerCube
from CubeElements import Color


def main():
    start = perf_counter()
    try:
        rubik_cube = BeginnerCube([
            Color.YELLOW, Color.RED, Color.WHITE, Color.RED, Color.GREEN, Color.GREEN, Color.WHITE, Color.GREEN,
            Color.WHITE,
            Color.GREEN, Color.WHITE, Color.RED, Color.WHITE, Color.WHITE, Color.ORANGE, Color.YELLOW, Color.YELLOW,
            Color.YELLOW,
            Color.BLUE, Color.ORANGE, Color.ORANGE, Color.BLUE, Color.ORANGE, Color.BLUE, Color.ORANGE, Color.BLUE,
            Color.BLUE,
            Color.GREEN, Color.YELLOW, Color.BLUE, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.ORANGE, Color.WHITE,
            Color.RED,
            Color.ORANGE, Color.GREEN, Color.RED, Color.RED, Color.RED, Color.BLUE, Color.GREEN, Color.WHITE,
            Color.BLUE,
            Color.GREEN, Color.RED, Color.YELLOW, Color.ORANGE, Color.BLUE, Color.GREEN, Color.RED, Color.ORANGE,
            Color.WHITE
        ])
    except utils.InvalidCubeConfiguration as cube_exception:
        print(cube_exception)
        return
    except Exception as e:
        print(e)
    else:
        rubik_cube.solve()

        for face in rubik_cube.faces:
            for row in face.face_matrix:
                print(row)
            print("----------")

        end = perf_counter()
        print(f"TIME : {end - start}")
        print(rubik_cube.moves_number)


if __name__ == "__main__":
    main()

