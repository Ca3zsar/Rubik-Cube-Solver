import random

import numpy as np

from cube import CubeCompact, Color
from collections import deque
import database

directions = {
    CubeCompact.up_rotate: 0,
    CubeCompact.down_rotate: 1,
    CubeCompact.left_rotate: 2,
    CubeCompact.right_rotate: 3,
    CubeCompact.front_rotate: 4,
    CubeCompact.back_rotate: 5,
    CubeCompact.up_rotate_twice: 0,
    CubeCompact.down_rotate_twice: 1,
    CubeCompact.left_rotate_twice: 2,
    CubeCompact.right_rotate_twice: 3,
    CubeCompact.front_rotate_twice: 4,
    CubeCompact.back_rotate_twice: 5,
    CubeCompact.up_rotate_counter: 0,
    CubeCompact.down_rotate_counter: 1,
    CubeCompact.left_rotate_counter: 2,
    CubeCompact.right_rotate_counter: 3,
    CubeCompact.front_rotate_counter: 4,
    CubeCompact.back_rotate_counter: 5
}

opposite_faces = [1, 0, 3, 2, 5, 4]

corners = [
    {Color.RED, Color.BLUE, Color.WHITE},  # ULF
    {Color.RED, Color.GREEN, Color.WHITE},  # URF
    {Color.ORANGE, Color.BLUE, Color.WHITE},  # DLF
    {Color.ORANGE, Color.GREEN, Color.WHITE},  # DRF
    {Color.RED, Color.BLUE, Color.YELLOW},  # ULB
    {Color.RED, Color.GREEN, Color.YELLOW},  # URB
    {Color.ORANGE, Color.BLUE, Color.YELLOW},  # DLB
    {Color.ORANGE, Color.GREEN, Color.YELLOW}  # DRB
]

colors = list(Color)


def get_corner_orientation(corner):
    if corner[0] == Color.RED or corner[0] == Color.ORANGE:
        return 0
    try:
        found = corners.index(set(corner))
        if found == 4 or found == 1 or found == 2 or found == 7:
            if corner[1] == Color.RED or corner[1] == Color.ORANGE:
                return 1
            else:
                return 2
        else:
            if corner[2] == Color.RED or corner[2] == Color.ORANGE:
                return 1
            else:
                return 2
    except ValueError:
        print("Corner not found")


def get_corner_position(corner):
    corner = set(corner)
    try:
        return corners.index(corner)
    except ValueError:
        print("Corner not found")
        return


def get_corner_colors(index, faces):
    match index:
        case 0:
            return ((faces[0] >> 32) >> 4) & 0xF, ((faces[0] & 0xFFFFFFFF) >> 20) & 0xF, ((faces[1] >> 32) >> 28) & 0xF
        case 1:
            return ((faces[0] >> 32) >> 12) & 0xF, ((faces[1] & 0xFFFFFFFF) >> 28) & 0xF, ((faces[1] >> 32) >> 20) & 0xF
        case 2:
            return (((faces[2] & 0xFFFFFFFF) >> 28) & 0xF), ((faces[0] & 0xFFFFFFFF) >> 12) & 0xF, ((faces[1] >> 32) >> 4) & 0xF
        case 3:
            return (((faces[2] & 0xFFFFFFFF) >> 20) & 0xF), ((faces[1] & 0xFFFFFFFF) >> 4) & 0xF, ((faces[1] >> 32) >> 12) & 0xF
        case 4:
            return (((faces[0] >> 32) >> 28) & 0xF), ((faces[0] & 0xFFFFFFFF) >> 28) & 0xF, ((faces[2] >> 32) >> 20) & 0xF
        case 5:
            return (((faces[0] >> 32) >> 20) & 0xF), ((faces[1] & 0xFFFFFFFF) >> 20) & 0xF, ((faces[2] >> 32) >> 28) & 0xF
        case 6:
            return (((faces[2] & 0xFFFFFFFF) >> 4) & 0xF), ((faces[0] & 0xFFFFFFFF) >> 4) & 0xF, ((faces[2] >> 32) >> 12) & 0xF
        case 7:
            return (((faces[2] & 0xFFFFFFFF) >> 12) & 0xF), ((faces[1] & 0xFFFFFFFF) >> 12) & 0xF, ((faces[2] >> 32) >> 4) & 0xF


def save_corners(faces, depth):
    response = 0
    for i in range(7):
        corner_colors = [colors[color] for color in get_corner_colors(i, faces)]
        corner_index = get_corner_position(corner_colors)
        corner_orientation = get_corner_orientation(corner_colors)
        response = (response << 5) | (((corner_index & 7) << 2) | (corner_orientation & 3))

    database.add_row(response.to_bytes(9, "big"), depth.to_bytes(1, "big"))


# def save_to_database():
#     content = queue.get()
#     save_corners(faces, depth)


def cube_bfs(cube: tuple, max_depth: int = 11):
    """
    Breadth-first search algorithm for the cube.
    """
    # Initialize the queue with the initial state
    deq = deque([(cube, np.int16((0 << 6) | (7 << 3) | 7))])

    # Initialize the visited set
    visited = set()
    visited.add(cube)
    # While the queue is not empty
    while deq:
        # Get the first element of the queue
        cube = deq.popleft()
        # Save the cube to the database
        # save_corners(cube[0], cube[1])
        if (cube[1] >> 6) >= max_depth:

            del cube
            continue

        for move, face in directions.items():
            if ((cube[1] >> 3) & 7) != 7 and (cube[1] & 7) != 7:
                if ((cube[1] >> 3) & 7) == opposite_faces[(cube[1] & 7)] and (face == (cube[1] & 7) or face == ((cube[1] >> 3) & 7)):
                    continue

            if (cube[1] & 7) == face:
                continue

            child = move(cube[0])

            if child not in visited:
                deq.append((child, (((cube[1]>>6) + 1) << 6) | ((cube[1] & 7) << 3) | face))
                visited.add(child)

            del child
        del move, face
        del cube

    print(len(visited))
    # time.sleep(10)
    # return visited


def cube_bfs_solve(cube : tuple, goal:tuple, max_depth: int = 6):
    deq = [(cube, np.int16((0 << 6) | (7 << 3) | 7))]
    visited = set()
    visited.add(cube)
    # While the queue is not empty
    while deq:
        # Get the first element of the queue
        new_list = []
        for cube in deq:
            if cube[0] == goal:
                return cube[1] >> 6

            if (cube[1] >> 6) >= max_depth:
                del cube
                continue

            for move, face in directions.items():
                if ((cube[1] >> 3) & 7) != 7 and (cube[1] & 7) != 7:
                    if ((cube[1] >> 3) & 7) == opposite_faces[(cube[1] & 7)] and (
                            face == (cube[1] & 7) or face == ((cube[1] >> 3) & 7)):
                        continue

                if (cube[1] & 7) == face:
                    continue

                child = move(cube[0])

                if child not in visited:
                    new_list.append((child, (((cube[1] >> 6) + 1) << 6) | ((cube[1] & 7) << 3) | face))
                    visited.add(child)

                del child
            del move, face
            del cube

        deq = new_list

def get_scrambled_cube(cube: tuple):
    max_moves = 6
    for i in range(max_moves):
        cube = random.choice(list(directions.keys()))(cube)

    return cube