import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_puzzle(grid, attempts):
    clear_screen()
    print("Simultaneous Sudoku Solver!")
    
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("------+-------+------ ")
        
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            
            if grid[i][j] != 0:
                print(grid[i][j], end=" ")
            elif (i, j) in attempts:
                print(f"\033[91m{attempts[(i,j)]}\033[0m", end=" ")
            else:
                print(".", end=" ")
        print()
    time.sleep(0.2)

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

def solve_sudoku(grid):
    empty_cells = [(i, j) for i in range(9) for j in range(9) if grid[i][j] == 0]
    
    if not empty_cells:
        return True
    
    row, col = min(empty_cells, key=lambda x: len([n for n in range(1,10) if is_valid(grid, x[0], x[1], n)]))
    
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            attempts = {}
            for (i,j) in empty_cells:
                if (i,j) == (row,col):
                    attempts[(i,j)] = num
                else:
                    for n in range(1,10):
                        if is_valid(grid, i, j, n):
                            attempts[(i,j)] = n
                            break
            
            print_puzzle(grid, attempts)
            
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0
    
    return False

time.sleep(2)

if __name__ == "__main__":
    from puzzles import solvable, unsolvable
    
    print("1. Solve valid puzzle")
    print("2. Try unsolvable puzzle")
    choice = input("Select (1/2): ")
    
    puzzle = solvable if choice == "1" else unsolvable
    print("\nStarting solver...")
    time.sleep(1)
    
    if solve_sudoku(puzzle):
        clear_screen()
        print("Solution found:")
        print_puzzle(puzzle, {})
    else:
        print("\nNo solution exists - invalid puzzle!")