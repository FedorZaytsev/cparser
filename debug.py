import Node
import lexer
import json

def printNode1(node, padding):
    str = ''
    if type(node) is Node.Node:
        str += padding + node.name+'(\n'
        childs = []
        for ch in node:
            childs.append(printNode1(ch, padding + '  '))
        str += ',\n'.join(childs)
        str += '\n' + padding + ')'
        return str
    elif type(node) is lexer.Lexem:
        str += padding + node.__str__()
        return str


def printNode(node):
    print(printNode1(node, ''))


def printNodeWithSkip1(node, padding):
    str = ''
    if type(node) is Node.Node:
        if node.count() > 1:
            str += padding + node.name+'(\n'
            childs = []
            for ch in node:
                childs.append(printNodeWithSkip1(ch, padding + '  '))
            str += ',\n'.join(childs)
            str += '\n' + padding + ')'
            return str
        else:
            return printNodeWithSkip1(node.get(0), padding)
    elif type(node) is lexer.Lexem:
        str += padding + node.__str__()
        return str


def printNodeWithSkip(node):
    print(printNodeWithSkip1(node, ''))


def Node2Json(node):
    def generateDictionaryRec(node):
        childs = []
        for child in node:
            if type(child) is Node.Node:
                childs.append(generateDictionaryRec(child))
            elif type(child) is lexer.Lexem:
                childs.append(child.getType())

        return {'name': node.name, 'childs': childs}

    return json.dumps(generateDictionaryRec(node),sort_keys=True, indent=4)


def compare(node, dict):
    if node.name != dict['name']:
        return False
    if len(node.children) != len(dict['childs']):
        return False
    for i in range(len(node.children)):
        e1 = node.get(i)
        e2 = dict['childs'][i]
        if type(e1) is lexer.Lexem:
            if e1.getType() != e2:
                return False
        elif not compare(e1, e2):
            return False

    return True

