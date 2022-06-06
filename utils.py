import string
import sys

# remove punctuation
def normalize(sentence):
    for p in string.punctuation:
        sentence = sentence.replace(p, '')
    return sentence.strip()

def display(result, initial, render):
    if result is None:
        print(initial + '\n')
    else:
        if render:
            draw(result)
        else:
            result.pretty_print()


def draw(result):
    while True:
        try:
            result.draw()
        except EOFError:
            sys.exit()

        sys.exit()


def load(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
