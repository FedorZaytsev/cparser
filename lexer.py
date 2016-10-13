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
        if self.isEnd():
            return chr(0)
        return self.text[self.position]

    def getString(self, end):
        return self.text[self.position: end.position]

    def getStringForDebug(self):
        return self.text[self.position:]

    # Check is substring beginning from self.ptr match str
    def match(self, str2):
        return self.text.find(str2, self.position, self.position + len(str2) + 1) == self.position

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

    def __str__(self):
        return "Lexem('{}', {})".format(self.representation, self.type)


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
        'auto': 'AUTO',
        'break': 'BREAK',
        'case': 'CASE',
        'char': 'CHAR',
        'const': 'CONST',
        'continue': 'CONTINUE',
        'default': 'DEFAULT',
        'do': 'DO',
        'double': 'DOUBLE',
        'else': 'ELSE',
        'enum': 'ENUM',
        'extern': 'EXTERN',
        'float': 'FLOAT',
        'for': 'FOR',
        'goto': 'GOTO',
        'if': 'IF',
        'inline': 'INLINE',
        'int': 'INT',
        'long': 'LONG',
        'register': 'REGISTER',
        'restrict': 'RESTRICT',
        'return': 'RETURN',
        'short': 'SHORT',
        'signed': 'SIGNED',
        'sizeof': 'SIZEOF',
        'static': 'STATIC',
        'struct': 'STRUCT',
        'switch': 'SWITCH',
        'typedef': 'TYPEDEF',
        'union': 'UNION',
        'unsigned': 'UNSIGNED',
        'void': 'VOID',
        'volatile': 'VOLATILE',
        'while': 'WHILE',
        '_Alignas': 'ALIGNAS',
        '_Alignof': 'ALIGNOF',
        '_Atomic': 'ATOMIC',
        '_Bool': 'BOOL',
        '_Complex': 'COMPLEX',
        '_Generic': 'GENERIC',
        '_Imaginary': 'IMAGINARY',
        '_Noreturn': 'NORETURN',
        '_Static_assert': 'STATIC_ASSERT',
        '_Thread_local': 'THREAD_LOCAL',
        '__func__': 'FUNC_NAME',
    }

    def __init__(self, data):
        assert (type(data) is str)
        self.data = data
        self.ptr = Position(data, 0, 1, 1)
        self.current_lexem_id = -1
        self.LEXEM = None
        self.lst = []
        self.states = []

        while not self.ptr.isEnd():
            if self.parsePreprocessor(): continue
            if self.parseWhitespace(): continue
            if self.parseComment(): continue
            if self.parseOperators(): continue
            if self.parseIdent(): continue
            if self.parseInt(): continue
            if self.parseFloat(): continue
            if self.parseString(): continue

            print("Unknown token '{}'".format(self.ptr.getStringForDebug()))
            raise Exception("Unknown token")

    # [0-7]
    def parseO(self, ptr):
        ch = ptr.getChar()
        if ch in '01234567':
            ptr.next()
            return True
        return False

    # [0-9]
    def parseD(self, ptr):
        ch = ptr.getChar()
        if ch.isdigit():
            ptr.next()
            return True
        return False

    # [a-zA-Z_]
    def parseL(self, ptr):
        ch = ptr.getChar()
        if ch.isalpha() or ch == '_':
            ptr.next()
            return True
        return False

    # [a-zA-Z_0-9]
    def parseA(self, ptr):
        return self.parseD(ptr) or self.parseL(ptr)

    # (0[xX])
    def parseHP(self, ptr):
        if ptr.match("0x") or ptr.match("0X"):
            ptr.inc(2)
            return True
        return False

    # [a-fA-F0-9]
    def parseH(self, ptr):
        ch = ptr.getChar()
        if ch.isdigit() or ch.lower() in 'abcdef':
            ptr.next()
            return True
        return False

    # (((u|U)(l|L|ll|LL)?)|((l|L|ll|LL)(u|U)?))
    def parseIS(self, ptr):
        def parseuU(ptr):
            if ptr.getChar() in 'uU':
                ptr.next()
                return True
            return False

        def parselLllLL(ptr):
            if ptr.match('ll') or ptr.match('LL'):
                ptr.next(2)
                return True
            if ptr.getChar() in 'lL':
                ptr.next()
                return True
            return False

        end = copy.copy(ptr)
        if parseuU(end):
            if parselLllLL(end):
                ptr.inc(3)
            else:
                ptr.inc(1)
            return True
        if parselLllLL(end):
            if parseuU(end):
                ptr.inc(3)
            else:
                ptr.inc(2)
            return True
        return False

    # [1-9]
    def parseNZ(self, ptr):
        ch = ptr.getChar()
        if ch.isdigit() and ch != '0':
            ptr.next()
            return True
        return False

    # ([Ee][+-]?{D}+)
    def parseE(self, ptr):
        end = copy.copy(ptr)
        if end.getChar().lower() != 'e':
            return False
        end.next()
        if end.getChar() == '+' or end.getChar() == '-':
            end.next()

        if not end.getChar().isdigit():
            return False

        # skip [Ee]
        ptr.next()
        if ptr.getChar() == '+' or ptr.getChar() == '-':
            ptr.next()
        self.parseOneOrMore(self.parseD, ptr)
        return True

    # (u|U|L)
    def parseCP(self, ptr):
        if ptr.getChar() in 'uUL':
            ptr.next()
            return True
        return False

    # (f|F|l|L)
    def parseFS(self, ptr):
        if ptr.getChar().lower() == 'f' or ptr.getChar().lower() == 'l':
            ptr.next()
            return True
        return False

    # ([Pp][+-]?{D}+)
    def parseP(self, ptr):
        if ptr.getChar().lower() != 'p':
            return False
        ptr.next()
        if ptr.getChar() == '+' or ptr.getChar() == '-':
            ptr.next()
        return self.parseOneOrMore(self.parseD, ptr)

    # (u8|u|U|L)
    def parseSP(self, ptr):
        if ptr.match('u8'):
            ptr.inc(2)
            return True
        if ptr.getChar().lower == 'u' or ptr.getChar() == 'L':
            ptr.next()
            return True
        return False

    # {A}*
    def parseRec(self, f, ptr):
        while f(ptr):
            pass
        return True

    # {A}?
    def parseProb(self, f, ptr):
        f(ptr)
        return True

    # {A}+
    def parseOneOrMore(self, f, ptr):
        if not f(ptr):
            return False
        return self.parseRec(f, ptr)

    # {L}{A}*
    # IDENTIFIER
    def parseIdent(self):
        end = copy.copy(self.ptr)
        if not self.parseL(end):
            return False

        self.parseRec(self.parseA, end)

        rep = self.ptr.getString(end)
        if rep in self.keywords:
            self.pushLexem(self.keywords[rep], rep)
        else:
            self.pushLexem("IDENTIFIER", rep)
        return True

    # I_CONSTANT
    def parseInt(self):

        parsers = [self.parseInt1, self.parseInt2, self.parseInt3, self.parseInt4]

        for f in parsers:
            end = copy.copy(self.ptr)
            if f(end):
                self.pushLexem("I_CONSTANT", self.ptr.getString(end))
                return True

        return False

    # {HP}{H}+{IS}?
    # I_CONSTANT
    def parseInt1(self, end):
        if not self.parseHP(end):
            return False
        if not self.parseOneOrMore(self.parseH, end):
            return False
        self.parseProb(self.parseIS, end)

        return True

    # {NZ}{D}*{IS}?
    # I_CONSTANT
    def parseInt2(self, end):
        if not self.parseNZ(end):
            return False

        self.parseRec(self.parseD, end)
        self.parseProb(self.parseIS, end)

        return True

    # "0"{O}*{IS}?
    # I_CONSTANT
    def parseInt3(self, end):
        if end.getChar() != '0':
            return False
        self.parseRec(self.parseO, end)
        self.parseProb(self.parseIS, end)

        return True

    # CP?'(\\.|[^\\'])+'
    # I_CONSTANT
    # regexp changed becouse of too much complexity
    # this regexp can accept char constants with errors, but who cares?
    def parseInt4(self, end):
        self.parseProb(self.parseCP, end)
        if end.getChar() != '\'':
            return False
        end.next()
        while end.getChar() != '\'':
            end.next()
        end.next()
        return True

    def parseFloat(self):
        parsers = [self.parseFloat1, self.parseFloat2, self.parseFloat3, self.parseFloat4, self.parseFloat5,
                   self.parseFloat6]
        for f in parsers:
            end = copy.copy(self.ptr)
            if f(end):
                self.pushLexem("F_CONSTANT", self.ptr.getString(end))
                return True

        return False

    # {D}+{E}{FS}?
    # F_CONSTANT
    def parseFloat1(self, ptr):
        if not self.parseOneOrMore(self.parseD, ptr):
            return False

        if not self.parseE(ptr):
            return False

        self.parseProb(self.parseFS, ptr)
        return True

    # {D}*"."{D}+{E}?{FS}?
    # F_CONSTANT
    def parseFloat2(self, ptr):
        self.parseRec(self.parseD, ptr)
        if not ptr.getChar == '.':
            return False
        ptr.next()

        if not self.parseOneOrMore(self.parseD, ptr):
            return False

        self.parseProb(self.parseE, ptr)
        self.parseProb(self.parseFS, ptr)

        return True

    # {D}+"."{E}?{FS}?
    # F_CONSTANT
    def parseFloat3(self, ptr):
        if not self.parseOneOrMore(self.parseD, ptr):
            return False
        if not ptr.getChar() == '.':
            return False
        ptr.next()
        self.parseProb(self.parseE, ptr)
        self.parseProb(self.parseFS, ptr)
        return True

    # {HP}{H}+{P}{FS}?
    # F_CONSTANT
    def parseFloat4(self, ptr):
        if not self.parseHP(ptr):
            return False
        if not self.parseOneOrMore(self.parseH, ptr):
            return False
        if not self.parseP(ptr):
            return False
        self.parseProb(self.parseFS, ptr)
        return True

    # {HP}{H}*"."{H}+{P}{FS}?
    # F_CONSTANT
    def parseFloat5(self, ptr):
        if not self.parseHP(ptr):
            return False
        self.parseRec(self.parseH, ptr)
        if ptr.getChar() != '.':
            return False
        ptr.next()
        if not self.parseOneOrMore(self.parseH, ptr):
            return False
        self.parseH(ptr)
        self.parseProb(self.parseFS, ptr)
        return True

    # {HP}{H}+"."{P}{FS}?
    # F_CONSTANT
    def parseFloat6(self, ptr):
        if not self.parseHP(ptr):
            return False
        if not self.parseOneOrMore(self.parseH, ptr):
            return False
        if ptr.getChar() != '.':
            return False
        ptr.next()
        if not self.parseP(ptr):
            return False
        self.parseProb(self.parseFS, ptr)
        return True

    # L?\"(\\.|[^\\"])*\"
    def parseString(self):
        end = copy.copy(self.ptr)
        self.parseL(end)
        if end.getChar() != '"':
            return False
        end.next()
        while True:
            if end.match('\\"'):
                end.inc(2)
                continue
            if end.getChar() == '"':
                end.next()
                break
            end.next()
        self.pushLexem("STRING_LITERAL", self.ptr.getString(end))
        return True

    def parseComment(self):
        end = copy.copy(self.ptr)
        if end.match("//"):
            while end.getChar() != '\n':
                end.next()
            self.pushLexem("COMMENT", self.ptr.getString(end))
            return True
        if end.match("/*"):
            while not end.match("*/"):
                end.next()
            end.inc(2)
            self.pushLexem("COMMENT", self.ptr.getString(end))
            return True
        return False

    def parsePreprocessor(self):
        end = copy.copy(self.ptr)
        if end.getChar() == '#' and (len(self.lst) == 0 or (len(self.lst) > 0 and self.lst[-1].getType() == 'NEWLINE')):
            while True:
                if end.match('\\\n'):
                    end.inc(2)
                    continue
                if end.isEnd():
                    self.ptr = end
                    return True
                if end.getChar() == '\n':
                    # CHECK THIS POINT
                    end.next()
                    self.ptr = end
                    return True
                end.next()
        return False

    def parseWhitespace(self):
        if self.ptr.getChar() == '\n':
            self.pushLexem('NEWLINE', self.ptr.getChar())
            return True

        if self.ptr.getChar().isspace():
            self.pushLexem('SPACE', self.ptr.getChar())
            return True
        return False

    def parseOperators(self):
        bestk = ''
        bestv = ''
        for k, v in self.operators.items():
            if self.ptr.match(k):
                if len(k) > len(bestk):
                    bestk = k
                    bestv =v
        if len(bestk) > 0:
            self.pushLexem(bestv, bestk)
            return True
        return False

    def pushLexem(self, name, representation):
        #print("Found lexem {} '{}' '{}'".format(self.ptr, name, representation))
        self.ptr.inc(len(representation))
        self.lst.append(Lexem(self.ptr, representation, name))
        if self.LEXEM is None:
            self.LEXEM = self.lst[0]

    def get(self):
        if self.current_lexem_id == -1:
            self.next()
        if self.current_lexem_id >= len(self.lst):
            return Lexem(self.ptr, 'EOF', 'EOF')
        return self.lst[self.current_lexem_id]

    def next(self):
        self.current_lexem_id += 1
        while self.current_lexem_id < len(self.lst) and (self.lst[self.current_lexem_id].getType() == "NEWLINE" or
                                                         self.lst[self.current_lexem_id].getType() == "SPACE" or
                                                         self.lst[self.current_lexem_id].getType() == "COMMENT"
                                                         ):
            self.current_lexem_id += 1

        if self.current_lexem_id < len(self.lst):
            self.LEXEM = self.lst[self.current_lexem_id]
        else:
            self.LEXEM = None

    def pushState(self):
        self.states.append({'ptr': self.current_lexem_id})

    def popState(self):
        state = self.states[-1]
        self.current_lexem_id = state['ptr']
        if self.current_lexem_id < len(self.lst):
            self.LEXEM = None
            if self.current_lexem_id != -1:
                self.LEXEM = self.lst[self.current_lexem_id]
        else:
            self.LEXEM = None
        self.removeSavedState()

    def removeSavedState(self):
        self.states = self.states[:-1]

    def getComments(self):
        lst = []
        ptr = self.current_lexem_id + 1
        while ptr < len(self.lst):
            lexem = self.lst[ptr]
            if lexem.getType() == 'SPACE' or lexem.getType() == 'NEWLINE':
                ptr += 1
                continue
            if lexem.getType() == 'COMMENT':
                lst.append(lexem)
                ptr += 1
                continue

            break

        return lst

