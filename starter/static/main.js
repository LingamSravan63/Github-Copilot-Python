// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const TOP_SCORES_KEY = 'sudoku-top-scores';
const THEME_KEY = 'sudoku-theme';
let puzzle = [];
let hintsUsed = 0;
let timerInterval = null;
let elapsedSeconds = 0;
let gameState = 'idle';
let scoreSavedForGame = false;

function formatElapsedTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function updateTimerDisplay() {
  const timer = document.getElementById('timer');
  if (timer) {
    timer.innerText = `Time: ${formatElapsedTime(elapsedSeconds)}`;
  }
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function startTimer() {
  stopTimer();
  timerInterval = setInterval(() => {
    if (gameState !== 'active') {
      return;
    }
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function resetTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
}

function normalizePlayerName(name) {
  const normalized = String(name || '').trim() || 'Player';
  return normalized.slice(0, 20);
}

function loadTopScores() {
  try {
    const raw = localStorage.getItem(TOP_SCORES_KEY);
    if (!raw) {
      return [];
    }

    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed.filter((entry) => {
      if (!entry || typeof entry !== 'object') {
        return false;
      }
      return typeof entry.name === 'string'
        && Number.isFinite(entry.elapsedSeconds)
        && typeof entry.difficulty === 'string'
        && Number.isFinite(entry.hintsUsed);
    });
  } catch (error) {
    return [];
  }
}

function saveTopScores(scores) {
  try {
    localStorage.setItem(TOP_SCORES_KEY, JSON.stringify(scores));
  } catch (error) {
    // Ignore storage failures quietly.
  }
}

function addScoreEntry(score) {
  const scores = loadTopScores();
  scores.push(score);
  scores.sort((a, b) => {
    if (a.elapsedSeconds !== b.elapsedSeconds) {
      return a.elapsedSeconds - b.elapsedSeconds;
    }
    return a.hintsUsed - b.hintsUsed;
  });
  saveTopScores(scores.slice(0, 10));
  renderTopScores();
}

function loadTheme() {
  try {
    const savedTheme = localStorage.getItem(THEME_KEY);
    if (savedTheme === 'dark') {
      return 'dark';
    }
  } catch (error) {
    // Ignore storage errors and fall back to the default light theme.
  }
  return 'light';
}

function applyTheme(theme) {
  const isDark = theme === 'dark';
  document.body.classList.toggle('dark-mode', isDark);

  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    const buttonText = isDark ? 'Light Mode' : 'Dark Mode';
    themeToggle.textContent = buttonText;
    themeToggle.setAttribute('aria-pressed', String(isDark));
  }
}

function toggleTheme() {
  const nextTheme = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
  applyTheme(nextTheme);

  try {
    localStorage.setItem(THEME_KEY, nextTheme);
  } catch (error) {
    // Ignore storage errors and keep the current in-memory theme.
  }
}

function renderTopScores() {
  const tableBody = document.getElementById('top-scores-body');
  if (!tableBody) {
    return;
  }

  const scores = loadTopScores();
  tableBody.innerHTML = '';

  if (scores.length === 0) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 5;
    cell.textContent = 'No scores yet.';
    row.appendChild(cell);
    tableBody.appendChild(row);
    return;
  }

  scores.forEach((score, index) => {
    const row = document.createElement('tr');
    const rank = document.createElement('td');
    const name = document.createElement('td');
    const time = document.createElement('td');
    const difficulty = document.createElement('td');
    const hints = document.createElement('td');

    rank.textContent = String(index + 1);
    name.textContent = score.name;
    time.textContent = formatElapsedTime(score.elapsedSeconds);
    difficulty.textContent = score.difficulty;
    hints.textContent = String(score.hintsUsed);

    row.append(rank, name, time, difficulty, hints);
    tableBody.appendChild(row);
  });
}

function completeGame() {
  if (gameState === 'completed' || scoreSavedForGame) {
    return;
  }

  gameState = 'completed';
  stopTimer();

  const boardDiv = document.getElementById('sudoku-board');
  if (boardDiv) {
    const inputs = boardDiv.getElementsByTagName('input');
    for (let idx = 0; idx < inputs.length; idx++) {
      const inp = inputs[idx];
      if (inp.disabled) {
        continue;
      }
      inp.disabled = true;
      inp.classList.remove('conflict');
      inp.classList.remove('incorrect');
    }
  }

  const msg = document.getElementById('message');
  if (msg) {
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
  }

  const playerNameInput = document.getElementById('player-name');
  const playerName = normalizePlayerName(playerNameInput ? playerNameInput.value : 'Player');
  const difficulty = document.getElementById('difficulty')?.value || 'medium';
  const score = {
    name: playerName,
    elapsedSeconds: elapsedSeconds,
    difficulty,
    hintsUsed,
    savedAt: new Date().toISOString()
  };

  addScoreEntry(score);
  scoreSavedForGame = true;
}

function getVisibleBoard() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = [];
  for (let row = 0; row < SIZE; row++) {
    board[row] = [];
    for (let col = 0; col < SIZE; col++) {
      const value = inputs[row * SIZE + col].value;
      board[row][col] = value ? parseInt(value, 10) : 0;
    }
  }
  return board;
}

