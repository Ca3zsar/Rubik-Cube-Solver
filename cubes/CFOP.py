from .elements.CubeElements import FaceDirection
from .Cube import RubikCube
from . import utils


class CFOPCube(RubikCube):
    """
    A class used to represent a cube in a simple way.
    It has a list of 6 CubeFace objects, each representing a face of the cube.
    """

    def permute_corner(self, face: FaceDirection):
        self.make_rotation(face, True)
        self.make_rotation(FaceDirection.UP, True)
        self.make_rotation(face, False)
        self.make_rotation(FaceDirection.UP, False)

    def inverse_permute_corner(self, face: FaceDirection):
        self.make_rotation(FaceDirection.UP, True)
        self.make_rotation(face, True)
        self.make_rotation(FaceDirection.UP, False)
        self.make_rotation(face, False)

    def counter_permute_corner(self, face: FaceDirection):
        self.make_rotation(face, False)
        self.make_rotation(FaceDirection.UP, False)
        self.make_rotation(face, True)
        self.make_rotation(FaceDirection.UP, True)

    def inverse_counter_permute_corner(self, face: FaceDirection):
        self.make_rotation(FaceDirection.UP, False)
        self.make_rotation(face, False)
        self.make_rotation(FaceDirection.UP, True)
        self.make_rotation(face, True)

    def form_cross(self):
        down_color = self.faces[FaceDirection.DOWN.value].face_color

        # Locate where the edges with the color from the bottom face are
        positions = [(1, 0), (2, 1), (1, 2), (0, 1)]
        sides = [1, 4, 3, 2]

        color_number = 0
        for index, position in enumerate(positions):
            if self.faces[FaceDirection.DOWN.value].face_matrix[position[0]][position[1]] == down_color and \
                    self.faces[sides[index]].face_matrix[2][1] == self.faces[sides[index]].face_color:
                color_number += 1

        if color_number == 4:
            return

        sides = [FaceDirection.LEFT, FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK]
        up_pos = [(1, 0), (2, 1), (1, 2), (0, 1)]
        down_pos = [(1, 0), (0, 1), (1, 2), (2, 1)]
        colors = [self.faces[1].face_color, self.faces[2].face_color, self.faces[3].face_color,
                  self.faces[4].face_color]

        sign = lambda x: (1, -1)[x < 0]

        while color_number < 4:
            i = 1
            #In while e problema la diff ( caz back cu left)
            while i < 5:
                if self.faces[0].face_matrix[positions[i - 1][0]][positions[i - 1][1]] == down_color:
                    diff = colors.index(self.faces[i].face_color) - colors.index(self.faces[i].face_matrix[0][1])

                    if abs(diff) == 3:
                        diff = sign(diff) * (-1)

                    direction = diff > 0

                    for _ in range(abs(diff)):
                        self.make_rotation(FaceDirection.UP, direction)
                    to_rotate = sides[(i - 1 - diff) % 4].value

                    self.make_rotation(self.faces[to_rotate].face_direction, True)
                    self.make_rotation(self.faces[to_rotate].face_direction, True)

                    i = 1
                else:
                    i += 1

            for index, face in enumerate(sides):
                if self.faces[face.value].face_matrix[1][0] == down_color:
                    face_to_check = sides[index - 1]

                    if self.faces[face_to_check.value].face_matrix[1][2] == self.faces[face.value].face_color:
                        self.make_rotation(FaceDirection.DOWN, False)
                        self.make_rotation(face_to_check, True)
                        self.make_rotation(FaceDirection.DOWN, True)
                    elif self.faces[face_to_check.value].face_matrix[1][2] == \
                            self.faces[face_to_check.value].face_color:
                        self.make_rotation(face_to_check, True)
                    else:
                        other_color = self.faces[face_to_check.value].face_matrix[1][2]
                        diff = colors.index(self.faces[face_to_check.value].face_color) - colors.index(other_color)
                        direction = diff > 0
                        for _ in range(abs(diff)):
                            self.make_rotation(FaceDirection.DOWN, direction)

                        self.make_rotation(face_to_check, True)

                        for _ in range(abs(diff)):
                            self.make_rotation(FaceDirection.DOWN, not direction)

                if self.faces[face.value].face_matrix[1][2] == down_color:
                    face_to_check = sides[(index + 1) % 4]

                    if self.faces[face_to_check.value].face_matrix[1][0] == self.faces[face.value].face_color:
                        self.make_rotation(FaceDirection.DOWN, True)
                        self.make_rotation(face_to_check, False)
                        self.make_rotation(FaceDirection.DOWN, False)
                    elif self.faces[face_to_check.value].face_matrix[1][0] == \
                            self.faces[face_to_check.value].face_color:
                        self.make_rotation(face_to_check, False)
                    else:
                        other_color = self.faces[face_to_check.value].face_matrix[1][0]
                        diff = colors.index(self.faces[face_to_check.value].face_color) - colors.index(other_color)
                        direction = diff > 0
                        for _ in range(abs(diff)):
                            self.make_rotation(FaceDirection.DOWN, direction)

                        self.make_rotation(face_to_check, False)

                        for _ in range(abs(diff)):
                            self.make_rotation(FaceDirection.DOWN, not direction)

                if self.faces[face.value].face_matrix[0][1] == down_color:
                    next_face = self.faces[sides[(index + 1) % 4].value]
                    prev_face = self.faces[sides[(index - 1)].value]
                    if self.faces[0].face_matrix[up_pos[index][0]][up_pos[index][1]] == next_face.face_color:
                        self.make_rotation(FaceDirection.DOWN, False)
                        self.make_rotation(face, True)
                        self.make_rotation(FaceDirection.DOWN, True)
                        self.make_rotation(next_face.face_direction, False)

                    elif self.faces[0].face_matrix[up_pos[index][0]][up_pos[index][1]] == prev_face.face_color:
                        self.make_rotation(FaceDirection.DOWN, True)
                        self.make_rotation(face, False)
                        self.make_rotation(FaceDirection.DOWN, False)
                        self.make_rotation(prev_face.face_direction, True)

                    else:
                        self.make_rotation(FaceDirection.UP, True)
                        break

                if self.faces[face.value].face_matrix[2][1] == down_color:
                    next_face = self.faces[sides[(index + 1) % 4].value]
                    prev_face = self.faces[sides[(index - 1)].value]

                    if self.faces[FaceDirection.DOWN.value].face_matrix[down_pos[index][0]][down_pos[index][1]] == \
                            prev_face.face_color:
                        self.make_rotation(face, True)
                        self.make_rotation(prev_face.face_direction, True)
                    elif self.faces[FaceDirection.DOWN.value].face_matrix[down_pos[index][0]][down_pos[index][1]] == \
                            next_face.face_color:
                        self.make_rotation(face, False)
                        self.make_rotation(next_face.face_direction, False)
                    else:
                        self.make_rotation(face, True)

            color_number = 0
            for index, position in enumerate(down_pos):
                if self.faces[FaceDirection.DOWN.value].face_matrix[position[0]][position[1]] == down_color:
                    if self.faces[sides[index].value].face_matrix[2][1] == self.faces[sides[index].value].face_color:
                        color_number += 1
                    else:
                        self.make_rotation(sides[index], True)

            # print(self)
            # print("----------------------------------")


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
        self.form_cross()
        print("Cross done")
        self.bring_corners_down()

    def solve_middle_layer(self):
        up_color = self.faces[FaceDirection.UP.value].face_color

        sides = [FaceDirection.LEFT, FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK]

        pieces = [
            (1, 0), (2, 1), (1, 2), (0, 1)
        ]

        while not utils.is_middle_solved(self.faces[1:5]):
            found_on_third_layer = False
            matched_on_third_layer = False
            for i in range(3):
                found_on_third_layer = False
                matched_on_third_layer = False
                for index in range(len(sides)):
                    up_piece = self.faces[FaceDirection.UP.value].face_matrix[pieces[index][0]][pieces[index][1]]

                    if self.faces[sides[index].value].face_matrix[0][1] != up_color:
                        if self.faces[sides[index].value].face_matrix[0][1] == self.faces[sides[index].value].face_color:
                            if up_piece != up_color:
                                matched_on_third_layer = True
                                found_on_third_layer = True

                                if up_piece == self.faces[sides[index - 1].value].face_color == up_piece:
                                    face_to_move = sides[index - 1]
                                    direction = 0
                                else:
                                    face_to_move = sides[(index + 1) % len(sides)]
                                    direction = 1

                                self.bring_third_layer_to_second(sides[index], face_to_move, direction)
                        else:
                            if up_piece != up_color:
                                found_on_third_layer = True

                if not matched_on_third_layer:
                    self.make_rotation(FaceDirection.UP, True)

            if not found_on_third_layer:
                for index in range(len(sides)):
                    if (self.faces[sides[index].value].face_matrix[1][2] != self.faces[sides[index].value].face_color or
                        self.faces[sides[(index + 1) % len(sides)].value].face_matrix[1][0] !=
                        self.faces[sides[(index + 1) % len(sides)].value].face_color) and \
                            self.faces[sides[index].value].face_matrix[1][2] != up_color and \
                            self.faces[sides[(index + 1) % len(sides)].value].face_matrix[1][0] != up_color:
                        self.bring_third_layer_to_second(sides[index], sides[(index + 1) % len(sides)], 1)
                        break

                self.make_rotation(FaceDirection.UP, True)

    def OLL(self):
        up_color = self.faces[0].face_color

        while not utils.is_cross_formed(self.faces[0]):
            if utils.is_horizontal_line(self.faces[0]):
                self.form_final_cross(1)
            elif utils.is_vertical_line(self.faces[0]):
                self.make_rotation(FaceDirection.UP, True)
            elif moves := utils.wanted_corner(self.faces[0]):
                self.make_rotation(moves[0], True)
                self.make_rotation(FaceDirection.UP, True)
                self.make_rotation(moves[1], True)
                self.make_rotation(FaceDirection.UP, False)
                self.make_rotation(moves[1], False)
                self.make_rotation(moves[0], False)
                # self.form_final_cross(2)
            elif rotations := utils.any_corner(self.faces[0]):
                for _ in range(rotations):
                    self.make_rotation(FaceDirection.UP, True)
            else:
                self.form_final_cross(2)

        rotations = 0
        while not utils.face_solved(self.faces[0]) and rotations < 3:
            # OLL Cases
            facets = [self.faces[0].face_matrix[0][0], self.faces[0].face_matrix[0][2],
                      self.faces[0].face_matrix[2][0], self.faces[0].face_matrix[2][2]]

            if not (number := facets.count(up_color)):
                side_facets = [self.faces[1].face_matrix[0][0], self.faces[1].face_matrix[0][2],
                               self.faces[3].face_matrix[0][0], self.faces[3].face_matrix[0][2]]

                appearances = side_facets.count(up_color)
                if appearances == 4:
                    self.make_rotation(FaceDirection.RIGHT, True)
                    self.make_rotation(FaceDirection.UP, True)
                    self.make_rotation(FaceDirection.RIGHT, False)
                    self.make_rotation(FaceDirection.UP, True)
                    self.make_rotation(FaceDirection.RIGHT, True)
                    self.make_rotation(FaceDirection.UP, False)
                    self.make_rotation(FaceDirection.RIGHT, False)
                    self.make_rotation(FaceDirection.UP, True)
                    self.make_rotation(FaceDirection.RIGHT, True)
                    self.make_rotation(FaceDirection.UP, True)
                    self.make_rotation(FaceDirection.UP, True)
                    self.make_rotation(FaceDirection.RIGHT, False)

                    return
                else:
                    # R U2 R2 U' R2 U' R2 U2 R
                    if appearances == 0:
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.UP, True)

                    if appearances == 2:
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.RIGHT, True)
            else:
                if number == 1:
                    if self.faces[0].face_matrix[0][2] == up_color:
                        condition = all([self.faces[1].face_matrix[0][0] == up_color,
                                         self.faces[2].face_matrix[0][0] == up_color,
                                         self.faces[3].face_matrix[0][0] == up_color])
                        if condition:
                            self.make_rotation(FaceDirection.RIGHT, True)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.RIGHT, False)
                            self.make_rotation(FaceDirection.UP, False)
                            self.make_rotation(FaceDirection.RIGHT, True)
                            self.make_rotation(FaceDirection.UP, False)
                            self.make_rotation(FaceDirection.RIGHT, False)
                        else:
                            # Can't really prove this at the moment
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.UP, True)

                            self.make_rotation(FaceDirection.RIGHT, True)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.RIGHT, False)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.RIGHT, True)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.RIGHT, False)
                elif number == 2:
                    if self.faces[0].face_matrix[0][0] == up_color and self.faces[0].face_matrix[2][2] == up_color:
                        if self.faces[3].face_matrix[0][2] == up_color and self.faces[2].face_matrix[0][0] == up_color:
                            self.make_rotation(FaceDirection.FRONT, True)
                            self.make_rotation(FaceDirection.RIGHT, False)
                            self.make_rotation(FaceDirection.FRONT, False)
                            self.make_rotation(FaceDirection.LEFT, True)
                            self.make_rotation(FaceDirection.FRONT, True)
                            self.make_rotation(FaceDirection.RIGHT, True)
                            self.make_rotation(FaceDirection.FRONT, False)
                            self.make_rotation(FaceDirection.LEFT, False)
                    elif self.faces[0].face_matrix[0][0] == up_color and self.faces[0].face_matrix[0][2] == up_color:
                        if self.faces[2].face_matrix[0][0] == up_color and self.faces[2].face_matrix[0][2] == up_color:
                            #R2 D R' U2 R D' R' U2 R'
                            self.make_rotation(FaceDirection.RIGHT, True)
                            self.make_rotation(FaceDirection.RIGHT, True)
                            self.make_rotation(FaceDirection.DOWN, True)
                            self.make_rotation(FaceDirection.RIGHT, False)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.RIGHT, True)
                            self.make_rotation(FaceDirection.DOWN, False)
                            self.make_rotation(FaceDirection.RIGHT, False)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.UP, True)
                            self.make_rotation(FaceDirection.RIGHT, False)
                    elif self.faces[0].face_matrix[0][2] == up_color and self.faces[0].face_matrix[2][2] == up_color:
                        if self.faces[4].face_matrix[0][2] == up_color and self.faces[2].face_matrix[0][0] == up_color:
                            #r U R' U' r' F R F'
                            self.make_rotation(FaceDirection.LEFT, True)
                            self.make_rotation(FaceDirection.FRONT, True)
                            self.make_rotation(FaceDirection.RIGHT, False)
                            self.make_rotation(FaceDirection.FRONT, False)
                            self.make_rotation(FaceDirection.LEFT, False)
                            self.make_rotation(FaceDirection.FRONT, True)
                            self.make_rotation(FaceDirection.RIGHT, True)
                            self.make_rotation(FaceDirection.FRONT, False)

            rotations += 1
            self.make_rotation(FaceDirection.UP, True)

        if utils.face_solved(self.faces[0]):
            return

        # Not OLL Cases yet
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

        while not utils.face_solved(self.faces[0]):
            if self.faces[2].face_matrix[0][0] != up_color and self.faces[1].face_matrix[0][2] != up_color:
                self.make_rotation(FaceDirection.UP, True)
                continue

            if self.faces[2].face_matrix[0][0] == up_color:
                rotations = 4
            else:
                rotations = 2
            for _ in range(rotations):
                self.make_rotation(FaceDirection.LEFT, True)
                self.make_rotation(FaceDirection.DOWN, True)
                self.make_rotation(FaceDirection.LEFT, False)
                self.make_rotation(FaceDirection.DOWN, False)

    def PLL_one_completed(self, faces_solved):
        moves = [FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK, FaceDirection.LEFT]

        while not utils.is_cube_solved(self.faces):
            face = faces_solved[0]
            next_face = (face + 1) % 4
            prev_face = (face - 1) % 4

            # PLL (Ua) : R2 U R U R' U' R' U' R' U R'
            if self.faces[next_face + 1].face_matrix[0][1] == self.faces[prev_face + 1].face_color:
                self.make_rotation(moves[faces_solved[0] - 2], True)
                self.make_rotation(moves[faces_solved[0] - 2], True)
                self.make_rotation(FaceDirection.UP, True)
                self.make_rotation(moves[faces_solved[0] - 2], True)
                self.make_rotation(FaceDirection.UP, True)
                self.make_rotation(moves[faces_solved[0] - 2], False)
                self.make_rotation(FaceDirection.UP, False)
                self.make_rotation(moves[faces_solved[0] - 2], False)
                self.make_rotation(FaceDirection.UP, False)
                self.make_rotation(moves[faces_solved[0] - 2], False)
                self.make_rotation(FaceDirection.UP, True)
                self.make_rotation(moves[faces_solved[0] - 2], False)

            # PLL (Ub) : R U' R U R U R U' R' U' R2
            if self.faces[prev_face + 1].face_matrix[0][1] == self.faces[next_face + 1].face_color:
                self.make_rotation(moves[faces_solved[0] - 2], True)
                self.make_rotation(FaceDirection.UP, False)
                self.make_rotation(moves[faces_solved[0] - 2], True)
                self.make_rotation(FaceDirection.UP, True)
                self.make_rotation(moves[faces_solved[0] - 2], True)
                self.make_rotation(FaceDirection.UP, True)
                self.make_rotation(moves[faces_solved[0] - 2], True)
                self.make_rotation(FaceDirection.UP, False)
                self.make_rotation(moves[faces_solved[0] - 2], False)
                self.make_rotation(FaceDirection.UP, False)
                self.make_rotation(moves[faces_solved[0] - 2], True)
                self.make_rotation(moves[faces_solved[0] - 2], True)

    def PLL(self):
        if utils.is_cube_solved(self.faces):
            return

        faces_solved = utils.get_solved_faces(self)
        moves = [FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK, FaceDirection.LEFT]

        if faces_solved:
            self.PLL_one_completed(faces_solved)
        else:
            while not utils.is_cube_solved(self.faces):
                matches = utils.match_perfect_corners(self.faces)
                while len(matches) != 4:
                    if len(matches) != 2:
                        self.make_rotation(FaceDirection.UP, True)
                        matches = utils.match_perfect_corners(self.faces)
                        continue

                    if abs(matches[0] - matches[1]) == 1 or abs(matches[0] - matches[1]) == 3:
                        first = (matches[1] + 1) if matches[1] != 3 else 1
                        self.make_rotation(moves[first], True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(moves[first], False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(moves[first], False)
                        self.make_rotation(moves[first - 1], True)
                        self.make_rotation(moves[first], True)
                        self.make_rotation(moves[first], True)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(moves[first], False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(moves[first], True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(moves[first], False)
                        self.make_rotation(moves[first - 1], False)
                    else:
                        if matches[0] == 1:
                            first = FaceDirection.FRONT
                            second = FaceDirection.RIGHT
                        else:
                            first = FaceDirection.RIGHT
                            second = FaceDirection.BACK

                        self.make_rotation(first, True)
                        self.make_rotation(second, True)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(second, False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(second, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(second, False)
                        self.make_rotation(first, False)
                        self.make_rotation(second, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(second, False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(second, False)
                        self.make_rotation(first, True)
                        self.make_rotation(second, True)
                        self.make_rotation(first, False)

                    for _ in range(3):
                        matches = utils.match_perfect_corners(self.faces)
                        if len(matches) == 4:
                            break
                        self.make_rotation(FaceDirection.UP, True)

                    matches = utils.match_perfect_corners(self.faces)

                faces_solved = utils.get_solved_faces(self)

                if len(faces_solved) == 4:
                    return

                if len(faces_solved) == 1:
                    self.PLL_one_completed(faces_solved)
                    return

                if not faces_solved and len(utils.match_perfect_corners(self.faces)) == 4:
                    if self.faces[1].face_matrix[0][1] == self.faces[3].face_color and \
                            self.faces[2].face_matrix[0][1] == self.faces[4].face_color and \
                            self.faces[3].face_matrix[0][1] == self.faces[1].face_color:

                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.RIGHT, False)
                    elif self.faces[1].face_matrix[0][1] == self.faces[4].face_color and \
                                    self.faces[2].face_matrix[0][1] == self.faces[3].face_color and \
                                    self.faces[3].face_matrix[0][1] == self.faces[2].face_color:
                        self.make_rotation(FaceDirection.UP, True)

                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.RIGHT, False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.RIGHT, True)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.RIGHT, False)
                    elif self.faces[1].face_matrix[0][1] == self.faces[2].face_color and \
                                    self.faces[2].face_matrix[0][1] == self.faces[1].face_color and \
                                    self.faces[3].face_matrix[0][1] == self.faces[4].face_color:
                        self.make_rotation(FaceDirection.UP, True)

                        self.make_rotation(FaceDirection.BACK, False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.BACK, True)
                        self.make_rotation(FaceDirection.BACK, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.BACK, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.BACK, False)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.BACK, True)
                        self.make_rotation(FaceDirection.UP, True)
                        self.make_rotation(FaceDirection.BACK, True)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.BACK, True)
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.BACK, False)

                for _ in range(3):
                    if utils.is_cube_solved(self.faces):
                        return
                    self.make_rotation(FaceDirection.UP, True)

                faces_solved = utils.get_solved_faces(self)
                if len(faces_solved) == 1:
                    self.PLL_one_completed(faces_solved)
                    return

    def solve(self):
        """
        The solving algorithm is an easy sequence of steps
        """
        # print("Bottom : ")
        self.solve_bottom_layer()
        print("Bottom done")
        # for face in self.faces:
        #     for facet in face.face_matrix:
        #         print(facet, end=' ')
        #     print()
        # print(f"Finished bottom : {self.moves_number}")
        # print("Middle : ")
        # for face in self.faces:
        #     print(face.face_matrix)
        self.solve_middle_layer()
        print("Middle done")
        # print(f"Finished middle : {self.moves_number}")
        # print("Top : ")
        self.OLL()
        print("OLL done")
        # print(f"OLL : {self.moves_number}")
        self.PLL()
        print("PLL done")
        # print(f"Finished top : {self.moves_number}")
