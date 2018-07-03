# VAR programming language
# Copyright 2018 Marcus Hansson
#
# Usage:      [Python 3 path] var.py [file name]
# Example:    c:\Python34\python.exe var.py test.var

import sys
import string

VARIABLE = "VAR"
OUTPUT = "OUT"
INPUT = "INP"
INCREMENT = "INC"
DECREMENT = "DEC"
WHILE = "WHL"
END = "END"
INTEGER = "INT"
STRING = "STR"

LETTERS = string.ascii_lowercase + string.ascii_uppercase
NUMBERS = "0123456789"
SPACE = " "
NEW_LINE = "\n"
QUOTATION_MARK = '"'
BRACKET_LEFT = "["
BRACKET_RIGHT = "]"
COMMENT = "//"

class Operation:
    def __init__(self, code):
        self.code = code
        self.variables = {}
        self.code_pointer = -1
        self.char = ""
        self.loops = {}

    def prepare_loops(self, code):
        temp_loop_stack, self.loops = [], {}
        command = ""
        command_position = True  # True if the current character is part of any first word

        for position, char in enumerate(code):
            if command_position:
                if char in ["\n", " "]:
                    command = command.upper()
                    command_position = False

                    if command == WHILE:
                        temp_loop_stack.append(position)

                    elif command == END:
                        start = temp_loop_stack.pop()
                        self.loops[start] = position
                        self.loops[position] = start
                        command_position = True

                    command = ""

                else:
                    command += char
            else:
                if char == "\n":
                    command_position = True


    def update_char(self):
        try:
            self.char = self.code[self.code_pointer]
        except IndexError as e:
            return False

        return True

    def next_char(self):
        self.code_pointer += 1
        return self.update_char()

    def set_char(self, new_index):
        self.code_pointer = new_index
        return self.update_char()

    def create_variable(self):
        var_name = self.get_chars_until([SPACE, BRACKET_LEFT])
        var_index = None

        if self.char == BRACKET_LEFT:
            self.next_char()
            var_index = self.get_index()

        self.next_char()

        ascii_list = self.get_value()

        self.assign_variable(var_name, var_index, ascii_list)

    def assign_variable(self, var_name, var_index, new_ascii_list):
        self.next_char()

        if var_name not in self.variables:
            self.variables[var_name] = [0]

        if var_index:
            current_ascii_list = self.variables[var_name].copy()

            while len(current_ascii_list) < var_index:
                current_ascii_list.append(0)

            before_index = current_ascii_list[:var_index]
            after_index = current_ascii_list[var_index + 1:]
            new_ascii_list = before_index + new_ascii_list + after_index

        self.variables[var_name] = new_ascii_list

    def get_variable_as_ascii_list(self):
        var_name = self.get_chars_until([NEW_LINE, BRACKET_LEFT])

        if self.char == BRACKET_LEFT:
            self.next_char()
            var_index = self.get_index()
            current_ascii_list = self.get_variable_value(var_name)

            while len(current_ascii_list) < var_index + 1:
                current_ascii_list.append(0)

            ascii_list = [current_ascii_list[var_index]]

        else:
            ascii_list = self.get_variable_value(var_name)

        return ascii_list

    def get_string_as_ascii_list(self):
        self.next_char()
        string = self.get_chars_until([QUOTATION_MARK])
        ascii_list = self.convert_to_ascii(string)
        return ascii_list

    def get_number_as_ascii_list(self):
        var_value = self.get_chars_until([NEW_LINE])
        ascii_list = [int(var_value)]
        return ascii_list

    def create_input_variable(self):
        var_name = self.get_chars_until([NEW_LINE])
        var_value = input()
        ascii_list = self.convert_to_ascii(var_value)

        self.assign_variable(var_name, None, ascii_list)

    def get_var_change(self):
        if self.char == " ":
            self.next_char()

            var_value = self.get_value()

        else:
            var_value = [1]

        return var_value

    def decrement_value(self):
        self.adjust_value("decrement")

    def increment_value(self):
        self.adjust_value("increment")

    def adjust_value(self, adjust_string):
        var_name = self.get_chars_until([SPACE, NEW_LINE])
        adj_value = self.get_var_change()

        if len(adj_value) > 1:
            self.print_error(3, adjust_string, var_name)

        try:
            adj_value = int(adj_value[0])
        except ValueError as e:
            self.print_error(2, adjust_string, var_name, adj_value)

        self.next_char()

        if var_name in self.variables:
            var_value = self.variables[var_name]
        else:
            self.print_error(1, var_name)

        if len(var_value) > 1:
             self.print_error(3, adjust_string, self.convert_from_ascii(var_value))

        if adjust_string == "increment":
            self.variables[var_name][0] = (var_value[0] + adj_value) % 255
        else:
            self.variables[var_name][0] = (var_value[0] - adj_value) % 255

    def get_chars_until(self, end_char_list):
        chars = ""

        while self.char not in end_char_list:
            chars += self.char

            if not self.next_char():
                self.print_error(4, end_char_list)

        return chars

    def get_variable_value(self, var_name):
        value_list = []

        if var_name in self.variables.keys():
            value_list = self.variables[var_name].copy()
        else:
            self.print_error(1, var_name)

        return value_list

    def convert_from_ascii(self, value_list):
        value = ""

        while value_list[len(value_list) - 1] == 0:
            del value_list[-1]
            if len(value_list) == 0:
                break

        for number in value_list:
            value += chr(number)

        return value

    def convert_to_ascii(self, string):
        value_list = []

        for char in string:
            value_list.append(ord(char))

        return value_list

    def get_index(self):
        if self.char in NUMBERS:
            inside_brackets = self.get_chars_until([BRACKET_RIGHT])
            var_index = int(inside_brackets)

        elif self.char.isalpha():
            inside_brackets = self.get_chars_until([BRACKET_RIGHT])
            inside_brackets_ascii_list = self.get_variable_value(inside_brackets)
            var_index = int(inside_brackets_ascii_list[0])

        else:
            self.print_error(8)

        self.next_char()

        return var_index

    def get_value(self):
        if self.char == QUOTATION_MARK:
            ascii_list = self.get_string_as_ascii_list()

        elif self.char in NUMBERS:
            ascii_list = self.get_number_as_ascii_list()

        elif self.char.isalpha():
            ascii_list = self.get_variable_as_ascii_list()

        else:
            self.print_error(8)

        return ascii_list

    def print_output(self):
        ascii_list = self.get_value()
        output = self.convert_from_ascii(ascii_list)

        print(output, end="")


    def while_not_zero(self):
        var_name = self.get_chars_until([NEW_LINE])

        new_index = self.code_pointer - len(var_name)
        self.set_char(new_index)

        ascii_list = self.get_variable_as_ascii_list()

        var_value = ascii_list[0]

        if var_value == 0:
            self.code_pointer = self.loops[self.code_pointer - len(var_name) - 1]

    def end_while(self):
        self.set_char(self.loops[self.code_pointer - 1] + 1)
        self.while_not_zero()

    def make_integer(self):
        var_name = self.get_chars_until([NEW_LINE])
        ascii_list = self.variables[var_name].copy()
        var_value = self.convert_from_ascii(ascii_list)

        try:
            self.variables[var_name] = [int(var_value)]
        except ValueError as e:
            print(e)
            self.print_error(6, var_name)

    def make_string(self):
        var_name = self.get_chars_until([NEW_LINE])
        ascii_list = self.variables[var_name].copy()

        if len(ascii_list) == 1:
            self.variables[var_name] = self.convert_to_ascii(str(ascii_list[0]))
        else:
            self.print_error(7, var_name)


    def print_error(self, number, arg1="", arg2="", arg3=""):
        error_message = "\nERROR: "

        if number == 1:
            error_message += "No variable named '" + arg1 + "'."

        elif number == 2:
            error_message += "Cannot " + arg1 + " variable '" + arg2 + "' with '" + arg3 + "'."

        elif number == 3:
            error_message += "Cannot " + arg1 + " variable '" + arg2 + "' by a string value (unless length is 1)."

        elif number == 4:
            error_message += "Missing '" + str(arg1) + "'."

        elif number == 5:
            error_message += "Cannot assign '" + arg1 + "' to '" + arg2 + "' by using indexing. Only single value or character allowed."

        elif number == 6:
            error_message += "Cannot make variable '" + arg1 + "' to type integer."

        elif number == 7:
            error_message += "Cannot make variable '" + arg1 + "' to type string."

        elif number == 8:
            error_message += "Invalid syntax."

        print(error_message)
        sys.exit()


