from grammar import Grammar, Rule
from utils import convert_to_tree, display, normalize


class EarleyState(object):
    """
    Represents a state in the Earley algorithm.
    """

    GAM = '<GAM>'

    def __init__(self, rule, dot=0, sent_pos=0, chart_pos=0, back_pointers=[], action=""):
        self.rule = rule
        self.dot = dot
        self.sent_pos = sent_pos
        self.chart_pos = chart_pos
        self.back_pointers = back_pointers
        self.action = action

    def __eq__(self, other):
        if type(other) is EarleyState:
            return self.rule == other.rule and self.dot == other.dot and \
                   self.sent_pos == other.sent_pos

        return False

    def __len__(self):
        return len(self.rule)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        def str_helper(state):
            return ('(' + state.rule.lhs + ' -> ' +
                    ' '.join(state.rule.rhs[:state.dot] + ['*'] +
                             state.rule.rhs[state.dot:]) +
                    (', [%d, %d])' % (state.sent_pos, state.chart_pos)))

        return (str_helper(self))
        # ' (' + ', '.join(str_helper(s) for s in self.back_pointers) + ')')

    def next(self):
        if self.dot < len(self):
            return self.rule[self.dot]

    def is_complete(self):
        return len(self) == self.dot

    @staticmethod
    def start_state(start):
        return EarleyState(Rule(EarleyState.GAM, [start]), action="Start")


class ChartEntry(object):
    def __init__(self, states):
        self.states = states

    def __iter__(self):
        return iter(self.states)

    def __len__(self):
        return len(self.states)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n'.join(str(s) for s in self.states)

    def add(self, state):
        """
        Add the given state (if it hasn't already been added).
        """

        if state not in self.states:
            self.states.append(state)


class Chart(object):
    def __init__(self, entries):
        # List of chart entries.
        self.entries = entries

    def __getitem__(self, i):
        return self.entries[i]

    def __len__(self):
        return len(self.entries)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n\n'.join([("Chart[%d]:\n" % i) + str(entry) for i, entry in
                            enumerate(self.entries)])

    @staticmethod
    def init(word_amount, start):
        dummy = ChartEntry([EarleyState.start_state(start)])
        entries = [dummy]

        for i in range(word_amount):
            entry = ChartEntry([])
            entries.append(entry)

        return Chart(entries)


class EarleyParser(object):
    def __init__(self, sentence, grammar):
        self.words = sentence.split()
        self.grammar = grammar

        self.chart = Chart.init(len(self.words), self.grammar.start)

    def predictor(self, state, pos):

        for rule in self.grammar[state.next()]:
            self.chart[pos].add(EarleyState(rule, dot=0,
                                            sent_pos=state.chart_pos, chart_pos=state.chart_pos, action="Predict"))

    def scanner(self, state, pos):
        if state.chart_pos < len(self.words):
            word = self.words[state.chart_pos]

            if any((word in r) for r in self.grammar[state.next()]):
                self.chart[pos + 1].add(EarleyState(Rule(state.next(), [word]),
                                                    dot=1, sent_pos=state.chart_pos,
                                                    chart_pos=(state.chart_pos + 1), action="Scan"))

    def completer(self, state, pos):
        for prev_state in self.chart[state.sent_pos]:
            if prev_state.next() == state.rule.lhs:
                self.chart[pos].add(EarleyState(prev_state.rule,
                                                dot=(prev_state.dot + 1), sent_pos=prev_state.sent_pos,
                                                chart_pos=pos,
                                                back_pointers=(prev_state.back_pointers + [state]), action="Complete"))

    def parse(self):
        # Checks whether the next symbol for the given state is a tag.
        def is_tag(state):
            return self.grammar.is_tag(state.next())

        for i in range(len(self.chart)):
            for state in self.chart[i]:
                if not state.is_complete():
                    if is_tag(state):
                        self.scanner(state, i)
                    else:
                        self.predictor(state, i)
                else:
                    self.completer(state, i)


def main():
## process input
    grammar = Grammar.load_grammar("grammatik.txt")
    sentence = normalize(load_sentence("input.txt")) #remove punctuation , . ' ' etc 

## parse input
    parser = EarleyParser(sentence, grammar)
    parser.parse() # parse = из цельного в структуру из соеденнных елементов
 
## print result
    # parser.chart - list
    # i - index of chart in list, char - element of parser.chart
    for i, chart in enumerate(parser.chart):
        print("-" * 100)
        for state in chart.states:
            # print (10 spaces + state.action) (40 spaces + state) (slice sentence from i-position till end)
            print("{0: <10} {1: <40} {2} ".format(state.action, str(state), " ".join(sentence.split()[i:])))

## build tree and visualize
    tree = convert_to_tree(parser)
    display(tree, sentence, render=True)


def load_sentence(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

#startpoint in python
if __name__ == '__main__':
    main()
