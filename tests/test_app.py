import copy

import pytest

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