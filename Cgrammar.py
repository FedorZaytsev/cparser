
CGrammarEntryPoint = 'translation_unit'
CGrammar = {
    'abstract_declarator': {
        'rules': [
            {'rule': ['pointer','direct_abstract_declarator'], 'first': ['*']},
            {'rule': ['pointer'], 'first': ['*']},
            {'rule': ['direct_abstract_declarator'], 'first': ['(','[']}
        ],
        'follow': [')',':',',']
    },
    'additive_expression': {
        'rules': [
            {'rule': ['multiplicative_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['additive_expression','+','multiplicative_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['additive_expression','-','multiplicative_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['+','-','LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'alignment_specifier': {
        'rules': [
            {'rule': ['ALIGNAS','(','type_name',')'], 'first': ['ALIGNAS']},
            {'rule': ['ALIGNAS','(','constant_expression',')'], 'first': ['ALIGNAS']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS',';','*','IDENTIFIER','(','[',',',')']
    },
    'and_expression': {
        'rules': [
            {'rule': ['equality_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['and_expression','&','equality_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'argument_expression_list': {
        'rules': [
            {'rule': ['assignment_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['argument_expression_list',',','assignment_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': [',',')']
    },
    'assignment_expression': {
        'rules': [
            {'rule': ['conditional_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['unary_expression','assignment_operator','assignment_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': [']',',',')',':',';','}']
    },
    'assignment_operator': {
        'rules': [
            {'rule': ['='], 'first': ['=']},
            {'rule': ['MUL_ASSIGN'], 'first': ['MUL_ASSIGN']},
            {'rule': ['DIV_ASSIGN'], 'first': ['DIV_ASSIGN']},
            {'rule': ['MOD_ASSIGN'], 'first': ['MOD_ASSIGN']},
            {'rule': ['ADD_ASSIGN'], 'first': ['ADD_ASSIGN']},
            {'rule': ['SUB_ASSIGN'], 'first': ['SUB_ASSIGN']},
            {'rule': ['LEFT_ASSIGN'], 'first': ['LEFT_ASSIGN']},
            {'rule': ['RIGHT_ASSIGN'], 'first': ['RIGHT_ASSIGN']},
            {'rule': ['AND_ASSIGN'], 'first': ['AND_ASSIGN']},
            {'rule': ['XOR_ASSIGN'], 'first': ['XOR_ASSIGN']},
            {'rule': ['OR_ASSIGN'], 'first': ['OR_ASSIGN']}
        ],
        'follow': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']
    },
    'atomic_type_specifier': {
        'rules': [
            {'rule': ['ATOMIC','(','type_name',')'], 'first': ['ATOMIC']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS',';','*','IDENTIFIER','(','[',':',')',',']
    },
    'block_item': {
        'rules': [
            {'rule': ['declaration'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT']},
            {'rule': ['statement'], 'first': ['IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','WHILE','DO','FOR','GOTO','CONTINUE','BREAK','RETURN']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','WHILE','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'block_item_list': {
        'rules': [
            {'rule': ['block_item'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','WHILE','DO','FOR','GOTO','CONTINUE','BREAK','RETURN']},
            {'rule': ['block_item_list','block_item'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','WHILE','DO','FOR','GOTO','CONTINUE','BREAK','RETURN']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','WHILE','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'cast_expression': {
        'rules': [
            {'rule': ['unary_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['(','type_name',')','cast_expression'], 'first': ['(']}
        ],
        'follow': ['*','/','%','+','-','=','MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN','ADD_ASSIGN','SUB_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'compound_statement': {
        'rules': [
            {'rule': ['{','}'], 'first': ['{']},
            {'rule': ['{','block_item_list','}'], 'first': ['{']}
        ],
        'follow': ['WHILE','ELSE','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'conditional_expression': {
        'rules': [
            {'rule': ['logical_or_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['logical_or_expression','?','expression',':','conditional_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': [']',',',')',':',';','}']
    },
    'constant': {
        'rules': [
            {'rule': ['I_CONSTANT'], 'first': ['I_CONSTANT']},
            {'rule': ['F_CONSTANT'], 'first': ['F_CONSTANT']},
            {'rule': ['ENUMERATION_CONSTANT'], 'first': ['ENUMERATION_CONSTANT']}
        ],
        'follow': ['[','(','.','PTR_OP','INC_OP','DEC_OP','=','MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN','ADD_ASSIGN','SUB_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','*','/','%','+','-','LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'constant_expression': {
        'rules': [
            {'rule': ['conditional_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': [')',']',':',',','}',';']
    },
    'declaration': {
        'rules': [
            {'rule': ['declaration_specifiers',';'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']},
            {'rule': ['declaration_specifiers','init_declarator_list',';'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']},
            {'rule': ['static_assert_declaration'], 'first': ['STATIC_ASSERT']}
        ],
        'follow': [';','IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','{','CASE','DEFAULT','IF','SWITCH','WHILE','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'declaration_list': {
        'rules': [
            {'rule': ['declaration'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT']},
            {'rule': ['declaration_list','declaration'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','{']
    },
    'declaration_specifiers': {
        'rules': [
            {'rule': ['storage_class_specifier','declaration_specifiers'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER']},
            {'rule': ['storage_class_specifier'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER']},
            {'rule': ['type_specifier','declaration_specifiers'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME']},
            {'rule': ['type_specifier'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME']},
            {'rule': ['type_qualifier','declaration_specifiers'], 'first': ['CONST','RESTRICT','VOLATILE','ATOMIC']},
            {'rule': ['type_qualifier'], 'first': ['CONST','RESTRICT','VOLATILE','ATOMIC']},
            {'rule': ['function_specifier','declaration_specifiers'], 'first': ['INLINE','NORETURN']},
            {'rule': ['function_specifier'], 'first': ['INLINE','NORETURN']},
            {'rule': ['alignment_specifier','declaration_specifiers'], 'first': ['ALIGNAS']},
            {'rule': ['alignment_specifier'], 'first': ['ALIGNAS']}
        ],
        'follow': [';','*','IDENTIFIER','(','[',',',')']
    },
    'declarator': {
        'rules': [
            {'rule': ['pointer','direct_declarator'], 'first': ['*']},
            {'rule': ['direct_declarator'], 'first': ['IDENTIFIER','(']}
        ],
        'follow': [')','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','{','=',':',';',',']
    },
    'designation': {
        'rules': [
            {'rule': ['designator_list','='], 'first': ['[','.']}
        ],
        'follow': ['{','IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']
    },
    'designator': {
        'rules': [
            {'rule': ['[','constant_expression',']'], 'first': ['[']},
            {'rule': ['.','IDENTIFIER'], 'first': ['.']}
        ],
        'follow': ['=','[','.']
    },
    'designator_list': {
        'rules': [
            {'rule': ['designator'], 'first': ['[','.']},
            {'rule': ['designator_list','designator'], 'first': ['[','.']}
        ],
        'follow': ['=','[','.']
    },
    'direct_abstract_declarator': {
        'rules': [
            {'rule': ['(','abstract_declarator',')'], 'first': ['(']},
            {'rule': ['[',']'], 'first': ['[']},
            {'rule': ['[','*',']'], 'first': ['[']},
            {'rule': ['[','STATIC','type_qualifier_list','assignment_expression',']'], 'first': ['[']},
            {'rule': ['[','STATIC','assignment_expression',']'], 'first': ['[']},
            {'rule': ['[','type_qualifier_list','STATIC','assignment_expression',']'], 'first': ['[']},
            {'rule': ['[','type_qualifier_list','assignment_expression',']'], 'first': ['[']},
            {'rule': ['[','type_qualifier_list',']'], 'first': ['[']},
            {'rule': ['[','assignment_expression',']'], 'first': ['[']},
            {'rule': ['direct_abstract_declarator','[',']'], 'first': ['(','[']},
            {'rule': ['direct_abstract_declarator','[','*',']'], 'first': ['(','[']},
            {'rule': ['direct_abstract_declarator','[','STATIC','type_qualifier_list','assignment_expression',']'], 'first': ['(','[']},
            {'rule': ['direct_abstract_declarator','[','STATIC','assignment_expression',']'], 'first': ['(','[']},
            {'rule': ['direct_abstract_declarator','[','type_qualifier_list','assignment_expression',']'], 'first': ['(','[']},
            {'rule': ['direct_abstract_declarator','[','type_qualifier_list','STATIC','assignment_expression',']'], 'first': ['(','[']},
            {'rule': ['direct_abstract_declarator','[','type_qualifier_list',']'], 'first': ['(','[']},
            {'rule': ['direct_abstract_declarator','[','assignment_expression',']'], 'first': ['(','[']},
            {'rule': ['(',')'], 'first': ['(']},
            {'rule': ['(','parameter_type_list',')'], 'first': ['(']},
            {'rule': ['direct_abstract_declarator','(',')'], 'first': ['(','[']},
            {'rule': ['direct_abstract_declarator','(','parameter_type_list',')'], 'first': ['(','[']}
        ],
        'follow': ['[','(',')',':',',']
    },
    'direct_declarator': {
        'rules': [
            {'rule': ['IDENTIFIER'], 'first': ['IDENTIFIER']},
            {'rule': ['(','declarator',')'], 'first': ['(']},
            {'rule': ['direct_declarator','[',']'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','[','*',']'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','[','STATIC','type_qualifier_list','assignment_expression',']'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','[','STATIC','assignment_expression',']'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','[','type_qualifier_list','*',']'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','[','type_qualifier_list','STATIC','assignment_expression',']'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','[','type_qualifier_list','assignment_expression',']'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','[','type_qualifier_list',']'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','[','assignment_expression',']'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','(','parameter_type_list',')'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','(',')'], 'first': ['IDENTIFIER','(']},
            {'rule': ['direct_declarator','(','identifier_list',')'], 'first': ['IDENTIFIER','(']}
        ],
        'follow': ['[','(',')','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','{','=',':',';',',']
    },
    'enum_specifier': {
        'rules': [
            {'rule': ['ENUM','{','enumerator_list','}'], 'first': ['ENUM']},
            {'rule': ['ENUM','{','enumerator_list',',','}'], 'first': ['ENUM']},
            {'rule': ['ENUM','IDENTIFIER','{','enumerator_list','}'], 'first': ['ENUM']},
            {'rule': ['ENUM','IDENTIFIER','{','enumerator_list',',','}'], 'first': ['ENUM']},
            {'rule': ['ENUM','IDENTIFIER'], 'first': ['ENUM']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS',';','*','IDENTIFIER','(','[',':',')',',']
    },
    'enumeration_constant': {
        'rules': [
            {'rule': ['IDENTIFIER'], 'first': ['IDENTIFIER']}
        ],
        'follow': ['=','}',',']
    },
    'enumerator': {
        'rules': [
            {'rule': ['enumeration_constant','=','constant_expression'], 'first': ['IDENTIFIER']},
            {'rule': ['enumeration_constant'], 'first': ['IDENTIFIER']}
        ],
        'follow': ['}',',']
    },
    'enumerator_list': {
        'rules': [
            {'rule': ['enumerator'], 'first': ['IDENTIFIER']},
            {'rule': ['enumerator_list',',','enumerator'], 'first': ['IDENTIFIER']}
        ],
        'follow': ['}',',']
    },
    'equality_expression': {
        'rules': [
            {'rule': ['relational_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['equality_expression','EQ_OP','relational_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['equality_expression','NE_OP','relational_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'exclusive_or_expression': {
        'rules': [
            {'rule': ['and_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['exclusive_or_expression','^','and_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'expression': {
        'rules': [
            {'rule': ['assignment_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['expression',',','assignment_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': [':',',',';',')',']']
    },
    'expression_statement': {
        'rules': [
            {'rule': [';'], 'first': [';']},
            {'rule': ['expression',';'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': [';','IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF',')','WHILE','ELSE','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','CASE','DEFAULT','{','IF','SWITCH','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'external_declaration': {
        'rules': [
            {'rule': ['function_definition'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']},
            {'rule': ['declaration'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT']
    },
    'function_definition': {
        'rules': [
            {'rule': ['declaration_specifiers','declarator','declaration_list','compound_statement'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']},
            {'rule': ['declaration_specifiers','declarator','compound_statement'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT']
    },
    'function_specifier': {
        'rules': [
            {'rule': ['INLINE'], 'first': ['INLINE']},
            {'rule': ['NORETURN'], 'first': ['NORETURN']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS',';','*','IDENTIFIER','(','[',',',')']
    },
    'generic_assoc_list': {
        'rules': [
            {'rule': ['generic_association'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','DEFAULT']},
            {'rule': ['generic_assoc_list',',','generic_association'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','DEFAULT']}
        ],
        'follow': [',',')']
    },
    'generic_association': {
        'rules': [
            {'rule': ['type_name',':','assignment_expression'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE']},
            {'rule': ['DEFAULT',':','assignment_expression'], 'first': ['DEFAULT']}
        ],
        'follow': [',',')']
    },
    'generic_selection': {
        'rules': [
            {'rule': ['GENERIC','(','assignment_expression',',','generic_assoc_list',')'], 'first': ['GENERIC']}
        ],
        'follow': ['[','(','.','PTR_OP','INC_OP','DEC_OP','=','MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN','ADD_ASSIGN','SUB_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','*','/','%','+','-','LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'identifier_list': {
        'rules': [
            {'rule': ['IDENTIFIER'], 'first': ['IDENTIFIER']},
            {'rule': ['identifier_list',',','IDENTIFIER'], 'first': ['IDENTIFIER']}
        ],
        'follow': [')',',']
    },
    'inclusive_or_expression': {
        'rules': [
            {'rule': ['exclusive_or_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['inclusive_or_expression','|','exclusive_or_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'init_declarator': {
        'rules': [
            {'rule': ['declarator','=','initializer'], 'first': ['*','IDENTIFIER','(']},
            {'rule': ['declarator'], 'first': ['*','IDENTIFIER','(']}
        ],
        'follow': [';',',']
    },
    'init_declarator_list': {
        'rules': [
            {'rule': ['init_declarator'], 'first': ['*','IDENTIFIER','(']},
            {'rule': ['init_declarator_list',',','init_declarator'], 'first': ['*','IDENTIFIER','(']}
        ],
        'follow': [';',',']
    },
    'initializer': {
        'rules': [
            {'rule': ['{','initializer_list','}'], 'first': ['{']},
            {'rule': ['{','initializer_list',',','}'], 'first': ['{']},
            {'rule': ['assignment_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['}',',',';']
    },
    'initializer_list': {
        'rules': [
            {'rule': ['designation','initializer'], 'first': ['[','.']},
            {'rule': ['initializer'], 'first': ['{','IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['initializer_list',',','designation','initializer'], 'first': ['[','.','{','IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['initializer_list',',','initializer'], 'first': ['[','.','{','IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['}',',']
    },
    'iteration_statement': {
        'rules': [
            {'rule': ['WHILE','(','expression',')','statement'], 'first': ['WHILE']},
            {'rule': ['DO','statement','WHILE','(','expression',')',';'], 'first': ['DO']},
            {'rule': ['FOR','(','expression_statement','expression_statement',')','statement'], 'first': ['FOR']},
            {'rule': ['FOR','(','expression_statement','expression_statement','expression',')','statement'], 'first': ['FOR']},
            {'rule': ['FOR','(','declaration','expression_statement',')','statement'], 'first': ['FOR']},
            {'rule': ['FOR','(','declaration','expression_statement','expression',')','statement'], 'first': ['FOR']}
        ],
        'follow': ['WHILE','ELSE','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'jump_statement': {
        'rules': [
            {'rule': ['GOTO','IDENTIFIER',';'], 'first': ['GOTO']},
            {'rule': ['CONTINUE',';'], 'first': ['CONTINUE']},
            {'rule': ['BREAK',';'], 'first': ['BREAK']},
            {'rule': ['RETURN',';'], 'first': ['RETURN']},
            {'rule': ['RETURN','expression',';'], 'first': ['RETURN']}
        ],
        'follow': ['WHILE','ELSE','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'labeled_statement': {
        'rules': [
            {'rule': ['IDENTIFIER',':','statement'], 'first': ['IDENTIFIER']},
            {'rule': ['CASE','constant_expression',':','statement'], 'first': ['CASE']},
            {'rule': ['DEFAULT',':','statement'], 'first': ['DEFAULT']}
        ],
        'follow': ['WHILE','ELSE','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'logical_and_expression': {
        'rules': [
            {'rule': ['inclusive_or_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['logical_and_expression','AND_OP','inclusive_or_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'logical_or_expression': {
        'rules': [
            {'rule': ['logical_and_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['logical_or_expression','OR_OP','logical_and_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['?','OR_OP',']',',',')',':',';','}']
    },
    'multiplicative_expression': {
        'rules': [
            {'rule': ['cast_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['multiplicative_expression','*','cast_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['multiplicative_expression','/','cast_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['multiplicative_expression','%','cast_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['*','/','%','+','-','LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'parameter_declaration': {
        'rules': [
            {'rule': ['declaration_specifiers','declarator'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']},
            {'rule': ['declaration_specifiers','abstract_declarator'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']},
            {'rule': ['declaration_specifiers'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']}
        ],
        'follow': [',',')']
    },
    'parameter_list': {
        'rules': [
            {'rule': ['parameter_declaration'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']},
            {'rule': ['parameter_list',',','parameter_declaration'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']}
        ],
        'follow': [',',')']
    },
    'parameter_type_list': {
        'rules': [
            {'rule': ['parameter_list',',','ELLIPSIS'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']},
            {'rule': ['parameter_list'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS']}
        ],
        'follow': [')']
    },
    'pointer': {
        'rules': [
            {'rule': ['*','type_qualifier_list','pointer'], 'first': ['*']},
            {'rule': ['*','type_qualifier_list'], 'first': ['*']},
            {'rule': ['*','pointer'], 'first': ['*']},
            {'rule': ['*'], 'first': ['*']}
        ],
        'follow': ['(','[','IDENTIFIER',')',':',',']
    },
    'postfix_expression': {
        'rules': [
            {'rule': ['primary_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC']},
            {'rule': ['postfix_expression','[','expression',']'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC']},
            {'rule': ['postfix_expression','(',')'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC']},
            {'rule': ['postfix_expression','(','argument_expression_list',')'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC']},
            {'rule': ['postfix_expression','.','IDENTIFIER'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC']},
            {'rule': ['postfix_expression','PTR_OP','IDENTIFIER'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC']},
            {'rule': ['postfix_expression','INC_OP'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC']},
            {'rule': ['postfix_expression','DEC_OP'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC']},
            {'rule': ['(','type_name',')','{','initializer_list','}'], 'first': ['(']},
            {'rule': ['(','type_name',')','{','initializer_list',',','}'], 'first': ['(']}
        ],
        'follow': ['[','(','.','PTR_OP','INC_OP','DEC_OP','=','MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN','ADD_ASSIGN','SUB_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','*','/','%','+','-','LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'primary_expression': {
        'rules': [
            {'rule': ['IDENTIFIER'], 'first': ['IDENTIFIER']},
            {'rule': ['constant'], 'first': ['I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT']},
            {'rule': ['string'], 'first': ['STRING_LITERAL','FUNC_NAME']},
            {'rule': ['(','expression',')'], 'first': ['(']},
            {'rule': ['generic_selection'], 'first': ['GENERIC']}
        ],
        'follow': ['[','(','.','PTR_OP','INC_OP','DEC_OP','=','MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN','ADD_ASSIGN','SUB_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','*','/','%','+','-','LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'relational_expression': {
        'rules': [
            {'rule': ['shift_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['relational_expression','<','shift_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['relational_expression','>','shift_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['relational_expression','LE_OP','shift_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['relational_expression','GE_OP','shift_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'selection_statement': {
        'rules': [
            {'rule': ['IF','(','expression',')','statement','ELSE','statement'], 'first': ['IF']},
            {'rule': ['IF','(','expression',')','statement'], 'first': ['IF']},
            {'rule': ['SWITCH','(','expression',')','statement'], 'first': ['SWITCH']}
        ],
        'follow': ['WHILE','ELSE','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'shift_expression': {
        'rules': [
            {'rule': ['additive_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['shift_expression','LEFT_OP','additive_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['shift_expression','RIGHT_OP','additive_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']}
        ],
        'follow': ['LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'specifier_qualifier_list': {
        'rules': [
            {'rule': ['type_specifier','specifier_qualifier_list'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME']},
            {'rule': ['type_specifier'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME']},
            {'rule': ['type_qualifier','specifier_qualifier_list'], 'first': ['CONST','RESTRICT','VOLATILE','ATOMIC']},
            {'rule': ['type_qualifier'], 'first': ['CONST','RESTRICT','VOLATILE','ATOMIC']}
        ],
        'follow': [';',':','*','IDENTIFIER','(','[',')']
    },
    'statement': {
        'rules': [
            {'rule': ['labeled_statement'], 'first': ['IDENTIFIER','CASE','DEFAULT']},
            {'rule': ['compound_statement'], 'first': ['{']},
            {'rule': ['expression_statement'], 'first': [';','IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']},
            {'rule': ['selection_statement'], 'first': ['IF','SWITCH']},
            {'rule': ['iteration_statement'], 'first': ['WHILE','DO','FOR']},
            {'rule': ['jump_statement'], 'first': ['GOTO','CONTINUE','BREAK','RETURN']}
        ],
        'follow': ['WHILE','ELSE','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','IDENTIFIER','CASE','DEFAULT','{',';','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','IF','SWITCH','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'static_assert_declaration': {
        'rules': [
            {'rule': ['STATIC_ASSERT','(','constant_expression',',','STRING_LITERAL',')',';'], 'first': ['STATIC_ASSERT']}
        ],
        'follow': [';','IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT','{','CASE','DEFAULT','IF','SWITCH','WHILE','DO','FOR','GOTO','CONTINUE','BREAK','RETURN','}']
    },
    'storage_class_specifier': {
        'rules': [
            {'rule': ['TYPEDEF'], 'first': ['TYPEDEF']},
            {'rule': ['EXTERN'], 'first': ['EXTERN']},
            {'rule': ['STATIC'], 'first': ['STATIC']},
            {'rule': ['THREAD_LOCAL'], 'first': ['THREAD_LOCAL']},
            {'rule': ['AUTO'], 'first': ['AUTO']},
            {'rule': ['REGISTER'], 'first': ['REGISTER']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS',';','*','IDENTIFIER','(','[',',',')']
    },
    'string': {
        'rules': [
            {'rule': ['STRING_LITERAL'], 'first': ['STRING_LITERAL']},
            {'rule': ['FUNC_NAME'], 'first': ['FUNC_NAME']}
        ],
        'follow': ['[','(','.','PTR_OP','INC_OP','DEC_OP','=','MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN','ADD_ASSIGN','SUB_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','*','/','%','+','-','LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'struct_declaration': {
        'rules': [
            {'rule': ['specifier_qualifier_list',';'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE']},
            {'rule': ['specifier_qualifier_list','struct_declarator_list',';'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE']},
            {'rule': ['static_assert_declaration'], 'first': ['STATIC_ASSERT']}
        ],
        'follow': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','STATIC_ASSERT','}']
    },
    'struct_declaration_list': {
        'rules': [
            {'rule': ['struct_declaration'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','STATIC_ASSERT']},
            {'rule': ['struct_declaration_list','struct_declaration'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','STATIC_ASSERT']}
        ],
        'follow': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','STATIC_ASSERT','}']
    },
    'struct_declarator': {
        'rules': [
            {'rule': [':','constant_expression'], 'first': [':']},
            {'rule': ['declarator',':','constant_expression'], 'first': ['*','IDENTIFIER','(']},
            {'rule': ['declarator'], 'first': ['*','IDENTIFIER','(']}
        ],
        'follow': [';',',']
    },
    'struct_declarator_list': {
        'rules': [
            {'rule': ['struct_declarator'], 'first': [':','*','IDENTIFIER','(']},
            {'rule': ['struct_declarator_list',',','struct_declarator'], 'first': [':','*','IDENTIFIER','(']}
        ],
        'follow': [';',',']
    },
    'struct_or_union': {
        'rules': [
            {'rule': ['STRUCT'], 'first': ['STRUCT']},
            {'rule': ['UNION'], 'first': ['UNION']}
        ],
        'follow': ['{','IDENTIFIER']
    },
    'struct_or_union_specifier': {
        'rules': [
            {'rule': ['struct_or_union','{','struct_declaration_list','}'], 'first': ['STRUCT','UNION']},
            {'rule': ['struct_or_union','IDENTIFIER','{','struct_declaration_list','}'], 'first': ['STRUCT','UNION']},
            {'rule': ['struct_or_union','IDENTIFIER'], 'first': ['STRUCT','UNION']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS',';','*','IDENTIFIER','(','[',':',')',',']
    },
    'translation_unit': {
        'rules': [
            {'rule': ['external_declaration'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT']},
            {'rule': ['translation_unit','external_declaration'], 'first': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS','STATIC_ASSERT']
    },
    'type_name': {
        'rules': [
            {'rule': ['specifier_qualifier_list','abstract_declarator'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE']},
            {'rule': ['specifier_qualifier_list'], 'first': ['VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE']}
        ],
        'follow': [')',':']
    },
    'type_qualifier': {
        'rules': [
            {'rule': ['CONST'], 'first': ['CONST']},
            {'rule': ['RESTRICT'], 'first': ['RESTRICT']},
            {'rule': ['VOLATILE'], 'first': ['VOLATILE']},
            {'rule': ['ATOMIC'], 'first': ['ATOMIC']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS',';','*','IDENTIFIER','(','[',':','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','GENERIC','INC_OP','DEC_OP','&','+','-','~','!','SIZEOF','ALIGNOF',']',')',',']
    },
    'type_qualifier_list': {
        'rules': [
            {'rule': ['type_qualifier'], 'first': ['CONST','RESTRICT','VOLATILE','ATOMIC']},
            {'rule': ['type_qualifier_list','type_qualifier'], 'first': ['CONST','RESTRICT','VOLATILE','ATOMIC']}
        ],
        'follow': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF','STATIC',']','CONST','RESTRICT','VOLATILE','ATOMIC','[',')',':',',']
    },
    'type_specifier': {
        'rules': [
            {'rule': ['VOID'], 'first': ['VOID']},
            {'rule': ['CHAR'], 'first': ['CHAR']},
            {'rule': ['SHORT'], 'first': ['SHORT']},
            {'rule': ['INT'], 'first': ['INT']},
            {'rule': ['LONG'], 'first': ['LONG']},
            {'rule': ['FLOAT'], 'first': ['FLOAT']},
            {'rule': ['DOUBLE'], 'first': ['DOUBLE']},
            {'rule': ['SIGNED'], 'first': ['SIGNED']},
            {'rule': ['UNSIGNED'], 'first': ['UNSIGNED']},
            {'rule': ['BOOL'], 'first': ['BOOL']},
            {'rule': ['COMPLEX'], 'first': ['COMPLEX']},
            {'rule': ['IMAGINARY'], 'first': ['IMAGINARY']},
            {'rule': ['atomic_type_specifier'], 'first': ['ATOMIC']},
            {'rule': ['struct_or_union_specifier'], 'first': ['STRUCT','UNION']},
            {'rule': ['enum_specifier'], 'first': ['ENUM']},
            {'rule': ['TYPEDEF_NAME'], 'first': ['TYPEDEF_NAME']}
        ],
        'follow': ['TYPEDEF','EXTERN','STATIC','THREAD_LOCAL','AUTO','REGISTER','VOID','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE','SIGNED','UNSIGNED','BOOL','COMPLEX','IMAGINARY','ATOMIC','STRUCT','UNION','ENUM','TYPEDEF_NAME','CONST','RESTRICT','VOLATILE','INLINE','NORETURN','ALIGNAS',';','*','IDENTIFIER','(','[',':',')',',']
    },
    'unary_expression': {
        'rules': [
            {'rule': ['postfix_expression'], 'first': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC']},
            {'rule': ['INC_OP','unary_expression'], 'first': ['INC_OP']},
            {'rule': ['DEC_OP','unary_expression'], 'first': ['DEC_OP']},
            {'rule': ['unary_operator','cast_expression'], 'first': ['&','*','+','-','~','!']},
            {'rule': ['SIZEOF','unary_expression'], 'first': ['SIZEOF']},
            {'rule': ['SIZEOF','(','type_name',')'], 'first': ['SIZEOF']},
            {'rule': ['ALIGNOF','(','type_name',')'], 'first': ['ALIGNOF']}
        ],
        'follow': ['=','MUL_ASSIGN','DIV_ASSIGN','MOD_ASSIGN','ADD_ASSIGN','SUB_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','*','/','%','+','-','LEFT_OP','RIGHT_OP','<','>','LE_OP','GE_OP','EQ_OP','NE_OP','&','^','|','AND_OP','?','OR_OP',']',',',')',':',';','}']
    },
    'unary_operator': {
        'rules': [
            {'rule': ['&'], 'first': ['&']},
            {'rule': ['*'], 'first': ['*']},
            {'rule': ['+'], 'first': ['+']},
            {'rule': ['-'], 'first': ['-']},
            {'rule': ['~'], 'first': ['~']},
            {'rule': ['!'], 'first': ['!']}
        ],
        'follow': ['IDENTIFIER','I_CONSTANT','F_CONSTANT','ENUMERATION_CONSTANT','STRING_LITERAL','FUNC_NAME','(','GENERIC','INC_OP','DEC_OP','&','*','+','-','~','!','SIZEOF','ALIGNOF']
    },
}
