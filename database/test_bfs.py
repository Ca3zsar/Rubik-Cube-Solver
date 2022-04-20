import sys

import numpy as np

from cube import CubeCompact, Color
import db_fill
from time import perf_counter

solved = CubeCompact(
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

if __name__ == '__main__':
    test(int(sys.argv[1]))