function validateBoard() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getVisibleBoard();
  const conflictingCells = new Set();

  function markDuplicates(cells) {
    const seen = new Map();
    for (const [row, col] of cells) {
      const value = board[row][col];
      if (value === 0) continue;
      if (seen.has(value)) {
        conflictingCells.add(row * SIZE + col);
        conflictingCells.add(seen.get(value));
      } else {
        seen.set(value, row * SIZE + col);
      }
    }
  }

  for (let row = 0; row < SIZE; row++) {
    markDuplicates(Array.from({length: SIZE}, (_, col) => [row, col]));
  }
  for (let col = 0; col < SIZE; col++) {
    markDuplicates(Array.from({length: SIZE}, (_, row) => [row, col]));
  }
  for (let boxRow = 0; boxRow < SIZE; boxRow += 3) {
    for (let boxCol = 0; boxCol < SIZE; boxCol += 3) {
      const cells = [];
      for (let row = boxRow; row < boxRow + 3; row++) {
        for (let col = boxCol; col < boxCol + 3; col++) {
          cells.push([row, col]);
        }
      }
      markDuplicates(cells);
    }
  }

  for (let idx = 0; idx < inputs.length; idx++) {
    const input = inputs[idx];
    if (!input.disabled) {
      input.classList.toggle('conflict', conflictingCells.has(idx));
    }
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let row = 0; row < SIZE; row++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let col = 0; col < SIZE; col++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = row;
      input.dataset.col = col;
      const boxIndex = Math.floor(row / 3) * 3 + Math.floor(col / 3);
      input.classList.add(boxIndex % 2 === 0 ? 'box-a' : 'box-b');
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        validateBoard();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  hintsUsed = 0;
  scoreSavedForGame = false;
  gameState = 'active';
  resetTimer();
  startTimer();
  document.getElementById('hint-count').innerText = `Hints: ${hintsUsed}`;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
      inp.classList.remove('conflict');
      inp.classList.remove('incorrect');
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  document.getElementById('message').style.color = '#d32f2f';
}

async function hint() {
  if (gameState === 'completed') {
    return;
  }
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board: getVisibleBoard()})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.innerText = data.error;
    return;
  }

  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const input = inputs[data.row * SIZE + data.col];
  if (!input || input.disabled || input.value) {
    msg.innerText = 'The selected cell is no longer available for a hint.';
    return;
  }

  input.value = data.value;
  input.disabled = true;
  input.classList.add('hinted');
  hintsUsed += 1;
  document.getElementById('hint-count').innerText = `Hints: ${hintsUsed}`;
  validateBoard();
}

async function checkSolution() {
  if (gameState === 'completed') {
    return;
  }

  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('incorrect');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0) {
    completeGame();
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  const savedTheme = loadTheme();
  applyTheme(savedTheme);
  renderTopScores();
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', hint);
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  // initialize
  newGame();
});