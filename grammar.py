from collections import defaultdict

# der gross lustig mann sieht die schoen klein frau
# und die frau fuettert die hungrig hundin
# aber die gut katze hoert die schlecht schlange,
# weil der klein kater liebt der gross hund,
# deshalb der schnell mann geht

# non-terminals:    {A, B, C}
# terminals:        {a, b, c}
# tokens:           {a, A, b, B, c, C} = non-terminal U terminal

# `Rule`:
# A -> C B d:
#   left_side:      A
#   right_side:     [C, B, d] 

# `Grammar`:
# {
#   left_side: [Rule(left_side, right_side_1), Rule(left_side, right_side_2)...]
#   ...
# }
# Example for Rules 
# - A -> A B d
# - A -> B d
# - B -> d
# Grammar: 
# {
#   "A" : [Rule("A", ["A", "B", "d"]), Rule("A", ["B", "d"])]
#   "B" : [Rule("B", ["d"])]
#   "d" : [] - terminal
# }

class Rule:
    # Represents a Context free Grammar (CFG) rule

    def __init__(self, left_side, right_side):
        # Represents the rule 'left_side -> right_side', where left_side is a non-terminal and
        # right_side is a list of non-terminals and terminals.
        self.left_side, self.right_side = left_side, right_side

    def __eq__(self, other):
        return type(other) is Rule and self.left_side == other.left_side and self.right_side == other.right_side

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.left_side + " -> " + " ".join(self.right_side)


class Grammar:
    # Represents a context free grammar (CFG)

    def __init__(self):
        # The rules are represented as a dictionary from left_side to _right_side
        self.rules = defaultdict(list)
        self.start = None

    def add(self, rule):
        # Adds the rule to the grammar

        self.rules[rule.left_side].append(rule)

    @staticmethod
    def load_grammar(path):
        # Reads grammar from the given path

        grammar = Grammar()

        with open(path) as f:
            for line in f:
                line = line.strip()

                if len(line) == 0:
                    continue

                if line.startswith("%"):
                    grammar.start = line.split("start")[1].strip()
                    continue
                entries = line.split("->")
                left_side = entries[0].strip()
                for right_side in entries[1].split("|"):
                    grammar.add(Rule(left_side, right_side.strip().split()))

        return grammar

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = [str(r) for r in self.rules[self.start]]

        for nt, rule_list in self.rules.iteritems():
            if nt == self.start:
                continue

            s += [str(r) for r in rule_list]

        return "\n".join(s)

    # Returns the rules for a given Non-terminal.
    def get_rules(self, non_terminal):
        return self.rules[non_terminal]

    # Checks, whether the given token is terminal
    def is_terminal(self, token):
        return len(self.rules[token]) == 0
