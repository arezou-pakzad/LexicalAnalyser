# from lexical_analyser import get_token_one_by_one
input_file = open("input.txt", 'r')
code = input_file.read()

output_file = open("scanner.txt", 'w+')
first_output = True

error_file = open("lexical_errors.txt", 'w+')
first_error = True

parser_file_dir = 'parser.txt'
parser_file = open(parser_file_dir, 'w+')

start_ind = 0
end_ind = 0
ind = -1
current_char = ''
next_char = ''
line_num = 1
line_changed = True
error_line_changed = True

TOKEN_INITIAL = 0
TOKEN_NUM = 1
TOKEN_KEYWORD = 2
TOKEN_ID = 3
TOKEN_SYMBOL = 4
TOKEN_COMMENT = 5
TOKEN_WHITESPACE = 6
TOKEN_EOF = 7
EOF = "@EOF@"
state = TOKEN_INITIAL
symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
whitespace = ['\n', '\r', '\t', ' ', '\v', '\f']
digit = [str(i) for i in range(10)]
alphabet = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
keywords = ['if', 'else', 'void', 'int', 'while', 'break', 'continue', 'switch', 'default', 'case', 'return', 'int']
comments = ['/', '*']
all_letters = symbols + whitespace + digit + alphabet + keywords + comments

current_token_type = current_token_string = ''


def get_string():
    global start_ind, end_ind, code
    return code[start_ind:end_ind]  # TODO- end_int + 1 ????


def get_char():
    global ind, code, current_char, next_char
    ind += 1
    if ind < len(code):
        current_char = code[ind]
        if ind + 1 < len(code):
            next_char = code[ind + 1]
        return current_char

    current_char = None
    return EOF


def num():
    global end_ind
    while current_char is not None:
        if current_char not in digit:
            if current_char in symbols or current_char in whitespace or current_char in all_letters:
                return True, get_string(), 'NUM'
            else:
                return False, get_string() + current_char, 'invalid input'
        get_char()
        end_ind = ind
    return True, get_string(), 'NUM'


def symbol():
    global end_ind
    if current_char == '=':
        if next_char == '=':
            get_char()
            end_ind = ind

    get_char()
    end_ind = ind
    return True, get_string(), 'SYMBOl'


def skip_whitespace():
    global line_num, line_changed, error_line_changed
    global end_ind
    while current_char in whitespace:
        if current_char == '\n':
            line_num += 1
            line_changed = True
            error_line_changed = True
        get_char()
        end_ind = ind


def id():
    global end_ind, ind
    while current_char is not None:

        if (current_char not in digit) and (current_char not in alphabet):
            if current_char in symbols or current_char in whitespace:
                if get_string() in keywords:
                    return True, get_string(), 'KEYWORD'

                return True, get_string(), 'ID'
            else:
                return False, get_string() + current_char, 'invalid input'
        get_char()
        end_ind = ind

    return True, get_string(), 'ID'


def comment():
    global end_ind
    if next_char == '/':
        get_char()
        end_ind = ind
        while current_char is not '\n' and current_char is not None:
            get_char()
            end_ind = ind

        return True, None, 'COMMENT'
    if next_char == '*':
        get_char()
        end_ind = ind

        while current_char is not None and (current_char + next_char != '*/'):
            get_char()
            end_ind = ind

        get_char()
        get_char()
        end_ind = ind

        return True, None, 'COMMENT'

    get_char()
    return False, get_string() + current_char, 'invald input'


def get_token_one_by_one():
    global state, end_ind, start_ind
    # get_char()
    error_flag = False
    token_string = token_type = ''
    while current_char is not None and not error_flag:
        error_flag = False
        skip_whitespace()
        start_ind = ind
        if current_char in digit:
            state = TOKEN_NUM
            is_token, token_string, token_type = num()

        elif current_char in symbols:
            state = TOKEN_SYMBOL
            is_token, token_string, token_type = symbol()

        elif current_char in alphabet:
            is_token, token_string, token_type = id()

        elif current_char == '/':
            state = TOKEN_COMMENT
            is_token, token_string, token_type = comment()

        else:
            is_token = False
            token_type = 'invalid input'
            token_string = current_char

        print('token string:          ', token_string, '   index:', start_ind)
        if is_token and state != TOKEN_COMMENT:
            print_token(token_type, token_string)
            start_ind = ind
            state = TOKEN_INITIAL
            return token_type, token_string
        elif not is_token:
            get_char()
            error_flag = True
            print_error(token_type, token_string)

        start_ind = ind
        state = TOKEN_INITIAL
    return token_type, token_string


