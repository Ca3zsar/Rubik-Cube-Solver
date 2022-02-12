from CubeElements import FaceDirection, Color, RubikCube
import utils


class BeginnerCube(RubikCube):
    """
    A class used to represent a cube in a simple way.
    It has a list of 6 CubeFace objects, each representing a face of the cube.
    """

    def check_up_color(self, face):
        if face == FaceDirection.RIGHT:
            return self.faces[FaceDirection.UP.value].face_matrix[1][2]

        if face == FaceDirection.BACK:
            return self.faces[FaceDirection.UP.value].face_matrix[0][1]

        if face == FaceDirection.LEFT:
            return self.faces[FaceDirection.UP.value].face_matrix[1][0]

        if face == FaceDirection.FRONT:
            return self.faces[FaceDirection.UP.value].face_matrix[2][1]

    def third_layer_to_up(self, face: FaceDirection, down_color: Color):
        sides = [FaceDirection.LEFT, FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK]
        positions = [(1, 0), (2, 1), (1, 2), (0, 1)]

        next_face = (sides.index(face) + 1) % len(sides)

        self.make_rotation(face, True)

        while self.faces[FaceDirection.UP.value].face_matrix[positions[next_face][0]][
            positions[next_face][1]] == down_color:
            self.make_rotation(FaceDirection.UP, True)

        self.make_rotation(sides[next_face], True)

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
                    face_to_check = sides[(sides.index(face) + 1) % 4]

                    if not (self.check_up_color(face_to_check) == down_color):
                        self.make_rotation(face, False)
                        self.make_rotation(face_to_check, True)
                        color_number += 1
                        continue

                    face_to_check = sides[(sides.index(face) - 1) % 4]

                    if not (self.check_up_color(face_to_check) == down_color):
                        self.make_rotation(face, True)
                        self.make_rotation(face_to_check, False)
                        color_number += 1
                        continue

                    if self.check_up_color(face) == down_color:
                        self.make_rotation(FaceDirection.UP, False)
                        self.make_rotation(FaceDirection.UP, False)

                    self.make_rotation(face, True)
                    self.make_rotation(FaceDirection.UP, True)
                    face_to_check = sides[(sides.index(face) - 1) % 4]
                    self.make_rotation(face_to_check, False)

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

        front_face = self.faces[2].face_matrix
        left_face = self.faces[1].face_matrix
        up_color = self.faces[0].face_color

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

    def fill_last_faces(self, faces_solved):
        moves = [FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK, FaceDirection.LEFT]

        while not utils.is_cube_solved(self.faces):
            self.permute_corner(moves[faces_solved[0]])
            self.counter_permute_corner(moves[faces_solved[0] - 2])

            self.inverse_permute_corner(moves[faces_solved[0]])
            self.inverse_counter_permute_corner(moves[faces_solved[0] - 2])

    def complete_cube(self, faces_solved):
        moves = [FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK, FaceDirection.LEFT]

        if faces_solved:
            self.fill_last_faces(faces_solved)
        else:
            while not faces_solved:
                self.permute_corner(moves[0])
                self.counter_permute_corner(moves[0 - 2])

                self.inverse_permute_corner(moves[0])
                self.inverse_counter_permute_corner(moves[0 - 2])

                rotations = 0
                while rotations < 3:
                    faces_solved = [i - 1 for i in range(1, 5) if utils.face_solved(self.faces[i])]
                    if faces_solved:
                        break
                    self.make_rotation(FaceDirection.UP, True)

            self.fill_last_faces(faces_solved)

    def finish_solving(self):
        rotations = 0
        faces_solved = []
        while not utils.is_cube_solved(self.faces) and rotations < 4:
            faces_solved = [i - 1 for i in range(1, 5) if utils.face_solved(self.faces[i])]
            if faces_solved:
                break

            rotations += 1
            self.make_rotation(FaceDirection.UP, True)
        if utils.is_cube_solved(self.faces):
            return

        self.complete_cube(faces_solved)

    def solve(self):
        """
        The solving algorithm is an easy sequence of steps
        """
        self.solve_bottom_layer()
        self.solve_middle_layer()
        self.solve_top_layer()
        self.finish_solving()