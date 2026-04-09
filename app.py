"""
Mega Tic-Tac-Toe – Dash web application.

Run with:  python app.py
Then open  http://localhost:8050  in any browser (desktop or mobile).
"""

import dash
import dash_bootstrap_components as dbc
from dash import ALL, Input, Output, State, callback_context, dcc, html, no_update

from ai.ai_player import AIPlayer
from game.board import DRAW, EMPTY, O, X, MegaTicTacToe

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)
app.title = "Mega Tic-Tac-Toe"
server = app.server   # expose Flask server for deployment

# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------


def _mini_board(mb_idx: int) -> html.Div:
    cells = [
        html.Button(
            "",
            id={"type": "cell", "mini": mb_idx, "cell": c},
            n_clicks=0,
            className="cell-btn",
            disabled=True,
        )
        for c in range(9)
    ]
    overlay = html.Div(
        "",
        id={"type": "mini-overlay", "idx": mb_idx},
        className="mini-overlay hidden",
    )
    return html.Div(
        [html.Div(cells, className="mini-board-grid"), overlay],
        id={"type": "mini-board", "idx": mb_idx},
        className="mini-board",
    )


app.layout = dbc.Container(
    [
        # ── Title ─────────────────────────────────────────────────────────
        html.H1("Mega Tic-Tac-Toe", className="text-center my-3 game-title"),

        # ── Settings card ────────────────────────────────────────────────
        dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Mode", className="settings-label"),
                                dbc.RadioItems(
                                    id="mode-select",
                                    options=[
                                        {"label": "vs Human",    "value": "pvp"},
                                        {"label": "vs Computer", "value": "pvc"},
                                    ],
                                    value="pvp",
                                    inline=True,
                                    className="mt-1",
                                ),
                            ],
                            xs=12, sm="auto",
                        ),
                        dbc.Col(
                            [
                                html.Label("AI Level", className="settings-label"),
                                dbc.Select(
                                    id="ai-level-select",
                                    options=[
                                        {"label": "Random", "value": "random"},
                                        {"label": "Easy",   "value": "easy"},
                                        {"label": "Medium", "value": "medium"},
                                        {"label": "Hard",   "value": "hard"},
                                        {"label": "Expert", "value": "expert"},
                                    ],
                                    value="medium",
                                    className="mt-1",
                                ),
                            ],
                            id="ai-level-col",
                            xs=12, sm="auto",
                            style={"display": "none"},
                        ),
                        dbc.Col(
                            dbc.Button(
                                "New Game",
                                id="new-game-btn",
                                color="success",
                                className="new-game-btn mt-1",
                            ),
                            xs=12, sm="auto",
                            className="d-flex align-items-end",
                        ),
                    ],
                    align="end",
                    className="g-3",
                )
            ),
            className="mb-3 settings-card",
        ),

        # ── Score row ────────────────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(html.Div(id="score-x",   className="score-box score-x"),   width=4),
                dbc.Col(html.Div(id="score-tie", className="score-box score-tie"), width=4),
                dbc.Col(html.Div(id="score-o",   className="score-box score-o"),   width=4),
            ],
            className="mb-2 text-center",
        ),

        # ── Game status ───────────────────────────────────────────────────
        html.Div(
            "Select a mode and click New Game to start.",
            id="game-info",
            className="game-info text-center mb-3",
        ),

        # ── Board ─────────────────────────────────────────────────────────
        html.Div(
            [_mini_board(i) for i in range(9)],
            id="mega-board",
            className="mega-board",
        ),

        # ── Stores ────────────────────────────────────────────────────────
        dcc.Store(id="game-state", data=None),
        dcc.Store(id="game-mode",  data={"mode": "pvp", "ai_level": "medium", "ai_player": O}),
        dcc.Store(id="scores",     data={"x": 0, "o": 0, "ties": 0}),
    ],
    fluid=True,
    className="game-container",
)

# ---------------------------------------------------------------------------
# Callbacks – settings
# ---------------------------------------------------------------------------


@app.callback(
    Output("ai-level-col", "style"),
    Input("mode-select", "value"),
)
def toggle_ai_level_visibility(mode):
    return {} if mode == "pvc" else {"display": "none"}


@app.callback(
    Output("game-mode", "data"),
    Input("mode-select", "value"),
    Input("ai-level-select", "value"),
)
def sync_game_mode(mode, level):
    return {"mode": mode, "ai_level": level, "ai_player": O}


# ---------------------------------------------------------------------------
# Callbacks – new game
# ---------------------------------------------------------------------------


@app.callback(
    Output("game-state", "data"),
    Input("new-game-btn", "n_clicks"),
    State("game-mode", "data"),
    prevent_initial_call=True,
)
def start_new_game(_, mode):
    game = MegaTicTacToe()

    # If AI plays as X it moves first
    if mode["mode"] == "pvc" and mode["ai_player"] == X:
        ai = AIPlayer(mode["ai_level"])
        move = ai.get_move(game)
        if move:
            game.make_move(*move)

    return game.to_dict()