def get_next_token():
    global state, end_ind, start_ind
    get_char()
    is_token = False
    token_string = token_type = ''
    while current_char is not None:
        skip_whitespace()
        start_ind = ind
        if current_char in digit:
            state = TOKEN_NUM
            is_token, token_string, token_type = num()

        elif current_char in symbols:
            state = TOKEN_SYMBOL
            is_token, token_string, token_type = symbol()

        elif current_char in alphabet:
            is_token, token_string, token_type = id()

        elif current_char == '/':
            state = TOKEN_COMMENT
            is_token, token_string, token_type = comment()

        else:
            is_token = False
            token_type = 'invalid input'
            token_string = current_char

        if is_token and state != TOKEN_COMMENT:
            print_token(token_type, token_string)
        elif not is_token:
            get_char()
            print_error(token_type, token_string)

        start_ind = ind
        state = TOKEN_INITIAL


def print_token(token_type, token_string):
    global output_file, line_changed, first_output

    if line_changed and not first_output:
        # print()
        output_file.write('\n')
    if line_changed:

        # print(str(line_num) + '. (' + token_type + ', ' + token_string + ')', end='')
        output_file.write(str(line_num) + '. (' + token_type + ', ' + token_string + ')')
        line_changed = False
    else:

        # print(' (' + token_type + ', ' + token_string + ')', end='')
        output_file.write(' (' + token_type + ', ' + token_string + ')')
    first_output = False


def print_error(token_type, token_string):
    global error_file, error_line_changed, first_error
    if error_line_changed and not first_error:
        # print()
        error_file.write('\n')
    if error_line_changed:
        # print(str(line_num) + '. (' + token_string + ', ' + token_type + ')', end='')
        error_file.write(str(line_num) + '. (' + token_string + ', ' + token_type + ')')
        error_line_changed = False
    else:
        # print(' (' + token_string + ', ' + token_type + ')', end='')
        error_file.write(' (' + token_string + ', ' + token_type + ')')
    first_error = False


class Non_terminal:
    def __init__(self, name, first_set, follow_set):
        self.name = name
        self.first_set = first_set
        self.follow_set = follow_set
        self.transition_dictionary = dict()
        self.final_state = 0
        self.initial_state = 0

    def set_transition_dictionary(self, transition_dictionary, initial_state, final_state):
        self.transition_dictionary = transition_dictionary
        self.final_state = final_state
        self.initial_state = initial_state



def write_to_parser_file(height, leaf):
    for i in range(height):
        parser_file.write('| ')
    parser_file.write(leaf + '\n')


def get_new_token():
    global current_token_type, current_token_string
    current_token_type, current_token_string = get_token_one_by_one()
    if current_token_type == 'SYMBOl':
        current_token_type = current_token_string
    elif current_token_type == '':
        current_token_type = '$'
    elif current_token_type == 'KEYWORD':
        current_token_type = current_token_string
    print(current_token_type, '     ', current_token_string)


