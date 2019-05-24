# from lexical_analyser import get_token_one_by_one
input_file = open("input.txt", 'r')
code = input_file.read()

output_file = open("scanner.txt", 'w+')
first_output = True

error_file = open("errors.txt", 'w+')
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


program = Non_terminal(name='program', first_set=['$', 'int', 'void'], follow_set=[])
declaration_list = Non_terminal(name='declaration_list', first_set=['EPSILON', 'int', 'void'],
                                follow_set=['$', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+',
                                            '-', 'ID', '}'])

declaration_list_1 = Non_terminal(name='declaration_list_1', first_set=['EPSILON', 'int', 'void'],
                                  follow_set=['$', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch',
                                              '+', '-', 'ID', '}'])

declaration = Non_terminal(name='declaration', first_set=['int', 'void'],
                           follow_set=['int', 'void', '$', '{', 'continue', 'break', ';', 'if', 'while', 'return',
                                       'switch', '+', '-', 'ID', '}'])

V1 = Non_terminal(name='V1', first_set=['(', ';', '['],
                  follow_set=['int', 'void', '$', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+',
                              '-', 'ID', '}'])

var_declaration = Non_terminal(name='var_declaration', first_set=['int', 'void'], follow_set=[])

prime = Non_terminal(name='prime', first_set=[';', '['],
                     follow_set=['int', 'void', '$', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch',
                                 '+', '-', 'ID', '}'])

type_specifier = Non_terminal(name='type_specifier', first_set=['int', 'void'], follow_set=['ID'])

fun_declaration = Non_terminal(name='fun_declaration', first_set=['int', 'void'], follow_set=[])

params = Non_terminal(name='params', first_set=['void'], follow_set=[')'])

param_list1 = Non_terminal(name='param_list1', first_set=['EPSILON', 'ID'], follow_set=[')'])

param_list = Non_terminal(name='param_list', first_set=['int', 'void'], follow_set=[])

param_list_1 = Non_terminal(name='param_list_1', first_set=[',', 'EPSILON'], follow_set=[')'])

param = Non_terminal(name='param', first_set=['int', 'void'], follow_set=[',', ')'])

prime1 = Non_terminal(name='prime1', first_set=['[', 'EPSILON'], follow_set=[',', ')'])

compound_stmt = Non_terminal(name='compound_stmt', first_set=['{'],
                             follow_set=['int', 'void', '$', '{', 'continue', 'break', ';', 'if', 'while', 'return',
                                         'switch', '+', '-', 'ID', '}', 'else', 'case', 'default'])

statement_list = Non_terminal(name='statement_list',
                              first_set=['EPSILON', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch',
                                         '+', '-', 'ID'],
                              follow_set=['}', 'case', 'default'])

statement_list_1 = Non_terminal(name='statement_list_1',
                                first_set=['EPSILON', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch',
                                           '+', '-', 'ID'],
                                follow_set=['}', 'case', 'default'])

statement = Non_terminal(name='statement',
                         first_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+', '-', 'ID'],
                         follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+', '-', 'ID',
                                     '}', 'else', 'case', 'default'])

expression_stmt = Non_terminal(name='expression_stmt', first_set=['continue', 'break', ';', '+', '-', 'ID'],
                               follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+', '-',
                                           'ID', '}', 'else', 'case', 'default'])

selection_stmt = Non_terminal(name='selection_stmt', first_set=['if'],
                              follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+', '-',
                                          'ID', '}', 'else', 'case', 'default'])

iteration_stmt = Non_terminal(name='iteration_stmt', first_set=['while'],
                              follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+', '-',
                                          'ID', '}', 'else', 'case', 'default'])

return_stmt = Non_terminal(name='return_stmt', first_set=['return'],
                           follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+', '-', 'ID',
                                       '}', 'else', 'case', 'default'])

prime2 = Non_terminal(name='prime2', first_set=[';', '+', '-', 'ID'],
                      follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+', '-', 'ID', '}',
                                  'else', 'case', 'default'])


