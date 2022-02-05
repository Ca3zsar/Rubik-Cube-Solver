from enum import Enum
import copy
import utils


class FaceDirection(Enum):
    UP = 0
    LEFT = 1
    FRONT = 2
    RIGHT = 3
    BACK = 4
    DOWN = 5


class Color(Enum):
    WHITE = 0
    RED = 1
    BLUE = 2
    ORANGE = 3
    GREEN = 4
    YELLOW = 5


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

    def __init__(self, configuration: list):
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
        print(face, clockwise)

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

            to_paste = list()

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

    def front_to_up_right(self, down_color: Color):
        while self.faces[FaceDirection.UP.value].face_matrix[2][1] == down_color:
            self.make_rotation(FaceDirection.UP, True)

        self.make_rotation(FaceDirection.FRONT, True)

        while self.faces[FaceDirection.UP.value].face_matrix[1][2] == down_color:
            self.make_rotation(FaceDirection.UP, True)
        self.make_rotation(FaceDirection.RIGHT, True)

    def check_up_color(self, face):
        if face == FaceDirection.RIGHT:
            return self.faces[FaceDirection.UP.value].face_matrix[1][2]

        if face == FaceDirection.BACK:
            return self.faces[FaceDirection.UP.value].face_matrix[0][1]

        if face == FaceDirection.LEFT:
            return self.faces[FaceDirection.UP.value].face_matrix[1][0]

        if face == FaceDirection.FRONT:
            return self.faces[FaceDirection.UP.value].face_matrix[2][1]

    def third_layer_to_up(self, face, down_color):

        if face == FaceDirection.FRONT:
            self.front_to_up_right(down_color)
        else:
            difference = face.value - FaceDirection.FRONT.value
            if difference > 0:
                for i in range(difference):
                    self.make_rotation(FaceDirection.UP, True)
            else:
                self.make_rotation(FaceDirection.UP, False)
            self.front_to_up_right(down_color)

    def permute_corner(self, face: FaceDirection):
        self.make_rotation(face, True)
        self.make_rotation(FaceDirection.UP, True)
        self.make_rotation(face, False)
        self.make_rotation(FaceDirection.UP, False)

    def counter_permute_corner(self, face: FaceDirection):
        self.make_rotation(face, False)
        self.make_rotation(FaceDirection.UP, False)
        self.make_rotation(face, True)
        self.make_rotation(FaceDirection.UP, True)

    def form_up_cross(self):
        down_color = self.faces[FaceDirection.DOWN.value].face_color

        # Locate where the edges with the color from the bottom face are
        positions = [(1, 0), (2, 1), (1, 2), (0, 1)]
        color_number = 0
        for position in positions:
            if self.faces[FaceDirection.UP.value].face_matrix[position[0]][position[1]] == down_color:
                color_number += 1

        if color_number == 4:
            return

        sides = [FaceDirection.LEFT, FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK]

        while color_number < 4:
            for face in sides:
                if self.faces[face.value].face_matrix[0][1] == down_color:
                    self.third_layer_to_up(face, down_color)
                    color_number += 1

                if self.faces[face.value].face_matrix[1][0] == down_color:
                    face_to_check = sides[sides.index(face) - 1]

                    while self.check_up_color(face_to_check) == down_color:
                        self.make_rotation(FaceDirection.UP, True)
                    self.make_rotation(face_to_check, False)
                    color_number += 1

                if self.faces[face.value].face_matrix[1][2] == down_color:
                    face_to_check = sides[(sides.index(face) + 1) % 4]

                    while self.check_up_color(face_to_check) == down_color:
                        self.make_rotation(FaceDirection.UP, True)
                    self.make_rotation(face_to_check, True)
                    color_number += 1

                if self.faces[face.value].face_matrix[2][1] == down_color:
                    while self.check_up_color(face) == down_color:
                        self.make_rotation(FaceDirection.UP, True)

                    self.make_rotation(face, True)
                    self.make_rotation(face, True)
                    self.third_layer_to_up(face, down_color)
                    color_number += 1

            if self.faces[FaceDirection.DOWN.value].face_matrix[0][1] == down_color:
                while self.check_up_color(FaceDirection.FRONT) == down_color:
                    self.make_rotation(FaceDirection.UP, True)

                self.make_rotation(FaceDirection.FRONT, True)
                self.make_rotation(FaceDirection.FRONT, True)
                color_number += 1

            if self.faces[FaceDirection.DOWN.value].face_matrix[1][0] == down_color:
                while self.check_up_color(FaceDirection.LEFT) == down_color:
                    self.make_rotation(FaceDirection.UP, True)

                self.make_rotation(FaceDirection.LEFT, True)
                self.make_rotation(FaceDirection.LEFT, True)
                color_number += 1

            if self.faces[FaceDirection.DOWN.value].face_matrix[1][2] == down_color:
                while self.check_up_color(FaceDirection.RIGHT) == down_color:
                    self.make_rotation(FaceDirection.UP, True)

                self.make_rotation(FaceDirection.RIGHT, True)
                self.make_rotation(FaceDirection.RIGHT, True)
                color_number += 1

            if self.faces[FaceDirection.DOWN.value].face_matrix[2][1] == down_color:
                while self.check_up_color(FaceDirection.BACK) == down_color:
                    self.make_rotation(FaceDirection.UP, True)

                self.make_rotation(FaceDirection.BACK, True)
                self.make_rotation(FaceDirection.BACK, True)
                color_number += 1

    def bring_corners_down(self):
        down_color = self.faces[FaceDirection.DOWN.value].face_color

        positions_up = [(2, 0, FaceDirection.LEFT, FaceDirection.FRONT),
                        (2, 2, FaceDirection.FRONT, FaceDirection.RIGHT),
                        (0, 2, FaceDirection.RIGHT, FaceDirection.BACK),
                        (0, 0, FaceDirection.BACK, FaceDirection.LEFT)]
        positions_down = [(0, 0, FaceDirection.LEFT, FaceDirection.FRONT),
                          (0, 2, FaceDirection.FRONT, FaceDirection.RIGHT),
                          (2, 2, FaceDirection.RIGHT, FaceDirection.BACK),
                          (2, 0, FaceDirection.BACK, FaceDirection.LEFT)]

        color_number = 0
        for position in positions_down:
            if utils.is_right_down_cube(position[0], position[1], self.faces[FaceDirection.DOWN.value],
                                        self.faces[position[2].value], self.faces[position[3].value]):
                color_number += 1
        if color_number == 4:
            return

        while color_number < 4:
            color_number = 0
            for position in positions_down:
                down_necessary = {down_color: 1,
                                  self.faces[position[2].value].face_color: 1,
                                  self.faces[position[3].value].face_color: 1}

                current = {self.faces[FaceDirection.DOWN.value].face_matrix[position[0]][position[1]]: 1,
                           self.faces[position[2].value].face_matrix[2][2]: 1,
                           self.faces[position[3].value].face_matrix[2][0]: 1}

                if down_color in current.keys():
                    if down_necessary == current:

                        while not utils.is_right_down_cube(position[0], position[1],
                                                           self.faces[FaceDirection.DOWN.value],
                                                           self.faces[position[2].value],
                                                           self.faces[position[3].value]):
                            self.permute_corner(position[3])

                    elif not utils.is_right_down_cube(position[0], position[1], self.faces[FaceDirection.DOWN.value],
                                                      self.faces[position[2].value], self.faces[position[3].value]):
                        # Bring the corner up
                        self.permute_corner(position[3])

            for index in range(len(positions_up)):
                position = positions_up[index]
                up_necessary = {down_color: 1,
                                self.faces[position[2].value].face_color: 1,
                                self.faces[position[3].value].face_color: 1}

                current = {self.faces[FaceDirection.UP.value].face_matrix[position[0]][position[1]]: 1,
                           self.faces[position[2].value].face_matrix[0][2]: 1,
                           self.faces[position[3].value].face_matrix[0][0]: 1}

                if down_color in current.keys():
                    if up_necessary == current:
                        while not utils.is_right_down_cube(positions_down[index][0], positions_down[index][1],
                                                           self.faces[FaceDirection.DOWN.value],
                                                           self.faces[position[2].value],
                                                           self.faces[position[3].value]):
                            self.permute_corner(position[3])

            for position in positions_down:
                if utils.is_right_down_cube(position[0], position[1], self.faces[FaceDirection.DOWN.value],
                                            self.faces[position[2].value], self.faces[position[3].value]):
                    color_number += 1

            if color_number == 4:
                break

            self.make_rotation(FaceDirection.UP, True)

    def bring_third_layer_to_second(self, main_face, second_face, direction):
        self.make_rotation(FaceDirection.UP, direction)

        self.make_rotation(second_face, direction)
        self.make_rotation(FaceDirection.UP, direction)
        self.make_rotation(second_face, not (bool(direction)))
        self.make_rotation(FaceDirection.UP, not (bool(direction)))

        self.make_rotation(main_face, not (bool(direction)))
        self.make_rotation(FaceDirection.UP, not (bool(direction)))
        self.make_rotation(main_face, direction)

    def form_final_cross(self, repetitions):
        self.make_rotation(FaceDirection.FRONT, True)

        for _ in range(repetitions):
            self.make_rotation(FaceDirection.RIGHT, True)
            self.make_rotation(FaceDirection.UP, True)
            self.make_rotation(FaceDirection.RIGHT, False)
            self.make_rotation(FaceDirection.UP, False)

        self.make_rotation(FaceDirection.FRONT, False)

    def solve_bottom_layer(self):
        self.form_up_cross()

        rotations = 0
        while rotations < 4:
            for face in [FaceDirection.LEFT, FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK]:
                if self.faces[face.value].face_matrix[0][1] == self.faces[face.value].face_color and \
                        self.check_up_color(face) == self.faces[FaceDirection.DOWN.value].face_color:
                    self.make_rotation(face, True)
                    self.make_rotation(face, True)
                    rotations += 1

            self.make_rotation(FaceDirection.UP, True)

        self.bring_corners_down()

    def solve_middle_layer(self):
        up_color = self.faces[FaceDirection.UP.value].face_color

        sides = [FaceDirection.LEFT, FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK]

        pieces = [
            (1, 0), (2, 1), (1, 2), (0, 1)
        ]

        while not utils.is_middle_solved(self.faces[1:5]):
            found_on_third_layer = False
            for index in range(len(sides)):
                up_piece = self.faces[FaceDirection.UP.value].face_matrix[pieces[index][0]][pieces[index][1]]

                if self.faces[sides[index].value].face_matrix[0][1] == self.faces[sides[index].value].face_color:
                    if up_piece != up_color:
                        found_on_third_layer = True

                        if up_piece == self.faces[sides[index - 1].value].face_color == up_piece:
                            face_to_move = sides[index - 1]
                            direction = 0
                        else:
                            face_to_move = sides[(index + 1) % len(sides)]
                            direction = 1

                        self.bring_third_layer_to_second(sides[index], face_to_move, direction)

            if not found_on_third_layer:
                for index in range(len(sides)):
                    if self.faces[sides[index].value].face_matrix[1][2] == \
                            self.faces[sides[(index + 1) % len(sides)].value].face_color and \
                            self.faces[sides[(index + 1) % len(sides)].value].face_matrix[1][0] == \
                            self.faces[sides[index].value].face_color:
                        self.bring_third_layer_to_second(sides[index], sides[(index + 1) % len(sides)], 1)
                        break

                self.make_rotation(FaceDirection.UP, True)

    def solve_top_layer(self):
        while not utils.is_cross_formed(self.faces[0]):
            if utils.is_horizontal_line(self.faces[0]):
                self.form_final_cross(1)
            elif utils.is_vertical_line(self.faces[0]):
                self.make_rotation(FaceDirection.UP, True)
            elif utils.wanted_corner(self.faces[0]):
                self.form_final_cross(2)
            elif rotations := utils.any_corner(self.faces[0]):
                for _ in range(rotations):
                    self.make_rotation(FaceDirection.UP, True)
            else:
                self.form_final_cross(2)

        faces_moves = [FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK, FaceDirection.LEFT]
        outcomes = [{0, 3}, {0, 1}, {1, 2}, {2, 3}]

        diagonal_moves = [(FaceDirection.RIGHT, FaceDirection.FRONT), (FaceDirection.BACK, FaceDirection.RIGHT)]
        diagonal_outcomes = [{0, 2}, {1, 3}]

        while len(matches := utils.match_corners(self.faces)) != 4:
            if len(matches) != 2:
                self.make_rotation(FaceDirection.UP, True)
                continue

            difference = abs(matches[0] - matches[1])
            if difference % 2 == 1:
                move = [i for i in range(4) if outcomes[i] == set(matches)][0]
                for _ in range(3):
                    self.permute_corner(faces_moves[(move + 1) % 4])
                for _ in range(3):
                    self.counter_permute_corner(faces_moves[move])
            else:
                move = 0 if diagonal_outcomes[0] == set(matches) else 1
                for _ in range(3):
                    self.permute_corner(diagonal_moves[move][0])
                for _ in range(3):
                    self.counter_permute_corner(diagonal_moves[move][1])

    def solve(self):
        """
        The solving algorithm is an easy sequence of steps
        """
        self.solve_bottom_layer()
        self.solve_middle_layer()
        self.solve_top_layer()


def main():
    try:
        rubik_cube = RubikCube([
            Color.GREEN, Color.WHITE, Color.ORANGE, Color.ORANGE, Color.WHITE, Color.WHITE, Color.RED, Color.WHITE,
            Color.WHITE,
            Color.ORANGE, Color.WHITE, Color.WHITE, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED,
            Color.RED,
            Color.GREEN, Color.BLUE, Color.RED, Color.BLUE, Color.BLUE, Color.ORANGE, Color.BLUE, Color.BLUE,
            Color.BLUE,
            Color.BLUE, Color.RED, Color.WHITE, Color.BLUE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE,
            Color.ORANGE,
            Color.BLUE, Color.GREEN, Color.WHITE, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN,
            Color.GREEN,
            Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW,
            Color.YELLOW, Color.YELLOW
        ])
    except utils.InvalidCubeConfiguration as cube_exception:
        print(cube_exception)
        return

    rubik_cube.solve()

    for face in rubik_cube.faces:
        for row in face.face_matrix:
            print(row)
        print("----------")


if __name__ == "__main__":
    main()