def parser(non_terminal, height):
    global current_token_type, current_token_string

    print('function: ', non_terminal.name)
    error_flag = False
    write_to_parser_file(height=height, leaf=non_terminal.name)
    s = non_terminal.initial_state
    while s != non_terminal.final_state and parser.running:
        flag = False
        this_state = {}
        for key, value in non_terminal.transition_dictionary.items():
            if key[0] == s:
                this_state[key] = value
        print('this state:', this_state)
        print('current state and token type: ', (s, current_token_type))
        print('len this state: ', len(this_state))
        if len(this_state) == 1:
            terminal_edge = list(this_state.keys())[0][1]
            if isinstance(terminal_edge, str) and terminal_edge != current_token_type:
                if current_token_type != '$':
                    # TODO error #LINE_NUM : Syntax Error! Missing #TERMINAL_NAME
                    print('error #LINE_NUM : Syntax Error! Missing #TERMINAL_NAME')
                    print('state: ', s, ' terminal edge: ', terminal_edge, ' token:', current_token_type)

                else:
                    print('LINE_NUM : Syntax Error! Malformed Input')
                    # TODO LINE_NUM : Syntax Error! Malformed Input
                    parser.running = False

        if (s, current_token_type) in this_state:  # .items added
            print('found the terminal edge')
            s = non_terminal.transition_dictionary[(s, current_token_type)]
            print('next state: ', s)
            write_to_parser_file(height + 1, current_token_type)
            print()
            get_new_token()
            if s == non_terminal.final_state:
                print(non_terminal.name, ' finished')
            flag = True

        elif len(this_state) > 0:
            for key, value in this_state.items():
                print(isinstance(key[1], Non_terminal) and (current_token_type in key[1].first_set))
                if isinstance(key[1], Non_terminal) and (current_token_type in key[1].first_set or
                                                         (('EPSILON' in key[
                                                             1].first_set or error_flag) and current_token_type in key[
                                                              1].follow_set)):
                    if error_flag and 'EPSILON' not in key[1].first_set and current_token_type not in key[1].first_set:
                        print('Syntax Error! Missing #NON_TERMINAL_DESCRIPTION')
                        # TODO #LINE_NUM : Syntax Error! Missing #NON_TERMINAL_DESCRIPTION
                        s = value
                        error_flag = False
                        flag = True
                        break

                    print('inside')
                    print((key[0], key[1].name), value)
                    res = parser(key[1], height + 1)
                    s = value
                    flag = True
                    if not res:
                        # TODO: error handling
                        return False
                    break
        if not flag and (s, 'EPSILON') in this_state.keys():  # what is this?
            print('Epsilon')
            flag = True
            write_to_parser_file(height + 1, 'EPSILON')
            s = non_terminal.transition_dictionary[(s, 'EPSILON')]
            print()
            if s == non_terminal.final_state:
                print(non_terminal.name, ' finished')
        if not flag:
            # TODO write error
            get_new_token()
            if current_token_type == '$':
                print('Syntax Error! Unexpected EndOfFile')
                # TODO #LINE_NUM : Syntax Error! Unexpected EndOfFile
                parser.running = False

            error_flag = True

    return True



program	= Non_terminal(name = 'program', first_set=['$', 'int', 'void'], follow_set=[])

DeclarationList = Non_terminal(name = 'declaration_list', first_set= ['EPSILON', 'int', 'void'] ,
                               follow_set=['$', '{', 'continue', 'break', ';', 'if',
'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}'])


DeclarationList1 = Non_terminal(name = 'declaration_list1', first_set= ['EPSILON', 'int', 'void'],
                                follow_set=['$', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-',
                                            '(', 'NUM', '}'])
Declaration	= Non_terminal(name = 'declatation', first_set=['int', 'void'],
                              follow_set =['int', 'void', '$', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch'
                                  , 'ID', '+', '-', '(', 'NUM', '}'])

FTypeSpecifier2 = Non_terminal(name = 'FTypeSpecifier2', first_set=	['ID'],
                               follow_set=['int', 'void', 'eof', '{', 'continue',
'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}'])

VarDeclaration	= Non_terminal(name= 'var_declaration', first_set=['int', 'void'], follow_set=[])

FTypeSpecifier	= Non_terminal(name= 'FTypeSpecifier', first_set= ['ID'],
                                 follow_set=['int', 'void', '$', '{', 'continue', 'break', ';', 'if', 'while',
'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}'])

