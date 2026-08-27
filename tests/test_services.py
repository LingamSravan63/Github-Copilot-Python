import pytest

import sudoku_logic
from services.game_service import find_hint, find_incorrect_cells
from services.validation_service import validate_board, validate_difficulty


@pytest.fixture
def completed_board():
    return [
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


def test_validate_board_accepts_a_9x9_board(completed_board):
    assert validate_board(completed_board) == completed_board


@pytest.mark.parametrize('board', [None, [], [[0] * 9 for _ in range(8)]])
def test_validate_board_rejects_invalid_shape(board):
    with pytest.raises(ValueError, match='9x9'):
        validate_board(board)


def test_validate_difficulty_normalizes_supported_value():
    assert validate_difficulty('HaRd', {'hard': 27}) == 'hard'


def test_validate_difficulty_rejects_unsupported_value():
    with pytest.raises(ValueError, match='Unsupported difficulty: expert'):
        validate_difficulty('expert', {'easy': 45})


def test_find_incorrect_cells_reports_only_mismatches(completed_board):
    submitted = [row[:] for row in completed_board]
    submitted[0][0] = sudoku_logic.EMPTY

    assert find_incorrect_cells(submitted, completed_board) == [[0, 0]]


def test_find_hint_skips_original_clues_and_filled_cells(completed_board):
    puzzle = [row[:] for row in completed_board]
    puzzle[0][0] = sudoku_logic.EMPTY
    puzzle[0][1] = sudoku_logic.EMPTY
    submitted = [row[:] for row in puzzle]
    submitted[0][0] = 9

    assert find_hint(puzzle, completed_board, submitted) == {
        'row': 0,
        'col': 1,
        'value': completed_board[0][1],
    }


def test_find_hint_rejects_a_full_board(completed_board):
    with pytest.raises(ValueError, match='No empty cells'):
        find_hint(completed_board, completed_board, completed_board)
