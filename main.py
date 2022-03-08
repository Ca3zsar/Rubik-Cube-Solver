from time import perf_counter
from cubes.LayerByLayer import BeginnerCube
from cubes.CFOP import CFOPCube
from cubes.elements.CubeElements import Color
from cubes import utils
import generator

def test():
    for i in range(10):
        faces = generator.generate()
        cfop = CFOPCube(faces)
        # beginner = BeginnerCube(faces)

        try:
            cfop.solve()
        except KeyboardInterrupt as e:
            print(cfop)
            return

        # beginner.solve()

        cfop_moves = utils.process_moves(cfop.moves)
        # beginner_moves = utils.process_moves(beginner.moves)

        print(f"{i}. CFOP : {len(cfop_moves)}")


def main():
    try:
        rubik_cube = CFOPCube([
            Color.WHITE, Color.BLUE, Color.GREEN, Color.BLUE, Color.WHITE, Color.WHITE, Color.YELLOW, Color.GREEN,
            Color.ORANGE,
            Color.BLUE, Color.ORANGE, Color.BLUE, Color.ORANGE, Color.RED, Color.YELLOW, Color.YELLOW, Color.RED,
            Color.WHITE,
            Color.RED, Color.RED, Color.GREEN, Color.BLUE, Color.BLUE, Color.ORANGE, Color.RED, Color.GREEN,
            Color.WHITE,
            Color.WHITE, Color.ORANGE, Color.YELLOW, Color.YELLOW, Color.ORANGE, Color.BLUE, Color.ORANGE, Color.RED,
            Color.ORANGE,
            Color.RED, Color.RED, Color.RED, Color.WHITE, Color.GREEN, Color.GREEN, Color.YELLOW, Color.GREEN,
            Color.GREEN,
            Color.GREEN, Color.WHITE, Color.BLUE, Color.YELLOW, Color.YELLOW, Color.WHITE, Color.ORANGE, Color.YELLOW,
            Color.BLUE
        ])
    except utils.InvalidCubeConfiguration as cube_exception:
        print(cube_exception)
        return
    except Exception as e:
        print(e)
    else:
        try:
            start = perf_counter()
            rubik_cube.solve()
        except KeyboardInterrupt as e:
            print(rubik_cube)
        except Exception as e:
            print(rubik_cube)
            return
        else:
            end = perf_counter()
            print(f"TIME : {end - start}")

            for face in rubik_cube.faces:
                for row in face.face_matrix:
                    print(row)
                print("----------")

            moves = utils.process_moves(rubik_cube.moves)
            for move in moves:
                print(move)
            print(f"Movements without pruning : {rubik_cube.moves_number}")

            print(f"Movements after pruning : {len(moves)}")


if __name__ == "__main__":
    test()
    # main()