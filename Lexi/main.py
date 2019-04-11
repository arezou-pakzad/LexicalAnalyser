# TODO define lines, print on file, while,
import sys

input_file = open("input.txt", 'r')
code = input_file.read()

output_file = open("scanner.txt", 'a')

error_file = open("lexical_errors.txt", 'a')

start_ind = 0
end_ind = 0
ind = -1
current_char = ''
next_char = ''
line_num = 1
line_changed = True

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
    # print('num')
    global end_ind
    while current_char is not None:

        if current_char not in digit:
            if current_char in symbols or current_char in whitespace:
                return True, get_string(), 'NUM'
            else:
                return False, get_string() + current_char, 'invalid input'
        get_char()
        end_ind = ind
    return True, get_string(), 'NUM'


def symbol():
    # print('symbol')
    global end_ind
    if current_char == '=':
        if next_char == '=':
            get_char()
            end_ind = ind

    get_char()
    end_ind = ind
    # print('get_string in symbols', get_string(), start_ind, '  ', end_ind)
    return True, get_string(), 'SYMBOl'


def skip_whitespace():
    global line_num, line_changed
    global end_ind
    while current_char in whitespace:
        if current_char == '\n':
            line_num += 1
            line_changed = True
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
    # print('comment')
    global end_ind
    if next_char == '/':
        # print('this is a comment')
        get_char()
        end_ind = ind
        while current_char is not '\n' and current_char is not None:
            # print(current_char, 'is not the end of comment')
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

        if is_token and state != TOKEN_COMMENT:
            print_token(token_type, token_string)
        elif not is_token:
            get_char()
            print_error(token_type, token_string)

        start_ind = ind
        state = TOKEN_INITIAL


def print_token(token_type, token_string):
    global output_file, line_changed
    if line_changed and line_num != 1:
        print()
    if line_changed:
        print(str(line_num) + '. (' + token_type + ', ' + token_string + ')', end='')
        line_changed = False
    else:
        print(' (' + token_type + ', ' + token_string + ')', end='')

    # output_file.write(str(line_num) + '. (' + token_type + ', ' + token_string + ')\n')


def print_error(token_type, token_string):
    global error_file, line_changed
    if line_changed and line_num != 1:
        print()
    if line_changed:
        print(str(line_num) + '. (' + token_string + ', ' + token_type + ')', end='')
        # line_changed = False
    else:
        print(' (' + token_string + ', ' + token_type + ')', end='')

    # error_file.write(str(line_num) + '. (' + token_string + ', ' + token_type + ')')


get_next_token()
output_file.close()
error_file.close()
input_file.close()