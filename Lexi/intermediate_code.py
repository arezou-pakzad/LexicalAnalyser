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

    def get_top_index(self):
        return len(self.stack) - 1


class Program_block:
    def __init__(self):
        self.program = ['' for i in range(10000)]
        self.index = 0

    def write(self, index, statement):
        self.program[index] = statement

    def increase_index(self):
        self.index += 1


class Data_block:
    def __init__(self):
        self.index = 0
        self.memory = [0 for i in range(10000)]
        self.temp_start = 8000
        self.temp_index = self.temp_start
        self.array_start = 5000
        self.array_index = self.array_start


    def write(self, item):
        self.memory[self.index] = item
        self.index += 4
        return self.index - 4

    def write(self, item, addr):
        self.memory[addr] = item


    def write_array(self, array, size):
        addr = self.write(array[0])
        for i in range(1, size):
            self.write(array[i])
        return addr

    def read(self, addr):
        return self.memory[addr]

    def get_temp(self):
        return_value = self.temp_index
        self.temp_index = (self.temp_index + 4) % 7000 + 7000
        return return_value


    def write_array(self, array, size):

        addr = self.array_index
        self.write(addr) #TODO
        for i in range(size):
            self.write(item= array[i], addr= self.array_index)
            self.array_index += 4
        return addr


    def write_array(self, size):
        addr = self.array_index
        self.array_index += 4 * size
        return addr


class Activation_record:
    def init(self, name, PB_index, DB_index):
        self.name = name
        self.PB_index = PB_index
        self.DB_index = DB_index
        self.symbol_counter = 0
        self.symbol_dict = {}
        self.array_dict = {}


    def add_symbol(self, symbol_str, DB):
        if symbol_str not in self.symbol_dict.keys():
            DB.write(0, self.DB_index + self.symbol_counter)
            self.symbol_dict[symbol_str] = self.DB_index + self.symbol_counter
            self.symbol_counter += 4
        else:
            pass
            #TODO ERROR


    def update_symbol(self, symbol_str, symbol_value, DB):
        if symbol_str not in self.symbol_dict.keys():
            #TODO print error
            return
        DB.write(symbol_value, self.symbol_dict[symbol_str])


    def add_array(self, array_size, array_name, DB):
        if array_name not in self.array_dict.keys():
            address = DB.write_array(size = array_size)
            self.write(address, self.DB_index + self.symbol_counter)  # TODO
            self.array_dict[array_name] = (address, array_size)
            self.symbol_counter += 4


    def get_symbol(self, symbol_str):
        if symbol_str not in self.symbol_dict.keys():
            #TODO print error
            return
        return self.symbol_dict[symbol_str]

    def get_array(self, array_str, index, DB):
        if array_str not in self.array_dict.keys():
            #TODO print error
            return
        return DB.read(self.array_dict[array_str][0] + 4 * index)


    def update_array(self, array_str,value ,index, DB):
        if array_str not in self.array_dict.keys():
            #TODO print error
            return

        DB.write(value, self.array_dict[array_str][0] + 4 * index)


class Activation_record:
    def __init__(self, name, PB_index, DB_index):
        self.name = name
        self.PB_index = PB_index
        self.DB_index = DB_index
        self.symbol_counter = 0
        self.symbol_dict = {}
        self.array_dict = {}

    def add_symbol(self, symbol, symbol_value, DB):
        if symbol not in self.symbol_array.keys():
            DB.write(symbol_value, self.DB_index + self.symbol_counter)
            self.symbol_counter += 4
            self.symbol_dict[symbol] = self.DB_index + self.symbol_counter

