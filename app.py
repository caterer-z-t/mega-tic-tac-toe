##############################################################################
###
###                             Imports
###
##############################################################################

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from helper_funs.helper_fn import ultimate
# from dash_bootstrap_components import dbc

##############################################################################
###
###                             Layout
###
##############################################################################

app = dash.Dash(__name__,)

# Basic layout to start with
app.layout = html.Div([
    html.H1("Ultimate Tic Tac Toe"),
    dcc.Store(id='game-state', data={'game': None}),  # To store the game state
    html.Div(id='tic-tac-toe-board'),  # Placeholder for the game board
    html.Button('Start New Game', id='new-game', n_clicks=0)
])

@app.callback(
    Output('game-state', 'data'),
    Output('tic-tac-toe-board', 'children'),
    Input('new-game', 'n_clicks'),
    State('game-state', 'data')
)
def start_new_game(n_clicks, data):
    if n_clicks == 0:
        return data, html.Div("Click the button to start a new game")
    game = ultimate()
    data['game'] = game
    return data, html.Div("Game started")

if __name__ == '__main__':
    app.run_server(debug=True)
