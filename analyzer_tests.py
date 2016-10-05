import lexer
import analyzer


def process(source, func):
    lex = lexer.Lexer(source)
    syntax = analyzer.Analyzer(lex)
    return getattr(syntax, func)()


def catcherror(source, func):
    try:
        node = process(source, func)
    except analyzer.AnalyzerException as e:
        pass


def testEl(node, idx, name):
    if type(idx) is int:
        assert node.get(idx).getType() == name
    if type(idx) is list:
        n = node
        for i in idx:
            n = n.get(i)

        assert n.getType() == name



def test_storage_class_specifier():
    arr = [['typedef', 'TYPEDEF'], ['extern', 'EXTERN'], ['static', 'STATIC'], ['_Thread_local', 'THREAD_LOCAL'], ['auto', 'AUTO'], ['register', 'REGISTER']]
    for el in arr:
        node = process(el[0], 'parse_storage_class_specifier')
        assert(node.size() == 1)
        assert(node.get(0).getType() == el[1])

    try:
        node = process('enum', 'parse_storage_class_specifier')
    except analyzer.AnalyzerException as e:
        pass


def test_type_qualifier():
    arr = [['const', 'CONST'], ['restrict', 'RESTRICT'], ['volatile', 'VOLATILE'], ['_Atomic', 'ATOMIC']]
    for el in arr:
        node = process(el[0], 'parse_type_qualifier')
        assert(node.size() == 1)
        assert(node.get(0).getType() == el[1])

    catcherror('enum', 'parse_storage_class_specifier')

    catcherror('123', 'parse_storage_class_specifier')


def test_function_specifier():
    arr = [['inline', 'INLINE'], ['_Noreturn', 'NORETURN']]
    for el in arr:
        node = process(el[0], 'parse_function_specifier')
        assert node.size() == 1
        assert node.get(0).getType() == el[1]

    catcherror('test', 'parse_function_specifier')


def test_type_qualifier_list():
    node = process('const  const   const \n volatile', 'parse_type_qualifier_list')
    assert node.size() == 4
    assert node.get(0).getType() == 'CONST'
    assert node.get(1).getType() == 'CONST'
    assert node.get(2).getType() == 'CONST'
    assert node.get(3).getType() == 'VOLATILE'


def test_pointer():
    node = process('*', 'parse_pointer')
    assert node.size() == 1
    assert node.get(0).getType() == '*'

    node = process('** const _Atomic volatile ** const', 'parse_pointer')
    assert node.size() == 8
    testEl(node, 0, '*')
    testEl(node, 1, '*')
    testEl(node, 2, 'CONST')
    testEl(node, 3, 'ATOMIC')
    testEl(node, 4, 'VOLATILE')
    testEl(node, 5, '*')
    testEl(node, 6, '*')
    testEl(node, 7, 'CONST')

def test_primary_expression():
    arr = ['my_cool_var   ', '0x55', '1234', '"abcd"', '']


def test_generic_selection():
    node = process('_Generic( \'a\', char: 1, int: 2, long: 3, default: 0)', 'parse_generic_selection')
    print(node)



test_storage_class_specifier()
test_type_qualifier()
test_function_specifier()
test_type_qualifier_list()
test_pointer()
test_primary_expression()
test_generic_selection()
