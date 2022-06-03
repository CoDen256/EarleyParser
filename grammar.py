from collections import defaultdict


class Rule(object):
    """
    Represents a CFG rule.
    """

    def __init__(self, left_side, right_side):
        # Represents the rule 'left_side -> right_side', where left_side is a non-terminal and
        # right_side is a list of non-terminals and terminals.
        self.left_side, self.right_side = left_side, right_side

    def __eq__(self, other):
        if type(other) is Rule:
            return (
                self.left_side == other.left_side
                and self.right_side == other.right_side
            )

        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.left_side + " -> " + " ".join(self.right_side)


class Grammar(object):
    """
    Represents a CFG.
    """

    def __init__(self):
        # The rules are represented as a dictionary from L.H.S to R.H.S.
        self.rules = defaultdict(list)
        self.start = None

    def add(self, rule):
        """
        Adds the given rule to the grammar.
        """

        self.rules[rule.left_side].append(rule)

    @staticmethod
    def load_grammar(fpath):
        """
        Loads the grammar from file
        """

        grammar = Grammar()

        with open(fpath) as f:
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

    # Checks, whether the given symbol is terminal
    def is_terminal(self, sym):
        return len(self.rules[sym]) == 0