FID1 = Non_terminal(name = 'FID1', first_set=[';', '['],
                    follow_set=['int', 'void', '$', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}'])

TypeSpecifier = Non_terminal(name = 'TypeSpecifier', first_set=['int', 'void'],
                             follow_set=['ID'])
FunDeclaration = Non_terminal(name = 'FunDeclaration', first_set=	['int', 'void'], follow_set=[])

Params	= Non_terminal(name = 'params', first_set=['int', 'void'], follow_set=[')'])
Fvoid	= Non_terminal(name = 'Fvoid', first_set=['EPSILON', 'ID'], follow_set=[')'])
ParamList	= Non_terminal(name = 'ParamList', first_set=['int', 'void'], follow_set=[])
ParamList1	= Non_terminal(name = 'param_list1', first_set=[',', 'EPSILON'], follow_set=[')'])
Param = Non_terminal(name = 'param', first_set=['int', 'void'], follow_set= [',' ')'])
FTypeSpecifier1 = Non_terminal(name = 'FTypeSpecifier1', first_set=['ID'], follow_set=[',', ')'])
FID2 = Non_terminal(name = 'FID2', first_set=['EPSILON', '['], follow_set=[',', ')'])
CompoundStmt = Non_terminal(name = 'CompoundStmt', first_set=['{'],
                            follow_set=['int', 'void', '$', '{', 'continue',
                        'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else', 'case', 'default'])
StatementList = Non_terminal(name = 'StatementList', first_set=['EPSILON', '{', 'continue',
                        'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM'], follow_set=['}', 'case', 'default'])

StatementList1	= Non_terminal(name = 'StatementList1',
                                 first_set=['EPSILON','{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM'],
                                 follow_set=['}', 'case', 'default'])
Statement	= Non_terminal(name = 'Statement',
                            first_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM'],
            follow_set = ['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else', 'case', 'default'])

ExpressionStmt	= Non_terminal(name = 'ExpressionStmt', first_set=['continue', 'break', ';', 'ID', '+', '-', '(', 'NUM'],
                                 follow_set=['{', 'continue', 'break', ';', 'if', 'while',
                                        'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else', 'case', 'default'])
SelectionStmt = Non_terminal(name = 'SelectionStmt', first_set=['if'],
                             follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM',
                                '}', 'else', 'case', 'default'])
IterationStmt = Non_terminal(name = 'IterationStmt', first_set=['while'],
                             follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return',
                                         'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else', 'case', 'default'])
ReturnStmt	= Non_terminal(name = 'ReturnStmt', first_set=['return'],
                             follow_set=['{', 'continue', 'break', ';',
                             'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}',
                                         'else', 'case', 'default'])
Freturn	= Non_terminal(name = 'Freturn', first_set=[';', 'ID', '+', '-', '(', 'NUM'],
                          follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch',
                                      'ID', '+', '-', '(', 'NUM', '}', 'else', 'case', 'default'])
SwitchStmt = Non_terminal(name = 'SwitchStmt', first_set=['switch'],
                          follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch',
                                      'ID', '+', '-', '(', 'NUM', '}', 'else', 'case', 'default'])
CaseStmts = Non_terminal(name = 'CaseStmts', first_set=['EPSILON', 'case'], follow_set=['default', '}'])
CaseStmts1	= Non_terminal(name = 'CaseStmts1', first_set=['EPSILON', 'case'], follow_set=['default', '}'])
CaseStmt = Non_terminal(name = 'CaseStmt', first_set=['case'], follow_set=['case', 'default', '}'])
DefaultStmt	= Non_terminal(name = 'DefaultStmt', first_set=['default','EPSILON'], follow_set=['}'])
Expression	= Non_terminal(name = 'Expression', first_set=['ID', '+', '-', '(', 'NUM'],
                             follow_set=[';', ')', ']', ','])
Var	= Non_terminal(name='Var', first_set=['ID'], follow_set=['=', '*', '+', '-', '<', '==', ';', ')', ']', ','])
FID = Non_terminal(name = 'FID', first_set=['EPSILON', '['], follow_set=['=', '*', '+', '-', '<', '==', ';', ')', ']', ','])
SimpleExpression = Non_terminal(name = 'SimpleExpression', first_set = ['+', '-', '(', 'ID', 'NUM'], follow_set=[';', ')', ']', ','])
FAdditiveExpression = Non_terminal(name = 'FAdditiveExpression', first_set=['EPSILON', '<', '=='], follow_set=[';', ')', ']', ','])
Relop = Non_terminal(name = 'Relop', first_set = ['<', '=='], follow_set=['+', '-', '(', 'ID', 'NUM'])
AdditiveExpression	= Non_terminal(name = 'AdditiveExpression', first_set = ['+', '-', '(', 'ID', 'NUM'],
                                     follow_set=['<', '==', ';', ')', ']', ','])
