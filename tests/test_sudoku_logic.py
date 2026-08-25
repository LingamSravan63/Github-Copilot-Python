import random

import sudoku_logic


def test_create_empty_board_has_expected_shape_and_values():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(value == sudoku_logic.EMPTY for row in board for value in row)


def test_fill_board_creates_a_complete_valid_board():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True
    assert all(sorted(row) == list(range(1, sudoku_logic.SIZE + 1)) for row in board)
    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            value = board[row][col]
            board[row][col] = sudoku_logic.EMPTY
            assert sudoku_logic.is_safe(board, row, col, value) is True
            board[row][col] = value


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1

    assert sudoku_logic.is_safe(board, 0, 1, 1) is False
    assert sudoku_logic.is_safe(board, 1, 0, 1) is False
    assert sudoku_logic.is_safe(board, 1, 1, 1) is False


def test_generate_puzzle_returns_solution_and_requested_clue_count():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=81)

    assert puzzle == solution
    assert all(value != sudoku_logic.EMPTY for row in puzzle for value in row)


def test_generated_puzzle_has_one_solution_and_agrees_with_solution():
    random.seed(7)

    puzzle, solution = sudoku_logic.generate_puzzle()

    assert sudoku_logic.count_solutions(puzzle, limit=2) == 1
    assert all(
        puzzle[row][col] == sudoku_logic.EMPTY or puzzle[row][col] == solution[row][col]
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
    )


def test_generated_solutions_are_valid_for_representative_seeds():
    for seed in (11, 23):
        random.seed(seed)
        puzzle, solution = sudoku_logic.generate_puzzle()

        assert all(sorted(row) == list(range(1, sudoku_logic.SIZE + 1)) for row in solution)
        assert all(
            len({solution[row][col] for row in range(sudoku_logic.SIZE)}) == sudoku_logic.SIZE
            for col in range(sudoku_logic.SIZE)
        )
        assert all(
            len({
                solution[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
            }) == sudoku_logic.SIZE
            for start_row in range(0, sudoku_logic.SIZE, 3)
            for start_col in range(0, sudoku_logic.SIZE, 3)
        )
        assert sudoku_logic.count_solutions(puzzle, limit=2) == 1