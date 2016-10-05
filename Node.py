

class NodeChildIterator():
    def __init__(self, node):
        self.node = node
        self.ptr = 0

    def __next__(self):
        if self.ptr >= self.node.size():
            raise StopIteration
        else:
            self.ptr += 1
            return self.node.get(self.ptr-1)


def create(name, node=None):
    if not node is None:
        return node
    return Node(name)


class Node():
    def __init__(self, name):
        self.name = name
        self.children = []

    def __iter__(self):
        return NodeChildIterator(self)

    def count(self):
        return len(self.children)

    def size(self):
        return self.count()

    def get(self, idx):
        return self.children[idx]

    def append(self, el):
        if type(el) is tuple and len(el) == 2 and type(el[1]) is bool:
            if el[1]:
                self.children.append(el[0])
            return el[1]

        self.children.append(el)

    def concat(self, el):
        if type(el) is tuple and len(el) == 2 and type(el[1]) is bool:
            if el[1]:
                for e in el[0]:
                    self.children.append(e)
            return el[1]

        assert type(el) is Node
        for e in el:
            self.children.append(e)

    def skip(self, el):
        if type(el) is tuple and len(el) == 2 and type(el[1]) is bool:
            return el[1]

        return el

    def normalize(self):
        if len(self.children) == 1:
            return self.children[0]
        return self

    def __str__(self):
        s = self.name + '(' + ', '.join( str(child) for child in self.children ) + ')'
        return s