switch_stmt = Non_terminal(name='switch_stmt', first_set=['switch'],
                           follow_set=['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', '+', '-', 'ID',
                                       '}',
                                       'else', 'case', 'default'])

case_stmts_1 = Non_terminal(name='case_stmts_1', first_set=['EPSILON', 'case'], follow_set=['default', '}'])

case_stmt = Non_terminal(name='case_stmt', first_set=['case'], follow_set=['case', 'default', '}'])

default_stmt = Non_terminal(name='default_stmt', first_set=['default', 'EPSILON'], follow_set=['}'])

expression = Non_terminal(name='expression', first_set=['+', '-', 'ID'], follow_set=[';', ')', ']', ','])

Var4 = Non_terminal(name='Var4', follow_set=[';', ')', ']', ','], first_set=['[', '=', '(', 'ID', 'NUM'])

var = Non_terminal(name='Var', first_set=['ID'], follow_set=[])

Var3 = Non_terminal(name='Var3', first_set=['[', 'EPSILON'], follow_set=['='])

simple_expression = Non_terminal(name='simple_expression', first_set=['+', '-', '(', 'ID', 'NUM'], follow_set=[])

Var2 = Non_terminal(name='Var2', first_set=['EPSILON', '<', '=='], follow_set=[';', ')', ']', ','])

relop = Non_terminal(name='relop', first_set=['<', '=='], follow_set=['+', '-', '(', 'ID', 'NUM'])

additive_expression = Non_terminal(name='additive_expression', first_set=['+', '-', '(', 'ID', 'NUM'],
                                   follow_set=['<', '==', ';', ')', ']', ','])

additive_expression_1 = Non_terminal(name='additive_expression_1', first_set=['EPSILON', '+', '-'],
                                     follow_set=['<', '==', ';', ')', ']', ','])

addop = Non_terminal(name='addop', first_set=['+', '-'], follow_set=['+', '-', '(', 'ID', 'NUM'])

term = Non_terminal(name='term', first_set=['+', '-', '(', 'ID', 'NUM'],
                    follow_set=['+', '-', '<', '==', ';', ')', ']', ','])

term_1 = Non_terminal(name='term_prime', first_set=['*', 'EPSILON'],
                      follow_set=['+', '-', '<', '==', ';', ')', ']', ','])

signed_factor = Non_terminal(name='signed_factor', first_set=['+', '-', '(', 'ID', 'NUM'],
                             follow_set=['*', '+', '-', '<', '==', ';', ')', ']', ','])

factor = Non_terminal(name='factor', first_set=['(', 'ID', 'NUM'],
                      follow_set=['*', '+', '-', '<', '==', ';', ')', ']', ','])

Var1 = Non_terminal(name='Var1', first_set=['EPSILON', '[', '('],
                    follow_set=['*', '+', '-', '<', '==', ';', ')', ']', ','])

call = Non_terminal(name='call', first_set=['ID'], follow_set=[])

args = Non_terminal(name='args', first_set=['EPSILON, +, -, ID'], follow_set=[')'])

arg_list = Non_terminal(name='arg_list', first_set=['+', '-', 'ID'], follow_set=[')'])

arg_list_1 = Non_terminal(name='arg_list_1', first_set=[',', 'EPSILON'], follow_set=[')'])

switch_stmt_dictionary = {(0, 'switch'): 1, (1, '('): 2, (2, expression): 3, (3, ')'): 4,
                          (4, '{'): 5, (5, case_stmts_1): 6, (6, default_stmt): 7, (7, '}'): 8}
switch_stmt.set_transition_dictionary(switch_stmt_dictionary, 0, 8)

case_stmts_1_dictionary = {(0, case_stmt): 1, (1, case_stmts_1): 2, (0, 'EPSILON'): 2}
case_stmts_1.set_transition_dictionary(case_stmts_1_dictionary, 0, 2)

case_stmt_dictionary = {(0, 'case'): 1, (1, 'NUM'): 2, (2, ':'): 3, (3, statement_list): 4}
case_stmt.set_transition_dictionary(case_stmt_dictionary, 0, 4)

