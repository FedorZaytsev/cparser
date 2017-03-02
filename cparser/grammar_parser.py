import sys

mytokens = []
myrules = {}

def parseWhitespaces(data, ptr):
    while ptr < len(data) and (data[ptr].isspace() or data[ptr] == '\n'):
        ptr += 1
    return ptr


def getLexem(data, ptr):
    ptr = parseWhitespaces(data, ptr)
    beginning = ptr
    while ptr < len(data) and not data[ptr].isspace() and not data[ptr] == '\n':
        ptr += 1
    return data[beginning: ptr], ptr


def parseToken(data, ptr):
    end = ptr
    if data.find('%token', ptr) == ptr:
        if data.find('\n', ptr) != -1:
            end = data.find('\n', ptr) + 1
            data = data[ptr: end - 1]
        _, ptr = getLexem(data, data.find('\n'))
        tokens = []
        while ptr < len(data):
            token, ptr = getLexem(data, ptr)
            tokens.append(invert(token))
        return tokens, end
    return [], end


def parseStartPoint(data, ptr):
    startLexem = '%start'
    if data.find(startLexem, ptr) == ptr:
        _, ptr = getLexem(data, data.find(startLexem, ptr) + len(startLexem))
    return ptr


def skipComments(data):
    isComment = False
    newData = ""
    for idx in range(len(data)):
        if data.find('/*', idx, idx+3) == idx:
            isComment = True
        if idx >= 2 and data.find('*/', idx-2, idx) == idx-2:
            isComment = False
        if not isComment:
            newData += data[idx]
    return newData


def invert(str):
    return str
    if str[0].lower() == str[0]:
        return str.upper()
    return str.lower()


def addToken(str):
    global mytokens
    if not str in mytokens:
        mytokens.append(str)


def isTerminal(str):
    if str[0] == '\'' and str[len(str)-1] == '\'':
        return True
    return str.upper() == str


def postProcess(str):
    if str[0] == '\'':
        return str[1:-1]
    return str

def parseRule(data, ptr):
    global myrules
    name, ptr = getLexem(data, ptr)
    name = invert(name)
    temp, ptr = getLexem(data, ptr)
    if temp != ':':
        print(data[ptr:])
        sys.exit(0)

    assert(temp == ':')
    temp, ptr = getLexem(data, ptr)
    temp = invert(temp)
    rules = []
    rule = ""
    while temp != ';':
        if temp == '|':
            temp, ptr = getLexem(data, ptr)
        lrule = ""
        while temp != ';' and temp != '|':
            lrule += '"' + postProcess(temp) + '", '
            temp, ptr = getLexem(data, ptr)
        lrule = '{' + lrule[:-2] + '}'

        rule += lrule + ', '

    print("m_rules[\"{}\"] = ".format(name) + "{" + rule[:-2] + "};")

    assert(not name in myrules)
    myrules[name] = rules
    return ptr


def printTokens(toks):
    str = "tokens "
    for t in toks:
        str += "<"+t+">" + ", "
    print(str[:-2]+".")

"""
def generateFirstForRule(rule, first):
    if isTerminal(rule)


def calculateFirst(rules):

    result = {}
    changed = True
    while changed:
        for key, v in rules:
            for rule in v:
                f = generateFirstForRule(rule, result)

                if not key in result:
                    result[key] = []

                ....



    return first
"""

def main():
    global mytokens
    global myrules
    with open("grammar.txt") as f:
        lines = skipComments(f.read())
        ptr = 0
        for i in range(13):
            toks, ptr = parseToken(lines, ptr)
            mytokens += toks
        ptr = parseWhitespaces(lines, ptr)
        while ptr < len(lines):
            ptr = parseRule(lines, ptr)
            ptr = parseWhitespaces(lines, ptr)
        printTokens(mytokens)
        print(myrules)

        #calculateFirst(myrules)







if __name__ == "__main__":
    main()