# ---------------------------------------------------------------------------
# Callbacks – player move (+ AI response)
# ---------------------------------------------------------------------------


@app.callback(
    Output("game-state", "data", allow_duplicate=True),
    Input({"type": "cell", "mini": ALL, "cell": ALL}, "n_clicks"),
    State("game-state", "data"),
    State("game-mode", "data"),
    prevent_initial_call=True,
)
def handle_cell_click(_, state, mode):
    if not state:
        return no_update

    triggered = callback_context.triggered_id
    if not triggered or not isinstance(triggered, dict):
        return no_update

    mb = triggered["mini"]
    c  = triggered["cell"]

    game = MegaTicTacToe.from_dict(state)
    if not game.make_move(mb, c):
        return no_update

    # AI responds immediately after the human move
    if mode["mode"] == "pvc" and not game.game_over:
        if game.current_player == mode["ai_player"]:
            ai = AIPlayer(mode["ai_level"])
            move = ai.get_move(game)
            if move:
                game.make_move(*move)

    return game.to_dict()


# ---------------------------------------------------------------------------
# Callbacks – score tracking
# ---------------------------------------------------------------------------


@app.callback(
    Output("scores", "data"),
    Input("game-state", "data"),
    State("scores", "data"),
)
def update_scores(state, scores):
    if not state or not state.get("game_over"):
        return no_update
    w = state["game_winner"]
    if w == X:
        return {**scores, "x": scores["x"] + 1}
    if w == O:
        return {**scores, "o": scores["o"] + 1}
    if w == DRAW:
        return {**scores, "ties": scores["ties"] + 1}
    return no_update


# ---------------------------------------------------------------------------
# Callbacks – render board & UI from game state
# ---------------------------------------------------------------------------


@app.callback(
    Output({"type": "cell",         "mini": ALL, "cell": ALL}, "children"),
    Output({"type": "cell",         "mini": ALL, "cell": ALL}, "disabled"),
    Output({"type": "cell",         "mini": ALL, "cell": ALL}, "className"),
    Output({"type": "mini-overlay", "idx":  ALL},              "children"),
    Output({"type": "mini-overlay", "idx":  ALL},              "className"),
    Output({"type": "mini-board",   "idx":  ALL},              "className"),
    Output("game-info", "children"),
    Input("game-state", "data"),
)
def render_board(state):
    if not state:
        return (
            [""] * 81, [True] * 81, ["cell-btn"] * 81,
            [""] * 9, ["mini-overlay hidden"] * 9, ["mini-board"] * 9,
            "Select a mode and click New Game to start.",
        )

    game = MegaTicTacToe.from_dict(state)
    valid = set(game.get_valid_moves())

    cell_children, cell_disabled, cell_classes = [], [], []

    for mb in range(9):
        for c in range(9):
            val = game.cells[mb][c]
            sym = "X" if val == X else ("O" if val == O else "")
            active = (mb, c) in valid

            cls = "cell-btn"
            if val == X:
                cls += " cell-x"
            elif val == O:
                cls += " cell-o"
            if active:
                cls += " cell-active"

            cell_children.append(sym)
            cell_disabled.append(not active)
            cell_classes.append(cls)

    overlay_children, overlay_classes, board_classes = [], [], []

    for mb in range(9):
        w = game.mini_winners[mb]
        if w == X:
            overlay_children.append("X")
            overlay_classes.append("mini-overlay won-x")
        elif w == O:
            overlay_children.append("O")
            overlay_classes.append("mini-overlay won-o")
        elif w == DRAW:
            overlay_children.append("=")
            overlay_classes.append("mini-overlay draw")
        else:
            overlay_children.append("")
            overlay_classes.append("mini-overlay hidden")

        is_active_board = (
            not game.game_over
            and w == EMPTY
            and any(game.cells[mb][c2] == EMPTY for c2 in range(9))
            and (game.active_board == -1 or game.active_board == mb)
        )
        cls = "mini-board"
        if is_active_board:
            cls += " mini-board-active"
        if w == X:
            cls += " mini-board-won-x"
        elif w == O:
            cls += " mini-board-won-o"
        elif w == DRAW:
            cls += " mini-board-draw"
        board_classes.append(cls)

    if game.game_over:
        if game.game_winner == X:
            info = "X wins the game!"
        elif game.game_winner == O:
            info = "O wins the game!"
        else:
            info = "It's a draw!"
    else:
        p = "X" if game.current_player == X else "O"
        b = "any board" if game.active_board == -1 else f"board {game.active_board + 1}"
        info = f"{p}'s turn — play in {b}"

    return (
        cell_children, cell_disabled, cell_classes,
        overlay_children, overlay_classes, board_classes,
        info,
    )


@app.callback(
    Output("score-x",   "children"),
    Output("score-tie", "children"),
    Output("score-o",   "children"),
    Input("scores", "data"),
)
def render_scores(scores):
    return (
        f"X  {scores['x']}",
        f"Draws  {scores['ties']}",
        f"O  {scores['o']}",
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
