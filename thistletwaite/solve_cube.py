import collections

face_names = ["U", "D", "F", "B", "L", "R"]
affected_cubies = [[0, 1, 2, 3, 0, 1, 2, 3], [4, 7, 6, 5, 4, 5, 6, 7], [0, 9, 4, 8, 0, 3, 5, 4],
                   [2, 10, 6, 11, 2, 1, 7, 6], [3, 11, 7, 9, 3, 2, 6, 5], [1, 8, 5, 10, 1, 0, 4, 7]]
phase_moves = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
               [0, 1, 2, 3, 4, 5, 7, 10, 12, 13, 14, 15, 16, 17], [0, 1, 2, 3, 4, 5, 7, 10, 13, 16],
               [1, 4, 7, 10, 13, 16]]


# "UF", "UR", "UB", "UL", "DF", "DR", "DB", "DL", "FR", "FL", "BR", "BL",
# "UFR", "URB", "UBL", "ULF", "DRF", "DFL", "DLB", "DBR"

def move_str(move):
    return face_names[move // 3] + {1: '', 2: '2', 3: "'"}[move % 3 + 1]

def inverse_move(move):
    return move + 2 - 2 * (move % 3)

class CubeState:
    def __init__(self, state):
        self.state = state

    def compute_id(self, phase):
        if phase == 0:
            return tuple(self.state[20:32])
        elif phase == 1:
            result = self.state[31:40]
            for e in range(12):
                result[0] |= (self.state[e] // 8) << e
            return tuple(result)
        elif phase == 2:
            result = [0, 0, 0]
            for e in range(12):
                result[0] |= (2 if (self.state[e] > 7) else (self.state[e] & 1)) << (2 * e)
            for c in range(8):
                result[1] |= ((self.state[c + 12] - 12) & 5) << (3 * c)
            for i in range(12, 20):
                for j in range(i + 1, 20):
                    result[2] ^= int(self.state[i] > self.state[j])
            return tuple(result)
        else:
            return tuple(self.state)

    def apply_move(self, move):
        face, turns = move // 3, move % 3 + 1
        new_state = self.state[:]
        counter = False
        if turns == 3:
            turns = 1
            counter = True
        for turn in range(turns):
            oldstate = new_state[:]
            for i in range(8):
                is_corner = int(i > 3)
                affected_cubie = affected_cubies[face][i] + is_corner * 12
                if not counter:
                    substitute = affected_cubies[face][(i - 3) if (i & 3) == 3 else i + 1] + is_corner * 12
                else:
                    substitute = affected_cubies[face][(i + 3) if (i & 3) == 0 else i - 1] + is_corner * 12
                # print(target, substitute)
                orientationDelta = int(1 < face < 4) if i < 4 else (0 if face < 2 else 2 - (i & 1))
                new_state[affected_cubie] = oldstate[substitute]
                new_state[affected_cubie + 20] = oldstate[substitute + 20] + orientationDelta

                if turn == turns - 1:
                    new_state[affected_cubie + 20] %= 2 + is_corner
        return CubeState(new_state)


def test(test_state=None, debug=False):
    goal_state = CubeState(list(range(20)) + 20 * [0])

    if test_state:
        state = CubeState(test_state.permutation)
    else:
        return None
    SOLUTION = []

    for phase in range(4):
        current_id, goal_id = state.compute_id(phase), goal_state.compute_id(phase)
        
        if current_id == goal_id:
            continue

        predecessor = {}
        last_move = {}
        direction = {}

        direction[current_id] = 1
        direction[goal_id] = 2

        states = collections.deque()
        states.append(state)
        states.append(goal_state)

        phase_ok = False

        while not phase_ok:
            old_state = states.popleft()
            old_id = old_state.compute_id(phase)
            old_dir = direction.get(old_id)

            for move in phase_moves[phase]:
                if last_move.get(old_id) and last_move.get(old_id) // 3 == move // 3:
                    continue

                next_state = old_state.apply_move(move)
                next_id = next_state.compute_id(phase)
                new_dir = direction.get(next_id, 0)

                if new_dir and new_dir != old_dir:
                    if old_dir > 1:
                        aux = next_id
                        next_id = old_id
                        old_id = aux
                        move = inverse_move(move)
                    
                    moves = [move]
                    while old_id != current_id:
                        moves.insert(0, last_move[old_id])
                        old_id = predecessor[old_id]

                    while next_id != goal_id:
                        moves.append(inverse_move(last_move[next_id]))
                        next_id = predecessor[next_id]
                    
                    for move in moves:
                        SOLUTION.append(move)
                        state = state.apply_move(move)
                    
                    phase_ok = True
                    break

                if not new_dir:
                    states.append(next_state)
                    direction[next_id] = old_dir
                    predecessor[next_id] = old_id
                    last_move[next_id] = move

            if phase_ok:
                break
    
    #process solution
    if debug:
        print(len(SOLUTION))
        print(' '.join(map(str,SOLUTION)))
        print(' '.join(map(move_str,SOLUTION)))

    i = 0
    while i < len(SOLUTION) - 1:
        if SOLUTION[i] // 3 == SOLUTION[i + 1] // 3:
            if SOLUTION[i] == inverse_move(SOLUTION[i + 1]):
                SOLUTION.pop(i)
                SOLUTION.pop(i)
            elif SOLUTION[i] == SOLUTION[i + 1]:
                SOLUTION.pop(i + 1)
                SOLUTION[i] = SOLUTION[i] + 1
            else:
                SOLUTION[i] = inverse_move(SOLUTION[i])
                SOLUTION.pop(i+1)
            i -= 1
        i += 1
                

    if debug:
        print(len(SOLUTION))
        print(' '.join(map(str,SOLUTION)))
        print(' '.join(map(move_str,SOLUTION)))
    return SOLUTION
        


if __name__ == "__main__":
    # fill_phase_3()
    test()
