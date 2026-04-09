'use strict';

// ─────────────────────────────────────────
//  Constants
// ─────────────────────────────────────────

const EMPTY = 0, X = 1, O = -1, DRAW = 2;

const WINNING_COMBOS = [
  [0,1,2],[3,4,5],[6,7,8],
  [0,3,6],[1,4,7],[2,5,8],
  [0,4,8],[2,4,6],
];

const LEVEL_DEPTH = { random: 0, easy: 0, medium: 2, hard: 3, expert: 4 };

// ─────────────────────────────────────────
//  Game logic
// ─────────────────────────────────────────

class MegaTicTacToe {
  constructor() { this.reset(); }

  reset() {
    this.cells        = Array.from({length: 9}, () => new Array(9).fill(EMPTY));
    this.miniWinners  = new Array(9).fill(EMPTY);
    this.currentPlayer = X;
    this.activeBoard  = -1;   // -1 = any available board
    this.gameWinner   = EMPTY;
    this.gameOver     = false;
    this.moveHistory  = [];
  }

  boardAvailable(idx) {
    return this.miniWinners[idx] === EMPTY &&
           this.cells[idx].some(c => c === EMPTY);
  }

  getValidMoves() {
    if (this.gameOver) return [];
    const boards = this.activeBoard === -1
      ? Array.from({length: 9}, (_,i) => i).filter(i => this.boardAvailable(i))
      : [this.activeBoard];
    const moves = [];
    for (const b of boards)
      for (let c = 0; c < 9; c++)
        if (this.cells[b][c] === EMPTY) moves.push([b, c]);
    return moves;
  }

  makeMove(mb, cell) {
    if (!this.getValidMoves().some(([b,c]) => b === mb && c === cell)) return false;

    this.cells[mb][cell] = this.currentPlayer;
    this.moveHistory.push([mb, cell, this.currentPlayer]);
    this.miniWinners[mb] = this._checkMiniWinner(mb);
    this.gameWinner      = this._checkGameWinner();
    this.activeBoard     = this.boardAvailable(cell) ? cell : -1;
    this.currentPlayer   = this.currentPlayer === X ? O : X;

    if (this.gameWinner !== EMPTY) {
      this.gameOver = true;
    } else if (this.getValidMoves().length === 0) {
      this.gameOver   = true;
      this.gameWinner = DRAW;
    }
    return true;
  }

  _checkMiniWinner(idx) {
    const c = this.cells[idx];
    for (const [a,b,cc] of WINNING_COMBOS)
      if (c[a] !== EMPTY && c[a] === c[b] && c[b] === c[cc]) return c[a];
    return c.every(v => v !== EMPTY) ? DRAW : EMPTY;
  }

  _checkGameWinner() {
    const w = this.miniWinners;
    for (const [a,b,c] of WINNING_COMBOS)
      if (w[a] !== EMPTY && w[a] !== DRAW && w[a] === w[b] && w[b] === w[c]) return w[a];
    return EMPTY;
  }

  copy() {
    const g = Object.create(MegaTicTacToe.prototype);
    g.cells         = this.cells.map(r => [...r]);
    g.miniWinners   = [...this.miniWinners];
    g.currentPlayer = this.currentPlayer;
    g.activeBoard   = this.activeBoard;
    g.gameWinner    = this.gameWinner;
    g.gameOver      = this.gameOver;
    g.moveHistory   = [...this.moveHistory];
    return g;
  }
}

// ─────────────────────────────────────────
//  AI player
// ─────────────────────────────────────────

class AIPlayer {
  constructor(level = 'medium') { this.level = level; }

  getMove(game) {
    const moves = game.getValidMoves();
    if (!moves.length) return null;
    if (this.level === 'random') return _pick(moves);
    if (this.level === 'easy')   return this._easyMove(game, moves);
    return this._minimaxBest(game, LEVEL_DEPTH[this.level] ?? 2);
  }

  // ── Heuristic (easy) ──────────────────

  _easyMove(game, moves) {
    const player   = game.currentPlayer;
    const opponent = player === X ? O : X;

    for (const [mb,c] of moves) {            // win the game
      const g = game.copy(); g.makeMove(mb,c);
      if (g.gameWinner === player) return [mb,c];
    }
    for (const [mb,c] of moves)              // win a mini-board
      if (_wouldWinMini(game.cells[mb], c, player)) return [mb,c];
    for (const [mb,c] of moves)              // block opponent mini-board win
      if (_wouldWinMini(game.cells[mb], c, opponent)) return [mb,c];

    const centers = moves.filter(([,c]) => c === 4);
    return centers.length ? _pick(centers) : _pick(moves);
  }

