import emoji
from nltk import FreqDist
from nltk.corpus import brown
import numpy as np


freqs = FreqDist(w.lower() for w in brown.words() if len(w) == 5)
word_list = list(w for w, _ in freqs.most_common(1000))


def get_todays_letters():
    todays_word = np.random.choice(word_list, 1)[0]
    todays_letters = list(todays_word)
    return todays_letters


def compare_guess(todays_letters, guess_letters):
    greens = [i for i, (l1, l2) in enumerate(zip(todays_letters, guess_letters)) if l1 == l2]
    yellows = [i for i, l in enumerate(guess_letters) if l in todays_letters and i not in greens]
    greys = [i for i, _ in enumerate(guess_letters) if i not in greens and i not in yellows]

    res = []
    for i in range(5):
        if i in greens:
            res.append(emoji.emojize(':green_square:'))
        elif i in yellows:
            res.append(emoji.emojize(':yellow_square:'))
        elif i in greys:
            res.append(emoji.emojize(':black_large_square:'))
        else:
            raise ValueError("Something went wrong")

    return res


def play():
    todays_letters = get_todays_letters()

    results = []
    winner = False

    for _ in range(6):
        guess = input('Your guess')
        guess_letters = list(guess)

        if len(guess_letters) != 5:
            print("That's not a 5-letter word. Try again.")
            continue

        res = compare_guess(todays_letters, guess_letters)
        print(res)
        results.append(res)

        if res == [emoji.emojize(':green_square:')] * 5:
            print("Good job!")
            print(results)
            winner = True
            break

    if not winner:
        print(f"You lost! The correct word was '{''.join(todays_letters)}'.")
        print(results)
