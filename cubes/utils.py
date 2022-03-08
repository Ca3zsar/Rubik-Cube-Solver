from .elements.CubeElements import CubeFace, FaceDirection


class InvalidCubeConfiguration(Exception):
    def __init__(self, message):
        super().__init__(f"The cube configuration supplied is not valid.{message}")


def compute_face_score(face: CubeFace, colors, placement) -> int:
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    score = 0

    for corner in corners:
        if face.face_matrix[corner[0]][corner[1]] in colors:
            if placement == FaceDirection.UP or placement == FaceDirection.DOWN:
                pass
            else:
                # Check the up row
                if corner[0] == 0:
                    if corner[1] == 0:
                        score += 1
                    else:
                        score += 2
                else:
                    if corner[1] == 0:
                        score += 2
                    else:
                        score += 1

    return score


def validate_cube_configuration(cube) -> bool:
    """
    This function receives a cube and apply a corner parity verification.
    To put it briefly, for the up and down faces it check the corners:
    if one on the up/down facets of the corner the color is the one of the center facet
    of the up/down face, then add 0, if the color of the center facet is on the right side
    ( as holding the corresponding face towards us), add 1, and in the last case, add 2.
    If the sum is divisible by 3, than the configuration might be valid, otherwise it
    is wrong.
    TODO : Add edge parity check
    TODO : Add permutation parity check
    """

    # Apply corner parity check
    up_color = cube.faces[FaceDirection.UP.value].face_matrix[1][1]
    down_color = cube.faces[FaceDirection.DOWN.value].face_matrix[1][1]

    score = 0

    # Check the Up and Down faces
    for direction in FaceDirection:
        score += compute_face_score(cube.faces[direction.value], (up_color, down_color), direction)

    if score % 3 != 0:
        return False

    return True


def is_right_down_cube(position_1, position_2, down_side: CubeFace, first_side: CubeFace,
                       second_side: CubeFace) -> bool:
    """
    For a specific bottom color and 2 faces check if the right side down corner
    is correctly put and return True
    """

    return down_side.face_matrix[position_1][position_2] == down_side.face_color and \
           first_side.face_matrix[2][2] == first_side.face_color and \
           second_side.face_matrix[2][0] == second_side.face_color


def is_middle_solved(faces: list[CubeFace]) -> bool:
    for face in faces:
        for i in range(3):
            if face.face_matrix[1][i] != face.face_color:
                return False

    return True


def is_cross_formed(face: CubeFace) -> bool:
    """
    For the top face check if the cross is formed
    :param face: the top face to check
    :return bool: return if the cross is formed
    """

    facets = face.face_matrix
    if facets[0][1] == facets[1][0] == facets[1][2] == facets[2][1] == face.face_color:
        return True
    return False


def is_horizontal_line(face: CubeFace) -> bool:
    """
    For the top face check if there is a horizontal line parallel to the front face
    :param face: the top face
    :return bool: return if there is a horizontal line
    """
    facets = face.face_matrix
    return facets[1][0] == facets[1][1] == facets[1][2]


def is_vertical_line(face: CubeFace) -> bool:
    """
    For the top face check if there is a vertical line parallel to the front face
    :param face: the top face
    :return bool: return if there is a vertical line
    """
    facets = face.face_matrix
    return facets[0][1] == facets[1][1] == facets[2][1]


def wanted_corner(face: CubeFace) -> (FaceDirection, bool):
    """
    For the top face check if there is a corner that's looking like 9 o'clock
    :param face: the top face
    :return bool: return if there is the wanted corner
    """
    facets = face.face_matrix
    if facets[0][1] == facets[1][1] == facets[1][0]:
        return FaceDirection.FRONT, FaceDirection.RIGHT
    if facets[0][1] == facets[1][1] == facets[1][2]:
        return FaceDirection.LEFT, FaceDirection.FRONT
    if facets[2][1] == facets[1][1] == facets[1][2]:
        return FaceDirection.BACK, FaceDirection.LEFT
    if facets[2][1] == facets[1][1] == facets[1][0]:
        return FaceDirection.RIGHT, FaceDirection.BACK
    return False


