import random
from time import perf_counter

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


class CubeState:
    def __init__(self, state, route=None):
        self.state = state
        self.route = route or []

    def id_(self, phase):
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
        newstate = self.state[:]
        counter = False
        if turns == 3:
            turns = 1
            counter = True
        for turn in range(turns):
            oldstate = newstate[:]
            for i in range(8):
                isCorner = int(i > 3)
                target = affected_cubies[face][i] + isCorner * 12
                if not counter:
                    killer = affected_cubies[face][(i - 3) if (i & 3) == 3 else i + 1] + isCorner * 12
                else:
                    killer = affected_cubies[face][(i + 3) if (i & 3) == 0 else i - 1] + isCorner * 12
                # print(target, killer)
                orientationDelta = int(1 < face < 4) if i < 4 else (0 if face < 2 else 2 - (i & 1))
                newstate[target] = oldstate[killer]
                newstate[target + 20] = oldstate[killer + 20] + orientationDelta
                if turn == turns - 1:
                    newstate[target + 20] %= 2 + isCorner
        return CubeState(newstate, self.route + [move])


def test(test_state=None, debug=False):
    goal_state = CubeState(list(range(20)) + 20 * [0])
    if test_state:
        state = CubeState(test_state.permutation)
        # print(test_state)
    else:
        state = CubeState(goal_state.state[:])
        moves = [random.randint(0, 17) for _ in range(30)]
        # print(' '.join([move_str(move) for move in moves]) + '\n')

        for move in moves:
            state = state.apply_move(move)

    state.route = []

    for phase in range(4):
        current_id, goal_id = state.id_(phase), goal_state.id_(phase)
        states = [state]
        state_ids = {current_id}
        if current_id != goal_id:
            phase_ok = False
            while not phase_ok:
                next_states = []
                possible_variants = []
                for cur_state in states:
                    for move in phase_moves[phase]:
                        if cur_state.route and move // 3 == cur_state.route[-1] // 3:
                            continue

                        if len(cur_state.route) >= 2 and cur_state.route[-1] // 6 == cur_state.route[-2] // 6 and move // 3 == cur_state.route[-2] // 3:
                            continue

                        next_state = cur_state.apply_move(move)
                        next_id = next_state.id_(phase)
                        if next_id == goal_id:
                            possible_variants.append(next_state)

                            phase_ok = True
                        if next_id not in state_ids:
                            state_ids.add(next_id)
                            next_states.append(next_state)

                if possible_variants:
                    found = False
                    for cur_state in possible_variants:
                        if cur_state.state == goal_state.state:
                            state = cur_state
                            found = True
                            break
                    if not found:
                        state = random.choice(possible_variants)

                states = next_states
    # return ' '.join([move_str(m) for m in state.route]) + ' (%d moves)' % len(state.route)
    return state.route


if __name__ == "__main__":
    test()