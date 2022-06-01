# Consider the corners to be in the following order:
# UFR, URB, UBL, ULF, DRF, DFL, DLB, DBR

# And the edges in the following order:
# UF, UR, UB, UL, DF, DR, DB, DL, FR, FL, BR, BL

# Centers will be received in the following order
faces_strings = ["U", "D", "F", "B", "L", "R"]

edges_ind = ["UF", "UR", "UB", "UL", "DF", "DR", "DB", "DL", "FR", "FL", "BR", "BL"]
corners_ind = ["UFR", "URB", "UBL", "ULF", "DRF", "DFL", "DLB", "DBR"]


class CubeRepresentation:
    def __init__(self, centers, cube):
        self.edges = []
        self.corners = []
        self.generate_cubies(centers)
        self.permutation = [0] * 40

        self.create_permutation(cube.faces)
        # self.path = path if path else []

    def generate_cubies(self, centers):
        order = [2, 5, 3, 4]
        for index in order:
            self.edges.append([centers[0], centers[index]])

        for index in order:
            self.edges.append([centers[1], centers[index]])

        self.edges.append([centers[2], centers[5]])
        self.edges.append([centers[2], centers[4]])
        self.edges.append([centers[3], centers[5]])
        self.edges.append([centers[3], centers[4]])

        for index, value in enumerate(order):
            self.corners.append([centers[0], centers[value], centers[order[(index+1) % 4]]])

        order = [5, 2, 4, 3]
        for index, value in enumerate(order):
            self.corners.append([centers[1], centers[value], centers[order[(index+1) % 4]]])

    def get_edge_index(self, edge):
        try:
            return self.edges.index(edge)
        except ValueError:
            return None

    def get_corner_index(self, corner):
        try:
            return self.corners.index(corner)
        except ValueError:
            return None

    def create_permutation(self, state):
        indices = [(2, 1), (1, 2), (0, 1), (1, 0)]
        faces_indices = [2, 3, 4, 1]

        piece_index = 0
        for index, face_index in zip(indices, faces_indices):
            current_piece = [state[0].face_matrix[index[0]][index[1]], state[face_index].face_matrix[0][1]]
            self.set_piece(current_piece, piece_index, self.get_edge_index)
            piece_index += 1

        indices = [(0, 1), (1, 2), (2, 1), (1, 0)]
        for index, face_index in zip(indices, faces_indices):
            current_piece = [state[5].face_matrix[index[0]][index[1]], state[face_index].face_matrix[2][1]]
            self.set_piece(current_piece, piece_index, self.get_edge_index)
            piece_index += 1

        pieces = [
            [state[2].face_matrix[1][2], state[3].face_matrix[1][0]],
            [state[2].face_matrix[1][0], state[1].face_matrix[1][2]],
            [state[4].face_matrix[1][0], state[3].face_matrix[1][2]],
            [state[4].face_matrix[1][2], state[1].face_matrix[1][0]],
        ]

        for piece in pieces:
            self.set_piece(piece, piece_index, self.get_edge_index)
            piece_index += 1

        # Now the corners
        indices = [(2, 2), (0, 2), (0, 0), (2, 0)]
        for i, (index, face_index) in enumerate(zip(indices, faces_indices)):
            current_piece = [state[0].face_matrix[index[0]][index[1]], state[face_index].face_matrix[0][2], state[faces_indices[(i+1) % 4]].face_matrix[0][0]]
            self.set_piece(current_piece, piece_index, self.get_corner_index)
            piece_index += 1
        #
        faces_indices = [3, 2, 1, 4]
        indices = [(0, 2), (0, 0), (2, 0), (2, 2)]

        for i, (index, face_index) in enumerate(zip(indices, faces_indices)):
            current_piece = [state[5].face_matrix[index[0]][index[1]], state[face_index].face_matrix[2][0], state[faces_indices[(i+1) % 4]].face_matrix[2][2]]
            self.set_piece(current_piece, piece_index, self.get_corner_index)
            piece_index += 1

    def set_piece(self, current_piece, piece_index, callback):
        found = False
        while not found:
            pos = callback(current_piece)
            if pos is not None:
                self.permutation[piece_index] = pos if piece_index < 12 else pos + 12
                found = True
            else:

                current_piece = current_piece[1:] + current_piece[:1]
                self.permutation[piece_index + 20] += 1



