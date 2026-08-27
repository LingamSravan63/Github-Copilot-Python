"""Validation helpers shared by Flask routes and game services."""

import sudoku_logic

BOARD_ERROR = 'Board must be a 9x9 grid of values from 0 to 9'


def validate_board(board):
    """Return a valid 9x9 board or raise ValueError with a user-facing error."""
    if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
        raise ValueError(BOARD_ERROR)

    valid = all(
        isinstance(row, list)
        and len(row) == sudoku_logic.SIZE
        and all(
            isinstance(value, int) and 0 <= value <= sudoku_logic.SIZE
            for value in row
        )
        for row in board
    )
    if not valid:
        raise ValueError(BOARD_ERROR)
    return board


def validate_difficulty(difficulty, supported_difficulties):
    """Return a normalized difficulty or raise ValueError for unsupported input."""
    normalized = difficulty.lower()
    if normalized not in supported_difficulties:
        raise ValueError(f'Unsupported difficulty: {normalized}')
    return normalized
