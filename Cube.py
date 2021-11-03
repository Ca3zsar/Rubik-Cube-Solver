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

class RubikCube:
    '''
    A class used to represent a cube in a simple way. 
    It has a list of 6 CubeFace objects, each representing a face of the cube.
    '''

    movements = {
        FaceDirection.UP : [(FaceDirection.LEFT,'L',0),(FaceDirection.BACK,'L',0),(FaceDirection.RIGHT,'L',0),(FaceDirection.FRONT,'L',0)],
        FaceDirection.LEFT : [],
        FaceDirection.FRONT : [],
        FaceDirection.RIGHT : [],
        FaceDirection.BACK : [],
        FaceDirection.DOWN : [(FaceDirection.FRONT,'L',2),(FaceDirection.RIGHT,'L',2),(FaceDirection.BACK,'L',2),(FaceDirection.LEFT,'L',2)]
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
    
    def make_clockwise_rotation(self, face : FaceDirection):
        '''
        Receive a chosen face and rotate it clockwise.
        '''

        # Make a copy of the actual faces
        faces_copy = copy.deepcopy(self.faces)
        
        # Rotate the chosen face clockwise
        faces_copy[face.value].rotate_clockwise()
        
        moves = RubikCube.movements[face]

        # Apply the change to the other faces
        for i in range(len(moves)):
            if moves[i][1] == 'L':
                previous = (i-1)%len(moves)
                faces_copy[moves[i][0].value].face_matrix[moves[i][2]] = self.faces[moves[previous][0].value].face_matrix[moves[previous][2]][:]
            else:
                pass

        self.faces = faces_copy[:]


def main():
    try:
        rubik_cube= RubikCube([
            Color.ORANGE, Color.GREEN, Color.ORANGE, Color.WHITE, Color.WHITE, Color.YELLOW, Color.ORANGE, Color.BLUE, Color.YELLOW,
            Color.BLUE, Color.RED, Color.BLUE, Color.BLUE, Color.RED, Color.ORANGE, Color.YELLOW, Color.ORANGE, Color.GREEN,
            Color.YELLOW, Color.YELLOW, Color.BLUE, Color.GREEN, Color.BLUE, Color.ORANGE, Color.WHITE, Color.RED, Color.WHITE,
            Color.RED, Color.GREEN, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.BLUE, Color.BLUE, Color.ORANGE, Color.GREEN,
            Color.WHITE, Color.WHITE, Color.WHITE, Color.RED, Color.GREEN, Color.WHITE, Color.RED, Color.RED, Color.GREEN,
            Color.RED, Color.YELLOW, Color.RED, Color.BLUE, Color.YELLOW, Color.WHITE, Color.ORANGE, Color.GREEN, Color.YELLOW
        ])
    except utils.InvalidCubeConfiguration as cube_exception:
        print(cube_exception)


if __name__ == "__main__":
    main()


