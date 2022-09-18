import string
import sys
from nltk import Tree

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


def get_helper(grammar, state, start_token):
    if all([grammar.is_terminal(token) for token in state.rule.right_side]):
        return Tree(state.rule.left_side, state.rule.right_side)

    return Tree(state.rule.left_side, [get_helper(grammar, s, start_token) for s in state.parents])


def build_tree(start_token, charts, grammar):
    for state in reversed(charts[-1].states):
        if state.is_complete() and state.rule.left_side == start_token and \
                state.origin == 0:
            return get_helper(grammar, state, start_token)

    return None

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