default_stmt_dictinoary = {(0, 'default'): 1, (1, ':'): 2, (2, statement_list): 3, (0, 'EPSILON'): 1}
default_stmt.set_transition_dictionary(default_stmt_dictinoary, 0, 3)

expression_dictionary = {(0, '+'): 1, (1, factor): 2, (2, term_1): 3, (3, additive_expression_1): 4, (4, Var2): 5,
                         (0, '-'): 6, (6, factor): 2, (0, 'ID'): 7, (7, Var4): 5}
expression.set_transition_dictionary(expression_dictionary, 0, 5)

Var4_dictionary = {(0, Var3): 1, (1, '='): 2, (2, expression): 3,
                   (0, factor): 4, (4, term_1): 5, (5, additive_expression_1): 6, (6, Var2): 3}
Var4.set_transition_dictionary(Var4_dictionary, 0, 3)

var_dictionary = {(0, 'ID'): 1, (1, Var3): 2}
var.set_transition_dictionary(var_dictionary, 0, 2)

Var3_dictionary = {(0, '['): 1, (1, expression): 2, (2, ']'): 3, (0, 'EPSILON'): 3}
Var3.set_transition_dictionary(Var3_dictionary, 0, 3)

simple_expression_dictionary = {(0, additive_expression): 1, (1, Var2): 2}
simple_expression.set_transition_dictionary(simple_expression_dictionary, 0, 2)

Var2_dictionary = {(0, relop): 1, (1, additive_expression): 2, (0, 'EPSILON'): 2}
Var2.set_transition_dictionary(Var2_dictionary, 0, 2)

relop_dictionary = {(0, '<'): 1, (1, '=='): 2}
relop.set_transition_dictionary(relop_dictionary, 0, 2)

additive_expression_dictionary = {(0, term): 1, (1, additive_expression_1): 2}
additive_expression.set_transition_dictionary(additive_expression_dictionary, 0, 2)

additive_expression_1_dictionary = {(0, addop): 1, (1, term): 2, (2, additive_expression_1): 3, (0, 'EPSILON'): 3}
additive_expression_1.set_transition_dictionary(additive_expression_1_dictionary, 0, 3)

addop_dictionary = {(0, '+'): 1, (1, '-'): 2}
addop.set_transition_dictionary(addop_dictionary, 0, 2)

term_dictionary = {(0, signed_factor): 1, (1, term_1): 2}
term.set_transition_dictionary(term_dictionary, 0, 2)

term_1_dictionary = {(0, '*'): 1, (1, signed_factor): 2, (2, term_1): 3, (0, 'EPSILON'): 3}
term_1.set_transition_dictionary(term_1_dictionary, 0, 3)

signed_factor_dictionary = {(0, factor): 1, (0, '+'): 2, (2, factor): 1, (0, '-'): 3, (3, factor): 1}
signed_factor.set_transition_dictionary(signed_factor_dictionary, 0, 1)

factor_dictionary = {(0, '('): 1, (1, expression): 2, (2, ')'): 3, (0, 'ID'): 4, (4, Var1): 3, (0, 'NUM'): 3}
factor.set_transition_dictionary(factor_dictionary, 0, 3)

Var1_dictionary = {(0, 'EPSILON'): 1, (0, '['): 2, (2, expression): 3, (3, ']'): 1, (0, '('): 4, (4, args): 5,
                   (5, ')'): 1}
Var1.set_transition_dictionary(Var1_dictionary, 0, 1)

call_dictionary = {(0, 'ID'): 1, (1, '('): 2, (2, args): 3, (3, ')'): 4}
call.set_transition_dictionary(call_dictionary, 0, 4)

args_dictionary = {(0, arg_list): 1, (0, 'EPSILON'): 1}
args.set_transition_dictionary(args_dictionary, 0, 1)

arg_list_dictionary = {(0, expression): 1, (1, arg_list_1): 2}
arg_list.set_transition_dictionary(arg_list_dictionary, 0, 2)

arg_list_1_dictionary = {(0, ','): 1, (1, expression): 2, (2, arg_list_1): 3, (0, 'EPSILON'): 3}
arg_list_1.set_transition_dictionary(arg_list_1_dictionary, 0, 3)

