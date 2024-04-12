import numpy as np
import random
import time
import tkinter as tk


def initialize_positions(rows, columns):
    matrix = np.zeros((rows, columns))
    array = [0] * columns
    for i in range(columns):
        array[i] = random.randint(0, rows - 1)
    return matrix, array


def insert_queens(matrix, array):       # insert queens on the board: each queen represents -1 on the board
    rows, columns = matrix.shape
    for i in range(columns):
        matrix[array[i]][i] = -1
    return matrix


def calculate_heuristic(columns, array):
    h = 0
    for i in range(columns - 1):
        for j in range(i+1, columns):
            if array[i] == array[j] or abs(array[i] - array[j]) == j - i:
                h += 1
    return h


def insert_heuristics(matrix, array):
    rows, columns = matrix.shape
    for x in range(columns):
        temp = array.copy()
        for y in range(rows):
            temp[x] = y
            if matrix[y][x] != -1:
                matrix[y][x] = calculate_heuristic(columns, temp)
    return matrix


def find_minimum_heuristics(matrix, array):
    min_h = []
    rows, columns = matrix.shape
    minimum = calculate_heuristic(columns, array)
    temp = [0, 0, 0]    # [row, col, value]
    rows, columns = matrix.shape
    for x in range(columns):
        for y in range(rows):
            temp[0], temp[1], temp[2] = y, x, matrix[y][x]
            if matrix[y][x] != -1:
                if minimum > matrix[y][x]:
                    minimum = matrix[y][x]
                    min_h.clear()
                    min_h.append(temp.copy())
                elif minimum == matrix[y][x]:
                    min_h.append(temp.copy())
    return min_h


def update_position(array, position):
    array[position[1]] = position[0]
    return array


def climbing_hill(matrix, array, random_start_count, total_movements):
    rows, columns = matrix.shape
    current_heuristic = calculate_heuristic(columns, array)
    next_heuristics = -1

    while 0 < current_heuristic != next_heuristics:
        current_heuristic = calculate_heuristic(columns, array)
        matrix = insert_queens(matrix, array)
        matrix = insert_heuristics(matrix, array)
        minimum_heuristic = find_minimum_heuristics(matrix, array)
        if len(minimum_heuristic) == 0 or current_heuristic == 0:
            break
        selected_position = minimum_heuristic[random.randint(0, len(minimum_heuristic) - 1)]
        array = update_position(array, selected_position)
        total_movements += 1
        next_heuristics = calculate_heuristic(columns, array)
    if current_heuristic != 0:
        random_start_count += 1
        m, a = initialize_positions(rows, columns)
        return climbing_hill(m, a, random_start_count, total_movements)
    else:
        return array, random_start_count, total_movements


def show_board(solution):           # implementing the graphics
    root = tk.Tk()
    root.title("8 Queens Solution")
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    for i in range(8):
        for j in range(8):
            color = 'white' if (i + j) % 2 == 0 else 'gray'
            canvas.create_rectangle(j*50, i*50, (j+1)*50, (i+1)*50, fill=color)

    for i in range(8):
        canvas.create_text((i*50+25), (solution[i]*50+25), text='Q', font=('Arial', 24, 'bold'))

    root.mainloop()


def main():
    start_time = time.time()

    m, a = initialize_positions(8, 8)
    print(f'Initial State: {a}')
    rand_start_count = 0
    total_move = 0
    solution, rand_start_count, total_move = climbing_hill(m, a, rand_start_count, total_move)

    end_time = time.time()

    execution_time = end_time - start_time
    formatted_execution_time = "{:.4f}".format(execution_time)

    show_board(solution)

    return {
        "solution_array": solution,
        "random_start_count": rand_start_count,
        "total_movements": total_move,
        "execution_time": formatted_execution_time
    }


if __name__ == "__main__":
    for i in range(3):
        result = main()
        print(f"Solution Array: {result['solution_array']}")
        print(f"Random Start Count: {result['random_start_count']}")
        print(f"Total Movements: {result['total_movements']}")
        print(f"Execution Time: {result['execution_time']} seconds")
        print("-----------------------------------------------------")




