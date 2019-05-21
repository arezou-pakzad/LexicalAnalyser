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





program = Non_terminal(name = 'program', first_set= ['int', 'void'], follow_set=[])
declaration = Non_terminal(name = 'declaration', first_set=['int','void'],
                           follow_set=['$' ,'int' ,'void', 'continue', 'break' ,'NUM',';', '{', 'if' ,'while', 'return',

                                       'switch', 'id', '+', '-', '(', '}'])
var_declaration = Non_terminal(name = 'var_declaration', first_set=['int', 'void'],
                              follow_set=['$' ,'int' ,'void', 'continue','NUM', 'break' ,';', '{', 'if' ,'while', 'return',

                                       'switch', 'id', '+', '-', '(', '}'] )

fun_declaration = Non_terminal(name = 'var_declaration', first_set=['int', 'void'],
                              follow_set=['$' ,'int' ,'void', 'NUM','continue', 'break' ,';', '{', 'if' ,'while', 'return',

                                       'switch', 'id', '+', '-', '(', '}'])

params = Non_terminal(name = 'params', first_set=['void', 'int'], follow_set=[')'])

param_list = Non_terminal(name = 'param_list', first_set=['int','void'],follow_set=[',', ')'])
param = Non_terminal(name = 'param', first_set=['int','void'],follow_set=[',', ')'])

type_specifier = Non_terminal(name = ['int', 'void'],first_set=['int', 'void'] ,follow_set=['ID'])

declaration_list = Non_terminal(name = 'declaration_list', first_set=['int' ,'void'],
                                follow_set=['$', 'int' ,'void', 'continue',
'break', ';', '{', 'if','while', 'return', 'switch','NUM', 'ID', '+', '-', '(', '}'])

compound_stmt = Non_terminal(name = 'compound_stmt', first_set=['{'],
                             follow_set=['default', 'case', 'else', '$', 'int', 'void',
'continue', 'break', ';', '{', 'if', 'while','NUM', 'return', 'switch', 'id','+', '-', '(', '}'])


expression_stmt = Non_terminal(name = 'expression_stmt', first_set=['continue','NUM', 'break',';', 'id', '+', '-', '('],
                               follow_set=['default' ,'case', 'else', '}', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch',
                                           'ID', '+', '-', 'NUM','('])

selection_stmt = Non_terminal(name = 'selection_stmt' , first_set=['if'],
                              follow_set=['default', 'case', 'else', '}','NUM', 'continue', 'break', ';',
                                          '{', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '('])

iteration_stmt = Non_terminal(name = 'iteration_stmt', first_set=['while'],
                              follow_set=['default','NUM', 'case', 'else', '}', 'continue', 'break', ';', '{',
                              'if', 'while', 'return', 'switch', 'ID' ,'+', '-', '('])

statement = Non_terminal(name = 'statement', first_set=['continue', 'NUM','break', ';', '{', 'if', 'while', 'return', 'switch', 'ID', '+',
                                                        '-', '('],
                         follow_set=['default', 'case', 'else', '}', 'NUM','continue', 'break', ';', '{',
                                     'if', 'while', 'return', 'switch', 'ID', '+', '-', '('])

return_stmt = Non_terminal(name = 'return_stmt', first_set= ['return'], follow_set=['default', 'case', 'else', '}', 'continue', 'break', ';', '{',
                              'if', 'while', 'return', 'switch', 'NUM','ID' ,'+', '-', '('])
switch_stmt = Non_terminal(name = 'switch_stmt', first_set=['switch'], follow_set=['default', 'case', 'else', '}', 'continue', 'break', ';', '{',
                              'if', 'while', 'return', 'switch', 'NUM','ID' ,'+', '-', '('])

case_stmts = Non_terminal(name = 'case_stmts', first_set=['case'], follow_set=['default', '}', 'case'])

cast_stmt = Non_terminal(name = 'case_stmt', first_set=['case'], follow_set=['default', '}', 'case'])


default_stmt = Non_terminal(name = 'default_stmt', first_set=['default'], follow_set=['}'])

statement_list = Non_terminal(name = 'statement_list', first_set=['continue','NUM', 'break', ';', '{', 'if', 'while', 'return', 'switch', 'ID', '+',
                                                        '-', '('],
                              follow_set=['default', 'case', '}', 'NUM','continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', 'ID', '+' ,
                                          '-', '('])

simple_expresion = Non_terminal(name = 'simple_expression', first_set=['+','NUM', '-', '(', 'ID'],
                                follow_set=[',', ';', ']', ')'])


relop = Non_terminal(name = 'relop', first_set=['<', '=='], follow_set=['+','NUM', '-', '(', 'ID'])

additive_expression = Non_terminal(name = 'additive_expression', first_set=['+', 'NUM','-', '(', 'id'],
                                   follow_set=[',', '<','==', '+', '-', ';', ']', ')'])

addop = Non_terminal(name= 'addop', first_set=['+', '-'], follow_set=['+','NUM','-', '(', 'ID'])

term = Non_terminal(name = 'term', first_set=['+', 'NUM','-', '(', 'ID'], follow_set=[',' ,'*', '<', '==', '+', '-', ';', ']', ')'])

signed_factor = Non_terminal(name = 'signed_factor', first_set=['+','NUM', 'minus', '(', 'ID'],
                             follow_set=[',', '*', '<', '==', '+', '-', ';', ']', ')'])

factor = Non_terminal(name = 'factor', first_set=['(','NUM','ID'], follow_set=[',' ,'*', '<', '==', '+', '-', ';', ']', ')'])

var = Non_terminal(name='var', first_set=['ID'], follow_set=[',' ,'*', '<', '==', '+', '-', ';', ']', ')','='])

call = Non_terminal(name = 'call', first_set = ['ID'], follow_set=[',','*','<','==', '+', '-', ';', ']', ')'])

args = Non_terminal(name= 'args', first_set=['ID','+', '-', '(', 'MUM'], follow_set=[')'])

arg_list = Non_terminal(name = 'arg_list', first_set=['ID', '+', '-', '(', 'MUM'], follow_set=[')', ','])
expression = Non_terminal(name='expression', first_set=['ID', '+', '-', '(', 'NUM'], follow_set=[',' ,';', ']', ')'])



































get_char()
get_new_token()
parser.running = True
parser(program, height=0)

























































































