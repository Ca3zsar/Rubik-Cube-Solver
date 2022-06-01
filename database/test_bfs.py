import sys

from cube import CubeCompact, Color
import db_fill
from time import perf_counter

solved = CubeCompact.create_cube(
        [
            [Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED],
            [Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE,
             Color.BLUE],
            [Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE,
             Color.WHITE],
            [Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN,
             Color.GREEN],
            [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW,
             Color.YELLOW, Color.YELLOW],
            [Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE,
             Color.ORANGE, Color.ORANGE]
        ]
    )

def test(depth=1):
    start = perf_counter()

    res = db_fill.cube_bfs(solved, depth)
    end = perf_counter()
    print(end - start)
    return res


def solve():
    start = perf_counter()

    scrambled = db_fill.get_scrambled_cube(solved)
    res = db_fill.cube_bfs_solve(scrambled, solved, 6)
    end = perf_counter()
    print(end - start)
    print(res)

if __name__ == '__main__':
    # test(int(sys.argv[1]))
    solve()