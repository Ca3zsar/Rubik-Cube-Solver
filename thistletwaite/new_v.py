import random
from time import perf_counter

face_names = ["U", "D", "F", "B", "L", "R"]
affected_cubies = [[0, 1, 2, 3, 0, 1, 2, 3],
                   [4, 5, 6, 7, 4, 5, 6, 7],
                   [2, 8, 4, 9, 3, 2, 5, 4],
                   [0, 10, 6, 11, 1, 0, 7, 6],
                   [3, 9, 7, 10, 0, 3, 4, 7],
                   [1, 11, 5, 8, 2, 1, 6, 5]]

phase_moves = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
               [1, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
               [1, 4, 7, 10, 12, 13, 14, 15, 16, 17],
               [1, 4, 7, 10, 13, 16]]


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
                result[0] |= (1 if self.state[e] > 7 else self.state[e] & 1) << (2*e)
            return tuple(result)
        elif phase == 2:
            result = [0, 0, 0, 0]
            for e in range(12):
                result[0] |= (0 if self.state[e] in {3, 7, 9, 10} else (2 if self.state[e] in {0, 2, 4, 6} else 1)) << (2 * e)
            result[1] = int({self.state[12], self.state[14], self.state[17], self.state[19]} == {12, 14, 17, 19}) and\
                int({self.state[32], self.state[34], self.state[37], self.state[39]} == {0, 0, 0, 0})
            result[2] = int({self.state[13], self.state[15], self.state[16], self.state[18]} == {13, 15, 16, 18}) and \
                int({self.state[33], self.state[35], self.state[36], self.state[38]} == {0, 0, 0, 0})
            # for c in range(8):
            #     result[1] |= ((self.state[c + 12] - 12) & 5) << (3 * c)
            for i in range(12, 20):
                for j in range(i + 1, 20):
                    result[3] ^= int(self.state[i] > self.state[j])
            return tuple(result)
        else:
            return tuple(self.state)

    def apply_move(self, move):
        face, turns = move // 3, move % 3 + 1
        newstate = self.state[:]
        for turn in range(turns):
            oldstate = newstate[:]
            for i in range(8):
                isCorner = int(i > 3)
                target = affected_cubies[face][i] + isCorner * 12
                killer = affected_cubies[face][(i - 3) if (i & 3) == 3 else i + 1] + isCorner * 12
                # print(target, killer)
                orientationDelta = int(face < 2) if i < 4 else (0 if face > 3 else 2 - (i & 1))
                newstate[target] = oldstate[killer]
                newstate[target + 20] = oldstate[killer + 20] + orientationDelta
                if turn == turns - 1:
                    newstate[target + 20] %= 2 + isCorner
        return CubeState(newstate, self.route + [move])


def main():
    total_time = 0
    for _ in range(10):
        start = perf_counter()
        goal_state = CubeState(list(range(20)) + 20 * [0])
        state = CubeState(goal_state.state[:])
        # state = state.apply_move(0)
        # print(" ".join(move_str(move) for move in state.route))
        # print('*** randomize ***')
        moves = [random.randint(0, 17) for _ in range(10)]
        print(' '.join([move_str(move) for move in moves]) + '\n')
        for move in moves:
            state = state.apply_move(move)
        state.route = []
        # print('*** solve ***')

        for phase in range(4):
            current_id, goal_id = state.id_(phase), goal_state.id_(phase)
            states = [state]
            state_ids = {current_id}
            if current_id != goal_id:
                phase_ok = False
                while not phase_ok:
                    next_states = []
                    for cur_state in states:
                        for move in phase_moves[phase]:
                            if cur_state.route and move // 3 == cur_state.route[-1] // 3:
                                continue

                            if len(cur_state.route) >= 2 and cur_state.route[-1] // 6 == cur_state.route[-2] // 6 and move // 3 == cur_state.route[-2] // 3:
                                continue

                            next_state = cur_state.apply_move(move)
                            next_id = next_state.id_(phase)
                            if next_id == goal_id:
                                print(str(phase) + " ::: " +  ' '.join([move_str(m) for m in next_state.route]) + ' (%d moves)' % len(next_state.route))
                                phase_ok = True
                                state = next_state
                                break
                            if next_id not in state_ids:
                                state_ids.add(next_id)
                                next_states.append(next_state)
                        if phase_ok:
                            break
                    states = next_states
        stop = perf_counter()

        print(stop-start)
        print("----------------")
        total_time += (stop-start)

    print(total_time/10)

if __name__ == "__main__":
    main()
