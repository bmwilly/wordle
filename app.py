import dash
from dash import html, dcc
from dash.dependencies import ALL, Input, Output, State
import emoji

from utils import get_todays_letters, compare_guess

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Wordle"),
        dcc.Store(id="store"),
        html.Div(id="guess-inputs"),
        html.Button("Submit", id="submit-button", n_clicks=0),
        html.Div(id="guess-output"),
        html.Div(id="result-output"),
        html.Div(id="end-output"),
    ]
)


@app.callback(
    Output("store", "data"),
    Input("submit-button", "n_clicks"),
    State({"type": "guess-input", "index": ALL}, "value"),
    State("store", "data"),
)
def update_store(n_clicks, values, data):
    if data is None:
        data = {
            "guesses": [],
            "results": [],
            "winner": False,
            "todays_letters": get_todays_letters(),
        }

    if n_clicks > 0 and not data["winner"] and len(data["guesses"]) < 6:
        guess = values[-1]
        guess_letters = list(guess)

        if len(guess_letters) == 5:
            res = compare_guess(data["todays_letters"], guess_letters)
            data["guesses"].append(guess)
            data["results"].append(res)

            if res == [emoji.emojize(":green_square:")] * 5:
                data["winner"] = True

    return data


@app.callback(
    Output("guess-inputs", "children"),
    Input("submit-button", "n_clicks"),
    State({"type": "guess-input", "index": ALL}, "value"),
)
def update_inputs(n_clicks, values):
    if n_clicks == 0:
        return [dcc.Input(id={"type": "guess-input", "index": n_clicks}, type="text", value="")]
    else:
        return [
            dcc.Input(id={"type": "guess-input", "index": i}, type="text", value=val)
            for i, val in enumerate(values)
        ] + [dcc.Input(id={"type": "guess-input", "index": n_clicks}, type="text", value="")]


@app.callback(
    Output("guess-output", "children"),
    Output("result-output", "children"),
    Output("end-output", "children"),
    Input("store", "data"),
)
def update_output(data):
    if data is None:
        return "", "", ""

    if data["winner"]:
        return "\t".join(data["guesses"][-1]), "\t".join(data["results"][-1]), "Good job!"

    if len(data["guesses"]) == 6 and not data["winner"]:
        return "", "", f"You lost! The correct word was '{''.join(data['todays_letters'])}'."

    if len(data["guesses"]) > 0:
        return "\t".join(data["guesses"][-1]), "\t".join(data["results"][-1]), ""

    return "", "", ""


if __name__ == "__main__":
    app.run_server(debug=True)
