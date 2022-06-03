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
        if type(other) is State:
            return (
                self.rule == other.rule
                and self.dot == other.dot
                and self.origin == other.origin
            )

        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        def str_helper(state):
            return (
                "("
                + state.rule.left_side
                + " -> "
                + " ".join(
                    state.rule.right_side[: state.dot] + ["*"] + state.rule.right_side[state.dot :]
                )
                + (", %d)" % (state.origin))
            )

        return str_helper(self)

    def next_token(self):
        if self.dot < len(self.rule.right_side):
            return self.rule.right_side[self.dot]

    def is_complete(self):
        return len(self.rule.right_side) == self.dot


class Chart:
    def __init__(self):
        self.states = []

    def add_state(self, state):
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
                    if self.grammar.is_tag(state.next_token()):
                        self.scanner(charts, state, i)
                    else:
                        self.predictor(charts, state, i)
                else:
                    self.completer(charts, state, i)
        return charts

    def create_charts(self, num):
        start_state = State(Rule(State.START, [self.grammar.start]), action="Start")
        start_chart = Chart()
        start_chart.add_state(start_state)  # Add start state to start chart

        charts = []
        charts.append(start_chart)  # Add start chart to charts
        for i in range(num):
            charts.append(Chart())

        return charts
        
    def is_word_in_rules(self, word, rules):
        for rule in rules:
            if word in rule.right_side:
                return True
        return False

    def predictor(self, charts, state, position):
        token = state.next_token() # token to the right of the dot
        for rule in self.grammar.get_rules(token):
            new_state = State(rule, dot=0, origin=position, action="Predict")
            charts[position].add_state(new_state)

    def scanner(self, charts, state, position):  # dot near tag, e.g. N -> * Det Noun, where 'Det' -> det
        token = state.next_token() # token to the right of the dot
        
        if position < len(self.words): # if last chart, then skip
            word = self.words[position] # current word to scan
            rules = self.grammar.get_rules(token)
            if self.is_word_in_rules(word, rules):
                new_rule = Rule(token, [word])  # 'Det' -> det
                new_state = State(new_rule, dot=1, origin=state.origin, action="Scan")
                charts[position + 1].add_state(new_state)

    def completer(self, charts, state, position):
        for prev_state in charts[state.origin].states:
            if prev_state.next_token() == state.rule.left_side:
                new_state = State(prev_state.rule, dot=(prev_state.dot + 1), origin=prev_state.origin, action="Complete")
                charts[position].add_state(new_state)


def main():
    ## PROCESS INPUT
    grammar = Grammar.load_grammar("grammatik.txt")
    sentence = normalize(load("input.txt"))  # remove punctuation , . ' ' etc

    ## PARSE INPUT
    parser = EarleyParser(sentence, grammar)
    charts = parser.parse()
     # parse = из цельной строки в структуру из соеденнных елементов

    ## PRINT RESULT
    # parser.chart - list
    # i - index of chart in list, char - element of parser.chart
    for i, chart in enumerate(charts):
        print("-" * 50, f"Chart #{i}", "-"*50)
        for state in chart.states:
            # print (10 spaces + state.action) (40 spaces + state) (slice sentence from i-position till end)
            print(
                "{0: <10} {1: <40} {2} ".format(
                    state.action, str(state), " ".join(sentence.split()[i:])
                )
            )

    ## build tree and visualize
    # tree = convert_to_tree(parser)
    # display(tree, sentence, render=True)


# startpoint in python
if __name__ == "__main__":
    main()
