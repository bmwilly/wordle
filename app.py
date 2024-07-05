import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import emoji

from utils import get_todays_letters, compare_guess

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Wordle"),
        dcc.Store(id="store"),
        dcc.Input(id="guess-input", type="text", value=""),
        html.Button("Submit", id="submit-button", n_clicks=0),
        html.Div(id="guess-output"),
        html.Div(id="end-output"),
    ]
)


@app.callback(
    Output("store", "data"),
    Input("submit-button", "n_clicks"),
    State("guess-input", "value"),
    State("store", "data"),
)
def update_store(n_clicks, value, data):
    if data is None:
        data = {
            "guesses": [],
            "results": [],
            "winner": False,
            "todays_letters": get_todays_letters(),
        }

    if n_clicks > 0 and not data["winner"] and len(data["guesses"]) < 6:
        guess_letters = list(value)

        if len(guess_letters) == 5:
            res = compare_guess(data["todays_letters"], guess_letters)
            data["guesses"].append(value)
            data["results"].append(res)

            if res == [emoji.emojize(":green_square:")] * 5:
                data["winner"] = True

    return data


@app.callback(
    Output("guess-output", "children"),
    Output("end-output", "children"),
    Input("store", "data"),
)
def update_output(data):
    if data is None:
        return [], ""

    guess_output = [
        html.Div(
            [
                html.Span(guess, style={"display": "inline-block", "width": "20%"}),
                html.Span("\t".join(result), style={"display": "inline-block", "width": "30%"}),
            ]
        )
        for guess, result in zip(data["guesses"], data["results"])
    ]

    if data["winner"]:
        end_output = "Good job!"
    elif len(data["guesses"]) == 6 and not data["winner"]:
        end_output = f"You lost! The correct word was '{''.join(data['todays_letters'])}'."
    else:
        end_output = ""

    return guess_output, end_output


if __name__ == "__main__":
    app.run_server(debug=True)
