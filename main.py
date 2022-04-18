import statistics
from functools import reduce
from time import perf_counter
from cubes.CFOP import CFOPCube
from cubes.elements.CubeElements import Color
from cubes import utils, distances
import generator
import matplotlib.pyplot as plt


def start_solver(index, cube, values):
    cube.solve()
    cfop_moves = utils.process_moves(cube.moves)
    values.append(len(cfop_moves))
    print(f"{index} : {len(cfop_moves)}")


def test():
    batch = 1000
    start = perf_counter()

    cubes = []
    while len(cubes) < batch:
        cube = generator.generate()
        if cube not in cubes:
            cubes.append(cube)

    threads = [None] * batch
    values = []
    try:
        for i in range(batch):
            faces = cubes[i]
            cfop = CFOPCube(faces)
            start_solver(i, cfop, values)
            # threads[i] = threading.Thread(target=start_solver, args=(i, cfop, values,))
            # threads[i].start()
    except:
        print(cfop)

    # for i in range(len(threads)):
    #     threads[i].join()

    intervals = {}
    for value in values:
        temp_value = value - value % 10
        intervals[temp_value] = intervals.get(temp_value, 0) + 1

    print("AVERAGE ")
    print(f"CFOP : {statistics.mean(values)}")
    print("MEDIAN ")
    print(statistics.median(values))
    print(
        f"Over 170 : {reduce(lambda a, b: a + 1 if b > 170 else a, [0] + values, )} . Under 85 : {reduce(lambda a, b: a + 1 if b < 85 else a, [0] + values, )}")
    end = perf_counter()
    print(f"TIME : {end - start}")
    plt.bar(list(intervals.keys()), list(intervals.values()))
    min_value = min(intervals.keys())
    max_value = max(intervals.keys())
    plt.xticks(range(min_value, max_value + 10, 10))
    plt.yticks(range(0, max(intervals.values()) + 1, 10))
    plt.show()


def main():
    rubik_cube = CFOPCube([
        [Color.BLUE, Color.WHITE, Color.WHITE, Color.BLUE, Color.WHITE, Color.WHITE, Color.BLUE, Color.WHITE, Color.WHITE],
        [Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED],
        [Color.YELLOW, Color.BLUE, Color.BLUE, Color.YELLOW, Color.BLUE, Color.BLUE, Color.YELLOW, Color.BLUE, Color.BLUE],
        [Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE],
        [Color.GREEN, Color.GREEN, Color.WHITE, Color.GREEN, Color.GREEN, Color.WHITE, Color.GREEN, Color.GREEN, Color.WHITE],
        [Color.GREEN, Color.YELLOW, Color.YELLOW, Color.GREEN, Color.YELLOW, Color.YELLOW, Color.GREEN, Color.YELLOW, Color.YELLOW]
    ])
    print(distances.compute_number_of_moves(rubik_cube))
    # except utils.InvalidCubeConfiguration as cube_exception:
    #     print(cube_exception)
    #     return
    # except Exception as e:
    #     print(e)
    # else:
    #     try:
    #         start = perf_counter()
    #         rubik_cube.solve()
    #     except KeyboardInterrupt:
    #         print(rubik_cube)
    #     else:
    #         end = perf_counter()
    #         print(f"TIME : {end - start}")
    #
    #         for face in rubik_cube.faces:
    #             for row in face.face_matrix:
    #                 print(row)
    #             print("----------")
    #
    #         moves = utils.process_moves(rubik_cube.moves)
    #         for move in moves:
    #             print(move)
    #         print(f"Movements without pruning : {rubik_cube.moves_number}")
    #
    #         print(f"Movements after pruning : {len(moves)}")


if __name__ == "__main__":
    # test()
    main()
