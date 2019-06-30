class While_stmt:
    def __init__(self, number, start_index):
        self.number = number
        self.start_index = start_index

    def set_goto(self, next_stmt):
        self.next_stmt = next_stmt

    def get_number(self):
        return self.number

    def get_start_index(self):
        return self.start_index


class While_pointer:
    def __init__(self, stmt):
        self.stmt = stmt

    def get_stmt(self):
        return self.stmt

    def set_stmt(self, stmt):
        self.stmt = stmt



class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self, number):
        for i in range(number):
            self.stack.pop()

    def get_item(self, index):
        top = len(self.stack) - 1
        return self.stack[top - index]



class Program_block:
    def __init__(self):
        self.program = [] * 100000
        self.index = 0

    def write(self, index, statement):
        self.program[index] = statement

    def increase_index(self):
        self.index += 1