# # First sets
# First sets
# # Sets
# program EOF, int, void
# declaration_list ε, int, void
# declaration_list_prime ε, int, void
# declaration int, void
# V1 (, ;, [
# var_declaration int, void
# prime ;, [
# type_specifier int, void
# fun_declaration int, void
# params void
# param_list1 ε, ID
# param_list int, void
# param_list_prime ,, ε
# param int, void
# prime1 [, ε
# compound_stmt {
# statement_list ε, {, continue, break, ;, if, while, return, switch, +, -, ID
# statement_list_prime ε, {, continue, break, ;, if, while, return, switch, +, -, ID
# statement {, continue, break, ;, if, while, return, switch, +, -, ID
# expression_stmt continue, break, ;, +, -, ID
# selection_stmt if
# iteration_stmt while
# return_stmt return
# prime2 ;, +, -, ID
# switch_stmt switch
# case_stmts_prime ε, case
# case_stmt case
# default_stmt default, ε
# expression +, -, ID
# Var4 [, =, (, ID, NUM
# var ID
# Var3 [, ε
# simple_expression +, -, (, ID, NUM
# Var2 ε, <, ==
# relop <, ==
# additive_expression +, -, (, ID, NUM
# additive_expression_prime ε, +, -
# addop +, -
# term +, -, (, ID, NUM
# term_prime *, ε
# signed_factor +, -, (, ID, NUM
# factor (, ID, NUM
# Var1 ε, [, (
# call ID
# args ε, +, -, ID
# arg_list +, -, ID
# arg_list_prime ,, ε


# Follow sets
# # Sets
# program -|
# declaration_list EOF, {, continue, break, ;, if, while, return, switch, +, -, ID, }
# declaration_list_prime EOF, {, continue, break, ;, if, while, return, switch, +, -, ID, }
# declaration int, void, EOF, {, continue, break, ;, if, while, return, switch, +, -, ID, }
# V1 int, void, EOF, {, continue, break, ;, if, while, return, switch, +, -, ID, }
# var_declaration
# prime int, void, EOF, {, continue, break, ;, if, while, return, switch, +, -, ID, }
# type_specifier ID
# fun_declaration
# params )
# param_list1 )
# param_list
# param_list_prime )
# param ,, )
# prime1 ,, )
# compound_stmt int, void, EOF, {, continue, break, ;, if, while, return, switch, +, -, ID, }, else, case, default
# statement_list }, case, default
# statement_list_prime }, case, default
# statement {, continue, break, ;, if, while, return, switch, +, -, ID, }, else, case, default
# expression_stmt {, continue, break, ;, if, while, return, switch, +, -, ID, }, else, case, default
# selection_stmt {, continue, break, ;, if, while, return, switch, +, -, ID, }, else, case, default
# iteration_stmt {, continue, break, ;, if, while, return, switch, +, -, ID, }, else, case, default
# return_stmt {, continue, break, ;, if, while, return, switch, +, -, ID, }, else, case, default
# prime2 {, continue, break, ;, if, while, return, switch, +, -, ID, }, else, case, default
# switch_stmt {, continue, break, ;, if, while, return, switch, +, -, ID, }, else, case, default
# case_stmts_prime default, }
# case_stmt case, default, }
# default_stmt }
# expression ;, ), ], ,
# Var4 ;, ), ], ,
# var
# Var3 =
# simple_expression
# Var2 ;, ), ], ,
# relop +, -, (, ID, NUM
# additive_expression <, ==, ;, ), ], ,
# additive_expression_prime <, ==, ;, ), ], ,
# addop +, -, (, ID, NUM
# term +, -, <, ==, ;, ), ], ,
# term_prime +, -, <, ==, ;, ), ], ,
# signed_factor *, +, -, <, ==, ;, ), ], ,
# factor *, +, -, <, ==, ;, ), ], ,
# Var1 *, +, -, <, ==, ;, ), ], ,
# call
# args )
# arg_list )
# arg_list_prime )


get_char()
get_new_token()
parser.running = True
parser(program, height=0)
