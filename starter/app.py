from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

DIFFICULTY_CLUES = {
    'easy': 45,
    'medium': 35,
    'hard': 27
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty')
    if difficulty is not None:
        difficulty = difficulty.lower()
        if difficulty not in DIFFICULTY_CLUES:
            return jsonify({'error': f'Unsupported difficulty: {difficulty}'}), 400
        clues = DIFFICULTY_CLUES[difficulty]
    else:
        clues = int(request.args.get('clues', 35))
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

@app.route('/hint', methods=['POST'])
def hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    board = data.get('board') if isinstance(data, dict) else None
    if not _is_valid_board_payload(board):
        return jsonify({'error': 'Board must be a 9x9 grid of values from 0 to 9'}), 400

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] == sudoku_logic.EMPTY and board[row][col] == sudoku_logic.EMPTY:
                return jsonify({
                    'row': row,
                    'col': col,
                    'value': solution[row][col]
                })

    return jsonify({'error': 'No empty cells available for a hint'}), 409

def _is_valid_board_payload(board):
    if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
        return False
    return all(
        isinstance(row, list)
        and len(row) == sudoku_logic.SIZE
        and all(isinstance(value, int) and 0 <= value <= sudoku_logic.SIZE for value in row)
        for row in board
    )

if __name__ == '__main__':
    app.run(debug=True)