AdditiveExpression1 = Non_terminal(name = 'AdditiveExpression1', first_set=['EPSILON', '+', '-'], follow_set=['<', '==', ';', ')', ']', ','])
Addop = Non_terminal(name = 'Addop', first_set = ['+', '-'], follow_set=['+', '-', '(', 'ID', 'NUM'])
Term = Non_terminal(name = 'Term', first_set = ['+', '-', '(', 'ID', 'NUM'], follow_set=['+', '-', '<', '==', ';', ')', ']', ','])
Term1 = Non_terminal(name = 'term1', first_set = ['*', 'EPSILON'], follow_set=['+', '-', '<', '==', ';', ')', ']', ','])
SignedFactor = Non_terminal(name = 'SignedFactor', first_set = ['+', '-', '(', 'ID', 'NUM'], follow_set=['*', '+', '-', '<', '==', ';', ')', ']', ','])

Factor	= Non_terminal(name = 'Factor', first_set = ['(', 'ID', 'NUM'], follow_set=['*', '+', '-', '<', '==', ';', ')', ']', ','])
Call = Non_terminal(name = 'Call', first_set=['ID'], follow_set = ['*', '+', '-', '<', '==', ';', ')', ']', ','])
Args = Non_terminal(name = 'Args', first_set=['EPSILON', 'ID', '+', '-', '(', 'NUM'], follow_set=[')'])
ArgList	= Non_terminal(name = 'ArgList', first_set=['ID', '+', '-', '(', 'NUM'], follow_set=[')'])
ArgList1 = Non_terminal(name = 'ArgList1', first_set=[',', 'EPSILON'], follow_set=[')'])



program_dictionary = {(0, DeclarationList): 1, (1, '$') :2}
program.set_transition_dictionary(program_dictionary,0 , 2)

DeclarationList_dictionary = {(0, DeclarationList1): 1}
DeclarationList.set_transition_dictionary(DeclarationList_dictionary, 0, 1)


DeclarationList1_dictionary = {(0, Declaration) : 1, (1, DeclarationList1) : 2, (0, 'EPSILON') : 2}
DeclarationList1.set_transition_dictionary(DeclarationList1_dictionary, 0 , 2)

Declaration_dictionary = {(0, TypeSpecifier) : 1, (1, FTypeSpecifier2) : 2}
Declaration.set_transition_dictionary(Declaration_dictionary, 0 , 2)


FTypeSpecifier2_dictionary = {(0, FTypeSpecifier) : 1,
                              (0, 'ID') : 2,
                              (2, '(') : 3,
                              (3, Params) : 4,
                              (4, ')') : 5,
                              (5, CompoundStmt) : 1}
FTypeSpecifier2.set_transition_dictionary(FTypeSpecifier2_dictionary, 0, 1)


VarDeclaration_dictionary = {(0, TypeSpecifier) : 1, (1, FTypeSpecifier) : 2}
VarDeclaration.set_transition_dictionary(VarDeclaration_dictionary, 0 , 2)

FTypeSpecifier_dictionary = {(0, 'ID'): 1, (1, FID1) : 2}
FTypeSpecifier.set_transition_dictionary(FTypeSpecifier_dictionary, 0, 2)

FID1_dictionary = {(0, '[') : 1,(1,'NUM') : 2, (2, ']') : 3, (3, ';'): 4, (0, ';') : 4}
FID1.set_transition_dictionary(FID1_dictionary, 0 , 4)

TypeSpecifier_dictionary = {(0, 'int') : 1, (0, 'void') : 1}

TypeSpecifier.set_transition_dictionary(TypeSpecifier_dictionary, 0 , 1)

FunDeclaration_dictionary = {(0, TypeSpecifier) : 1, (1, 'ID') : 2, (2, '(') : 3, (3, Params) : 4, (5, CompoundStmt) : 6}

Params_dictionary = {(0, 'int') : 1, (1, FTypeSpecifier1) : 2, (2, ParamList1) : 3, (0, 'void') : 4, (4, Fvoid) : 3}
Params.set_transition_dictionary(Params_dictionary, 0, 3)

