from cubes.elements.CubeElements import FaceDirection
from cubes.Cube import RubikCube
import random


def generate():
    solved_cube = RubikCube()

    moves = random.randint(35, 100)
    for i in range(moves):
        direction = random.choice(list(FaceDirection))
        orientation = random.randint(1, 100) % 2 == 0

        solved_cube.make_rotation(direction, orientation)

    faces = []
    for face in solved_cube.faces:
        for row in face.face_matrix:
            faces.extend(row)

    # print(solved_cube)
    return faces