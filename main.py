from grammar import Grammar, Rule
from utils import display, normalize, load
from nltk.tree import Tree

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

    def token_by_current_dot(self):
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
        # initialize all charts
        charts = self.create_charts(len(self.words))

        for i, chart in enumerate(charts):
            for state in chart.states:
                if self.check_predict(state):
                    self.predict(charts, i, state)
                if self.check_complete(state):
                    self.complete(charts, i, state)
                if self.check_scanner(state):
                    self.scanner(charts, i, state)
        return charts

    # right token is non terminal
    def predict(self, charts, i, state):
        token = state.token_by_current_dot()
        rules = self.grammar.get_rules(token) # [Rule(token, ...), Rule(token, ...)]
        for rule in rules:
            state = State(rule=rule, dot=0, origin=i, action="Predict")
            chart = charts[i]
            chart.add_state(state)

    # right token is terminal
    def scanner(self, charts, i, state):
        token = state.token_by_current_dot()
        word = self.words[i]
        if (token == word):
            new_state = State(state.rule, dot=state.dot+1,origin=state.origin, action="Scan")
            charts[i+1].add_state(new_state)

    # dot at the end
    def complete(self, charts, i, state):
        chart = charts[state.origin]
        left_side = state.rule.left_side
        for prev_state in chart.states:
            if (self.check_left_side_in_right_side(prev_state, left_side)):
                new_state = State(prev_state.rule, dot=prev_state.dot+1,
                            origin=prev_state.origin,
                            action="Complete")
                current_chart = charts[i]
                current_chart.add_state(new_state)

    # true, if dot in the left from token, token==left_side
    def check_left_side_in_right_side(self, prev_state, left_side):
        return prev_state.token_by_current_dot() == left_side

    def check_predict(self, state): # True/False
        # state is not complete
        # right token from dot - is non terminal
        return not state.is_complete() and not self.grammar.is_terminal(state.token_by_current_dot())

    def check_scanner(self, state): # True/False
        # state is not complete
        # right token from dot - is terminal
        return not state.is_complete() and self.grammar.is_terminal(state.token_by_current_dot())
    
    def check_complete(self, state): # True/False
        # state is complete
        return state.is_complete()

    def create_charts(self, num):
        # creation of fake chart
        fake_rule = Rule(left_side=State.START, right_side=[self.grammar.start])
        fake_state = State(fake_rule, dot=0, origin=0, action="START")
        fake_chart = Chart()
        fake_chart.add_state(fake_state)

        charts = []
        charts.append(fake_chart)

        # creation of real charts
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
    tree = sub_tree(State.START, charts, grammar)
    display(tree, sentence, render=True)

def sub_tree(symbol, charts, grammar):
    if (grammar.is_terminal(symbol) and symbol != State.START): return symbol
    for chart in reversed(charts):
        for state in reversed(chart.states):
            if (symbol == state.rule.left_side):
                return Tree(state.rule.left_side, [sub_tree(child, charts, grammar) for child in state.rule.right_side])

# startpoint in python
if __name__ == "__main__":
    main()
