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
    '''
    A class used to represent a cube face. It holds information such as:
    - a matrix of values, each value coresponding to a color
    - the color that this cube face should be at the ending of the algorithm
    '''
    def __init__(self, facets : list, direction : FaceDirection):
        # Create a matrix from the received list of values. The matrix should be of form 3x3
        self.face_matrix = [[facets[i*3],facets[i*3+1],facets[i*3+2]] for i in range(3)]
        
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
    '''
    A class used to represent a cube in a simple way. 
    It has a list of 6 CubeFace objects, each representing a face of the cube.
    '''

    movements = {
        FaceDirection.UP : [(FaceDirection.LEFT,'L',0,1),(FaceDirection.BACK,'L',0,1),(FaceDirection.RIGHT,'L',0,1),(FaceDirection.FRONT,'L',0,1)],
        FaceDirection.LEFT : [(FaceDirection.DOWN,'C',0,-1),(FaceDirection.BACK,'C',2,-1),(FaceDirection.UP,'C',0,1),(FaceDirection.FRONT,'C',0,1)],
        FaceDirection.FRONT : [(FaceDirection.UP,'L',2,1),(FaceDirection.RIGHT,'C',0,-1),(FaceDirection.DOWN,'L',0,1),(FaceDirection.LEFT,'C',2,-1)],
        FaceDirection.RIGHT : [(FaceDirection.FRONT,'C',2,1),(FaceDirection.UP,'C',2,-1),(FaceDirection.BACK,'C',0,-1),(FaceDirection.DOWN,'C',2,1)],
        FaceDirection.BACK : [(FaceDirection.LEFT,'C',0,1),(FaceDirection.DOWN,'L',2,-1),(FaceDirection.RIGHT,'C',2,1),(FaceDirection.UP,'L',0,-1)],
        FaceDirection.DOWN : [(FaceDirection.FRONT,'L',2,1),(FaceDirection.RIGHT,'L',2,1),(FaceDirection.BACK,'L',2,1),(FaceDirection.LEFT,'L',2,1)]
    }

    revert_movements = {
        FaceDirection.UP : [(FaceDirection.FRONT,'L',0,1),(FaceDirection.RIGHT,'L',0,1),(FaceDirection.BACK,'L',0,1),(FaceDirection.LEFT,'L',0,1)],
        FaceDirection.LEFT : [(FaceDirection.FRONT,'C',0,1),(FaceDirection.UP,'C',0,-1),(FaceDirection.BACK,'C',2,-1),(FaceDirection.DOWN,'C',0,1)],
        FaceDirection.FRONT : [(FaceDirection.LEFT,'C',2,1),(FaceDirection.DOWN,'L',0,-1),(FaceDirection.RIGHT,'C',0,1),(FaceDirection.UP,'L',2,-1)],
        FaceDirection.RIGHT : [(FaceDirection.DOWN,'C',2,-1),(FaceDirection.BACK,'C',0,-1),(FaceDirection.UP,'C',2,1),(FaceDirection.FRONT,'C',2,1)],
        FaceDirection.BACK : [(FaceDirection.UP,'L',0,1),(FaceDirection.RIGHT,'C',2,-1),(FaceDirection.DOWN,'L',2,1),(FaceDirection.LEFT,'C',0,-1)],
        FaceDirection.DOWN : [(FaceDirection.LEFT,'L',2,1),(FaceDirection.BACK,'L',2,1),(FaceDirection.RIGHT,'L',2,1),(FaceDirection.FRONT,'L',2,1)] 
    }

    def __init__(self, configuration : list):
        if len(configuration) != 54:
            raise utils.InvalidCubeConfiguration("Invalid length")

        for color in Color:
            if configuration.count(color) < 9:
                raise utils.InvalidCubeConfiguration("At least one color does not occur for exactly 9 times")

        self.face_length = 9
        self.faces = [CubeFace(configuration[direction.value*self.face_length:(direction.value+1)*self.face_length],direction) 
                        for direction in FaceDirection]

        if not utils.validate_cube_configuration(self):
            raise utils.InvalidCubeConfiguration("One or more facets might be twisted")
    
    def make_rotation(self, face : FaceDirection, clockwise : bool):
        '''
        Receive a chosen face and rotate it clockwise or counter clockwise.
        '''
        sign = 1
        if not clockwise:
            sign = -1

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
            previous = (i-1)%len(moves)
            #TODO : add optimisation : some operations might be repeated?

            to_paste = list()

            if moves[previous][1] == 'L':
                to_paste = self.faces[moves[previous][0].value].face_matrix[moves[previous][2]]
            else:
                to_paste = [list(column) for column in zip(*self.faces[moves[previous][0].value].face_matrix)][moves[previous][2]]
            
            if moves[previous][3] == -1:
                to_paste = list(reversed(to_paste))

            if moves[i][1] == 'L':
                faces_copy[moves[i][0].value].face_matrix[moves[i][2]] = to_paste
            else:
                for j in range(len(to_paste)):
                    faces_copy[moves[i][0].value].face_matrix[j][moves[i][2]] = to_paste[j]

        self.faces = faces_copy[:]


def main():
    try:
        rubik_cube= RubikCube([
            Color.ORANGE, Color.BLUE, Color.WHITE, Color.YELLOW, Color.WHITE, Color.WHITE, Color.GREEN, Color.RED, Color.GREEN,
            Color.YELLOW, Color.ORANGE, Color.ORANGE, Color.GREEN, Color.RED, Color.RED, Color.BLUE, Color.RED, Color.WHITE,
            Color.YELLOW, Color.YELLOW, Color.WHITE, Color.WHITE, Color.BLUE, Color.ORANGE, Color.RED, Color.WHITE, Color.BLUE,
            Color.ORANGE, Color.BLUE, Color.BLUE, Color.BLUE, Color.ORANGE, Color.YELLOW, Color.YELLOW, Color.WHITE, Color.YELLOW,
            Color.ORANGE, Color.YELLOW, Color.BLUE, Color.GREEN, Color.GREEN, Color.RED, Color.GREEN, Color.GREEN, Color.WHITE,
            Color.GREEN, Color.GREEN, Color.RED, Color.BLUE, Color.YELLOW, Color.ORANGE, Color.RED, Color.ORANGE, Color.RED
        ])
    except utils.InvalidCubeConfiguration as cube_exception:
        print(cube_exception)

    rubik_cube.make_rotation(FaceDirection.RIGHT, False)

    for face in rubik_cube.faces:
        for row in face.face_matrix:
            print(row)
        print("----------")


if __name__ == "__main__":
    main()


