import numpy as np
from enum import Enum


class Color(Enum):
    RED = 0
    BLUE = 1
    WHITE = 2
    GREEN = 3
    YELLOW = 4
    ORANGE = 5


order = [0, 1, 2, 5, 8, 7, 6, 3]


def ror(n, rotations, width):
    """
    Rotate a number n of width bits to the right by rotations times.
    """
    return (2 ** width - 1) & (n >> rotations | n << (width - rotations))


def rol(n, rotations, width):
    """
    Rotate a number n of width bits to the right by rotations times.
    """
    return (2 ** width - 1) & (n << rotations | n >> (width - rotations))


class CubeCompact:
    '''
    A compact cube representation, where faces are represented by half an integer each, without the corners.
    The colors are : RED, BLUE, WHITE, GREEN, YELLOW, ORANGE
    The face order is : UP, LEFT, FRONT, RIGHT, BACK, DOWN
    '''

    def __init__(self, faces: list[list[Color]]):
        self.faces = np.zeros(3, dtype=np.int64)
        for i in range(len(faces)):
            face_to_update = i // 2
            half_to_update = i % 2
            values = [faces[i][index].value for index in order]
            start = ((half_to_update + 1) % 2) * 32
            end = start + 32

            for index, value in enumerate(values):
                self.faces[face_to_update] |= (value << (end - (index + 1) * 4))

    def up_rotate(self):
        # Rotate the up face
        first_half = np.int32(self.faces[0] >> 32)
        rotated = ror(first_half, 8, 32)

        # Change the first layer of the right face
        left_half = self.faces[0] & 0xFFFFFFFF
        left_first_row = np.uint32(left_half >> 20)

        front_half = self.faces[1] >> 32
        front_first_row = front_half >> 20
        left_half = (left_half & 0xFFFFF) | (front_first_row << 20)

        right_half = self.faces[1] & 0xFFFFFFFF
        right_first_row = np.uint32(right_half >> 20)
        front_half = (front_half & 0xFFFFF) | (right_first_row << 20)

        back_half = self.faces[2] >> 32
        back_first_row = back_half >> 20
        right_half = (right_half & 0xFFFFF) | (back_first_row << 20)
        back_half = (back_half & 0xFFFFF) | (left_first_row << 20)

        self.faces[0] = left_half | (rotated << 32)
        self.faces[1] = right_half | (front_half << 32)
        self.faces[2] = (self.faces[2] & 0xFFFFFFFF) | (back_half << 32)

    def down_rotate(self):
        # Rotate the down face
        down_half = np.int32(self.faces[2] & 0xFFFFFFFF)
        rotated = ror(down_half, 8, 32)

        left_half = self.faces[0] & 0xFFFFFFFF
        left_last_row = np.uint32((left_half & 0xFFF0) >> 4)

        back_half = self.faces[2] >> 32
        back_last_row = (back_half & 0xFFF0) >> 4
        left_half = (left_half & 0xFFFF0000) | (back_last_row << 4) | (left_half & 0xF)

        right_half = self.faces[1] & 0xFFFFFFFF
        right_last_row = (right_half & 0xFFF0) >> 4
        back_half = (back_half & 0xFFFF0000) | (right_last_row << 4) | (back_half & 0xF)

        front_half = self.faces[1] >> 32
        front_last_row = (front_half & 0xFFF0) >> 4
        right_half = (right_half & 0xFFFF0000) | (front_last_row << 4) | (right_half & 0xF)

        front_half = (front_half & 0xFFFF0000) | (left_last_row << 4) | (front_half & 0xF)

        self.faces[0] = left_half | (self.faces[0] & 0x7FFFFFFF00000000)
        self.faces[1] = right_half | (front_half << 32)
        self.faces[2] = rotated | (back_half << 32)

    def left_rotate(self):
        # Rotate the left face
        left_half = np.int32(self.faces[0] & 0xFFFFFFFF)
        rotated = ror(left_half, 8, 32)

        up_half = self.faces[0] >> 32
        up_first_column = up_half & 0xF00000FF

        back_half = self.faces[2] >> 32
        back_third_column = back_half & 0x00FFF000
        up_half = (up_half & 0x0FFFFF00) | rol(back_third_column, 16, 32)

        down_half = self.faces[2] & 0xFFFFFFFF
        down_first_column = down_half & 0xF00000FF
        back_half = (back_half & 0xFF000FFF) | ror(down_first_column, 16, 32)

        front_half = self.faces[1] >> 32
        front_first_column = front_half & 0xF00000FF
        down_half = (down_half & 0x0FFFFF00) | front_first_column

        front_half = (front_half & 0x0FFFFF00) | up_first_column

        self.faces[0] = rotated | (up_half << 32)
        self.faces[1] = (front_half << 32) | (self.faces[1] & 0xFFFFFFFF)
        self.faces[2] = (back_half << 32) | down_half

    def right_rotate(self):
        # Rotate the right face
        right_half = np.int32(self.faces[1] & 0xFFFFFFFF)
        rotated = ror(right_half, 8, 32)

        up_half = self.faces[0] >> 32
        up_third_column = up_half & 0x00FFF000

        front_half = self.faces[1] >> 32
        front_third_column = front_half & 0x00FFF000
        up_half = (up_half & 0xFF000FFF) | front_third_column

        down_half = self.faces[2] & 0xFFFFFFFF
        down_third_column = down_half & 0x00FFF000
        front_half = (front_half & 0xFF000FFF) | down_third_column

        back_half = self.faces[2] >> 32
        back_first_column = back_half & 0xF00000FF
        down_half = (down_half & 0xFF000FFF) | rol(back_first_column, 16, 32)

        back_half = (back_half & 0x0FFFFF00) | rol(up_third_column, 16, 32)

        self.faces[0] = (up_half << 32) | (self.faces[0] & 0xFFFFFFFF)
        self.faces[1] = rotated | (front_half << 32)
        self.faces[2] = (back_half << 32) | (down_half & 0xFFFFFFFF)

    def front_rotate(self):
        front_half = np.int32(self.faces[1] >> 32)
        rotated = ror(front_half, 8, 32)

        up_half = self.faces[0] >> 32
        up_last_row = up_half & 0x0000FFF0

        left_half = self.faces[0] & 0xFFFFFFFF
        left_third_column = left_half & 0x00FFF000
        up_half = (up_half & 0xFFFF000F) | ror(left_third_column, 8, 32)

        down_half = self.faces[2] & 0xFFFFFFFF
        down_first_row = down_half & 0xFFF00000
        left_half = (left_half & 0xFF000FFF) | ror(down_first_row, 8, 32)

        right_half = self.faces[1] & 0xFFFFFFFF
        right_first_column = right_half & 0xF00000FF
        down_half = (down_half & 0x000FFFFF) | ror(right_first_column, 8, 32)

        right_half = (right_half & 0x0FFFFF00) | ror(up_last_row, 8, 32)

        self.faces[0] = (up_half << 32) | left_half
        self.faces[1] = (rotated << 32) | right_half
        self.faces[2] = (self.faces[2] & 0x7FFFFFFF00000000) | down_half

    def back_rotate(self):
        back_half = np.int32(self.faces[2] >> 32)
        rotated = ror(back_half, 8, 32)

        up_half = self.faces[0] >> 32
        up_first_row = up_half & 0xFFF00000

        right_half = self.faces[1] & 0xFFFFFFFF
        right_third_column = right_half & 0x00FFF000
        up_half = (up_half & 0x000FFFFF) | rol(right_third_column, 8, 32)

        down_half = self.faces[2] & 0xFFFFFFFF
        down_last_row = down_half & 0x0000FFF0
        right_half = (right_half & 0xFF000FFF) | rol(down_last_row, 8, 32)

        left_half = self.faces[0] & 0xFFFFFFFF
        left_first_column = left_half & 0xF00000FF
        down_half = (down_half & 0xFFFF000F) | rol(left_first_column, 8, 32)

        left_half = (left_half & 0x0FFFFF00) | rol(up_first_row, 8, 32)

        self.faces[0] = (up_half << 32) | left_half
        self.faces[1] = (self.faces[1] & 0x7FFFFFFF00000000) | right_half
        self.faces[2] = (rotated << 32) | down_half

    def up_rotate_counter(self):
        # Rotate the up face
        first_half = np.int32(self.faces[0] >> 32)
        rotated = rol(first_half, 8, 32)

        left_half = np.int32(self.faces[0] & 0xFFFFFFFF)
        left_first_row = np.int32(left_half >> 20)

        back_half = self.faces[2] >> 32
        back_first_row = back_half >> 20
        left_half = (left_half & 0xFFFFF) | (back_first_row << 20)

        right_half = self.faces[1] & 0xFFFFFFFF
        right_first_row = right_half >> 20
        back_half = (back_half & 0xFFFFF) | (right_first_row << 20)

        front_half = self.faces[1] >> 32
        front_first_row = front_half >> 20
        right_half = (right_half & 0xFFFFF) | (front_first_row << 20)

        front_half = (front_half & 0xFFFFF) | (left_first_row << 20)

        self.faces[0] = left_half | (rotated << 32)
        self.faces[1] = right_half | (front_half << 32)
        self.faces[2] = (self.faces[2] & 0xFFFFFFFF) | (back_half << 32)

    def down_rotate_counter(self):
        # Rotate the down face
        down_half = np.int32(self.faces[2] & 0xFFFFFFFF)
        rotated = rol(down_half, 8, 32)

        left_half = np.int32(self.faces[0] & 0xFFFFFFFF)
        left_last_row = np.int32((left_half & 0xFFF0) >> 4)

        front_half = np.int32(self.faces[1] >> 32)
        front_last_row = np.int32((front_half & 0xFFF0) >> 4)
        left_half = (left_half & 0xFFFF0000) | (front_last_row << 4) | (left_half & 0xF)

        right_half = np.int32(self.faces[1] & 0xFFFFFFFF)
        right_last_row = np.int32((right_half & 0xFFF0) >> 4)
        front_half = (front_half & 0xFFFF0000) | (right_last_row << 4) | (front_half & 0xF)

        back_half = np.int32(self.faces[2] >> 32)
        back_last_row = np.int32((back_half & 0xFFF0) >> 4)
        right_half = (right_half & 0xFFFF0000) | (back_last_row << 4) | (right_half & 0xF)

        back_half = (back_half & 0xFFFF0000) | (left_last_row << 4) | (back_half & 0xF)

        self.faces[0] = left_half | (self.faces[0] & 0x7FFFFFFF00000000)
        self.faces[1] = right_half | (front_half << 32)
        self.faces[2] = rotated | (back_half << 32)

    def left_rotate_counter(self):
        # Rotate the left face
        left_half = np.int32(self.faces[0] & 0xFFFFFFFF)
        rotated = rol(left_half, 8, 32)

        up_half = self.faces[0] >> 32
        up_first_column = up_half & 0xF00000FF

        front_half = self.faces[1] >> 32
        front_first_column = front_half & 0xF00000FF
        up_half = (up_half & 0x0FFFFF00) | front_first_column

        down_half = self.faces[2] & 0xFFFFFFFF
        down_first_column = down_half & 0xF00000FF
        front_half = (front_half & 0x0FFFFF00) | down_first_column

        back_half = self.faces[2] >> 32
        back_third_column = back_half & 0x00FFF000
        down_half = (down_half & 0x0FFFFF00) | rol(back_third_column, 16, 32)

        back_half = (back_half & 0xFF000FFF) | ror(up_first_column, 16, 32)

        self.faces[0] = rotated | (up_half << 32)
        self.faces[1] = (front_half << 32) | (self.faces[1] & 0xFFFFFFFF)
        self.faces[2] = (back_half << 32) | down_half

    def right_rotate_counter(self):
        # Rotate the right face
        right_half = np.int32(self.faces[1] & 0xFFFFFFFF)
        rotated = rol(right_half, 8, 32)

        up_half = self.faces[0] >> 32
        up_third_column = up_half & 0x00FFF000

        back_half = self.faces[2] >> 32
        back_first_column = back_half & 0xF00000FF
        up_half = (up_half & 0xFF000FFF) | rol(back_first_column, 16, 32)

        down_half = self.faces[2] & 0xFFFFFFFF
        down_third_column = down_half & 0x00FFF000
        back_half = (back_half & 0x0FFFFF00) | ror(down_third_column, 16, 32)

        front_half = self.faces[1] >> 32
        front_third_column = front_half & 0x00FFF000
        down_half = (down_half & 0xFF000FFF) | front_third_column

        front_half = (front_half & 0xFFFFF00F) | up_third_column

        self.faces[0] = (up_half << 32) | (self.faces[0] & 0xFFFFFFFF)
        self.faces[1] = rotated | (front_half << 32)
        self.faces[2] = (back_half << 32) | down_half

    def front_rotate_counter(self):
        # Rotate the front face
        front_half = np.int32(self.faces[1] >> 32)
        rotated = rol(front_half, 8, 32)

        up_half = self.faces[0] >> 32
        up_last_row = up_half & 0x0000FFF0

        right_half = self.faces[1] & 0xFFFFFFFF
        right_first_column = right_half & 0xF00000FF
        up_half = (up_half & 0xFFFF000F) | rol(right_first_column, 8, 32)

        down_half = self.faces[2] & 0xFFFFFFFF
        down_first_row = down_half & 0xFFF00000
        right_half = (right_half & 0x0FFFFF00) | rol(down_first_row, 8, 32)

        left_half = self.faces[0] & 0xFFFFFFFF
        left_third_column = left_half & 0x00FFF000
        down_half = (down_half & 0x000FFFFF) | rol(left_third_column, 8, 32)

        left_half = (left_half & 0xFF000FFF) | ror(up_last_row, 8, 32)

        self.faces[0] = (up_half << 32) | left_half
        self.faces[1] = (rotated << 32) | right_half
        self.faces[2] = (self.faces[2] & 0x7FFFFFFF00000000) | down_half

    def back_rotate_counter(self):
        back_half = np.int32(self.faces[2] >> 32)
        rotated = rol(back_half, 8, 32)

        up_half = self.faces[0] >> 32
        up_first_row = up_half & 0xFFF00000

        left_half = self.faces[0] & 0xFFFFFFFF
        left_first_column = left_half & 0xF00000FF
        up_half = (up_half & 0x000FFFFF) | ror(left_first_column, 8, 32)

        down_half = self.faces[2] & 0xFFFFFFFF
        down_last_row = down_half & 0x0000FFF0
        left_half = (left_half & 0x0FFFFF00) | ror(down_last_row, 8, 32)

        right_half = self.faces[1] & 0xFFFFFFFF
        right_third_column = right_half & 0x00FFF000
        down_half = (down_half & 0xFFFF000F) | ror(right_third_column, 8, 32)

        right_half = (right_half & 0xFF000FFF) | ror(up_first_row, 8, 32)

        self.faces[0] = (up_half << 32) | left_half
        self.faces[1] = (self.faces[1] & 0x7FFFFFFF00000000) | right_half
        self.faces[2] = (rotated << 32) | down_half
