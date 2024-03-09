import emoji
import streamlit as st
import pandas as pd
import numpy as np

from wordle import get_todays_letters, compare_guess, print_results


st.title("Wordle")


if "winner" not in st.session_state:
    st.session_state["winner"] = False

if "todays_letters" not in st.session_state:
    st.session_state["todays_letters"] = get_todays_letters()

if "guesses" not in st.session_state:
    st.session_state["guesses"] = []

if "results" not in st.session_state:
    st.session_state["results"] = []

if not st.session_state["winner"] and len(st.session_state["guesses"]) < 6:
    guess = st.text_input("Your guess:", key=f"guess_{len(st.session_state['guesses'])}")

    if guess:
        guess_letters = list(guess)

        if len(guess_letters) != 5:
            st.write("That's not a 5-letter word. Try again.")
        else:
            res = compare_guess(st.session_state["todays_letters"], guess_letters)
            st.write("\t".join(guess_letters))
            st.write("\t".join(res))
            st.session_state["guesses"].append(guess)
            st.session_state["results"].append(res)

            if res == [emoji.emojize(":green_square:")] * 5:
                st.write("Good job!")
                print_results(st.session_state["guesses"])
                st.session_state["winner"] = True

if not st.session_state["winner"] and len(st.session_state["guesses"]) == 6:
    st.write(f"You lost! The correct word was '{''.join(st.session_state['todays_letters'])}'.")
    print_results(st.session_state["guesses"])
