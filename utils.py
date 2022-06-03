from nltk.tree import Tree
import string
import sys

# remove 
def normalize(sentence):
    for p in string.punctuation:
        sentence = sentence.replace(p, '')
    return sentence.strip()


def get_helper(grammar, state):
    if grammar.is_tag(state.rule.lhs):
        return Tree(state.rule.lhs, [state.rule.rhs[0]])

    return Tree(state.rule.lhs,
                [get_helper(grammar, s) for s in state.back_pointers])


def convert_to_tree(parser):
    for state in parser.chart[-1]:
        if state.is_complete() and state.rule.lhs == parser.grammar.start and \
                state.sent_pos == 0 and state.chart_pos == len(parser.words):
            return get_helper(parser.grammar, state)

    return None


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
