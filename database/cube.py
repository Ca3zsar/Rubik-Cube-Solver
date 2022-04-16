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
        #Rotate the up face
        first_half = np.int32(self.faces[0] >> 32)
        rotated = ror(first_half, 8, 32)

        #Change the first layer of the right face
        left_half = np.int32(self.faces[0] & 0xFFFFFFFF)
        left_first_row = np.int32(left_half >> 20)

        front_half = self.faces[1] >> 32
        front_first_row = front_half >> 20
        left_half = (left_half & 0xFFFFF) | (front_first_row << 20)

        right_half = self.faces[1] & 0xFFFFFFFF
        right_first_row = np.int32(right_half >> 20)
        front_half = (front_half & 0xFFFFF) | (right_first_row << 20)

        back_half = self.faces[2] >> 32
        back_first_row = back_half >> 20
        right_half = (right_half & 0xFFFFF) | (back_first_row << 20)
        back_half = (back_half & 0xFFFFF) | (left_first_row << 20)

        self.faces[0] = left_half | (rotated << 32)
        self.faces[1] = right_half | (front_half << 32)
        self.faces[2] = (self.faces[2] & 0xFFFFFFFF) | (back_half << 32)

    def up_rotate_counter(self):
        #Rotate the up face
        first_half = np.int32(self.faces[0] >> 32)
        rotated = rol(first_half, 8, 32)

        left_half = np.int32(self.faces[0] & 0xFFFFFFFF)
        left_first_row = np.int32(left_half >> 20)

        back_half = self.faces[2] >> 32
        back_first_row = back_half >> 20
        left_half = (left_half & 0xFFFFF) | (back_first_row << 20)

        right_half = self.faces[1] & 0xFFFFFFFF
        right_first_row = np.int32(right_half >> 20)
        back_half = (back_half & 0xFFFFF) | (right_first_row << 20)

        front_half = self.faces[1] >> 32
        front_first_row = front_half >> 20
        right_half = (right_half & 0xFFFFF) | (front_first_row << 20)

        front_half = (front_half & 0xFFFFF) | (left_first_row << 20)

        self.faces[0] = left_half | (rotated << 32)
        self.faces[1] = right_half | (front_half << 32)
        self.faces[2] = (self.faces[2] & 0xFFFFFFFF) | (back_half << 32)

        self.faces[0] = (self.faces[0] & 0xFFFFFFFF) | (rotated << 32)

        #Change the first layer of the right face