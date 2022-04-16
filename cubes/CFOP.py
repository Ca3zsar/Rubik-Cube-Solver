from .elements.CubeElements import FaceDirection
from .Cube import RubikCube
from . import utils, oll
from . import f2l


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
                        opposite_face = sides[(index - 2)]
                        if other_color == self.faces[opposite_face.value].face_color:
                            self.make_rotation(FaceDirection.DOWN, True)
                            self.make_rotation(face_to_check, True)
                            self.make_rotation(FaceDirection.DOWN, False)
                        else:
                            self.complex_rotation("D2")
                            self.make_rotation(face_to_check, True)
                            self.complex_rotation("D2")

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
                    elif self.faces[FaceDirection.DOWN.value].face_matrix[down_pos[index][0]][down_pos[index][1]] == \
                            self.faces[face.value].face_color:
                        self.make_rotation(face, False)
                        self.make_rotation(FaceDirection.DOWN, True)
                        self.make_rotation(next_face.face_direction, False)
                        self.make_rotation(FaceDirection.DOWN, False)
                    else:
                        self.make_rotation(face, False)
                        self.make_rotation(FaceDirection.DOWN, False)
                        self.make_rotation(next_face.face_direction, False)
                        self.make_rotation(FaceDirection.DOWN, True)

            color_number = 0
            for index, position in enumerate(down_pos):
                if self.faces[FaceDirection.DOWN.value].face_matrix[position[0]][position[1]] == down_color:
                    if self.faces[sides[index].value].face_matrix[2][1] == self.faces[sides[index].value].face_color:
                        color_number += 1
                    else:
                        self.make_rotation(sides[index], True)

    def bring_third_layer_to_second(self, main_face, second_face, direction):
        d1 = "" if direction else "'"
        d2 = "'" if direction else ""
        s = second_face.name[0]
        m = main_face.name[0]

        self.complex_rotation(f"U{d1}{s}{d1}U{d1}{s}{d2}U{d2}{m}{d2}U{d2}{m}{d1}")

    def form_final_cross(self, repetitions):
        self.make_rotation(FaceDirection.FRONT, True)

        for _ in range(repetitions):
            self.permute_corner(FaceDirection.RIGHT)

        self.make_rotation(FaceDirection.FRONT, False)

    def solve_bottom_layer(self):
        self.form_cross()
        self.f2l()
        # print("Cross done")

    def OLL(self):
        up_color = self.faces[0].face_color

        while not utils.is_cross_formed(self.faces[0]):
            if utils.is_horizontal_line(self.faces[0]):
                if oll.oll_13(self.faces[2], self.faces[3], self.faces[4], self.faces[0], up_color):
                    self.complex_rotation("FURU'R2F'RURU'R'")
                elif oll.oll_14(self.faces[2], self.faces[1], self.faces[4], self.faces[0], up_color):
                    self.complex_rotation("R'FRUR'F'RFU'F'")
                elif oll.oll_39(self.faces[2], self.faces[3], self.faces[4], self.faces[0], up_color):
                    self.complex_rotation("LF'L'U'LUFU'L'")
                elif oll.oll_40(self.faces[2], self.faces[1], self.faces[4], self.faces[0], up_color):
                    self.complex_rotation("R'FRUR'U'F'UR")
                elif oll.oll_34(self.faces[2], self.faces[1], self.faces[3], self.faces[4], self.faces[0], up_color):
                    self.complex_rotation("RUR2U'R'FRURU'F'")
                elif self.faces[4].face_matrix[0][2] == up_color and self.faces[1].face_matrix[0][0] == up_color and \
                        self.faces[3].face_matrix[0][0] == up_color and self.faces[3].face_matrix[0][2] == up_color:
                    self.complex_rotation("FURU'R'URU'R'F'")
                elif oll.oll_55(self.faces[2], self.faces[4], up_color):
                    self.complex_rotation("R'FRURU'R2F'R2U'R'URUR'")
                elif oll.oll_45(self.faces[2], self.faces[1], self.faces[4], self.faces[0], up_color):
                    self.complex_rotation("FRUR'U'F'")
                elif oll.oll_33(self.faces[2], self.faces[4], self.faces[0], up_color):
                    self.complex_rotation("RUR'U'R'FRF'")
                elif oll.oll_56(self.faces[2], self.faces[1], self.faces[3], self.faces[4], up_color):
                    self.complex_rotation("LFL'URU'R'URU'R'LF'L'")
                else:
                    self.form_final_cross(1)
            elif utils.is_vertical_line(self.faces[0]):
                if oll.oll_46(self.faces[1], self.faces[3], self.faces[0], up_color):
                    self.complex_rotation("R'U'R'FRF'UR")
                elif oll.oll_52(self.faces[2], self.faces[1], self.faces[3], self.faces[4], up_color):
                    self.complex_rotation("RUR'URU'BU'B'R'")
                else:
                    self.make_rotation(FaceDirection.UP, True)
            elif moves := utils.wanted_corner(self.faces[0]):
                cond = False
                # 9 o'clock
                if moves[0] == FaceDirection.FRONT:
                    if oll.oll_29(self.faces[2], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("RUR'U'RU'R'F'U'FRUR'")
                        cond = True
                    elif oll.oll_9(self.faces[2], self.faces[1], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("RUR'U'R'FR2UR'U'F'")
                        cond = True
                    elif oll.oll_28(self.faces[2], self.faces[3], self.faces[0], up_color):
                        self.complex_rotation("FRUR'U'F'U2FRUR'U'F'")
                        cond = True
                    elif oll.oll_30(self.faces[2], self.faces[1], self.faces[3], self.faces[0], up_color):
                        self.complex_rotation("FR'FR2U'R'U'RUR'F2")
                        cond = True
                    elif oll.oll_32(self.faces[2], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("LUF'U'L'ULFL'")
                        cond = True
                    elif oll.oll_37(self.faces[2], self.faces[3], self.faces[0], up_color):
                        self.complex_rotation("FR'F'RURU'R'")
                        cond = True
                    elif oll.oll_38(self.faces[2], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("RUR'URU'R'U'R'FRF'")
                        cond = True
                    elif oll.oll_41(self.faces[2], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("RUR'URU2R'FRUR'U'F'")
                        cond = True
                    elif oll.oll_44(self.faces[2], self.faces[3], self.faces[0], up_color):
                        self.complex_rotation("FURU'R'F'")
                        cond = True
                    elif oll.oll_48(self.faces[2], self.faces[1], self.faces[3], self.faces[4], up_color):
                        self.complex_rotation("FRUR'U'RUR'U'F'")
                        cond = True

                # 3 o'clock
                if moves[0] == FaceDirection.LEFT:
                    if oll.oll_31(self.faces[2], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("R'U'FURU'R'F'R")
                        cond = True
                    if oll.oll_36(self.faces[2], self.faces[1], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("L'U'LU'L'ULULF'L'F")
                        cond = True
                    elif oll.oll_43(self.faces[2], self.faces[1], self.faces[0], up_color):
                        self.complex_rotation("F'U'L'ULF")
                        cond = True
                    elif oll.oll_47(self.faces[2], self.faces[1], self.faces[3], self.faces[4], up_color):
                        self.complex_rotation("R'U'R'FRF'R'FRF'UR")
                        cond = True

                if moves[0] == FaceDirection.RIGHT:
                    if oll.oll_10(self.faces[2], self.faces[1], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("RUR'UR'FRF'RU2R'")
                        cond = True
                    elif oll.oll_42(self.faces[2], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("R'U'RU'R'U2RFRUR'U'F'")
                        cond = True
                    elif oll.oll_49(self.faces[2], self.faces[3], self.faces[4], up_color):
                        self.complex_rotation("RB'R2FR2BR2F'R")
                        cond = True

                if moves[0] == FaceDirection.BACK:
                    if oll.oll_35(self.faces[2], self.faces[1], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("RUR'UR'FRF'RU2R'")
                        cond = True
                    elif oll.oll_50(self.faces[2], self.faces[1], self.faces[4], up_color):
                        self.complex_rotation("RB'RBR2U2FR'F'R")
                        cond = True

                if not cond:
                    self.make_rotation(moves[0], True)
                    self.make_rotation(FaceDirection.UP, True)
                    self.make_rotation(moves[1], True)
                    self.make_rotation(FaceDirection.UP, False)
                    self.make_rotation(moves[1], False)
                    self.make_rotation(moves[0], False)
            else:
                cond = False
                if self.faces[4].face_matrix[0][1] == up_color and self.faces[2].face_matrix[0][1] == up_color:
                    if utils.line_in_single_color(self.faces[1], 0, up_color) and utils.line_in_single_color(self.faces[3], 0, up_color):
                        self.complex_rotation("RU2R2FRF'U2R'FRF'")
                        cond = True
                    elif utils.line_in_single_color(self.faces[1], 0, up_color) and self.faces[4].face_matrix[0][0] == up_color and \
                            self.faces[2].face_matrix[0][2] == up_color:
                        self.complex_rotation("BL'B'LUL2F'L'FU'L'")
                        cond = True
                    elif oll.oll_20(self.faces[2], self.faces[1], self.faces[3], self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("RBUB'R'F2BD'L'DB'F2")
                        cond = True
                    elif oll.oll_17(self.faces[2], self.faces[1],self.faces[3],self.faces[4], self.faces[0], up_color):
                        self.complex_rotation("RUR'UR'FRF'U2R'FRF'")
                        cond = True
                if not cond:
                    self.form_final_cross(2)

        while not utils.face_solved(self.faces[0]):
            # OLL Cases
            if oll.oll_21(self.faces[2], self.faces[4], up_color):
                self.complex_rotation("RU2R'U'RUR'U'RU'R'")
            elif oll.oll_22(self.faces[2], self.faces[1], self.faces[4], up_color):
                self.complex_rotation("RU2R2U'R2U'R2U2R")
            elif oll.oll_23(self.faces[4], self.faces[0], up_color):
                self.complex_rotation("R2D'RU2R'DRU2R")
            elif oll.oll_22(self.faces[2], self.faces[4], self.faces[0], up_color):
                self.complex_rotation("LFR'F'L'FRF'")
            elif oll.oll_24(self.faces[2], self.faces[4], self.faces[0], up_color):
                self.complex_rotation("LFR'F'L'FRF'")
            elif oll.oll_25(self.faces[2], self.faces[1], self.faces[0], up_color):
                self.complex_rotation("F'LFR'F'L'FR")
            elif oll.oll_26(self.faces[2], self.faces[1], self.faces[3], self.faces[0], up_color):
                self.complex_rotation("RU2R'U'RU'R'")
            elif oll.oll_27(self.faces[2], self.faces[3], self.faces[4], self.faces[0], up_color):
                self.complex_rotation("RUR'URU2R'")
            if not utils.face_solved(self.faces[0]):
                self.make_rotation(FaceDirection.UP, True)

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
                        self.complex_rotation("R2U2R'U2R2U2R2U2R'U2R2")
                    elif self.faces[1].face_matrix[0][1] == self.faces[4].face_color and \
                            self.faces[2].face_matrix[0][1] == self.faces[3].face_color and \
                            self.faces[3].face_matrix[0][1] == self.faces[2].face_color:
                        self.complex_rotation("UR'U'R2URUR'U'RURU'RU'R'")
                    elif self.faces[1].face_matrix[0][1] == self.faces[2].face_color and \
                            self.faces[2].face_matrix[0][1] == self.faces[1].face_color and \
                            self.faces[3].face_matrix[0][1] == self.faces[4].face_color:
                        self.complex_rotation("UB'U'B2UBUB'U'BUBU'BU'B'")

                for _ in range(3):
                    if utils.is_cube_solved(self.faces):
                        return
                    self.make_rotation(FaceDirection.UP, True)

                faces_solved = utils.get_solved_faces(self)
                if len(faces_solved) == 1:
                    self.PLL_one_completed(faces_solved)
                    return

    def f2l(self):
        down_color = self.faces[5].face_color
        up_color = self.faces[0].face_color
        sides = [FaceDirection.LEFT, FaceDirection.FRONT, FaceDirection.RIGHT, FaceDirection.BACK]

        positions = [(2, 1), (1, 2), (0, 1), (1, 0)]
        corners = [(2, 0), (2, 2), (0, 2), (0, 0)]
        down_corners = [(0, 0), (0, 2), (2, 2), (2, 0)]
        case_3_pos = [(0, 1), (1, 0), (2, 1), (1, 2)]
        self.movement_made = False
        while not utils.is_middle_solved(self.faces[1:5]) or not utils.face_solved(self.faces[5]):
            rotations = 0
            while rotations < 4:
                self.movement_made = False
                for index, side in enumerate(sides):
                    next_face = sides[(index + 1) % 4]
                    prev_face = sides[index - 1]

                    if self.faces[side.value].face_matrix[0][2] == down_color and \
                            self.faces[0].face_matrix[corners[index][0]][corners[index][1]] == self.faces[side.value].face_color and \
                            self.faces[next_face.value].face_matrix[0][0] == self.faces[next_face.value].face_color:

                        if self.faces[next_face.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[positions[index][0]][positions[index][1]] == self.faces[side.value].face_color:
                            f2l.f2l_1(self, next_face)

                        elif self.faces[prev_face.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index][0]][case_3_pos[index][1]] == self.faces[next_face.value].face_color:
                            f2l.f2l_3(self, side)

                        elif self.faces[sides[index - 2].value].face_matrix[0][1] == self.faces[
                            next_face.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index - 1][0]][case_3_pos[index - 1][1]] == \
                                self.faces[side.value].face_color:
                            f2l.f2l_5(self, next_face)

                        elif self.faces[prev_face.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index][0]][case_3_pos[index][1]] == self.faces[side.value].face_color:
                            f2l.f2l_7(self, next_face)

                        elif self.faces[sides[index - 2].value].face_matrix[0][1] == self.faces[
                            side.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index - 1][0]][case_3_pos[index - 1][1]] == \
                                self.faces[next_face.value].face_color:
                            f2l.f2l_9(self, next_face, side)

                        elif self.faces[next_face.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[positions[index][0]][positions[index][1]] == self.faces[next_face.value].face_color:
                            f2l.f2l_11(self, next_face, side)

                        elif self.faces[side.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[positions[index - 1][0]][positions[index - 1][1]] == \
                                self.faces[next_face.value].face_color:
                            f2l.f2l_13(self, side)

                        elif self.faces[side.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[positions[index - 1][0]][positions[index - 1][1]] == \
                                self.faces[side.value].face_color:
                            f2l.f2l_15(self, next_face, prev_face, sides[(index + 2) % 4])

                        elif self.faces[side.value].face_matrix[1][2] == self.faces[side.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[next_face.value].face_color:
                            f2l.f2l_33(self, next_face)

                        elif self.faces[side.value].face_matrix[1][2] == self.faces[next_face.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[side.value].face_color:
                            f2l.f2l_35(self, next_face, side)

                    elif self.faces[side.value].face_matrix[0][2] == self.faces[side.value].face_color and \
                            self.faces[0].face_matrix[corners[index][0]][corners[index][1]] == self.faces[next_face.value].face_color and \
                            self.faces[next_face.value].face_matrix[0][0] == down_color:
                        if self.faces[side.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[positions[index - 1][0]][positions[index - 1][1]] == \
                                self.faces[next_face.value].face_color:
                            f2l.f2l_2(self, side)

                        elif self.faces[sides[index - 2].value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index - 1][0]][case_3_pos[index - 1][1]] == \
                                self.faces[side.value].face_color:
                            f2l.f2l_4(self, next_face)

                        elif self.faces[prev_face.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index][0]][case_3_pos[index][1]] == self.faces[next_face.value].face_color:
                            f2l.f2l_6(self, next_face, side)

                        elif self.faces[sides[index - 2].value].face_matrix[0][1] == self.faces[
                            side.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index - 1][0]][case_3_pos[index - 1][1]] == \
                                self.faces[next_face.value].face_color:
                            f2l.f2l_8(self, side)

                        elif self.faces[prev_face.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index][0]][case_3_pos[index][1]] == self.faces[side.value].face_color:
                            f2l.f2l_10(self, next_face)

                        elif self.faces[side.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[positions[index - 1][0]][positions[index - 1][1]] == \
                                self.faces[side.value].face_color:
                            f2l.f2l_12(self, next_face)

                        elif self.faces[next_face.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[positions[index][0]][positions[index][1]] == self.faces[side.value].face_color:
                            f2l.f2l_14(self, next_face)

                        elif self.faces[next_face.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[positions[index][0]][positions[index][1]] == self.faces[next_face.value].face_color:
                            f2l.f2l_16(self, next_face, side)

                        elif self.faces[side.value].face_matrix[1][2] == self.faces[side.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[next_face.value].face_color:
                            f2l.f2l_34(self, side)

                        elif self.faces[side.value].face_matrix[1][2] == self.faces[next_face.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[side.value].face_color:
                            f2l.f2l_36(self, next_face, side)

                    elif self.faces[side.value].face_matrix[0][2] == self.faces[next_face.value].face_color and \
                            self.faces[0].face_matrix[corners[index][0]][corners[index][1]] == down_color and \
                            self.faces[next_face.value].face_matrix[0][0] == self.faces[side.value].face_color:

                        if self.faces[next_face.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[positions[index][0]][positions[index][1]] == self.faces[side.value].face_color:
                            f2l.f2l_17(self, next_face)
                        elif self.faces[side.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[positions[index - 1][0]][positions[index - 1][1]] == \
                                self.faces[next_face.value].face_color:
                            f2l.f2l_18(self, side)
                        elif self.faces[sides[index - 2].value].face_matrix[0][1] == self.faces[
                            next_face.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index - 1][0]][case_3_pos[index - 1][1]] == \
                                self.faces[side.value].face_color:
                            f2l.f2l_19(self, next_face, side)
                        elif self.faces[prev_face.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index][0]][case_3_pos[index][1]] == self.faces[next_face.value].face_color:
                            f2l.f2l_20(self, next_face, side)
                        elif self.faces[prev_face.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index][0]][case_3_pos[index][1]] == self.faces[side.value].face_color:
                            f2l.f2l_21(self, next_face)

                        elif self.faces[sides[index - 2].value].face_matrix[0][1] == self.faces[
                            side.value].face_color and \
                                self.faces[0].face_matrix[case_3_pos[index - 1][0]][case_3_pos[index - 1][1]] == \
                                self.faces[next_face.value].face_color:
                            f2l.f2l_22(self, prev_face, side)
                        elif self.faces[side.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[positions[index - 1][0]][positions[index - 1][1]] == \
                                self.faces[side.value].face_color:
                            f2l.f2l_23(self, next_face)
                        elif self.faces[next_face.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[positions[index][0]][positions[index][1]] == self.faces[next_face.value].face_color:
                            f2l.f2l_24(self, next_face, side, prev_face)
                        elif self.faces[side.value].face_matrix[1][2] == self.faces[next_face.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[side.value].face_color:
                            f2l.f2l_31(self, next_face, side)

                        elif self.faces[side.value].face_matrix[1][2] == self.faces[side.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[next_face.value].face_color:
                            f2l.f2l_32(self, next_face)

                    elif utils.is_right_down_cube(down_corners[index][0], down_corners[index][1], self.faces[5],
                                                  self.faces[side.value], self.faces[next_face.value]):
                        if self.faces[next_face.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[positions[index][0]][positions[index][1]] == self.faces[side.value].face_color:
                            f2l.f2l_25(self, next_face, side)
                        elif self.faces[side.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[positions[index - 1][0]][positions[index - 1][1]] == \
                                self.faces[next_face.value].face_color:
                            f2l.f2l_26(self, next_face, side)
                        elif self.faces[side.value].face_matrix[1][2] == self.faces[next_face.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[side.value].face_color:
                            f2l.f2l_38(self, next_face, side)

                    elif self.faces[side.value].face_matrix[2][2] == down_color and \
                            self.faces[next_face.value].face_matrix[2][0] == self.faces[side.value].face_color and \
                            self.faces[5].face_matrix[down_corners[index][0]][down_corners[index][1]] == self.faces[next_face.value].face_color:

                        if self.faces[next_face.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[positions[index][0]][positions[index][1]] == self.faces[side.value].face_color:
                            f2l.f2l_27(self, next_face, side)
                        elif self.faces[side.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[positions[index - 1][0]][positions[index - 1][1]] == \
                                self.faces[next_face.value].face_color:
                            f2l.f2l_29(self, next_face, side)

                        elif self.faces[side.value].face_matrix[1][2] == self.faces[side.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[next_face.value].face_color:
                            f2l.f2l_39(self, next_face)
                        elif self.faces[side.value].face_matrix[1][2] == self.faces[next_face.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[side.value].face_color:
                            f2l.f2l_41(self, next_face, side)
                    elif self.faces[side.value].face_matrix[2][2] == self.faces[next_face.value].face_color and \
                            self.faces[next_face.value].face_matrix[2][0] == down_color and \
                            self.faces[5].face_matrix[down_corners[index][0]][down_corners[index][1]] == self.faces[
                        side.value].face_color:
                        if self.faces[side.value].face_matrix[0][1] == self.faces[side.value].face_color and \
                                self.faces[0].face_matrix[positions[index - 1][0]][positions[index - 1][1]] == \
                                self.faces[next_face.value].face_color:
                            f2l.f2l_28(self, next_face, side)

                        elif self.faces[next_face.value].face_matrix[0][1] == self.faces[next_face.value].face_color and \
                                self.faces[0].face_matrix[positions[index][0]][positions[index][1]] == self.faces[
                            side.value].face_color:
                            f2l.f2l_30(self, next_face)
                        elif self.faces[side.value].face_matrix[1][2] == self.faces[side.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[next_face.value].face_color:
                            f2l.f2l_40(self, next_face)
                        elif self.faces[side.value].face_matrix[1][2] == self.faces[next_face.value].face_color and \
                                self.faces[next_face.value].face_matrix[1][0] == self.faces[side.value].face_color:
                            f2l.f2l_42(self, next_face, prev_face, side)
                if not self.movement_made:
                    self.make_rotation(FaceDirection.UP, True)
                    rotations += 1

            moved = False
            for index, side in enumerate(sides):
                if (self.faces[side.value].face_matrix[1][2] != self.faces[side.value].face_color or
                    self.faces[sides[(index + 1) % 4].value].face_matrix[1][0] !=
                    self.faces[sides[(index + 1) % 4].value].face_color) and \
                        self.faces[sides[index].value].face_matrix[1][2] != up_color and \
                        self.faces[sides[(index + 1) % 4].value].face_matrix[1][0] != up_color:
                    self.bring_third_layer_to_second(sides[index], sides[(index + 1) % 4], True)
                    moved = True
                    break

            if moved:
                continue

            for index, side in enumerate(sides):
                next_face = sides[(index + 1) % 4]
                if not utils.is_placed_correctly(down_corners[index][0], down_corners[index][1], self.faces[5],
                                                 self.faces[side.value], self.faces[next_face.value]):
                    self.permute_corner(next_face)
                    # break

    def solve(self):
        """
        The solving algorithm is an easy sequence of steps
        """
        # print("Bottom : ")
        self.solve_bottom_layer()
        # print("Bottom done")
        # print(f"Finished bottom : {self.moves_number}")
        # print("Top : ")
        self.OLL()
        # print("OLL done")
        # print(f"OLL : {self.moves_number}")
        self.PLL()
        # print("PLL done")
        # print(f"Finished top : {self.moves_number}")