def up_corner(face: CubeFace) -> (FaceDirection, bool):
    """
    For the top face check if there is a corner that's looking like 9 o'clock
    :param face: the top face
    :return bool: return if there is the wanted corner
    """
    facets = face.face_matrix
    if facets[0][1] == facets[1][1] == facets[1][0]:
        return True
    return False


def any_corner(face: CubeFace) -> int:
    """
    For the top face check if there is any corner that's looking like 9 o'clock
    :param face: the top face
    :return bool: return the number of rotations to move the corner to the good location
    """
    facets = face.face_matrix
    if facets[0][1] == facets[1][1] == facets[1][2]:
        return 3

    if facets[1][1] == facets[1][2] == facets[2][1]:
        return 2

    if facets[1][0] == facets[1][1] == facets[2][1]:
        return 1

    return 0


def match_corners(faces: list[CubeFace]) -> list[int]:
    """
    Return the number of matching corners for the up face
    """
    up_color = faces[0].face_color
    up_pieces = [(2, 0), (2, 2), (0, 2), (0, 0)]
    sides = faces[1:5]

    matching = []

    for i in range(len(sides)):
        # Iterate through all 4 sides

        face_color = sides[i].face_color
        next_face_color = sides[(i + 1) % 4].face_color

        first_piece = sides[i].face_matrix[0][2]
        second_piece = sides[(i + 1) % 4].face_matrix[0][0]
        up_piece = faces[0].face_matrix[up_pieces[i][0]][up_pieces[i][1]]

        if {first_piece, second_piece, up_piece} == {face_color, next_face_color, up_color}:
            matching.append(i)

    return matching


def match_perfect_corners(faces: list[CubeFace]) -> list[int]:
    """
    Return the number of matching corners for the up face
    """
    up_color = faces[0].face_color
    up_pieces = [(2, 0), (2, 2), (0, 2), (0, 0)]
    sides = faces[1:5]

    matching = []

    for i in range(len(sides)):
        # Iterate through all 4 sides

        face_color = sides[i].face_color
        next_face_color = sides[(i + 1) % 4].face_color

        first_piece = sides[i].face_matrix[0][2]
        second_piece = sides[(i + 1) % 4].face_matrix[0][0]
        up_piece = faces[0].face_matrix[up_pieces[i][0]][up_pieces[i][1]]

        if first_piece == face_color and second_piece == next_face_color and up_piece == up_color:
            matching.append(i)

    return matching


def face_solved(face: CubeFace) -> bool:
    """
    Check if a face is entirely solved
    :param face: the face to check
    :return bool: if the face is solved
    """
    for i in range(3):
        for j in range(3):
            if face.face_matrix[i][j] != face.face_color:
                return False
    return True


def is_cube_solved(faces: list[CubeFace]) -> bool:
    """
    Check if the cube is solved
    """

    for face in faces:
        if not face_solved(face):
            return False
    return True


def process_moves(moves: list):
    last_move = (moves[0][0], moves[0][1], moves[0][2])
    new_moves = [moves[0]]

    for index, move in enumerate(moves[1:], 1):
        if last_move and move[0] == last_move[0]:
            repetitions = last_move[2]

            if move[1] != last_move[1]:
                repetitions *= (-1)

            new_moves.pop()
            repetitions += move[2]
            if repetitions == 3:
                repetitions = -1
            elif repetitions == -3:
                repetitions = 1

            clockwise = repetitions > 0

            if repetitions:
                last_move = (move[0], clockwise, abs(repetitions) % 4)
                new_moves.append(last_move)
        else:
            new_moves.append(move)
            last_move = move

    return new_moves


def get_solved_faces(cube):
    rotations = 0
    faces_solved = []
    while rotations < 4:
        faces_solved = [i - 1 for i in range(1, 5) if face_solved(cube.faces[i])]
        if faces_solved:
            if len(match_perfect_corners(cube.faces)) == 4:
                break
        cube.make_rotation(FaceDirection.UP, True)
        rotations += 1
    return faces_solved
