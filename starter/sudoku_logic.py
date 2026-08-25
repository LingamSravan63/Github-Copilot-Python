import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def count_solutions(board, limit=2):
    working_board = deep_copy(board)
    if limit <= 0 or not _is_valid_board(working_board):
        return 0

    def count_from_next_empty():
        for row in range(SIZE):
            for col in range(SIZE):
                if working_board[row][col] == EMPTY:
                    solution_count = 0
                    for candidate in range(1, SIZE + 1):
                        if is_safe(working_board, row, col, candidate):
                            working_board[row][col] = candidate
                            solution_count += count_from_next_empty()
                            working_board[row][col] = EMPTY
                            if solution_count >= limit:
                                return solution_count
                    return solution_count
        return 1

    return count_from_next_empty()

def _is_valid_board(board):
    if len(board) != SIZE or any(len(row) != SIZE for row in board):
        return False

    for row in board:
        if any(value not in range(EMPTY, SIZE + 1) for value in row):
            return False

    for row in range(SIZE):
        values = [value for value in board[row] if value != EMPTY]
        if len(values) != len(set(values)):
            return False

    for col in range(SIZE):
        values = [board[row][col] for row in range(SIZE) if board[row][col] != EMPTY]
        if len(values) != len(set(values)):
            return False

    for start_row in range(0, SIZE, 3):
        for start_col in range(0, SIZE, 3):
            values = [
                board[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
                if board[row][col] != EMPTY
            ]
            if len(values) != len(set(values)):
                return False

    return True

def remove_cells(board, clues):
    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(positions)

    for row, col in positions:
        if sum(value != EMPTY for current_row in board for value in current_row) <= clues:
            break

        original_value = board[row][col]
        if original_value == EMPTY:
            continue

        board[row][col] = EMPTY
        if count_solutions(board, limit=2) != 1:
            board[row][col] = original_value

def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