def execute(file_name):
    with open(file_name) as f:
        code = clean_code(f.readlines())
        compile_code(code)
        f.close()

def clean_code(code):
    COMMENT = "//"
    clean_code = ""

    for line in code:
        if COMMENT in line:
            line = line[:line.index(COMMENT)]

        line = line.strip()

        if line != "":
            clean_code += line + "\n"

    return clean_code

def compile_code(code):
    op = Operation(code)
    op.prepare_loops(code)

    command = ""

    while op.code_pointer < len(op.code):

        if op.char in ["\n", " "]:
            op.next_char()
            command = command.upper()

            if command == VARIABLE:
                op.create_variable()

            elif command == OUTPUT:
                op.print_output()

            elif command == INPUT:
                op.create_input_variable()

            elif command == INCREMENT:
                op.increment_value()

            elif command == DECREMENT:
                op.decrement_value()

            elif command == WHILE:
                op.while_not_zero()

            elif command == END:
                op.end_while()

            elif command == INTEGER:
                op.make_integer()

            elif command == STRING:
                op.make_string()

            command = ""

        else:
            command += op.char
            op.next_char()

def main():
    if len(sys.argv) == 2:
        execute(sys.argv[1])
    else:
        print("Please pass code file as argument: python3", sys.argv[0], "file_name")

if __name__ == "__main__":
    main()
