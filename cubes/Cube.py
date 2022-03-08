from .elements.CubeElements import FaceDirection, Color, CubeFace
from . import utils
import copy

class RubikCube:
    """
    A class used to represent a cube in a simple way.
    It has a list of 6 CubeFace objects, each representing a face of the cube.
    """

    movements = {
        FaceDirection.UP: [(FaceDirection.LEFT, 'L', 0, 1), (FaceDirection.BACK, 'L', 0, 1),
                           (FaceDirection.RIGHT, 'L', 0, 1), (FaceDirection.FRONT, 'L', 0, 1)],
        FaceDirection.LEFT: [(FaceDirection.DOWN, 'C', 0, -1), (FaceDirection.BACK, 'C', 2, -1),
                             (FaceDirection.UP, 'C', 0, 1), (FaceDirection.FRONT, 'C', 0, 1)],
        FaceDirection.FRONT: [(FaceDirection.UP, 'L', 2, 1), (FaceDirection.RIGHT, 'C', 0, -1),
                              (FaceDirection.DOWN, 'L', 0, 1), (FaceDirection.LEFT, 'C', 2, -1)],
        FaceDirection.RIGHT: [(FaceDirection.FRONT, 'C', 2, 1), (FaceDirection.UP, 'C', 2, -1),
                              (FaceDirection.BACK, 'C', 0, -1), (FaceDirection.DOWN, 'C', 2, 1)],
        FaceDirection.BACK: [(FaceDirection.LEFT, 'C', 0, 1), (FaceDirection.DOWN, 'L', 2, -1),
                             (FaceDirection.RIGHT, 'C', 2, 1), (FaceDirection.UP, 'L', 0, -1)],
        FaceDirection.DOWN: [(FaceDirection.FRONT, 'L', 2, 1), (FaceDirection.RIGHT, 'L', 2, 1),
                             (FaceDirection.BACK, 'L', 2, 1), (FaceDirection.LEFT, 'L', 2, 1)]
    }

    revert_movements = {
        FaceDirection.UP: [(FaceDirection.FRONT, 'L', 0, 1), (FaceDirection.RIGHT, 'L', 0, 1),
                           (FaceDirection.BACK, 'L', 0, 1), (FaceDirection.LEFT, 'L', 0, 1)],
        FaceDirection.LEFT: [(FaceDirection.FRONT, 'C', 0, 1), (FaceDirection.UP, 'C', 0, -1),
                             (FaceDirection.BACK, 'C', 2, -1), (FaceDirection.DOWN, 'C', 0, 1)],
        FaceDirection.FRONT: [(FaceDirection.LEFT, 'C', 2, 1), (FaceDirection.DOWN, 'L', 0, -1),
                              (FaceDirection.RIGHT, 'C', 0, 1), (FaceDirection.UP, 'L', 2, -1)],
        FaceDirection.RIGHT: [(FaceDirection.DOWN, 'C', 2, -1), (FaceDirection.BACK, 'C', 0, -1),
                              (FaceDirection.UP, 'C', 2, 1), (FaceDirection.FRONT, 'C', 2, 1)],
        FaceDirection.BACK: [(FaceDirection.UP, 'L', 0, 1), (FaceDirection.RIGHT, 'C', 2, -1),
                             (FaceDirection.DOWN, 'L', 2, 1), (FaceDirection.LEFT, 'C', 0, -1)],
        FaceDirection.DOWN: [(FaceDirection.LEFT, 'L', 2, 1), (FaceDirection.BACK, 'L', 2, 1),
                             (FaceDirection.RIGHT, 'L', 2, 1), (FaceDirection.FRONT, 'L', 2, 1)]
    }

    def __init__(self, configuration: list = None):
        self.moves_number = 0
        self.last_move = None
        self.moves = []

        if not configuration:
            self.face_length = 9
            self.faces = [
                CubeFace([color] * self.face_length, direction) for direction, color in zip(FaceDirection, Color)]
            return

        if len(configuration) != 54:
            raise utils.InvalidCubeConfiguration("Invalid length")

        for color in Color:
            if configuration.count(color) < 9:
                raise utils.InvalidCubeConfiguration("At least one color does not occur for exactly 9 times")

        self.face_length = 9
        self.faces = [
            CubeFace(configuration[direction.value * self.face_length:(direction.value + 1) * self.face_length],
                     direction)
            for direction in FaceDirection]

        if not utils.validate_cube_configuration(self):
            raise utils.InvalidCubeConfiguration("One or more facets might be twisted")

    def make_rotation(self, face: FaceDirection, clockwise: bool):
        """
        Receive a chosen face and rotate it clockwise or counterclockwise.
        """
        if type(face) != FaceDirection:
            print(type(face))
        if face != self.last_move:
            self.moves_number += 1
            self.last_move = face
            self.moves.append((face, clockwise, 1))
        else:
            self.moves.pop()
            self.moves.append((face, clockwise, 2))
            self.last_move = None

        # Make a copy of the actual faces
        faces_copy = copy.deepcopy(self.faces)

        # Rotate the chosen face clockwise
        if clockwise:
            faces_copy[face.value].rotate_clockwise()
        else:
            faces_copy[face.value].rotate_counter()

        if clockwise:
            moves = RubikCube.movements[face]
        else:
            moves = RubikCube.revert_movements[face]

        # Apply the change to the other faces
        for i in range(len(moves)):
            previous = (i - 1) % len(moves)
            # TODO : add optimisation : some operations might be repeated?

            if moves[previous][1] == 'L':
                to_paste = self.faces[moves[previous][0].value].face_matrix[moves[previous][2]]
            else:
                to_paste = [list(column) for column in zip(*self.faces[moves[previous][0].value].face_matrix)][
                    moves[previous][2]]

            if moves[previous][3] == -1:
                to_paste = list(reversed(to_paste))

            if moves[i][1] == 'L':
                faces_copy[moves[i][0].value].face_matrix[moves[i][2]] = to_paste
            else:
                for j in range(len(to_paste)):
                    faces_copy[moves[i][0].value].face_matrix[j][moves[i][2]] = to_paste[j]

        self.faces = faces_copy[:]

    def __str__(self):
        text = ''
        for face in self.faces:
            for line in face.face_matrix:
                for col in line:
                    text += f"{col}, "
            text += '\n'

        return text
