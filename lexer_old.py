import copy


class Position:
    def __init__(self, text, position, line, column):
        self.position = position
        self.line = line
        self.column = column
        self.text = text

    def copy(self):
        return Position(self.text, self.position, self.line, self.column)

    def next(self):
        if self.position < len(self.text):
            if self.text[self.position] == '\n':
                self.column = 0
                self.line += 1
            self.position += 1
            self.column += 1
        else:
            raise Exception("End of file")

    def inc(self, size):
        for i in range(0, size):
            self.next()

    def isEnd(self):
        return self.position >= len(self.text)

    def getChar(self):
        assert not self.isEnd()
        return self.text[self.position]

    def getString(self, end):
        return self.text[self.position: end.position]

    def getStringForDebug(self):
        return self.text[self.position:]

    # Check is substring beginning from self.ptr match str
    def match(self, str2):
        return self.text.find(str2, self.position) == self.position

    def __eq__(self, other):
        return self.position == other.position

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "{} of {} ({}, {})".format(self.position, len(self.text), self.line, self.column)


class Lexem:
    def __init__(self, position, representation, t):
        self.position = position
        self.representation = representation
        self.type = t

    def getType(self):
        return self.type


class Lexer:
    operators = {
        "...": 'ELLIPSIS',
        ">>=": 'RIGHT_ASSIGN',
        "<<=": 'LEFT_ASSIGN',
        "+=": 'ADD_ASSIGN',
        "-=": 'SUB_ASSIGN',
        "*=": 'MUL_ASSIGN',
        "/=": 'DIV_ASSIGN',
        "%=": 'MOD_ASSIGN',
        "&=": 'AND_ASSIGN',
        "^=": 'XOR_ASSIGN',
        "|=": 'OR_ASSIGN',
        ">>": 'RIGHT_OP',
        "<<": 'LEFT_OP',
        "++": 'INC_OP',
        "--": 'DEC_OP',
        "->": 'PTR_OP',
        "&&": 'AND_OP',
        "||": 'OR_OP',
        "<=": 'LE_OP',
        ">=": 'GE_OP',
        "==": 'EQ_OP',
        "!=": 'NE_OP',
        ";": ';',
        "{": '{',
        "<%": '{',
        "}": '}',
        "%>": '}',
        ",": ',',
        ":": ':',
        "=": '=',
        "(": '(',
        ")": ')',
        "[": '[',
        "<:": '[',
        "]": ']',
        ":>": ']',
        ".": '.',
        "&": '&',
        "!": '!',
        "~": '~',
        "-": '-',
        "+": '+',
        "*": '*',
        "/": '/',
        "%": '%',
        "<": '<',
        ">": '>',
        "^": '^',
        "|": '|',
        "?": '?',
    }

    keywords = {
        "auto": 'AUTO',
        "break": 'BREAK',
        "case": 'CASE',
        "char": 'CHAR',
        "const": 'CONST',
        "continue": 'CONTINUE',
        "default": 'DEFAULT',
        "do": 'DO',
        "double": 'DOUBLE',
        "else": 'ELSE',
        "enum": 'ENUM',
        "extern": 'EXTERN',
        "float": 'FLOAT',
        "for": 'FOR',
        "goto": 'GOTO',
        "if": 'IF',
        "int": 'INT',
        "long": 'LONG',
        "register": 'REGISTER',
        "return": 'RETURN',
        "short": 'SHORT',
        "signed": 'SIGNED',
        "sizeof": 'SIZEOF',
        "static": 'STATIC',
        "struct": 'STRUCT',
        "switch": 'SWITCH',
        "typedef": 'TYPEDEF',
        "union": 'UNION',
        "unsigned": 'UNSIGNED',
        "void": 'VOID',
        "volatile": 'VOLATILE',
        "while": 'WHILE',
    }

    lst = []

    def __init__(self, data):
        self.data = data
        self.ptr = Position(data, 0, 1, 1)

        while not self.ptr.isEnd():
            if self.parsePreprocessor():
                continue
            if self.parseWhitespace():
                continue
            if self.parseComment():
                continue
            if self.parseOperators():
                continue
            if self.parseNumber():
                continue
            if self.parseString():
                continue
            if self.parseExpression():
                continue

            print("Unknown token '{}'".format(self.ptr.getStringForDebug()))
            raise Exception("Unknown token")

    def parsePreprocessor(self):
        assert not self.ptr.isEnd()

        if (len(self.lst) > 0 and self.getLastLexem().getType() == "newline" or len(self.lst) == 0) and \
                        self.ptr.getChar() == '#':
            while not self.ptr.isEnd() and self.ptr.getChar() != '\n':
                self.ptr.next()
            if not self.ptr.isEnd():
                self.ptr.next()
            return True
        return False

    def parseComment(self):
        assert not self.ptr.isEnd()
        if self.ptr.match("//"):
            end = copy.copy(self.ptr)
            end.inc(2)
            while end.getChar() != '\n':
                end.next()
            end.next()
            self.pushLexem("comment", self.ptr.getString(end))
            return True
        if self.ptr.match("/*"):
            end = copy.copy(self.ptr)
            end.inc(2)
            while not end.match("*/"):
                end.next()
            end.inc(2)
            self.pushLexem("comment", self.ptr.getString(end))
            return True
        return False

    def parseWhitespace(self):
        assert not self.ptr.isEnd()
        if self.ptr.getChar().isspace():
            name = 'space'
            if self.ptr.getChar() == '\n':
                name = 'newline'
            self.pushLexem(name, self.ptr.getChar())
            return True
        return False

    # L?\"(\\.|[^\\"])*\"
    def parseString(self):
        assert not self.ptr.isEnd()

        end = copy.copy(self.ptr)
        if end.getChar().isalpha() or end.getChar() == '_':
            end.next()

        if end.getChar() == "\"":
            end.next()
            while end.getChar() != "\"":
                if end.match("\\\""):
                    end.next()
                end.next()
            end.next()
            self.pushLexem("string", self.ptr.getString(end))
            return True
        return False

    def parseOperators(self):
        assert not self.ptr.isEnd()

        def chooseBestMatchLexem(blexem, lexem):

            if blexem is None:
                return lexem

            if len(blexem[1]) > len(lexem[1]):
                return blexem
            if len(lexem[1]) > len(blexem[1]):
                return lexem

            raise Exception("Tokens with the same size {}'{}' {}'{}'".format(blexem[0], blexem[1], lexem[0], lexem[1]))

        bestLexem = None
        for lexem, name in self.operators.items():
            if self.ptr.match(lexem):
                bestLexem = chooseBestMatchLexem(bestLexem, [name, lexem])

        if bestLexem is not None:
            self.pushLexem(bestLexem[0], bestLexem[1])
            return True
        return False

    def parseNumber(self):
        assert not self.ptr.isEnd()

        end = copy.copy(self.ptr)

        def isHexChar(ptr):
            ch = ptr.getChar().lower()
            return ch.isdigit() or ch == 'a' or ch == 'b' or ch == 'c' or ch == 'd' or ch == 'e' or ch == 'f'

        def IsIS(end):
            return end.getChar() == 'u' or end.getChar() == 'U' or end.getChar() == 'l' or end.getChar() == 'L'

        def IsFS(end):
            return end.getChar() == 'f' or end.getChar() == 'F' or end.getChar() == 'l' or end.getChar() == 'L'

        # parse float

        # [Ee][+-]?{D}+
        def parseE(ptr):
            if ptr.match("e") or ptr.match("E"):
                ptr.next()
                if ptr.match("-") or ptr.match("+"):
                    ptr.next()
                while ptr.getChat().isdigit():
                    ptr.next()
                return True
            return False

        # {D}+{E}{FS}?
        if end.getChar().isdigit():
            while end.getChar().isdigit():
                end.next()
            if parseE(end):
                if IsFS(end):
                    end.next()
                self.pushLexem("constant", self.ptr.getString(end))
                return True
            else:
                end = copy.copy(self.ptr)

        # {D}*"."{D}+({E})?{FS}?
        if end.getChar().isdigit() or end.match("."):
            while end.getChar().isdigit():
                end.next()
            if end.match("."):
                end.next()
                if end.getChar().isdigit():
                    while end.getChar().isdigit():
                        end.next()
                    parseE(end)
                    if IsFS(end):
                        end.next()
                    self.pushLexem("constant", self.ptr.getString(end))
                else:
                    end = copy.copy(self.ptr)
            else:
                end = copy.copy(self.ptr)

        # {D}+"."{D}*({E})?{FS}?
        if end.getChar().isdigit():
            while end.getChar().isdigit():
                end.next()
            if end.match("."):
                end.next()
                while end.getChar().isdigit():
                    end.next()
                parseE(end)
                if IsFS(end):
                    end.next()
                self.pushLexem("constant", self.ptr.getString(end))
            else:
                end = copy.copy(self.ptr)

        # parse int
        # 0[xX]{H}+{IS}?
        if end.match("0x") or end.match("0X"):
            end.inc(2)
            while isHexChar(end):
                end.next()
            if IsIS(end):
                end.next()
            self.pushLexem("constant", self.ptr.getString(end))
            return True

        # 0{D}+{IS}?
        if end.match("0"):
            end.next()
            if end.getChar().isdigit():
                while end.getChar().isdigit():
                    end.next()
                if IsIS(end):
                    end.next()
                self.pushLexem("constant", self.ptr.getString(end))
                return True
            else:
                end = copy.copy(self.ptr)

        # {D}+{IS}?
        if end.getChar().isdigit():
            while end.getChar().isdigit():
                end.next()
            if IsIS(end):
                end.next()
            self.pushLexem("constant", self.ptr.getString(end))
            return True

        # char constant
        # L?'(\\.|[^\\'])+'
        if end.getChar().isalpha() or end.getChar() == '_':
            end.next()
        if not end.isEnd() and end.getChar() == '\'':
            end.next()

            while end.getChar() != '\'':
                if end.match("\\'"):
                    end.next()
                end.next()
            end.next()
            self.pushLexem("constant", self.ptr.getString(end))
            return True
        else:
            end = copy.copy(self.ptr)

        return False

    def parseExpression(self):
        assert not self.ptr.isEnd()

        end = copy.copy(self.ptr)
        if end.getChar().isalpha() or end.getChar() == '_':
            end.next()
            while end.getChar().isalpha() or end.getChar().isdigit() or end.getChar() == '_':
                end.next()

            rep = self.ptr.getString(end)
            if rep in self.keywords:
                self.pushLexem(self.keywords[rep], rep)
            else:
                self.pushLexem("identifier", rep)
            return True
        return False

    def pushLexem(self, name, representation):
        print("Found lexem {} '{}' '{}'".format(self.ptr, name, representation))
        self.ptr.inc(len(representation))
        self.lst.append(Lexem(self.ptr, representation, name))

    def isFinished(self):
        return self.ptr >= len(self.data)

    def getLastLexem(self):
        return self.lst[-1]
