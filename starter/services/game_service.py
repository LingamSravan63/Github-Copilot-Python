"""Reusable game operations for the Sudoku Flask application."""

import sudoku_logic


def find_incorrect_cells(board, solution):
    """Return row/column pairs whose submitted values differ from solution."""
    return [
        [row, col]
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
        if board[row][col] != solution[row][col]
    ]


def find_hint(puzzle, solution, board):
    """Return one eligible hint, or raise ValueError when no cell is available."""
    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] == sudoku_logic.EMPTY and board[row][col] == sudoku_logic.EMPTY:
                return {'row': row, 'col': col, 'value': solution[row][col]}
    raise ValueError('No empty cells available for a hint')
