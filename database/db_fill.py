from cube import CubeCompact
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