Fvoid_dictionary = {(0, FTypeSpecifier1) : 1, (1, ParamList1) : 2, (0, 'EPSILON') : 2}
Fvoid.set_transition_dictionary(Fvoid_dictionary, 0 , 2)

ParamList_dictionary = {
    (0, Param) : 1,
    (1, ParamList1) : 2
}
ParamList.set_transition_dictionary(ParamList_dictionary, 0, 2)

ParamList1_dictionary = {
    (0,',') : 1,
    (1, Param) : 2,
    (2, ParamList1) : 3,
    (0, 'EPSILON'): 3
}
ParamList1.set_transition_dictionary(ParamList1_dictionary, 0, 3)

Param_dictionary = {
    (0, TypeSpecifier) : 1,
    (1, FTypeSpecifier1) : 2
}
Param.set_transition_dictionary(Param_dictionary, 0, 2)

FTypeSpecifier1_dictionary = {
    (0, 'ID') : 1,
    (1, FID2) : 2
}
FTypeSpecifier1.set_transition_dictionary(FTypeSpecifier1_dictionary, 0, 2)

FID2_dictionary = {(0, 'EPSILON') : 1, (0, '[') : 2, (2, ']') : 1}
FID2.set_transition_dictionary(FID2_dictionary, 0 , 1)

CompoundStmt_dictionary = {(0, '{') : 1, (1, DeclarationList1) : 2, (2, StatementList) : 3, (3, '}') : 4}
CompoundStmt.set_transition_dictionary(CompoundStmt_dictionary, 0, 4)

StatementList_dictionary = {(0, StatementList1) : 1}
StatementList.set_transition_dictionary(StatementList_dictionary, 0 , 1)
StatementList1_dictionary = {(0, Statement) : 1, (1, StatementList1) : 2, (0, 'EPSILON') : 2}
StatementList1.set_transition_dictionary(StatementList1_dictionary, 0 , 2)

Statement_dictionary = {(0, ExpressionStmt) : 1, (0, CompoundStmt) :1 , (0, SelectionStmt) :1 ,
                        (0, IterationStmt) : 1,
                        (0, ReturnStmt) : 1,
                        (0, SwitchStmt) : 1}

Statement.set_transition_dictionary(Statement_dictionary, 0, 1)

ExpressionStmt_dictionary = {(0, Expression) : 1, (1, ';') : 2, (0, 'continue') : 2, (0, 'break') : 2, (0, ';') : 2}

ExpressionStmt.set_transition_dictionary(ExpressionStmt_dictionary, 0, 2)

SelectionStmt_dictionary = {(0, 'if') : 1, (1, '(') :2 , (2, Expression) : 3, (3, ')') : 4, (4, Statement) : 5, (5, 'else') : 6, (6, Statement) : 7}
SelectionStmt.set_transition_dictionary(SelectionStmt_dictionary, 0, 7)

IterationStmt_dictionary = {(0, 'while') : 1, (1, '(') : 2, (2, Expression) : 3, (3, ')') : 4, (4, Statement) : 5 }
IterationStmt.set_transition_dictionary(IterationStmt_dictionary, 0, 5)

ReturnStmt_dictionary = {(0, 'return') : 1, (1, Freturn) : 2}
ReturnStmt.set_transition_dictionary(ReturnStmt_dictionary, 0, 2)
Freturn_dictionary = {(0, ';'): 1, (0, Expression) : 2, (2, ';') : 1}

Freturn.set_transition_dictionary(Freturn_dictionary, 0 ,1)

SwitchStmt_dictionary = {(0, 'switch') : 1, (1, '(') : 2, (2, Expression) : 3, (3, ')') : 4, (4, '{'): 5, (5, CaseStmts) : 6, (6, DefaultStmt) : 7, (7, '}') : 8}
SwitchStmt.set_transition_dictionary(SwitchStmt_dictionary, 0, 8)

CaseStmts_dictionary = {(0, CaseStmts1) : 1}
CaseStmts.set_transition_dictionary(CaseStmts_dictionary, 0 , 1)
CaseStmts1_dictionary = {(0, CaseStmt) : 1, (1, CaseStmts1) : 2, (0, 'EPSILON') : 2}
CaseStmts1.set_transition_dictionary(CaseStmts1_dictionary, 0, 2)