  // ── Minimax + alpha-beta ──────────────

  _minimaxBest(game, depth) {
    const player = game.currentPlayer;
    let bestScore = -Infinity, bestMoves = [];

    const moves = this._orderMoves(game, _shuffle(game.getValidMoves()), player);
    for (const [mb,c] of moves) {
      const g = game.copy(); g.makeMove(mb,c);
      const score = this._minimax(g, depth-1, -Infinity, Infinity, false, player);
      if (score > bestScore)      { bestScore = score; bestMoves = [[mb,c]]; }
      else if (score === bestScore) bestMoves.push([mb,c]);
    }
    return _pick(bestMoves) ?? moves[0];
  }

  _minimax(game, depth, alpha, beta, maximizing, player) {
    const opponent = player === X ? O : X;
    if (game.gameOver) {
      if (game.gameWinner === player)   return  1000 + depth;
      if (game.gameWinner === opponent) return -1000 - depth;
      return 0;
    }
    if (depth === 0) return this._evaluate(game, player);

    const moves = game.getValidMoves();
    if (maximizing) {
      let val = -Infinity;
      for (const [mb,c] of moves) {
        const g = game.copy(); g.makeMove(mb,c);
        val   = Math.max(val, this._minimax(g, depth-1, alpha, beta, false, player));
        alpha = Math.max(alpha, val);
        if (beta <= alpha) break;
      }
      return val;
    } else {
      let val = Infinity;
      for (const [mb,c] of moves) {
        const g = game.copy(); g.makeMove(mb,c);
        val  = Math.min(val, this._minimax(g, depth-1, alpha, beta, true, player));
        beta = Math.min(beta, val);
        if (beta <= alpha) break;
      }
      return val;
    }
  }

  _evaluate(game, player) {
    const opponent = player === X ? O : X;
    let score = 0;
    for (const w of game.miniWinners) {
      if (w === player) score += 10; else if (w === opponent) score -= 10;
    }
    for (const [a,b,c] of WINNING_COMBOS) {
      const vals = [game.miniWinners[a], game.miniWinners[b], game.miniWinners[c]];
      const p = vals.filter(v => v === player).length;
      const o = vals.filter(v => v === opponent).length;
      if (o === 0 && p) score += p * 2;
      else if (p === 0 && o) score -= o * 2;
    }
    if (game.miniWinners[4] === player)   score += 4;
    if (game.miniWinners[4] === opponent) score -= 4;
    for (const corner of [0,2,6,8]) {
      if (game.miniWinners[corner] === player)   score += 2;
      if (game.miniWinners[corner] === opponent) score -= 2;
    }
    return score;
  }

  _orderMoves(game, moves, player) {
    const opponent = player === X ? O : X;
    return moves.sort((a, b) => _movePriority(game, a, player, opponent)
                              - _movePriority(game, b, player, opponent));
  }
}

function _movePriority(game, [mb,c], player, opponent) {
  const g = game.copy(); g.makeMove(mb,c);
  if (g.gameWinner === player) return 0;
  if (_wouldWinMini(game.cells[mb], c, player))   return 1;
  if (_wouldWinMini(game.cells[mb], c, opponent)) return 2;
  if (c === 4) return 3;
  if ([0,2,6,8].includes(c)) return 4;
  return 5;
}

function _wouldWinMini(cells, cellIdx, player) {
  const t = [...cells]; t[cellIdx] = player;
  return WINNING_COMBOS.some(([a,b,c]) => t[a] === player && t[b] === player && t[c] === player);
}

function _pick(arr)    { return arr[Math.floor(Math.random() * arr.length)]; }
function _shuffle(arr) { return arr.sort(() => Math.random() - 0.5); }

// ─────────────────────────────────────────
//  UI
// ─────────────────────────────────────────

const AI_PLAYER = O;   // human is always X

let game   = null;
let mode   = 'pvp';
let aiLevel = 'medium';
let scores  = { x: 0, o: 0, ties: 0 };

// ── Build DOM ────────────────────────────

function buildBoard() {
  const board = document.getElementById('mega-board');
  board.innerHTML = '';
  for (let mb = 0; mb < 9; mb++) {
    const wrap = document.createElement('div');
    wrap.className = 'mini-board';
    wrap.id = `mb-${mb}`;

    const grid = document.createElement('div');
    grid.className = 'mini-board-grid';

    for (let c = 0; c < 9; c++) {
      const btn = document.createElement('button');
      btn.className = 'cell-btn';
      btn.id = `cell-${mb}-${c}`;
      btn.disabled = true;
      btn.addEventListener('click', () => handleCellClick(mb, c));
      grid.appendChild(btn);
    }

    const overlay = document.createElement('div');
    overlay.className = 'mini-overlay hidden';
    overlay.id = `overlay-${mb}`;

    wrap.appendChild(grid);
    wrap.appendChild(overlay);
    board.appendChild(wrap);
  }
}

