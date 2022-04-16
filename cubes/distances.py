from functools import reduce

from .Cube import RubikCube, FaceDirection, CubeFace


def get_dist_values(actual_colors: list, wanted_colors: list) -> (int, int):
    first_set = set(actual_colors)
    second_set = set(wanted_colors)

    similarities = first_set.intersection(second_set)
    identical = reduce(lambda x, tuplu: x + (tuplu[1] == tuplu[0]), zip(actual_colors, wanted_colors), 0)

    return len(similarities), identical


# Number of moves needed to solve every corner cubie
def compute_number_of_moves(cube: RubikCube):
    distance = 0
    sides: list[CubeFace] = [face for face in cube.faces[1:5]]
    up_face = cube.faces[0]
    down_face = cube.faces[5]

    wanted_corners = []
    actual_corners = []

    up_positions = [(2, 0), (2, 2), (0, 2), (0, 0)]
    down_positions = [(0, 0), (0, 2), (2, 2), (2, 0)]

    for index, (face, up_pos, down_pos) in enumerate(zip(sides, up_positions, down_positions)):
        next_face = sides[(index + 1) % 4]
        # Up corners
        actual = [up_face.face_matrix[up_pos[0]][up_pos[1]], face.face_matrix[0][2], next_face.face_matrix[0][0]]
        wanted = [up_face.face_color, face.face_color, next_face.face_color]
        wanted_corners.append(wanted)
        actual_corners.append(actual)

        # Down corners
        actual = [down_face.face_matrix[down_pos[0]][down_pos[1]], face.face_matrix[2][2], next_face.face_matrix[2][0]]
        wanted = [down_face.face_color, face.face_color, next_face.face_color]
        wanted_corners.append(wanted)
        actual_corners.append(actual)

    for actual_corner, wanted_corner in zip(actual_corners, wanted_corners):
        dist, identical = get_dist_values(actual_corner, wanted_corner)

        if identical == 3:
            continue

        if identical == 1:
            if dist == 2:
                distance += 1
            else:
                distance += 2
        else:
            if dist == 0:
                distance += 3
            elif dist == 3:
                distance += 5
            elif dist == 2:
                distance += 3
            else:
                distance += 1

    return distance


def cube_bfs(cube: RubikCube, max_depth: int = 1, max_moves: int = None) -> int:
    """
    Breadth first search to find the minimum number of moves to solve the cube.
    :param cube: RubikCube
    :param max_depth: Maximum depth of the search
    :param max_moves: Maximum number of moves to find
    :return: Minimum number of moves to solve the cube
    """
    if max_moves is None:
        max_moves = compute_number_of_moves(cube)

    queue = [(cube, 0)]
    visited = set()

    while queue:
        current_cube, current_moves = queue.pop(0)

        if current_moves > max_moves:
            continue

        if current_cube.is_solved():
            return current_moves

        if current_cube in visited:
            continue

        visited.add(current_cube)

        for face_direction in FaceDirection:
            new_cube = current_cube.move(face_direction)

            if new_cube.is_solved():
                return current_moves + 1

            if new_cube not in visited:
                queue.append((new_cube, current_moves + 1))

    return max_moves
