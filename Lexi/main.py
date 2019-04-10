#TODO define lines, print on file, while,



input_file = open("input.txt", 'r')
code = input_file.read()
start_ind = 0
end_ind = 0
ind = -1
current_char = ''
next_char = ''
line = 0

TOKEN_INITIAL = 0
TOKEN_NUM = 1
TOKEN_KEYWORD = 2
TOKEN_ID = 3
TOKEN_SYMBOL = 4
TOKEN_COMMNET = 5
TOKEN_WHITESPACE = 6
TOKEN_EOF = 7

state = TOKEN_INITIAL
symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==']
whitespace = ['\n' , '\r' , '\t' , ' ' , '\v' , '\f' ]
digit = [str(i) for i in range(10)]
alphabet = [chr(i) for i in range(65 , 91)] + [chr(i) for i in range(97, 123)]
keywords = [ 'if', 'else' , 'void' ,'int', 'while', 'break', 'continue', 'switch', 'default', 'case', 'return' ]

def get_string():
    global start_ind, end_ind, code
    return code[start_ind:end_ind]

def get_char():
    global ind, code, current_char
    ind += 1
    current_char = code[ind]
    next_char = code[ind + 1]
    return current_char

def num():
    global end_ind
    while current_char is not None:
        get_char()
        end_ind = ind
        if current_char not in digit:
            if current_char in symbols or current_char in whitespace:
                return True, get_string(), 'NUM'
            else:
                return False, get_string() + current_char , 'invalid input'


def symbol():
    global end_ind
    if current_char == '=':
        if next_char == '=':
            end_ind = ind
    get_char()
    return True, get_string(), 'SYMBOl'


def skip_whitespace():
    global end_ind
    while current_char in whitespace:
        get_char()
        end_ind = ind

def id():
    global end_ind
    while current_char is not None:
        get_char()
        end_ind = ind
        if current_char not in digit or current_char not in alphabet:
            if current_char in symbols or current_char in whitespace:
                if get_string() in keywords:
                    return True, get_string(), 'KEYWORD'

                return True, get_string(), 'ID'
            else:
                return False, get_string() + current_char, 'invalid input'


def comment():
    global end_ind
    if next_char == '/':
        get_char()
        while current_char is not '\n':
            get_char()
            end_ind = ind

        return True, None, 'COMMENT'
    if next_char == '*':
        get_char()
        while current_char + next_char is not '*/':
            get_char()
            end_ind = ind

        return True, None, 'COMMENT'

    get_char()
    return False, get_string() + current_char, 'invald input'




def get_next_token():
    global state, end_ind, start_ind
    get_char()
    #TODO while
    if current_char in digit:

        state = TOKEN_NUM
        is_token, token_string, token_type = num()
        if is_token:
                #TODO add to file
            pass
        else:
            #TODO handle error
            get_char()


    elif current_char in symbols:
        state = TOKEN_SYMBOL
        is_token, token_string, token_type = symbol()
        #TODO add to file
        # start_ind = ind
        # state = TOKEN_INITIAL

    elif current_char in whitespace: #TODO after while
        skip_whitespace()
        # start_ind = ind
        # state = TOKEN_INITIAL

    elif current_char in alphabet:
        is_token, token_string, token_type = id()
        if is_token:
            #TOOD
            pass
        else:
            get_char()
            #TODO

    elif current_char == '/':
        is_token , token_string, token_type = comment()
        if not is_token:
            get_char()
            #TODO







    start_ind = ind
    state = TOKEN_INITIAL












