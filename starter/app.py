from flask import Flask, render_template, jsonify, request
import sudoku_logic
from services.game_service import find_hint, find_incorrect_cells
from services.validation_service import validate_board, validate_difficulty

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
        try:
            difficulty = validate_difficulty(difficulty, DIFFICULTY_CLUES)
        except ValueError as error:
            return jsonify({'error': str(error)}), 400
        clues = DIFFICULTY_CLUES[difficulty]
    else:
        clues = int(request.args.get('clues', 35))
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    board = data.get('board') if isinstance(data, dict) else None
    try:
        validate_board(board)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    return jsonify({'incorrect': find_incorrect_cells(board, solution)})

@app.route('/hint', methods=['POST'])
def hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    board = data.get('board') if isinstance(data, dict) else None
    try:
        validate_board(board)
        return jsonify(find_hint(puzzle, solution, board))
    except ValueError as error:
        status = 409 if str(error) == 'No empty cells available for a hint' else 400
        return jsonify({'error': str(error)}), status

if __name__ == '__main__':
    app.run(debug=True)