from sys import exit

instruction_type = {
    'add': 'A',
    'sub': 'A',
    'mul': 'A',
    'xor': 'A',
    'or': 'A',
    'and': 'A',
    'mov': 'BC',
    'ls': 'B',
    'rs': 'B',
    'div': 'C',
    'not': 'C',
    'cmp': 'C',
    'ld': 'D',
    'st': 'D',
    'jmp': 'E',
    'jlt': 'E',
    'jgt': 'E',
    'je': 'E',
    'hlt': 'F'
}
register_table = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111'
}

ISA = {
    'add': '10000',
    'sub': '10001',
    'movi': '10010',
    'movr': '10011',
    'ld': '10100',
    'st': '10101',
    'mul': '10110',
    'div': '10111',
    'rs': '11000',
    'ls': '11001',
    'xor': '11010',
    'or': '11011',
    'and': '11100',
    'not': '11101',
    'cmp': '11110',
    'jmp': '11111',
    'jlt': '01100',
    'jgt': '01101',
    'je': '01111',
    'hlt': '01010'
}

# VARIABLES
variables = []
variable_table = dict()
label_table = dict()
global current_mem_location  # We will increment this value by 2 for every instruction as every is instruction of of 2 bytes(16 bits).

# flags
variables_set = False  # this will be false while they are being set and true when insructions begin
halt_encountered = False  # this will be false until a hlt is enountered, if any instruction is encountered after the variable being true it'll throw an error


# UTILITY FUNCTIONS
def binary(num):  # converts any integer into 8 bit binary representation, only valid for 8 bit numbers, i.e. 0 to 255
    return "{:08b}".format(num)


def terminate():
    exit(0)


# Reads line by line and checks its validity, does not do the conversion.
def process_line(line, location):
    global current_mem_location, variables_set

    # empty line, to handle white spaces
    if not line:
        return
    elif halt_encountered:
        # checks if hlt has been encountered yet, if yes, it'll terminate.
        print(f'line {location}: ILLEGAL_COMMAND: HALT already encountered')
        terminate()
    elif line[-1] == ':':
        label_name = line[:-1]
        if label_name in variables:
            print(f'line {location}: ILLEGAL_LABEL: {label_name} clashes with a variable name')
            terminate()
        if label_name in label_table:
            print(f'line {location}: ILLEGAL_LABEL: {label_name} already a label')
            terminate()
        validate_name(label_name, location)
        label_table[label_name] = current_mem_location

        # variable declaration
    elif line[:3] == 'var':
        if variables_set:
            print(f'line {location}: ILLEGAL_DECLARATION: Cannot declare variable in the middle of program.')
            terminate()
        var_name = line[4:]
        if var_name in variables:
            print(f'line {location}: ILLEGAL_VARIABLE: Var {var_name} already a variable')
            terminate()
        if var_name in label_table:
            print(f'line {location}: ILLEGAL_VARIABLE: {var_name} clashes with a label name')
            terminate()
        validate_name(var_name, location)
        variables.append(var_name)

    else:
        if not variables_set: variables_set = True
        check_instruction(line, location)
        current_mem_location += 1  # To track the pointer in the memory, +2 because each instruction is of 2 byts


# Validation functions
def validate_name(name, location):
    # TODO
    if not name.isidentifier():
        print(f'line {location}: ILLEGAL_IDENTIFIER_NAME: {name} not a valid identifier. ')
        terminate()
    if name in instruction_type:
        print(f'line {location}: ILLEGAL_IDENTIFIER_NAME: {name} is a keyword.')
        terminate()


def validate_register(register,
                      location):  # This function does not check for Flag register, it'll throw error with that register because it's not allowed to use Flag register everywhere and its use is restricted.
    # Since FLAGS is only used with mov, it has been taken care of there itself.
    if register not in ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6']:
        print(f'line {location}: ILLEGAL_REGISTER_ERROR: {register} not a valid register. ')
        terminate()


def validate_value(value, location):  # checks for immediate value
    try:
        assert value[0] == '$'
        val = int(value[1:])
    except:
        print(f'line {location}: ILLEGAL_VALUE_ERROR: {value} is in invalid format')
        terminate()

    try:
        assert val >= 0 and val <= 255
    except:
        print(f'line {location}: OVERFLOW: {value} not in the range 0-255')
        terminate()


def validate_variable(name, location):  # It will be validated in first pass
    if name not in variables:
        print(f'line {location}: UNDECLARED_VARIABLE: {name} used without declaration')
        terminate()


def validate_label(name, location):  # It will be validated in second pass
    if name not in label_table:
        print(f'line {location}: UNDECLARED_LABEL: {name} used without declaration')
        terminate()