// ── Event handlers ───────────────────────

function bindEvents() {
  document.getElementById('new-game-btn').addEventListener('click', startNewGame);

  document.querySelectorAll('input[name="mode"]').forEach(r =>
    r.addEventListener('change', e => {
      mode = e.target.value;
      document.getElementById('ai-level-group').style.display =
        mode === 'pvc' ? '' : 'none';
    })
  );

  document.getElementById('ai-level').addEventListener('change', e => {
    aiLevel = e.target.value;
  });
}

function startNewGame() {
  game = new MegaTicTacToe();
  if (mode === 'pvc' && AI_PLAYER === X) {
    const move = new AIPlayer(aiLevel).getMove(game);
    if (move) game.makeMove(...move);
  }
  renderBoard();
}

function handleCellClick(mb, c) {
  if (!game || game.gameOver) return;
  if (mode === 'pvc' && game.currentPlayer === AI_PLAYER) return;
  if (!game.makeMove(mb, c)) return;

  renderBoard();
  if (game.gameOver) { recordResult(); return; }

  if (mode === 'pvc' && game.currentPlayer === AI_PLAYER) {
    setInfo('AI is thinking…');
    setTimeout(() => {
      const move = new AIPlayer(aiLevel).getMove(game);
      if (move) game.makeMove(...move);
      renderBoard();
      if (game.gameOver) recordResult();
    }, 60);
  }
}

function recordResult() {
  if (game.gameWinner === X)    scores.x++;
  else if (game.gameWinner === O) scores.o++;
  else                            scores.ties++;
  renderScores();
}

// ── Rendering ────────────────────────────

function renderBoard() {
  if (!game) return;
  const valid = new Set(game.getValidMoves().map(([b,c]) => `${b}-${c}`));

  for (let mb = 0; mb < 9; mb++) {
    for (let c = 0; c < 9; c++) {
      const btn = document.getElementById(`cell-${mb}-${c}`);
      const val = game.cells[mb][c];
      const active = valid.has(`${mb}-${c}`);

      btn.textContent = val === X ? 'X' : val === O ? 'O' : '';
      btn.disabled = !active;
      btn.className = 'cell-btn'
        + (val === X ? ' cell-x' : val === O ? ' cell-o' : '')
        + (active    ? ' cell-active' : '');
    }

    const w       = game.miniWinners[mb];
    const overlay = document.getElementById(`overlay-${mb}`);
    const mbDiv   = document.getElementById(`mb-${mb}`);

    if (w === X) {
      overlay.textContent = 'X'; overlay.className = 'mini-overlay won-x';
      mbDiv.className = 'mini-board mini-board-won-x';
    } else if (w === O) {
      overlay.textContent = 'O'; overlay.className = 'mini-overlay won-o';
      mbDiv.className = 'mini-board mini-board-won-o';
    } else if (w === DRAW) {
      overlay.textContent = '='; overlay.className = 'mini-overlay draw';
      mbDiv.className = 'mini-board mini-board-draw';
    } else {
      overlay.textContent = ''; overlay.className = 'mini-overlay hidden';
      const isActive = !game.gameOver
        && game.cells[mb].some(v => v === EMPTY)
        && (game.activeBoard === -1 || game.activeBoard === mb);
      mbDiv.className = 'mini-board' + (isActive ? ' mini-board-active' : '');
    }
  }

  const p = game.currentPlayer === X ? 'X' : 'O';
  const b = game.activeBoard === -1 ? 'any board' : `board ${game.activeBoard + 1}`;

  if (game.gameOver) {
    setInfo(
      game.gameWinner === X    ? 'X wins the game!' :
      game.gameWinner === O    ? 'O wins the game!' : "It's a draw!"
    );
  } else {
    setInfo(`${p}'s turn — play in ${b}`);
  }
}

function setInfo(msg) {
  document.getElementById('game-info').textContent = msg;
}

function renderScores() {
  document.getElementById('score-x').innerHTML   = `X &nbsp; ${scores.x}`;
  document.getElementById('score-tie').innerHTML = `Draws &nbsp; ${scores.ties}`;
  document.getElementById('score-o').innerHTML   = `O &nbsp; ${scores.o}`;
}

// ── Init ─────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  buildBoard();
  bindEvents();
});
