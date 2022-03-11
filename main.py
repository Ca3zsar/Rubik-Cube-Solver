import statistics
from time import perf_counter
# from cubes.LayerByLayer import BeginnerCube
from cubes.CFOP import CFOPCube
from cubes.elements.CubeElements import Color
from cubes import utils
import generator


def test():
    cfop_avg = 0
    # beginner_avg = 0
    batch = 1000
    values = []
    over_200 = 0
    under_100 = 0

    cubes = []
    while len(cubes) < batch:
        cube = generator.generate()
        if cube not in cubes:
            cubes.append(cube)

    for i in range(batch):
        faces = cubes[i]
        cfop = CFOPCube(faces)
        # print(cfop)
        # beginner = BeginnerCube(faces)

        try:
            cfop.solve()
            # beginner.solve()
        except KeyboardInterrupt:
            print(cfop)
            return

        cfop_moves = utils.process_moves(cfop.moves)
        # beginner_moves = utils.process_moves(beginner.moves)
        # beginner_avg += len(beginner_moves)
        cfop_avg += len(cfop_moves)
        values.append(len(cfop_moves))
        if len(cfop_moves) < 100:
            under_100 += 1
        elif len(cfop_moves) >= 200:
            over_200 +=1
        print(f"{i}. CFOP : {len(cfop_moves)}")
        # print(f"{i}. LayerByLayer : {len(beginner_moves)}")

    print("AVERAGE ")
    print(f"CFOP : {cfop_avg / batch}")
    print("MEDIAN ")
    print(statistics.median(values))
    print(f"Over 200 : {over_200} . Under 100 : {under_100}")
    # print(f"LayerByLayer : {beginner_avg/batch}")


def main():
    try:
        rubik_cube = CFOPCube([
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
        try:
            start = perf_counter()
            rubik_cube.solve()
        except KeyboardInterrupt:
            print(rubik_cube)
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
