from collections import defaultdict

class Rule(object):
    """
    Represents a CFG rule.
    """

    def __init__(self, lhs, rhs):
        # Represents the rule 'lhs -> rhs', where lhs is a non-terminal and
        # rhs is a list of non-terminals and terminals.
        self.lhs, self.rhs = lhs, rhs

    def __contains__(self, symbol):
        return symbol in self.rhs
    def __eq__(self, other):
        if type(other) is Rule:
            return self.lhs == other.lhs and self.rhs == other.rhs

        return False

    def __getitem__(self, i):
        return self.rhs[i]

    def __len__(self):
        return len(self.rhs)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.lhs + ' -> ' + ' '.join(self.rhs)

class Grammar(object):
    """
    Represents a CFG.
    """

    def __init__(self):
        # The rules are represented as a dictionary from L.H.S to R.H.S.
        self.rules = defaultdict(list) # {
                                       # lhs1: [Rule(lhs1, rhs1), Rule(lhs1, rhs2)...], 
                                       # lhs2: [Rule(lhs2, rhs3)...]
                                       # }
        self.start = None               # lhs1

    def add(self, rule):
        """
        Adds the given rule to the grammar.
        """

        self.rules[rule.lhs].append(rule)

    @staticmethod
    def load_grammar(fpath):
        """
        Loads the grammar from file (from the )
        """
        # create empty grammar
        grammar = Grammar()

        with open(fpath) as f:
            for line in f: # line of file
                line = line.strip() # remove spaces from right/left

                if len(line) == 0: # if empty, then skip
                    continue

                if line.startswith("%"):    # starts with %
                    grammar.start = line.split("start")[1].strip()  # takes value after 'start'
                    continue
                # line = NP -> Det Noun
                entries = line.split('->') # ['NP', 'Det Noun Verb | Noun ']
                lhs = entries[0].strip() # NP
                for rhs in entries[1].split('|'): # ['Det Noun Verb', 'Noun']
                    grammar.add(Rule(lhs, rhs.strip().split())) # ['Det', 'Noun', 'Verb']

        return grammar

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = [str(r) for r in self.rules[self.start]]

        for nt, rule_list in self.rules.iteritems():
            if nt == self.start:
                continue

            s += [str(r) for r in rule_list]

        return '\n'.join(s)

    # Returns the rules for a given Non-terminal.
    def __getitem__(self, non_terminal):
        return self.rules[non_terminal]

    def is_terminal(self, sym):
        """
        Checks is the given symbol is terminal.
        """
        # sym = `index` in dictionary, for example 'lhs'
        # self.rules['lhs'] returns list of rules
        return len(self.rules[sym]) == 0

    def is_tag(self, sym):
        """
        Checks whether the given symbol is a tag, i.e. a non-terminal with rules
        to solely terminals.
        """
        rules = self.rules[sym] #[ Rule(l,r1), Rule(l,r2)...]
        r_sides =  [rule.rhs for rule in rules] # [r1, r2, r3, r4...]
        r_side_terminal = [self.is_terminal(r_side) for r_side in r_sides] # [True, False, True...]
        return not self.is_terminal(sym) and \
               all(r_side_terminal)
