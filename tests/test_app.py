import copy

import pytest
from unittest.mock import patch

from app import CURRENT, app
import sudoku_logic


@pytest.fixture(autouse=True)
def reset_current_game():
    CURRENT['puzzle'] = None
    CURRENT['solution'] = None
    yield
    CURRENT['puzzle'] = None
    CURRENT['solution'] = None


def test_index_renders_the_game_page():
    client = app.test_client()

    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data


def test_new_game_returns_a_default_35_clue_puzzle():
    client = app.test_client()

    response = client.get('/new')
    puzzle = response.get_json()['puzzle']

    assert response.status_code == 200
    assert len(puzzle) == sudoku_logic.SIZE
    assert sum(value != sudoku_logic.EMPTY for row in puzzle for value in row) == 35
    assert CURRENT['puzzle'] == puzzle
    assert CURRENT['solution'] is not None


@pytest.mark.parametrize('difficulty, expected_clues', [
    ('easy', 45),
    ('medium', 35),
    ('hard', 27),
])
def test_new_game_maps_difficulty_to_clues(difficulty, expected_clues):
    client = app.test_client()

    with patch('app.sudoku_logic.generate_puzzle', return_value=(
        sudoku_logic.create_empty_board(), sudoku_logic.create_empty_board()
    )) as generate_puzzle:
        response = client.get(f'/new?difficulty={difficulty}')

    assert response.status_code == 200
    generate_puzzle.assert_called_once_with(expected_clues)


def test_new_game_defaults_missing_difficulty_to_medium():
    client = app.test_client()

    with patch('app.sudoku_logic.generate_puzzle', return_value=(
        sudoku_logic.create_empty_board(), sudoku_logic.create_empty_board()
    )) as generate_puzzle:
        response = client.get('/new')

    assert response.status_code == 200
    generate_puzzle.assert_called_once_with(35)


def test_new_game_rejects_unsupported_difficulty():
    client = app.test_client()

    response = client.get('/new?difficulty=expert')

    assert response.status_code == 400
    assert response.get_json() == {'error': 'Unsupported difficulty: expert'}


def test_difficulty_takes_precedence_over_legacy_clues_parameter():
    client = app.test_client()

    with patch('app.sudoku_logic.generate_puzzle', return_value=(
        sudoku_logic.create_empty_board(), sudoku_logic.create_empty_board()
    )) as generate_puzzle:
        response = client.get('/new?difficulty=hard&clues=45')

    assert response.status_code == 200
    generate_puzzle.assert_called_once_with(27)


def test_check_returns_no_incorrect_cells_for_the_current_solution():
    client = app.test_client()
    client.get('/new')

    response = client.post('/check', json={'board': copy.deepcopy(CURRENT['solution'])})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_reports_a_changed_cell():
    client = app.test_client()
    client.get('/new')
    board = copy.deepcopy(CURRENT['solution'])
    board[0][0] = sudoku_logic.EMPTY

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert [0, 0] in response.get_json()['incorrect']


def test_check_requires_a_game_in_progress():
    client = app.test_client()

    response = client.post('/check', json={'board': sudoku_logic.create_empty_board()})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}