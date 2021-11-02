from enum import Enum
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

class RubikCube:
    '''
    A class used to represent a cube in a simple way. 
    It has a list of 6 CubeFace objects, each representing a face of the cube.
    '''

    def __init__(self, configuration : list):
        if len(configuration) != 54:
            raise utils.InvalidCubeConfiguration("The cube configuration supplied is not valid. Invalid length")

        self.face_length = 9
        self.faces = [CubeFace(configuration[direction.value*self.face_length:(direction.value+1)*self.face_length],direction) 
                        for direction in FaceDirection]

        if not utils.validate_cube_configuration(self):
            raise utils.InvalidCubeConfiguration("The cube configuration supplied is not valid")
        

def main():
    try:
        rubik_cube= RubikCube([
            Color.ORANGE, Color.YELLOW, Color.WHITE, Color.BLUE, Color.WHITE, Color.YELLOW, Color.GREEN, Color.WHITE, Color.YELLOW,
            Color.BLUE, Color.ORANGE, Color.WHITE, Color.YELLOW, Color.RED, Color.GREEN, Color.ORANGE, Color.BLUE, Color.RED,
            Color.ORANGE, Color.ORANGE, Color.RED, Color.YELLOW, Color.BLUE, Color.WHITE, Color.BLUE, Color.ORANGE, Color.ORANGE,
            Color.GREEN, Color.RED, Color.GREEN, Color.GREEN, Color.ORANGE, Color.RED, Color.GREEN, Color.RED, Color.RED,
            Color.RED, Color.ORANGE, Color.WHITE, Color.BLUE, Color.GREEN, Color.BLUE, Color.WHITE, Color.WHITE, Color.BLUE,
            Color.YELLOW, Color.GREEN, Color.YELLOW, Color.WHITE, Color.YELLOW, Color.GREEN, Color.YELLOW, Color.RED, Color.BLUE
        ])
    
    except utils.InvalidCubeConfiguration as cube_exception:
        print(cube_exception)


if __name__ == "__main__":
    main()


