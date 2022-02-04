from Cube import RubikCube, CubeFace, FaceDirection


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


def validate_cube_configuration(cube: RubikCube) -> bool:
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
