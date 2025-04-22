import os
import time
from datetime import datetime
from puzzles import solvable, unsolvable

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_puzzle(grid, attempts, start_time, steps, highlight=None):
    clear_screen()
    print("🧸✨ Simultaneous Sudoku Solver ✨🧸")
    print(f"⏱️ Time: {time.time() - start_time:.2f}s | 🔄 Steps: {steps}")
    
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("------+-------+------ ")
        
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            
            if highlight and (i, j) == highlight:
                print(f"\033[92m{grid[i][j]}\033[0m", end=" ")
            elif grid[i][j] != 0:
                print(grid[i][j], end=" ")
            elif (i, j) in attempts:
                print(f"\033[91m{attempts[(i,j)]}\033[0m", end=" ")
            else:
                print(".", end=" ")
        print()
    time.sleep(0.1)

def is_valid(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False

    for x in range(9):
        if grid[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    
    return True

def find_empty_cell(grid):
    min_options = 10
    best_cell = None
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                options = [n for n in range(1,10) if is_valid(grid, i, j, n)]
                if len(options) < min_options:
                    min_options = len(options)
                    best_cell = (i, j)
                    if min_options == 1:
                        return best_cell
    return best_cell

def solve_sudoku(grid, start_time):
    steps = 0
    empty_cell = find_empty_cell(grid)
    
    if not empty_cell:
        return True, steps
    
    row, col = empty_cell
    
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            attempts = {}
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        for n in range(1,10):
                            if is_valid(grid, i, j, n):
                                attempts[(i,j)] = n
                                break
            
            steps += 1
            print_puzzle(grid, attempts, start_time, steps, highlight=(row, col))
            
            grid[row][col] = num
            solved, substeps = solve_sudoku(grid, start_time)
            steps += substeps
            if solved:
                return True, steps
            grid[row][col] = 0
    
    return False, steps

if __name__ == "__main__":
    
    print("1. Solve valid puzzle")
    print("2. Try unsolvable puzzle")
    choice = input("Select (1/2): ")
    
    puzzle = [row[:] for row in (solvable if choice == "1" else unsolvable)]
    print("\nStarting solver...")
    time.sleep(1)
    
    start_time = time.time()
    solved, steps = solve_sudoku(puzzle, start_time)
    time_taken = time.time() - start_time
    
    if solved:
        clear_screen()
        print("🎉 Solution found! 🎉")
        print(f"⏱️ Time: {time_taken:.2f}s | 🔄 Steps: {steps}")
        print_puzzle(puzzle, {}, start_time, steps)
    else:
        print("\n❌ No solution exists - invalid puzzle!")
        print(f"⏱️ Time: {time_taken:.2f}s | 🔄 Steps: {steps}")

    print("\nThanks for using the Sudoku Solver! 🧸")