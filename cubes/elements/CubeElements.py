from enum import Enum


class FaceDirection(Enum):
    UP = 0
    LEFT = 1
    FRONT = 2
    RIGHT = 3
    BACK = 4
    DOWN = 5


class Color(Enum):
    RED = 0
    BLUE = 1
    WHITE = 2
    GREEN = 3
    YELLOW = 4
    ORANGE = 5


class CubeFace:
    """
    A class used to represent a cube face. It holds information such as:
    - a matrix of values, each value corresponding to a color
    - the color that this cube face should be at the ending of the algorithm
    """

    def __init__(self, facets: list, direction: FaceDirection):
        # Create a matrix from the received list of values. The matrix should be of form 3x3
        self.face_matrix = [[facets[i * 3], facets[i * 3 + 1], facets[i * 3 + 2]] for i in range(3)]

        # Get the center color of this face
        self.face_color = self.face_matrix[1][1]

        # Set the direction of this face
        self.face_direction = direction

    def rotate_clockwise(self):
        rotated = [list(reversed(column)) for column in zip(*self.face_matrix)]
        self.face_matrix = rotated

    def rotate_counter(self):
        self.face_matrix = [row[::-1] for row in self.face_matrix]
        rotated = [list(reversed(column)) for column in zip(*self.face_matrix[::-1])]
        self.face_matrix = rotated


