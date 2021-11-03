from Cube import RubikCube, CubeFace, FaceDirection

class InvalidCubeConfiguration(Exception):
    def __init__(self,message):
        super().__init__(f"The cube configuration supplied is not valid.{message}")


def compute_face_score(face : CubeFace, colors, placement) -> int:
    corners = [(0,0),(0,2),(2,0),(2,2)]
    score = 0

    for corner in corners:
        if face.face_matrix[corner[0]][corner[1]] in colors:
            if placement == FaceDirection.UP or placement == FaceDirection.DOWN:
                pass
            else:
                #Check the up row
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


def validate_cube_configuration(cube : RubikCube) -> bool:
    '''
    This function receives a cube and apply a corner parity verification.
    To put it briefly, for the up and down faces it check the corners:
    if one on the up/down facets of the corner the color is the one of the center facet
    of the up/down face, then add 0, if the color of the center facet is on the right side 
    ( as holding the corresponding face towards us), add 1, and in the last case, add 2.
    If the sum is divisible by 3, than the configuration might be valid, otherwise it 
    is wrong. 
    TODO : Add edge parity check
    TODO : Add permutation parity check
    '''

    # Apply corner parity check
    up_color = cube.faces[FaceDirection.UP.value].face_matrix[1][1]
    down_color = cube.faces[FaceDirection.DOWN.value].face_matrix[1][1]

    score = 0

    #Check the Up and Down faces
    for direction in FaceDirection:
        score += compute_face_score(cube.faces[direction.value], (up_color, down_color), direction)

    if score % 3 != 0:
        return False
    
    return True