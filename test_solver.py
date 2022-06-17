from statistics import stdev
import sys
import cubes.Cube as cube
import cubes.elements.CubeElements as els
import generator
import thistletwaite.construct_cube as construct
import thistletwaite.optimsed_solver as optimised
import thistletwaite.solve_cube as solve
from time import perf_counter

moves = ["U", "U2", "U'", "D", "D2", "D'", "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'"]

def main():
    batch = 1000
    cubes = []

    while len(cubes) < batch:
        temp_cube = generator.generate()
        if temp_cube not in cubes:
            cubes.append(temp_cube)
    
    functions = [solve.test, optimised.test]

    for k in range(2):
        avg_time = 0
        avg_moves = 0
        solutions_length = []
        all_correct = True

        for i in range(batch):
            start = perf_counter()
            rubik = cube.RubikCube(cubes[i])
            centers = [
                rubik.faces[0].face_color,
                rubik.faces[5].face_color,
                rubik.faces[2].face_color,
                rubik.faces[4].face_color,
                rubik.faces[1].face_color,
                rubik.faces[3].face_color,
            ]

            cube_state = construct.CubeRepresentation(centers, rubik)
            solution = functions[k](cube_state, False)

            solution_str = "".join(map(lambda x: moves[x], solution))
            rubik.complex_rotation(solution_str)
            all_correct = all_correct and cube.utils.is_cube_solved(rubik.faces)
            if not all_correct:
                print(f"{i} - {cubes[i]}")
                break
                
            avg_moves += len(solution)
            solutions_length.append(len(solution))

            stop = perf_counter()
            avg_time += stop - start
            # print(f"{i}. {stop - start} ::: {len(solution)}")
        print("---------------")

        print(f"Average time : {avg_time / batch}")
        print(f"Average number of moves : {avg_moves / batch}")
        print(f"Standard deviation : {stdev(solutions_length)}")
        print(f"Maximal length : {max(solutions_length)}")
        print(f"Minimal length : {min(solutions_length)}")

if __name__ == "__main__":
    main()