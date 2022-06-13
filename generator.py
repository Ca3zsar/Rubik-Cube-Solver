from cubes.Cube import RubikCube
import random

opposites = {
        'F': 'B',
        'B': 'F',
        'U': 'D',
        'D': 'U',
        'L': 'R',
        'R': 'L',
    }


def generate(moves=30):
    solved_cube = RubikCube()

    last_two_moves = [None, None]
    for i in range(moves):
        if last_two_moves[1] is not None and last_two_moves[0] == opposites[last_two_moves[1]]:
            face_direction = random.choice(list(set(solved_cube.move_dict.keys()) - set(last_two_moves)))
        else:
            face_direction = random.choice(list(solved_cube.move_dict.keys() - {last_two_moves[1]}))

        last_two_moves[0] = last_two_moves[1]
        last_two_moves[1] = face_direction
        direction = "'" if random.randint(0, 1) == 0 else ""
        repeat = '2' if random.randint(0, 1) == 0 and not direction else ''
        solved_cube.complex_rotation(f"{face_direction}{direction}{repeat}")

    faces = []
    for face in solved_cube.faces:
        for row in face.face_matrix:
            faces.extend(row)

    # print(solved_cube)
    return faces


if __name__ == "__main__":
    faces = generate()
    for i in range(6):
        print(faces[i*9:i*9+9])
