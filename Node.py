import analyzer

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

    def append(self, el, concate=False):
        flag = True
        comments = ()
        value = None
        if type(el) is tuple:
            if type(el[0]) is tuple:
                value = el[0][0]
                comments = el[0][1]
            else:
                value = el[0]
                if type(el[1]) is list:
                    comments = el[1]

            if type(el[-1]) is bool:
                flag = el[-1]
        else:
            value = el

        if flag:
            if value:
                if concate:
                    for e in value:
                        self.children.append(e)
                else:
                    self.children.append(value)
            for e in comments:
                self.children.append(e)

        return flag

    def concat(self, el):
        return self.append(el, True)

    def skip(self, el):
        if type(el) is tuple and len(el) == 2 and type(el[1]) is bool:
            return el[1]

        return el

    def normalize(self):
        if len(self.children) == 1:
            return self.children[0]
        return self

    def dropExceptionIfEmpty(self):
        if self.count() == 0:
            raise analyzer.AnalyzerException(self.name, 'empty node')

        return self

    def __str__(self):
        s = self.name + '(' + ', '.join( str(child) for child in self.children ) + ')'
        return s




