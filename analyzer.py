import Cgrammar
import Node


class AnalyzerException(Exception):
    def __init__(self, rule, message):
        super(AnalyzerException, self).__init__(message)

        self.rule = rule


class Analyzer:
    def __init__(self, lexer):
        self.lexer = lexer
        self.grammar = Cgrammar.CGrammar

    def parse(self):
        return self.parse_translation_unit()

    def try2(self, func, args=[]):
        self.lexer.pushState()
        lnode = None
        try:
            if type(func) is list:
                assert len(args) == 0
                lnode = []
                for f in func:
                    if type(f) is list:
                        lnode.append(f[0](*f[1]))
                    else:
                        lnode.append(f())
            else:
                lnode = func(*args)
        except AnalyzerException:
            self.lexer.popState()
            return lnode, False

        self.lexer.removeSavedState()

        return lnode, True

    def checkLexem(self, rule, arr):
        lexem = self.lexer.get()
        for lex in arr:
            if lexem.getType() == lex:
                comments = self.lexer.getComments()
                self.lexer.next()
                return lexem, comments

        raise AnalyzerException(rule, "expected {} got {}".format(', '.join(arr), lexem))

    def checkFirst(self, rule):
        pass

    def parse_translation_unit(self):
        node = Node.create('translation_unit')

        node.append(self.parse_external_declaration())
        self.parse_translation_unit_lr(node)

        return node

    def parse_translation_unit_lr(self, node):

        if node.append(self.try2(self.parse_external_declaration)):
             self.parse_translation_unit_lr(node)
        return node

    def parse_external_declaration(self):
        node = Node.create('external_declaration')
        if node.append(self.try2(self.parse_function_definition)):
            return node
        if node.append(self.try2(self.parse_declaration)):
            return node

        raise AnalyzerException('external_declaration', '')

    def parse_function_definition(self):
        node = Node.create('function_definition')

        node.append(self.parse_declaration_specifiers())
        node.append(self.parse_declarator())
        node.append(self.try2(self.parse_declaration_list))
        node.append(self.parse_compound_statement())

        return node

    def parse_declaration_specifiers(self):
        node = Node.create('declaration_specifiers')

        if node.append(self.try2(self.parse_storage_class_specifier)):
            node.append(self.try2(self.parse_declaration_specifiers))
            return node

        if node.append(self.try2(self.parse_type_specifier)):
            node.append(self.try2(self.parse_declaration_specifiers))
            return node

        if node.append(self.try2(self.parse_type_qualifier)):
            node.append(self.try2(self.parse_declaration_specifiers))
            return node

        if node.append(self.try2(self.parse_function_specifier)):
            node.append(self.try2(self.parse_declaration_specifiers))
            return node

        if node.append(self.try2(self.parse_alignment_specifier)):
            node.append(self.try2(self.parse_declaration_specifiers))
            return node

        raise AnalyzerException('declaration_specifiers', '')

    # tested
    def parse_storage_class_specifier(self):
        node = Node.create('storage_class_specifier')
        arr = ['TYPEDEF', 'EXTERN', 'STATIC', 'THREAD_LOCAL', 'AUTO', 'REGISTER']
        if node.append(self.try2(self.checkLexem, ['storage_class_specifier', arr])):
            return node

        raise AnalyzerException('storage_class_specifier',
                                'expected {} got {}'.format(', '.join(arr), self.lexer.get().getType()))

    def parse_type_specifier(self):
        node = Node.create('type_specifier')
        arr = ['VOID', 'CHAR', 'SHORT', 'INT', 'LONG', 'FLOAT', 'DOUBLE', 'SIGNED', 'UNSIGNED', 'BOOL', 'COMPLEX',
               'IMAGINARY']

        if node.append(self.try2(self.checkLexem, ['type_specifier', arr])):
            return node

        if node.append(self.try2(self.parse_atomic_type_specifier)):
            return node

        if node.append(self.try2(self.parse_struct_or_union_specifier)):
            return node

        if node.append(self.try2(self.parse_enum_specifier)):
            return node

        # TODO change that to TYPEDEF_NAME
        #if node.append(self.try2(self.checkLexem, ['type_specifier', ['IDENTIFIER']])):
        #    return node

        raise AnalyzerException('type_specifier',
                                'expected {}, atomic_type, struct, union, enum or identifier got {}'.format(
                                    ', '.join(arr), self.lexer.get().getType()))

    # tested
    def parse_type_qualifier(self):
        node = Node.create('type_qualifier')

        arr = ['CONST', 'RESTRICT', 'VOLATILE', 'ATOMIC']
        node.append(self.checkLexem('type_qualifier', arr))

        return node

    # tested
    def parse_function_specifier(self):
        node = Node.create('function_specifier')
        arr = ['INLINE', 'NORETURN']
        if node.append(self.try2(self.checkLexem, ['function_specifier', arr])):
            return node

        raise AnalyzerException('type_qualifier',
                                'expected {} got {}'.format(', '.join(arr), self.lexer.get().getType()))

    def parse_alignment_specifier(self):
        node = Node.create('alignment_specifier')

        node.append(self.checkLexem('alignment_specifier', ['ALIGNAS']))
        node.append(self.checkLexem('alignment_specifier', ['(']))

        if node.append(self.try2(self.parse_type_name)):
            node.append(self.checkLexem('alignment_specifier', [')']))
            return node

        if node.append(self.try2(self.parse_constant_expression)):
            node.append(self.checkLexem('alignment_specifier', [')']))
            return node

        raise AnalyzerException('alignment_specifier', 'not a type name or constant expression')

    def parse_type_name(self):
        node = Node.create('type_name')

        node.append(self.parse_specifier_qualifier_list())
        node.append(self.try2(self.parse_abstract_declarator))

        return node

    def parse_specifier_qualifier_list(self):
        node = Node.create('specifier_qualifier_list')

        if node.append(self.try2(self.parse_type_specifier)):
            node.append(self.try2(self.parse_specifier_qualifier_list))
            return node

        if node.append(self.try2(self.parse_type_qualifier)):
            node.append(self.try2(self.parse_specifier_qualifier_list))
            return node

        raise AnalyzerException('specifier_qualifier_list', '')

    def parse_abstract_declarator(self):
        node = Node.create('abstract_declarator')

        if node.append(self.try2(self.parse_pointer)):
            node.append(self.try2(self.parse_direct_abstract_declarator))
            return node
        if node.append(self.try2(self.parse_direct_abstract_declarator)):
            return node

        raise AnalyzerException('abstract_declarator', '')

    # tested
    def parse_pointer(self):
        node = Node.create('pointer')

        node.append(self.checkLexem('pointer', ['*']))
        if node.concat(self.try2(self.parse_pointer)):
            return node

        if node.concat(self.try2(self.parse_type_qualifier_list)):
            node.concat(self.try2(self.parse_pointer))
            return node

        return node

    # tested
    def parse_type_qualifier_list(self):
        node = Node.create('type_qualifier_list')

        node.concat(self.parse_type_qualifier())
        self.parse_type_qualifier_list_lr(node)

        return node

    # tested
    def parse_type_qualifier_list_lr(self, node):
        if node.concat(self.try2(self.parse_type_qualifier)):
            self.parse_type_qualifier_list_lr(node)

    def parse_direct_abstract_declarator(self):
        rule_name = 'direct_abstract_declarator'
        node = Node.create(rule_name)

        if node.append(self.try2(self.checkLexem, [rule_name, ['(']])):

            if node.append(self.try2(self.parse_abstract_declarator)):
                node.append(self.checkLexem(rule_name, [')']))
                self.parse_direct_abstract_declarator_lr(node)
                return node

            if node.append(self.try2(self.checkLexem, [rule_name, [')']])):
                self.parse_direct_abstract_declarator_lr(node)
                return node

            if node.append(self.try2(self.parse_parameter_type_list)):
                node.append(self.checkLexem(rule_name, [')']))
                self.parse_direct_abstract_declarator_lr(node)
                return node

        if node.append(self.try2(self.checkLexem, [rule_name, ['[']])):

            if node.append(self.try2(self.checkLexem, [rule_name, [']']])):
                self.parse_direct_abstract_declarator_lr(node)
                return node

            if node.append(self.try2(self.checkLexem, [rule_name, ['*']])):
                node.append(self.checkLexem(rule_name, [']']))
                self.parse_direct_abstract_declarator_lr(node)
                return node

            if node.append(self.try2(self.checkLexem, [rule_name, ['STATIC']])):
                node.append(self.try2(self.parse_type_qualifier_list))
                node.append(self.parse_assignment_expression())
                node.append(self.checkLexem(rule_name, [']']))
                self.parse_direct_abstract_declarator_lr(node)
                return node

            if node.append(self.try2(self.parse_type_qualifier_list)):

                if node.append(self.try2(self.parse_assignment_expression)):
                    node.append(self.checkLexem(rule_name, [']']))
                    self.parse_direct_abstract_declarator_lr(node)
                    return node

                if node.append(self.try2(self.checkLexem, [rule_name, ['STATIC']])):
                    node.append(self.parse_assignment_expression())
                    node.append(self.checkLexem(rule_name, [']']))
                    self.parse_direct_abstract_declarator_lr(node)
                    return node

                if node.append(self.try2(self.checkLexem, [rule_name, [']']])):
                    self.parse_direct_abstract_declarator_lr(node)
                    return node

            if node.append(self.try2(self.parse_assignment_expression)):
                node.append(self.checkLexem(rule_name, [']']))
                self.parse_direct_abstract_declarator_lr(node)
                return node

        raise AnalyzerException('direct_abstract_declarator', '')

    def parse_direct_abstract_declarator_lr(self, node):
        rule_name = 'direct_abstract_declarator_lr'

        if node.append(self.try2(self.checkLexem, [rule_name, ['(']])):

            if node.append(self.try2(self.checkLexem, [rule_name, [')']])):
                node.append(self.parse_direct_abstract_declarator_lr(node))
                return node

            if node.append(self.try2(self.parse_parameter_type_list)):
                node.append(self.checkLexem(rule_name, [')']))
                node.append(self.parse_direct_abstract_declarator_lr(node))
                return node

        if node.append(self.try2(self.checkLexem, [rule_name, ['[']])):

            if node.append(self.try2(self.checkLexem, [rule_name, [']']])):
                node.append(self.parse_direct_abstract_declarator_lr(node))
                return node

            if node.append(self.try2(self.checkLexem, [rule_name, ['*']])):
                node.append(self.checkLexem(rule_name, [']']))
                node.append(self.parse_direct_abstract_declarator_lr(node))
                return node

            if node.append(self.try2(self.checkLexem, [rule_name, ['STATIC']])):
                node.append(self.try2(self.parse_type_qualifier_list))
                node.append(self.parse_assignment_expression())
                node.append(self.checkLexem(rule_name, [']']))
                node.append(self.parse_direct_abstract_declarator_lr(node))
                return node

            if node.append(self.try2(self.parse_type_qualifier_list)):

                if node.append(self.try2(self.parse_assignment_expression)):
                    node.append(self.checkLexem(rule_name, [']']))
                    node.append(self.parse_direct_abstract_declarator_lr(node))
                    return node

                if node.append(self.try2(self.checkLexem, [rule_name, ['STATIC']])):
                    node.append(self.parse_assignment_expression())
                    node.append(self.checkLexem(rule_name, [']']))
                    node.append(self.parse_direct_abstract_declarator_lr(node))
                    return node

                if node.append(self.try2(self.checkLexem, [rule_name, [']']])):
                    node.append(self.parse_direct_abstract_declarator_lr(node))
                    return node

            if node.append(self.try2(self.parse_assignment_expression)):
                node.append(self.checkLexem(rule_name, [']']))
                node.append(self.parse_direct_abstract_declarator_lr(node))
                return node

        return node

    def parse_parameter_type_list(self):
        node = Node.create('parameter_type_list')

        node.append(self.parse_parameter_list())
        if node.append(self.try2(self.checkLexem, ['parameter_type_list', [',']])):
            node.append(self.checkLexem('parameter_type_list', ['ELLIPSIS']))

        return node

    def parse_parameter_list(self):
        node = Node.create('parameter_list')

        node.append(self.parse_parameter_declaration())
        self.parse_parameter_list_lr(node)

        return node

    def parse_parameter_list_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['parameter_list_lr', [',']])):
            node.append(self.parse_parameter_declaration())
            self.parse_parameter_list_lr(node)

        return node

    def parse_parameter_declaration(self):
        node = Node.create('parameter_declaration')

        node.append(self.parse_declaration_specifiers())
        if node.append(self.try2(self.parse_declarator)):
            return node

        if node.append(self.try2(self.parse_abstract_declarator)):
            return node

        return node

    def parse_declarator(self):
        node = Node.create('declarator')

        node.append(self.try2(self.parse_pointer))
        node.append(self.parse_direct_declarator())

        return node

    def parse_direct_declarator(self):
        node = Node.create('direct_declarator')

        if node.append(self.try2(self.checkLexem, ['direct_declarator', ['IDENTIFIER']])):
            self.parse_direct_declarator_lr(node)
            return node

        if node.append(self.try2(self.checkLexem, ['direct_declarator', ['(']])):
            node.append(self.parse_declarator())
            node.append(self.checkLexem('direct_declarator', [')']))
            self.parse_direct_declarator_lr(node)
            return node

        raise AnalyzerException('direct_declarator', '')

    def parse_direct_declarator_lr(self, node):
        rule_name = 'direct_declarator_lr'

        if node.append(self.try2(self.checkLexem, [rule_name, ['(']])):

            if node.append(self.try2(self.checkLexem, [rule_name, [')']])):
                self.parse_direct_declarator_lr(node)
                return node

            if node.append(self.try2(self.parse_parameter_type_list)):
                node.append(self.checkLexem(rule_name, [')']))
                self.parse_direct_declarator_lr(node)
                return node

            if node.append(self.try2(self.parse_identifier_list)):
                node.append(self.checkLexem(rule_name, [')']))
                self.parse_direct_declarator_lr(node)
                return node

        if node.append(self.try2(self.checkLexem, [rule_name, ['[']])):

            if node.append(self.try2(self.checkLexem, [rule_name, [']']])):
                self.parse_direct_declarator_lr(node)
                return node

            if node.append(self.try2(self.checkLexem, [rule_name, ['*']])):
                node.append(self.checkLexem(rule_name, [']']))
                self.parse_direct_declarator_lr(node)
                return node

            if node.append(self.try2(self.checkLexem, [rule_name, ['STATIC']])):
                node.append(self.try2(self.parse_type_qualifier_list))
                node.append(self.parse_assignment_expression())
                node.append(self.checkLexem(rule_name, [']']))
                self.parse_direct_declarator_lr(node)
                return node

            if node.append(self.try2(self.parse_type_qualifier_list)):

                if node.append(self.try2(self.parse_assignment_expression)):
                    node.append(self.checkLexem(rule_name, [']']))
                    self.parse_direct_declarator_lr(node)
                    return node

                if node.append(self.try2(self.checkLexem, [rule_name, ['STATIC']])):
                    node.append(self.parse_assignment_expression())
                    node.append(self.checkLexem(rule_name, [']']))
                    self.parse_direct_declarator_lr(node)
                    return node

                if node.append(self.try2(self.checkLexem, [rule_name, [']']])):
                    self.parse_direct_declarator_lr(node)
                    return node

                if node.append(self.try2(self.checkLexem, [rule_name, ['*']])):
                    node.append(self.checkLexem(rule_name, [']']))
                    self.parse_direct_declarator_lr(node)
                    return node

            if node.append(self.try2(self.parse_assignment_expression)):
                node.append(self.checkLexem(rule_name, [']']))
                self.parse_direct_declarator_lr(node)
                return node

        return node

    def parse_assignment_expression(self):
        node = Node.create('assignment_expression')

        if node.concat(self.try2([self.parse_unary_expression, self.parse_assignment_operator])):
            node.append(self.parse_assignment_expression())
            return node

        if node.append(self.try2(self.parse_conditional_expression)):
            return node

        raise AnalyzerException('assignment_expression', '')

    def parse_conditional_expression(self):
        node = Node.create('conditional_expression')

        node.append(self.parse_logical_or_expression())
        if node.append(self.try2(self.checkLexem, ['conditional_expression', ['?']])):
            node.append(self.parse_expression())
            node.append(self.checkLexem('conditional_expression', [':']))
            node.append(self.parse_conditional_expression())
            return node

        return node

    def parse_logical_or_expression(self):
        node = Node.create('logical_or_expression')

        node.append(self.parse_logical_and_expression())
        self.parse_logical_or_expression_lr(node)

        return node

    def parse_logical_or_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['logical_or_expression_lr', ['OR_OP']])):
            node.append(self.parse_logical_and_expression())
            self.parse_logical_or_expression_lr(node)

        return node

    def parse_logical_and_expression(self):
        node = Node.create('logical_and_expression')

        node.append(self.parse_inclusive_or_expression())
        self.parse_logical_and_expression_lr(node)

        return node

    def parse_logical_and_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['logical_and_expression_lr', ['AND_OP']])):
            node.append(self.parse_inclusive_or_expression())
            self.parse_logical_and_expression_lr(node)

        return node

    def parse_inclusive_or_expression(self):
        node = Node.create('inclusive_or_expression')

        node.append(self.parse_exclusive_or_expression())
        self.parse_inclusive_or_expression_lr(node)

        return node

    def parse_inclusive_or_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['inclusive_or_expression_lr', ['|']])):
            node.append(self.parse_exclusive_or_expression())
            self.parse_inclusive_or_expression_lr(node)

    def parse_exclusive_or_expression(self):
        node = Node.create('exclusive_or_expression')

        node.append(self.parse_and_expression())
        self.parse_exclusive_or_expression_lr(node)

        return node

    def parse_exclusive_or_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['exclusive_or_expression_lr', ['^']])):
            node.append(self.parse_and_expression())
            self.parse_exclusive_or_expression_lr(node)

        return node

    def parse_and_expression(self):
        node = Node.create('and_expression')

        node.append(self.parse_equality_expression())
        self.parse_and_expression_lr(node)

        return node

    def parse_and_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['and_expression_lr', ['&']])):
            node.append(self.parse_equality_expression())
            self.parse_and_expression_lr(node)

        return node

    def parse_equality_expression(self):
        node = Node.create('equality_expression')

        node.append(self.parse_relational_expression())
        self.parse_equality_expression_lr(node)

        return node

    def parse_equality_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['equality_expression_lr', ['EQ_OP', 'NE_OP']])):
            node.append(self.parse_relational_expression())
            self.parse_equality_expression_lr(node)

        return node

    def parse_relational_expression(self):
        node = Node.create('relational_expression')

        node.append(self.parse_shift_expression())
        self.parse_relational_expression_lr(node)

        return node

    def parse_relational_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['relational_expression_lr', ['<', '>', 'LE_OP', 'GE_OP']])):
            node.append(self.parse_shift_expression())
            self.parse_relational_expression_lr(node)

        return node

    def parse_shift_expression(self):
        node = Node.create('shift_expression')

        node.append(self.parse_additive_expression())
        self.parse_shift_expression_lr(node)

        return node

    def parse_shift_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['shift_expression_lr', ['LEFT_OP', 'RIGHT_OP']])):
            node.append(self.parse_additive_expression())
            self.parse_shift_expression_lr(node)

        return node

    def parse_additive_expression(self):
        node = Node.create('additive_expression')

        node.append(self.parse_multiplicative_expression())
        self.parse_additive_expression_lr(node)

        return node

    def parse_additive_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['additive_expression_lr', ['+', '-']])):
            node.append(self.parse_multiplicative_expression())
            self.parse_additive_expression_lr(node)

        return node

    def parse_multiplicative_expression(self):
        node = Node.create('multiplicative_expression')

        node.append(self.parse_cast_expression())
        self.parse_multiplicative_expression_lr(node)

        return node

    def parse_multiplicative_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['multiplicative_expression_lr', ['*', '/', '%']])):
            node.append(self.parse_cast_expression())
            self.parse_multiplicative_expression_lr(node)

        return node

    def parse_cast_expression(self):
        node = Node.create('cast_expression')

        if node.append(self.try2(self.parse_unary_expression)):
            return node

        if node.append(self.try2(self.checkLexem, ['cast_expression', ['(']])):
            node.append(self.parse_type_name())
            node.append(self.checkLexem('cast_expression', [')']))
            node.append(self.parse_cast_expression())
            return node

        raise AnalyzerException('cast_expression', '')

    def parse_unary_expression(self):
        node = Node.create('unary_expression')

        if node.append(self.try2(self.parse_postfix_expression)):
            return node

        if node.append(self.try2(self.checkLexem, ['unary_expression', ['INC_OP', 'DEC_OP']])):
            node.append(self.parse_unary_expression())
            return node

        if node.append(self.try2(self.parse_unary_operator)):
            node.append(self.parse_cast_expression())
            return node

        if node.append(self.try2(self.checkLexem, ['unary_expression', ['SIZEOF']])):
            if node.append(self.try2(self.parse_unary_expression)):
                return node

            if node.append(self.try2(self.checkLexem, ['unary_expression', ['(']])):
                node.append(self.parse_type_name())
                node.append(self.checkLexem('unary_expression', [')']))
                return node

        if node.append(self.try2(self.checkLexem, ['unary_expression', ['ALIGNOF']])):
            node.append(self.checkLexem, ['unary_expression', ['(']])
            node.append(self.parse_type_name())
            node.append(self.checkLexem('unary_expression', [')']))
            return node

        raise AnalyzerException('unary_expression', '')

    def parse_unary_operator(self):
        node = Node.create('unary_operator')

        node.append(self.checkLexem('unary_operator', ['&', '*', '+', '-', '~', '!']))

        return node

    def parse_postfix_expression(self):
        node = Node.create('postfix_expression')

        if node.append(self.try2(self.parse_primary_expression)):
            self.parse_postfix_expression_lr(node)
            return node

        if node.append(self.try2(self.checkLexem, ['postfix_expression', ['(']])):
            node.append(self.parse_type_name())
            node.append(self.checkLexem('postfix_expression', [')']))
            node.append(self.checkLexem('postfix_expression', ['{']))
            node.append(self.parse_initializer_list())
            node.append(self.try2(self.checkLexem, ['postfix_expression', [',']]))
            node.append(self.checkLexem('postfix_expression', ['}']))
            self.parse_postfix_expression_lr(node)
            return node

        raise AnalyzerException('postfix_expression', '')

    def parse_postfix_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['postfix_expression_lr', ['[']])):
            node.append(self.parse_expression())
            node.append(self.checkLexem('postfix_expression_lr', [']']))
            self.parse_postfix_expression_lr(node)
            return node

        if node.append(self.try2(self.checkLexem, ['postfix_expression_lr', ['(']])):
            node.append(self.try2(self.parse_argument_expression_list))
            node.append(self.checkLexem('postfix_expression_lr', [')']))
            self.parse_postfix_expression_lr(node)
            return node

        if node.append(self.try2(self.checkLexem, ['postfix_expression_lr', ['.']])):
            node.append(self.checkLexem('postfix_expression_lr', ['IDENTIFIER']))
            self.parse_postfix_expression_lr(node)
            return node

        if node.append(self.try2(self.checkLexem, ['postfix_expression_lr', ['PTR_OP']])):
            node.append(self.checkLexem('postfix_expression_lr', ['IDENTIFIER']))
            self.parse_postfix_expression_lr(node)
            return node

        if node.append(self.try2(self.checkLexem, ['postfix_expression_lr', ['INC_OP', 'DEC_OP']])):
            self.parse_postfix_expression_lr(node)
            return node

    def parse_argument_expression_list(self):
        node = Node.create('argument_expression_list')

        node.append(self.parse_assignment_expression())
        self.parse_argument_expression_list_lr(node)

        return node

    def parse_argument_expression_list_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['argument_expression_list_lr', [',']])):
            node.append(self.parse_assignment_expression())
            self.parse_argument_expression_list_lr(node)

        return node

    def parse_expression(self):
        node = Node.create('expression')

        node.append(self.parse_assignment_expression())
        self.parse_expression_lr(node)

        return node

    def parse_expression_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['expression_lr', [',']])):
            node.append(self.parse_assignment_expression())
            self.parse_expression_lr(node)

    def parse_initializer_list(self):
        node = Node.create('initializer_list')

        node.append(self.try2(self.parse_designation))
        node.append(self.parse_initializer())
        self.parse_initializer_list_lr(node)

        return node

    def parse_initializer_list_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['initializer_list_lr', [',']])):
            node.append(self.try2(self.parse_designation))
            node.append(self.parse_initializer())
            self.parse_initializer_list_lr(node)

    def parse_designation(self):
        node = Node.create('designation')

        node.append(self.parse_designator_list())
        node.append(self.checkLexem('designation', ['=']))

        return node

    def parse_designator_list(self):
        node = Node.create('designator_list')

        node.append(self.parse_designator())
        self.parse_designator_list_lr(node)

        return node

    def parse_designator_list_lr(self, node):
        if node.append(self.try2(self.parse_designator)):
            self.parse_designator_list_lr(node)

    def parse_designator(self):
        node = Node.create('designator')
        if node.append(self.try2(self.checkLexem, ['designator', ['[']])):
            node.append(self.parse_constant_expression())
            node.append(self.checkLexem('designator', [']']))
            return node

        if node.append(self.try2(self.checkLexem, ['designator', ['.']])):
            node.append(self.checkLexem('designator', ['IDENTIFIER']))
            return node

        raise AnalyzerException('designator', '')

    def parse_constant_expression(self):
        node = Node.create('constant_expression')

        node.append(self.parse_conditional_expression())

        return node

    def parse_initializer(self):
        node = Node.create('initializer')

        if node.append(self.try2(self.checkLexem, ['initializer', ['{']])):
            node.append(self.parse_initializer_list())
            node.append(self.try2(self.checkLexem, ['initializer', [',']]))
            node.append(self.checkLexem('initializer', ['}']))
            return node

        if node.append(self.try2(self.parse_assignment_expression)):
            return node

        raise AnalyzerException('initializer', '')

    def parse_primary_expression(self):
        node = Node.create('primary_expression')

        if node.append(self.try2(self.checkLexem, ['primary_expression', ['IDENTIFIER']])):
            return node

        if node.append(self.try2(self.parse_constant)):
            return node

        if node.append(self.try2(self.parse_string)):
            return node

        if node.append(self.try2(self.checkLexem, ['primary_expression', ['(']])):
            node.append(self.parse_expression())
            node.append(self.checkLexem('primary_expression', [')']))
            return node

        if node.append(self.try2(self.parse_generic_selection)):
            return node

        raise AnalyzerException('primary_expression', '')

    def parse_constant(self):
        node = Node.create('constant')

        arr = ['I_CONSTANT', 'F_CONSTANT', 'ENUMERATION_CONSTANT']
        if node.append(self.try2(self.checkLexem, ['constant', arr])):
            return node

        raise AnalyzerException('constant', 'expected {} got {}'.format(', '.join(arr), self.lexer.get()))

    def parse_string(self):
        node = Node.create('string')

        arr = ['STRING_LITERAL', 'FUNC_NAME']
        if node.append(self.try2(self.checkLexem, ['string', arr])):
            return node

        raise AnalyzerException('string', 'expected {} got {}'.format(', '.join(arr), self.lexer.get()))

    def parse_generic_selection(self):
        node = Node.Node('generic_selection')

        node.append(self.checkLexem('generic_selection', ['GENERIC']))
        node.append(self.checkLexem('generic_selection', ['(']))
        node.append(self.parse_assignment_expression())
        node.append(self.checkLexem('generic_selection', [',']))
        node.append(self.parse_generic_assoc_list())
        node.append(self.checkLexem('generic_selection', [')']))

        return node

    def parse_generic_assoc_list(self):
        node = Node.create('generic_assoc_list')

        node.append(self.parse_generic_association())
        self.parse_generic_assoc_list_lr(node)

        return node

    def parse_generic_assoc_list_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['generic_assoc_list_lr', [',']])):
            node.append(self.parse_generic_association())
            self.parse_generic_assoc_list_lr(node)

    def parse_generic_association(self):
        node = Node.create('generic_association')

        if node.append(self.try2(self.parse_type_name)):
            node.append(self.checkLexem('generic_association', [':']))
            node.append(self.parse_assignment_expression())
            return node

        if node.append(self.try2(self.checkLexem, ['generic_association', ['DEFAULT']])):
            node.append(self.checkLexem('generic_association', [':']))
            node.append(self.parse_assignment_expression())
            return node

        raise AnalyzerException('generic_association', '')

    def parse_assignment_operator(self):
        node = Node.create('assignment_operator')

        arr = ['=', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN',
               'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN']
        if node.append(self.try2(self.checkLexem, ['assignment_operator', arr])):
            return node

        raise AnalyzerException('assignment_operator', 'expected {} got {}'.format(', '.join(arr), self.lexer.get()))

    def parse_identifier_list(self):
        node = Node.create('identifier_list')

        node.append(self.checkLexem('identifier_list', ['IDENTIFIER']))
        self.parse_identifier_list_lr(node)

        return node

    def parse_identifier_list_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['identifier_list_lr', [',']])):
            node.append(self.checkLexem('identifier_list_lr', ['IDENTIFIER']))
            self.parse_identifier_list_lr(node)

    def parse_atomic_type_specifier(self):
        node = Node.create('atomic_type_specifier')

        node.append(self.checkLexem('atomic_type_specifier', ['ATOMIC']))
        node.append(self.checkLexem('atomic_type_specifier', ['(']))
        node.append(self.parse_type_name())
        node.append(self.checkLexem('atomic_type_specifier', [')']))

        return node

    def parse_struct_or_union_specifier(self):
        node = Node.create('struct_or_union_specifier')

        node.append(self.parse_struct_or_union())
        if node.append(self.try2(self.checkLexem, ['struct_or_union_specifier', ['{']])):
            node.append(self.parse_struct_declaration_list())
            node.append(self.checkLexem('struct_or_union_specifier', ['}']))
            return node

        if node.append(self.try2(self.checkLexem, ['struct_or_union_specifier', ['IDENTIFIER']])):
            if node.append(self.try2(self.checkLexem, ['struct_or_union_specifier', ['{']])):
                node.append(self.parse_struct_declaration_list())
                node.append(self.checkLexem('struct_or_union_specifier', ['}']))
                return node
            return node

        raise AnalyzerException('struct_or_union_specifier', '')

    def parse_struct_or_union(self):
        node = Node.create('struct_or_union')

        arr = ['STRUCT', 'UNION']
        if node.append(self.try2(self.checkLexem, ['struct_or_union', arr])):
            return node

        raise AnalyzerException('struct_or_union', 'expected {} got {}'.format(', '.join(arr), self.lexer.get()))

    def parse_struct_declaration_list(self):
        node = Node.create('struct_declaration_list')

        node.append(self.parse_struct_declaration())
        self.parse_struct_declaration_list_lr(node)

        return node

    def parse_struct_declaration_list_lr(self, node):
        if node.append(self.try2(self.parse_struct_declaration)):
            self.parse_struct_declaration_list_lr(node)

    def parse_struct_declaration(self):
        node = Node.create('struct_declaration')

        if node.append(self.try2(self.parse_specifier_qualifier_list)):
            node.append(self.try2(self.parse_struct_declarator_list))
            node.append(self.checkLexem('struct_declaration', [';']))
            return node

        if node.append(self.try2(self.parse_static_assert_declaration)):
            return node

        raise AnalyzerException('struct_declaration', '')

    def parse_static_assert_declaration(self):
        node = Node.create('static_assert_declaration')

        node.append(self.checkLexem('static_assert_declaration', ['STATIC_ASSERT']))
        node.append(self.checkLexem('static_assert_declaration', ['(']))
        node.append(self.parse_constant_expression())
        node.append(self.checkLexem('static_assert_declaration', [',']))
        node.append(self.checkLexem('static_assert_declaration', ['STRING_LITERAL']))
        node.append(self.checkLexem('static_assert_declaration', [')']))
        node.append(self.checkLexem('static_assert_declaration', [';']))

        return node

    def parse_struct_declarator_list(self):
        node = Node.create('struct_declarator_list')

        node.append(self.parse_struct_declarator())
        self.parse_struct_declarator_list_lr(node)

        return node

    def parse_struct_declarator_list_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['struct_declarator_list_lr', [',']])):
            node.append(self.parse_struct_declarator())
            self.parse_struct_declarator_list_lr(node)

    def parse_struct_declarator(self):
        node = Node.create('struct_declarator')

        if node.append(self.try2(self.checkLexem, ['struct_declarator', [':']])):
            node.append(self.parse_constant_expression())
            return node

        if node.append(self.try2(self.parse_declarator)):
            if node.append(self.try2(self.checkLexem, ['struct_declarator', [':']])):
                node.append(self.parse_constant_expression())
                return node
            return node

        raise AnalyzerException('struct_declarator', '')

    def parse_enum_specifier(self):
        node = Node.create('enum_specifier')

        node.append(self.checkLexem('enum_specifier', ['ENUM']))
        if node.append(self.try2(self.checkLexem, ['enum_specifier', ['{']])):
            node.append(self.parse_enumerator_list())
            node.append(self.try2(self.checkLexem, ['enumerator_list', [',']]))
            node.append(self.checkLexem('enumerator_list', ['}']))
            return node

        if node.append(self.try2(self.checkLexem, ['enum_specifier', ['IDENTIFIER']])):
            if node.append(self.try2(self.checkLexem, ['enum_specifier', ['{']])):
                node.append(self.parse_enumerator_list())
                node.append(self.try2(self.checkLexem, ['enumerator_list', [',']]))
                node.append(self.checkLexem('enumerator_list', ['}']))
                return node
            return node

        raise AnalyzerException('enumerator_list', '')

    def parse_enumerator_list(self):
        node = Node.create('enumerator_list')

        node.append(self.parse_enumerator())
        self.parse_enumerator_list_lr(node)

        return node

    def parse_enumerator_list_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['enumerator_list_lr', [',']])):
            node.append(self.parse_enumerator())
            self.parse_enumerator_list_lr(node)

    def parse_enumerator(self):
        node = Node.create('enumerator')

        node.append(self.parse_enumeration_constant())
        if node.append(self.try2(self.checkLexem, ['enumerator', ['=']])):
            node.append(self.parse_constant_expression())

        return node

    def parse_enumeration_constant(self):
        node = Node.create('enumeration_constant')

        node.append(self.checkLexem('enumeration_constant', ['IDENTIFIER']))

        return node

    def parse_compound_statement(self):
        node = Node.create('compound_statement')

        node.append(self.checkLexem('compound_statement', ['{']))
        node.append(self.try2(self.parse_block_item_list))
        node.append(self.checkLexem('compound_statement', ['}']))

        return node

    def parse_block_item_list(self):
        node = Node.create('block_item_list')

        node.append(self.parse_block_item())
        self.parse_block_item_list_lr(node)

        return node

    def parse_block_item_list_lr(self, node):
        if node.append(self.try2(self.parse_block_item)):
            self.parse_block_item_list_lr(node)

    def parse_block_item(self):
        node = Node.create('block_item')

        if node.append(self.try2(self.parse_declaration)):
            return node

        if node.append(self.try2(self.parse_statement)):
            return node

        raise AnalyzerException('block_item', '')

    def parse_declaration(self):
        node = Node.create('declaration')

        if node.append(self.try2(self.parse_declaration_specifiers)):
            node.append(self.try2(self.parse_init_declarator_list))
            node.append(self.checkLexem('declaration', [';']))
            return node

        if node.append(self.try2(self.parse_static_assert_declaration)):
            return node

        raise AnalyzerException('declaration', '')

    def parse_init_declarator_list(self):
        node = Node.create('init_declarator_list')

        node.append(self.parse_init_declarator())
        self.parse_init_declarator_list_lr(node)

        return node

    def parse_init_declarator_list_lr(self, node):
        if node.append(self.try2(self.checkLexem, ['init_declarator_list_lr', [',']])):
            node.append(self.parse_init_declarator())
            self.parse_init_declarator_list_lr(node)

    def parse_init_declarator(self):
        node = Node.create('init_declarator')

        node.append(self.parse_declarator())
        if node.append(self.try2(self.checkLexem, ['init_declarator', ['=']])):
            node.append(self.parse_initializer())

        return node

    def parse_statement(self):
        node = Node.create('statement')

        if node.append(self.try2(self.parse_labeled_statement)):
            return node

        if node.append(self.try2(self.parse_compound_statement)):
            return node

        if node.append(self.try2(self.parse_expression_statement)):
            return node

        if node.append(self.try2(self.parse_selection_statement)):
            return node

        if node.append(self.try2(self.parse_iteration_statement)):
            return node

        if node.append(self.try2(self.parse_jump_statement)):
            return node

        raise AnalyzerException('statement', '')

    def parse_labeled_statement(self):
        node = Node.create('labeled_statement')

        if node.append(self.try2(self.checkLexem, ['labeled_statement', ['IDENTIFIER']])):
            node.append(self.checkLexem('labeled_statement', [':']))
            node.append(self.parse_statement())
            return node

        if node.append(self.try2(self.checkLexem, ['labeled_statement', ['CASE']])):
            node.append(self.parse_constant_expression())
            node.append(self.checkLexem('labeled_statement', [':']))
            node.append(self.parse_statement())
            return node

        if node.append(self.try2(self.checkLexem, ['labeled_statement', ['DEFAULT']])):
            node.append(self.checkLexem('labeled_statement', [':']))
            node.append(self.parse_statement())
            return node

        raise AnalyzerException('labeled_statement', '')

    def parse_expression_statement(self):
        node = Node.create('expression_statement')

        node.append(self.try2(self.parse_expression))
        node.append(self.checkLexem('expression_statement', [';']))

        return node

    def parse_selection_statement(self):
        node = Node.create('selection_statement')

        if node.append(self.try2(self.checkLexem, ['selection_statement', ['IF']])):
            node.append(self.checkLexem('selection_statement', ['(']))
            node.append(self.parse_expression())
            node.append(self.checkLexem('selection_statement', [')']))
            node.append(self.parse_statement())
            if node.append(self.try2(self.checkLexem, ['selection_statement', ['ELSE']])):
                node.append(self.parse_statement())
            return node

        if node.append(self.try2(self.checkLexem, ['selection_statement', ['SWITCH']])):
            node.append(self.checkLexem('selection_statement', ['(']))
            node.append(self.parse_expression())
            node.append(self.checkLexem('selection_statement', [')']))
            node.append(self.parse_statement())
            return node

        raise AnalyzerException('selection_statement', '')

    def parse_iteration_statement(self):
        node = Node.create('iteration_statement')

        if node.append(self.try2(self.checkLexem, ['iteration_statement', ['WHILE']])):
            node.append(self.checkLexem('iteration_statement', ['(']))
            node.append(self.parse_expression())
            node.append(self.checkLexem('iteration_statement', [')']))
            node.append(self.parse_statement())
            return node

        if node.append(self.try2(self.checkLexem, ['iteration_statement', ['DO']])):
            node.append(self.parse_statement())
            node.append(self.checkLexem('iteration_statement', ['WHILE']))
            node.append(self.checkLexem('iteration_statement', ['(']))
            node.append(self.parse_expression())
            node.append(self.checkLexem('iteration_statement', [')']))
            node.append(self.checkLexem('iteration_statement', [';']))
            return node

        if node.append(self.try2(self.checkLexem, ['iteration_statement', ['FOR']])):
            node.append(self.checkLexem('iteration_statement', ['(']))
            node.append(self.try2(self.parse_declaration))
            node.append(self.parse_expression_statement())
            node.append(self.try2(self.parse_expression_statement))
            node.append(self.try2(self.parse_expression))
            node.append(self.checkLexem('iteration_statement', [')']))
            node.append(self.parse_statement())
            return node

        raise AnalyzerException('iteration_statement', '')

    def parse_jump_statement(self):
        node = Node.create('jump_statement')

        if node.append(self.try2(self.checkLexem, ['jump_statement', ['GOTO']])):
            node.append(self.checkLexem('jump_statement', ['IDENTIFIER']))
            node.append(self.checkLexem('jump_statement', [';']))
            return node

        if node.append(self.try2(self.checkLexem, ['jump_statement', ['CONTINUE', 'BREAK']])):
            node.append(self.checkLexem('jump_statement', [';']))
            return node

        if node.append(self.try2(self.checkLexem, ['jump_statement', ['RETURN']])):
            node.append(self.try2(self.parse_expression))
            node.append(self.checkLexem('jump_statement', [';']))
            return node

        raise AnalyzerException('jump_statement', '')

    def parse_declaration_list(self):
        node = Node.create('declaration_list')

        node.append(self.parse_declaration())
        self.parse_declaration_list_lr(node)

        return node

    def parse_declaration_list_lr(self, node):
        if node.append(self.try2(self.parse_declaration)):
            self.parse_declaration_list_lr(node)
