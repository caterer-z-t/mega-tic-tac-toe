# Mega Tic-Tac-Toe

A web app for playing Ultimate Tic-Tac-Toe against a friend or an AI with multiple difficulty levels.

## Rules

The board is a 3×3 grid of mini 3×3 boards. Win three mini-boards in a row to win the game.

- The cell you play in determines **which mini-board** your opponent must play in next.
- If that mini-board is already won or full, the opponent may play in any available board.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Open `http://localhost:8050` in any browser or `http://http://0.0.0.0:8050/`

## AI Levels

| Level  | Method                        |
|--------|-------------------------------|
| Random | Uniform random move           |
| Easy   | Win/block heuristic           |
| Medium | Minimax depth 2               |
| Hard   | Minimax + alpha-beta depth 4  |
| Expert | Minimax + alpha-beta depth 6  |

## License

MIT
