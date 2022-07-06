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
        label_name = line[:-1].lstrip()
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
        var_name = line[4:].strip()
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
        
#checking the validity of instruction
def check_instruction(line,location): 
    inst = line.split()[0]
    type_ = instruction_type.get(inst,None)
    if type_=='A':
        check_instruction_A(line,location)
    elif type_=='B':
        check_instruction_B(line,location)
    elif type_=='C':
        check_instruction_C(line,location)
    elif type_=='D':
        check_instruction_D(line,location)
    elif type_=='E':
        check_instruction_E(line,location)
    elif type_=='F':
        check_instruction_F(line,location)
    elif type_=='BC':
        check_instruction_BC(line,location)
    else:
        print(f'line {location}: ILLEGAL_Instruction: Invalid Instruction {inst}')
        terminate()
def check_instruction_A(line,location):
    '''checks the type (add|sub|mul|xor|and) reg1 reg2 reg3'''
    inst,reg1,reg2,reg3 = line.split()
    for register in [reg1,reg2,reg3]:
        validate_register(register,location)
        
def check_instruction_B(line,location):
    inst,reg,val = line.split()
    validate_register(reg,location)
    validate_value(val,location)

def check_instruction_C(line,location):
    inst,reg1,reg2 = line.split()
    validate_register(reg1,location)
    validate_register(reg2,location)

def check_instruction_BC(line,location):
    inst,reg1,reg_or_imm = line.split()
    validate_register(reg1,location)
    ##reg_or_imm can be either reg or FLAGS or imm
    if reg_or_imm == 'FLAGS':
        return
    elif reg_or_imm[0]=='$':
        validate_value(reg_or_imm,location)
    else:
        validate_register(reg_or_imm,location)

def check_instruction_D(line,location):
    inst,reg,mem = line.split()
    validate_register(reg,location)
    validate_variable(mem,location)

def check_instruction_E(line, location):
    inst,mem = line.split()
    #label can be only checked at second pass
def check_instruction_F(line,location):
    global halt_encountered
    if line != 'hlt':
        print(f'line {location}: INVALID_COMMAND: \'{line}\' command not valid')
        terminate()
    # if halt_encountered:

    #     print(f'line {location}: MULTIPLE_HALTS: multiple halts are encountered')
    #     terminate()
    else:
        halt_encountered=True
#update the memory locations of the variables
def assign_var_location():
    global variable_table
    variable_table = {name:current_mem_location+1*idx for idx,name in enumerate(variables)}

##doubt: since memory is accessible in chunks of two bytes, will variables have difference of 1 byte in memory location, or 2??
## change ()*idx accordingly

instructions = []

def convert_line(line,location):
    #empty line or label or variable declaration: do nothing
    if not line or line[-1]==':' or line[:3]=='var':
        return

    else:
        instructions.append(get_instruction(line,location))

def get_instruction(line,location):
    inst = line.split()[0]
    #if inst not in instruction_type dict then throw an error
    type_ = instruction_type[inst]
    if type_=='A':
        return get_instruction_A(line)
    elif type_=='B':
        return get_instruction_B(line)
    elif type_=='C':
        return get_instruction_C(line)
    elif type_=='BC':
        return get_instruction_BC(line)
    elif type_=='D':
        return get_instruction_D(line)
    elif type_=='E':
        return get_instruction_E(line,location)
    elif type_=='F':
        return get_instruction_F(line)

def get_instruction_A(line):
    '''OPCODE(5) UNUSED(2) REG1(3) REG2(3) REG3(3)'''
    inst,reg1,reg2,reg3 = line.split()
    opcode = ISA[inst]
    reg1_addr = register_table[reg1]
    reg2_addr = register_table[reg2]
    reg3_addr = register_table[reg3]
    return opcode  + '0'*2 + reg1_addr + reg2_addr + reg3_addr

def get_instruction_B(line):
    '''OPCODE(5) REG(3) IMMEDIATE VALUE(8)'''
    inst,reg,value = line.split()
    opcode = ISA[inst]
    reg_addr = register_table[reg]
    imm = binary(int(value[1:]))
    return opcode  + reg_addr + imm

def get_instruction_C(line):
    '''OPCODE(5) UNUSED(5) REG1(3) REG2(3)'''
    inst,reg1,reg2 = line.split()
    opcode = ISA[inst]
    reg1_addr = register_table[reg1]
    reg2_addr = register_table[reg2]
    return opcode + '0'*5 + reg1_addr + reg2_addr

def get_instruction_BC(line):
    '''OPCODE(5) REG(3) IMMEDIATE VALUE(8) | OPCODE(5) UNUSED(5) REG1(3) REG2(3)'''
    inst,reg1,reg_or_imm = line.split()
    
    reg1_addr = register_table[reg1]
    if reg_or_imm[0] == '$':
        #imm
        opcode = ISA[inst+'i']
        imm = binary(int(reg_or_imm[1:]))
        return opcode  + reg1_addr + imm
    else:
        opcode = ISA[inst+'r']
        reg2_addr = register_table[reg_or_imm]
        return opcode + '0'*5 + reg1_addr + reg2_addr

def get_instruction_D(line):
    '''OPCODE(5) REGISTER(3) MEM_ADDR(8)'''
    inst,reg,mem = line.split()
    opcode = ISA[inst]
    reg_addr = register_table[reg]
    mem_addr = binary(variable_table[mem])
    return opcode + reg_addr + mem_addr

def get_instruction_E(line,location):
    '''OPCODE(5) UNUSED(3) MEM_ADDR(8)'''
    inst,mem = line.split()
    validate_label(mem,location)
    opcode = ISA[inst]
    mem_addr = binary(label_table[mem])
    return opcode +'0'*3 +mem_addr

def get_instruction_F(line):
    '''OPCODE(5) UNUSED(11)'''
    opcode = ISA['hlt']
    return opcode + '0'*11

def init():
    global current_mem_location,variables,variable_table,label_table,variables_set,halt_encountered,instructions
    current_mem_location = 0
    variables = []
    variable_table = dict()
    label_table = dict()
    variables_set=False
    halt_encountered=False
    instructions = []

def print_state():
    global current_mem_location,variables,variable_table,label_table,variables_set,halt_encountered
    print(current_mem_location,variables,variable_table,label_table,variables_set,halt_encountered)

def main(inp=None):
    init()
    if not inp:
        inp = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            inp.append(line)
        inp='\n'.join(line for line in inp)
    
    
    
    
    program = [[line.strip(),idx+1] for idx,line in enumerate(inp.split('\n'))]
    program2=[]
    for entry in program:
        line,line_no = entry
        if ':' in line:
            idx = line.index(':')+1
            program2.append([line[:idx],line_no])
            program2.append([line[idx:],line_no])
        else:
            program2.append([line,line_no])

    program=program2
    
    
    
    
    idx=0
    # print(*program,sep ='\n',end=f'\n --------------------------BREAK-----------------------------\n')################REMOVE
    loc = 0
    try:
        for entry in program:
            line,line_no = entry
            loc = line_no
            process_line(line,line_no)
        #No halts encountered
        if not halt_encountered:
            print(f'line {idx+1}: NO_HALTS: No HALTS were found.')
            terminate()

        assign_var_location()
        for entry in program:
            line,line_no = entry
            loc = line_no
            convert_line(line,line_no)
    
        print(*instructions,sep='\n')
    except SystemExit:
        print('Exiting program')
    except:
        print(f'line {loc}: ILLEGAL FORMAT')
main()
