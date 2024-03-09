from pathlib import Path

import emoji
import numpy as np


with Path("words.txt").open("r") as f:
    WORD_LIST = [w.strip() for w in f.readlines()]


def get_todays_letters() -> list[str]:
    todays_word = np.random.choice(WORD_LIST, 1)[0]
    return list(todays_word)


def compare_guess(todays_letters: list[str], guess_letters: list[str]) -> list[str]:
    assert len(todays_letters) == len(guess_letters) == 5, "Both words must be 5 letters long"

    greens = [i for i, (l1, l2) in enumerate(zip(todays_letters, guess_letters)) if l1 == l2]
    yellows = [i for i, l in enumerate(guess_letters) if l in todays_letters and i not in greens]
    greys = [i for i, _ in enumerate(guess_letters) if i not in greens and i not in yellows]

    res = []
    for i in range(5):
        if i in greens:
            res.append(emoji.emojize(":green_square:"))
        elif i in yellows:
            res.append(emoji.emojize(":yellow_square:"))
        elif i in greys:
            res.append(emoji.emojize(":black_large_square:"))
        else:
            raise ValueError("Something went wrong")

    return res
