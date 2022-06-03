from grammar import Grammar, Rule
from utils import convert_to_tree, display, normalize, load


class State:
    START = "<START>"

    def __init__(self, rule, dot=0, origin=0, action=""):
        self.rule = rule
        self.dot = dot
        self.origin = origin
        self.action = action

    def __eq__(self, other):
        return self.rule == other.rule and self.dot == other.dot and self.origin == other.origin

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        right_side = self.rule.right_side[: self.dot] + ['*'] + self.rule.right_side[self.dot :]
        rule = f"({self.rule.left_side} -> {' '.join(right_side)}, {self.origin})"
        return "{0: <10} {1: <40}".format(self.action, rule)

    def next_token(self):
        if self.dot < len(self.rule.right_side):
            return self.rule.right_side[self.dot]

    def is_complete(self):
        return len(self.rule.right_side) == self.dot


class Chart:
    def __init__(self):
        self.states = []

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)


class EarleyParser:
    def __init__(self, sentence, grammar):
        self.words = sentence.split()
        self.grammar = grammar

    def parse(self):
        charts = self.create_charts(len(self.words))

        for i, chart in enumerate(charts):
            for state in chart.states:
                if not state.is_complete():
                    if self.grammar.is_terminal(state.next_token()):
                        self.scanner(charts, state, i)
                    else:
                        self.predictor(charts, state, i)
                else:
                    self.completer(charts, state, i)
        return charts

    #   charts[pos]: State(A -> ...*B..., origin)           # state
    # + charts[pos]: State(B -> *......., pos)              # new_state
    def predictor(self, charts, state, pos):
        token = state.next_token() # token to the right of the dot - non terminal
        for rule in self.grammar.get_rules(token):
            new_state = State(rule, dot=0, origin=pos, action="Predict")
            charts[pos].add_state(new_state)


    #   charts[pos]:   State(A -> ...*b..., origin)         # state
    # + charts[pos+1]: State(A -> ...b*..., origin)         # new_state
    def scanner(self, charts, state, pos): 
        token = state.next_token()              # token to the right of the dot - terminal

        if pos >= len(self.words): return       # if last chart, then skip

        word = self.words[pos]                  # current word to scan
        if word == token:
            new_state = State(state.rule, dot=state.dot + 1, origin=state.origin, action="Scan")
            charts[pos + 1].add_state(new_state)


    #   charts[origin]  State(S -> ...*A..., prev_origin)       # prev_state
    #   charts[pos]:    State(A -> .......*, origin)            # state
    # + charts[pos]:    State(S -> ...A*..., prev_origin)       # new_state
    def completer(self, charts, state, pos):
        for prev_state in charts[state.origin].states:
            if prev_state.next_token() == state.rule.left_side:
                new_state = State(prev_state.rule, dot=prev_state.dot + 1, origin=prev_state.origin, action="Complete")
                charts[pos].add_state(new_state)

    def create_charts(self, num):
        start_state = State(Rule(State.START, [self.grammar.start]), action="Start")
        start_chart = Chart()
        start_chart.add_state(start_state)  # Add start state to start chart

        charts = []
        charts.append(start_chart)  # Add start chart to charts
        for i in range(num):
            charts.append(Chart())

        return charts

def main():
    ## PROCESS INPUT
    grammar = Grammar.load_grammar("grammatik.txt")
    sentence = normalize(load("input.txt"))  # remove punctuation , . ' ' etc

    ## PARSE INPUT
    parser = EarleyParser(sentence, grammar)
    charts = parser.parse() # parse = из цельной строки в структуру из соеденнных елементов

    ## PRINT RESULT
    # parser.chart - list
    # i - index of chart in list, char - element of parser.chart
    for i, chart in enumerate(charts):
        print("-" * 50, f"Chart #{i}", "-"*50)
        for state in chart.states:
            # print (10 spaces + state.action) (40 spaces + state) (slice sentence from i-position till end)
            print("{0: <50} {1} ".format(str(state), " ".join(sentence.split()[i:])))

    ## build tree and visualize
    # tree = convert_to_tree(parser)
    # display(tree, sentence, render=True)


# startpoint in python
if __name__ == "__main__":
    main()
