# from lexical_analyser import get_token_one_by_one
input_file = open("input.txt", 'r')
code = input_file.read()

output_file = open("scanner.txt", 'w+')
first_output = True

error_file = open("lexical_errors.txt", 'w+')
first_error = True

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
    get_char()
    token_string = token_type = ''
    if current_char is not None:
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

    def set_transition_dictionary(self, transition_dictionary, final_state, initial_state):
        self.transition_dictionary = transition_dictionary
        self.final_state = final_state
        self.initial_state = initial_state


E = Non_terminal(name='E', first_set=['NUM', '('], follow_set=[')', '$'])
T = Non_terminal(name='T', first_set=['NUM', '('], follow_set=['+', ')', '$'])
X = Non_terminal(name='X', first_set=['+', 'EPSILON'], follow_set=['$', ')'])
Y = Non_terminal(name='Y', first_set=['*', 'EPSILON'], follow_set=['+', ')', '$'])

E_dictionary = {
    (0, T): 1,
    (1, X): 2
}
E.set_transition_dictionary(E_dictionary, final_state=2, initial_state=0)

T_dictionary = {
    (3, '('): 4,
    (4, E): 5,
    (5, ')'): 6,
    (3, 'NUM'): 7,
    (7, Y): 6
}
T.set_transition_dictionary(T_dictionary, final_state=6, initial_state=3)

X_dictionary = {
    (8, '+'): 9,
    (9, E): 10,
    (8, 'EPSILON'): 10
}

X.set_transition_dictionary(X_dictionary, final_state=10, initial_state=8)

Y_dictionary = {
    (11, '*'): 12,
    (12, T): 13,
    (11, 'EPSILON'): 13
}
Y.set_transition_dictionary(Y_dictionary, final_state=13, initial_state=11)


def function(non_terminal, token_type, token):
    print('function: ' , non_terminal.name)
    s = non_terminal.initial_state
    while s != non_terminal.final_state:
        flag = False
        this_state = {}
        for key, value in non_terminal.transition_dictionary.items():
            if key[0] == s:
                this_state[key] = value
        print('this state:' ,this_state)
        print('current state and token type: ' , (s, token_type))
        if (s, token_type) in this_state: #.items added
            print('found the terminal edge')
            s = non_terminal.transition_dictionary[(s, token_type)]
            print('next state: ' , s)
        elif len(this_state) > 0:
            for key, value in this_state.items():
                if isinstance(key[1], Non_terminal) and (token_type in key[1].first_set or
                                                     ('EPSILON' in key[1].first_set and token_type in key[1].follow_set)):
                    print('inside')
                    print((key[0], key[1].name), value)
                    res = function(key[1], token_type, token)
                    s = value
                    flag = True
                    if not res:
                        # TODO: error handling
                        return False
                    break
        if not flag and (s, 'EPSILON') in this_state.keys(): #what is this?
            print('Epsilon')
            s = non_terminal.transition_dictionary[(s, 'EPSILON')]
        print()
        if s == non_terminal.final_state:
            print(non_terminal.name , ' finished')
            break
        token_type, token = get_token_one_by_one()
        if token_type == 'SYMBOl':
            token_type = token
        elif token_type == '':
            token_type = '$'
        print(token_type, '   ' , token)

    return True


t_type, t_string = get_token_one_by_one()
if t_type == 'SYMBOl':
    t_type = t_string
print(t_type, t_string)
function(E, t_type, t_string)


# first sets
# program	int, void
# declaration-list	int, void
# declaraion-list	EPSILON
# declaration	int, void
# var-declaration	int, void
# A	[, ;
# type-specifier	int, void
# fun-declaration	int, void
# params	void, int
# param-list	int, void
# param	int, void
# B	[, EPSILON
# compound-stmt	{
# statement-list	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM
# statement	{, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM
# expression-stmt	continue, break, ;, ID, +, -, (, NUM
# selection-stmt	if
# iteration-stmt	while
# return-stmt	return
# C	;, ID, +, -, (, NUM
# switch-stmt	switch
# case-stmts	EPSILON
# case-stmt	case
# default-stmt	default, EPSILON
# expression	ID, +, -, (, NUM
# var	ID
# D	[, EPSILON
# simple-expression	+, -, (, ID, NUM
# E	EPSILON, <, ==
# relop	<, ==
# additive-expression	+, -, (, ID, NUM
# F	EPSILON, +, -
# addop	+, -
# term	+, -, (, ID, NUM
# G	*, EPSILON
# signed-factor	+, -, (, ID, NUM
# factor	(, ID, NUM
# call	ID
# args	EPSILON, ID, +, -, (, NUM
# arg-list	ID, +, -, (, NUM
# H	,, EPSILON


# follow sets
# program	-|
# declaration-list	EOF, EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM
# declaraion-list
# declaration	int, void
# var-declaration	int, void
# A	int, void
# type-specifier	ID
# fun-declaration	int, void
# params	)
# param-list	)
# param	,, )
# B	,, )
# compound-stmt	int, void, EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# statement-list	}
# statement	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# expression-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# selection-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# iteration-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# return-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# C	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# switch-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# case-stmts	default, EPSILON
# case-stmt
# default-stmt	}
# expression	;, ), ], ,, EPSILON
# var	=, *, EPSILON
# D	=, *, EPSILON
# simple-expression	;, ), ], ,, EPSILON
# E	;, ), ], ,, EPSILON
# relop	+, -, (, ID, NUM
# additive-expression	EPSILON, <, ==, ;, ), ], ,
# F	EPSILON, <, ==, ;, ), ], ,
# addop	+, -, (, ID, NUM
# term	EPSILON, +, -
# G	EPSILON, +, -
# signed-factor	*, EPSILON
# factor	*, EPSILON
# call	*, EPSILON
# args	)
# arg-list	)
# H	)
