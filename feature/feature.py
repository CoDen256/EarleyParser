class FStructure:
    def __init__(self):
        self.content = {} # actual dictionary
        self.link = None # link

    def getSource(self):
        if self.link is not None:
            return self.link
        else:
            return self.content

    def __getitem__(self, attribute):
        return self.getSource()[attribute]

    def __setitem__(self, key, value):
        self.getSource()[key] = value


    def getFeaturePath(self, *attributes):
        base = self
        for attr in attributes:
            if not isinstance(base, str):
                if attr not in base.keys():
                    base = base[attr]

            else:
                return base
        return base

    def __eq__(self, other):
        if other.link == self.link:
            return True
        if other.content.equals(self.content):
            return True

    def keys(self):
        return self.getSource().keys()

    def values(self):
        return self.getSource().keys()

    @staticmethod
    def unify(f1, args1, f2, args2):
        pass

    @staticmethod
    def assertAtomic(f, args, atomic):
        pass


def test():
    fstructuresWithLinkShouldReturnLink()
    validPath()

def fstructuresWithLinkShouldReturnLink():
    f1 = FStructure()
    f1["bla"] = 1
    f2 = FStructure()
    f2["bla"] = 2

    f1.link = f2
    assert f1["bla"] == 2

    f2["bla"] = 100
    assert f1["bla"] == 100

def validPath():
    f1 = FStructure()
    f2 = FStructure()
    f3 = FStructure()

    f1["f2"] = f2
    f2["f3"] = f3

    f3["arg"] = "sing"

    assert f1.getFeaturePath("f2", "f3", "arg") == "sing"

    assert f1.getFeaturePath("f2") == f2

    assert f1.getFeaturePath("f2", "f3") == f3


if __name__ == '__main__':
    test()