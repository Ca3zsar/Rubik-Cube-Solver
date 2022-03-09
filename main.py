from time import perf_counter
from cubes.LayerByLayer import BeginnerCube
from cubes.CFOP import CFOPCube
from cubes.elements.CubeElements import Color
from cubes import utils
import generator


def test():
    cfop_avg = 0
    beginner_avg = 0
    batch = 100000
    for i in range(batch):
        faces = generator.generate()
        cfop = CFOPCube(faces)
        # print(cfop)
        # beginner = BeginnerCube(faces)

        try:
            cfop.solve()
            # beginner.solve()
        except KeyboardInterrupt as e:
            print(cfop)
            return

        cfop_moves = utils.process_moves(cfop.moves)
        # beginner_moves = utils.process_moves(beginner.moves)
        # beginner_avg += len(beginner_moves)
        cfop_avg += len(cfop_moves)
        # print(f"{i}. CFOP : {len(cfop_moves)}")
        # print(f"{i}. LayerByLayer : {len(beginner_moves)}")

    print("AVERAGE ")
    print(f"CFOP : {cfop_avg/batch}")
    # print(f"LayerByLayer : {beginner_avg/batch}")

def main():
    try:
        rubik_cube = CFOPCube([
            Color.GREEN, Color.GREEN, Color.YELLOW, Color.BLUE, Color.WHITE, Color.WHITE, Color.BLUE, Color.YELLOW,
            Color.YELLOW,
            Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.RED, Color.WHITE, Color.BLUE, Color.BLUE,
            Color.GREEN,
            Color.ORANGE, Color.GREEN, Color.BLUE, Color.RED, Color.BLUE, Color.BLUE, Color.ORANGE, Color.ORANGE,
            Color.WHITE,
            Color.RED, Color.ORANGE, Color.GREEN, Color.WHITE, Color.ORANGE, Color.GREEN, Color.BLUE, Color.BLUE,
            Color.WHITE,
            Color.ORANGE, Color.RED, Color.YELLOW, Color.ORANGE, Color.GREEN, Color.WHITE, Color.RED, Color.RED,
            Color.ORANGE,
            Color.WHITE, Color.YELLOW, Color.RED, Color.YELLOW, Color.YELLOW, Color.RED, Color.WHITE, Color.YELLOW,
            Color.GREEN
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
