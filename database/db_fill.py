from cube import CubeCompact, Color
from collections import deque

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


def cube_bfs(cube: CubeCompact, max_depth: int = 11):
    """
    Breadth-first search algorithm for the cube.
    """
    # Initialize the queue with the initial state
    queue = deque([(cube, 0, [None, None])])

    # Initialize the visited set
    visited = set()
    visited.add(cube)
    # While the queue is not empty
    while queue:
        # Get the first element of the queue
        cube = queue.popleft()

        if cube[1] >= max_depth:
            del cube
            break

        for move, face in directions.items():
            if cube[2][0] is not None and cube[2][1] is not None:
                if cube[2][0] == opposite_faces[cube[2][1]] and face == cube[2][1] or \
                        face == cube[2][0]:
                    continue

            if cube[2][1] == face:
                continue

            child = CubeCompact(compact_faces=move(cube[0]))

            if child not in visited:
                queue.append((child, cube[1] + 1, [cube[2][1], face]))
                visited.add(child)
            del child
        del move, face
        del cube
    print(len(visited))
    return visited
