import copy

import sudoku_logic


COMPLETED_BOARD = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

UNIQUE_PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def test_count_solutions_returns_one_for_a_completed_board():
    assert sudoku_logic.count_solutions(COMPLETED_BOARD) == 1


def test_count_solutions_returns_one_for_a_known_unique_puzzle():
    assert sudoku_logic.count_solutions(UNIQUE_PUZZLE) == 1


def test_count_solutions_stops_at_two_for_an_underconstrained_board():
    assert sudoku_logic.count_solutions(sudoku_logic.create_empty_board(), limit=2) == 2


def test_count_solutions_returns_zero_for_conflicting_clues():
    invalid_board = copy.deepcopy(COMPLETED_BOARD)
    invalid_board[0][1] = invalid_board[0][0]

    assert sudoku_logic.count_solutions(invalid_board) == 0


def test_count_solutions_does_not_modify_the_input_board():
    board = copy.deepcopy(UNIQUE_PUZZLE)
    original_board = copy.deepcopy(board)

    sudoku_logic.count_solutions(board)

    assert board == original_board