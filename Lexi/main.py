input_file = open("input.txt", 'r')
code = input_file.read()
ind = 0
current_char = ''

digit = [str(i) for i in range(10)]
alphabet = [chr(i) for i in range()]


def get_next_char():
    global ind, code, current_char
    current_char = code[ind]
    ind += 1
    return current_char


def get_next_token():
    while get_next_char() is not None:
        if current_char






