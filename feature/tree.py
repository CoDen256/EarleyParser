from feature import FStructure


class FTree:
    commands = []

    def __init__(self, node, children_schemata, children):
        self.node = node
        self.children_schemata = children_schemata
        self.children = children
        self.functional_schema = None
        self.parent = None
        self.f = None

    def get(self, index):
        return self.children[min(index, len(self.children))]

    def printTree(self, depth=0):
        print(depth * "\t" + self.node)
        for child in self.children:
            child.printTree(depth + 1)

    def initialize(self):
        self.f = FStructure()
        for i, child in enumerate(self.children):
            child.parent = self
            child.functional_schema = self.children_schemata[i]
            child.initialize()

    def createUnificationCommands(self):
        for child in self.children:
            child.createUnificationCommands()
        if self.functional_schema is None: return
        trimmed = self.functional_schema[1:-1]
        schemata = trimmed.split(",")

        for s in schemata:
            command = None
            schema = s.strip()
            left, right = schema.split("=")
            if self.isatomic(left) or self.isatomic(right):
                assert not (self.isatomic(left) and self.isatomic(right))
                atomic, f_const = (left, right) if self.isatomic(left) else (right, left)
                f, args = self.getReference(f_const)
                command = AssertionCommand(f, args, atomic)
            else:
                f1, args1 = self.getReference(left)
                f2, args2 = self.getReference(right)
                command = UnificationCommand(f1, args1, f2, args2)

            FTree.commands.append(command)

    def getReference(self, constituent):
        reference = constituent[0]
        args = constituent[1:].split()
        if reference == "^":
            return self.parent.f, args
        if reference == "!":
            return self.f, args
        raise Exception("Invalid format of functional schemata")

    def isatomic(self, schema):
        return "^" not in schema and "!" not in schema

    def __repr__(self):
        return self.node

    def __str__(self):
        return self.node


class UnificationCommand:
    def __init__(self, f1, args1, f2, args2):
        self.f1 = f1
        self.f2 = f2
        self.args1 = args1
        self.args2 = args2

    def execute(self):
        FStructure.unify(self.f1, self.args1, self.f2, self.args2)


class AssertionCommand:
    def __init__(self, f, args, atomic):
        self.f = f
        self.atomic = atomic
        self.args = args

    def execute(self):
        FStructure.assertAtomic(self.f, self.args, self.atomic)


    def __str__(self):
        return f"(f {self.args}) = {self.atomic}"

    def __repr__(self):
        return self.__str__()