CaseStmt_dictionary = {(0, 'case') : 1, (1, 'NUM') : 2, (2, ':') : 3, (3, StatementList) : 4}
CaseStmt.set_transition_dictionary(CaseStmt_dictionary, 0 , 4)
DefaultStmt_dictionary = {(0, 'default') : 1, (1, ':') : 2, (2, StatementList) : 3, (0, 'EPSILON') : 3}
DefaultStmt.set_transition_dictionary(DefaultStmt_dictionary, 0, 3)
Expression_dictionary = {(0, Var) : 1, (1, '=') : 2, (2, Expression) : 3, (0, SimpleExpression) : 3}
Expression.set_transition_dictionary(Expression_dictionary, 0, 3)
Var_dictionary = {(0, 'ID') : 1, (1, FID):2}
Var.set_transition_dictionary(Var_dictionary, 0, 2)

FID_dictionary = {(0, 'EPSILON') : 1, (0, '[') : 2, (2, Expression)  : 3, (3, ']') : 1}
FID.set_transition_dictionary(FID_dictionary, 0 , 1)

SimpleExpression_dictionary = {(0, AdditiveExpression) : 1 , (1, FAdditiveExpression) : 2}
SimpleExpression.set_transition_dictionary(SimpleExpression_dictionary, 0, 2)
FAdditiveExpression_dictionary = {(0, Relop) : 1, (1, AdditiveExpression) : 2, (0, 'EPSILON') : 2}
FAdditiveExpression.set_transition_dictionary(FAdditiveExpression_dictionary, 0, 2)
Relop_dictionary = {(0, '==') : 1, (0, '<') : 1}
Relop.set_transition_dictionary(Relop_dictionary, 0, 1)
AdditiveExpression_dictionary = {(0, Term) : 1, (1, AdditiveExpression1) : 2}
AdditiveExpression.set_transition_dictionary(AdditiveExpression_dictionary, 0 , 2)

AdditiveExpression1_dictionary = {(0, Addop) : 1,(1, Term) : 2, (2, AdditiveExpression1) : 3, (0, 'EPSILON') :3}
AdditiveExpression1.set_transition_dictionary(AdditiveExpression1_dictionary, 0, 3)

Addop_dictionary = {(0, '+') : 1 , (0, '-') : 1}
Addop.set_transition_dictionary(Addop_dictionary, 0, 1)
Term_dictionary = {(0, SignedFactor) : 1,  (1, Term1) : 2}

Term.set_transition_dictionary(Term_dictionary, 0, 2)
Term1_dictionary = {(0, '*') : 1, (1, SignedFactor) : 2 , (2, Term1) : 3, (0, 'EPSILON') : 3}
Term.set_transition_dictionary(Term1_dictionary, 0, 3)
SignedFactor_dictionary = {(0, Factor) : 1, (0, '+') : 2, (2, Factor) : 1, (0, '-') : 3, (3, Factor) : 1}
SignedFactor.set_transition_dictionary(SignedFactor_dictionary, 0 , 1)
Factor_dictionary = {(0, '(') : 1 ,(1, Expression) : 2, (2, ')') :3, (0, Var) : 3, (0, Call) : 3, (0, 'NUM') : 3}
Factor.set_transition_dictionary(Factor_dictionary, 0, 3)
Call_dictionary = {(0, 'ID') : 1, (1, '(') : 2, (2, Args) : 3, (3, ')') : 4}
Call.set_transition_dictionary(Call_dictionary, 0, 4)
Args_dictionary = {(0, ArgList) : 1, (0, 'EPSILON') : 1}
Args.set_transition_dictionary(Args_dictionary, 0, 1)
ArgList_dictionary = {(0, Expression) : 1, (1, ArgList1) : 2}
ArgList.set_transition_dictionary(ArgList_dictionary, 0, 2)
ArgList1_dictionary = {(0, ',') : 1 , (1, Expression) : 2, (2, ArgList1) : 3, (0, 'EPSILON') : 3}
ArgList1.set_transition_dictionary(ArgList1_dictionary, 0, 3)


























get_char()
get_new_token()
parser.running = True
parser(program, height=0)

























































































