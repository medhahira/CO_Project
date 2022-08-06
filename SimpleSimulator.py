"""
<PC (8 bits)><space><R0 (16 bits)><space>...<R6 (16 bits)><space><FLAGS (16 bits)>
start execution at address 0
executed until hlt is reached
we need an output like the one shown above after the execution of each instruction step
"""
import matplotlib.pyplot as plt
import sys
PC = 0
cycle = 0
cycles = []
pcs = []


isa = {
    #opcode : [type, instruction]
    "10000":["A", "add"],
    "10001":["A", "sub"],
    "10010":["B", "mov"],
    "10011":["C", "mov"],
    "10100":["D", "ld"],
    "10101":["D", "st"],
    "10110":["A", "mul"],
    "10111":["C", "div"],
    "11000":["B", "rs"],
    "11001":["B", "ls"],
    "11010":["A", "xor"],
    "11011":["A", "or"],
    "11100":["A", "and"],
    "11101":["C", "not"],
    "11110":["C", "cmp"],
    "11111":["E", "jmp"],
    "01100":["E", "jlt"],
    "01101":["E","jgt" ],
    "01111":["E", "je"],
    "01010":["F", "hlt"],
}
regs = {
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111",
}
encoding_reg = {
    "000": "R0",
    "001":"R1",
    "010":"R2",
    "011":"R3",
    "100" : "R4",
    "101":"R5",
    "110" : "R6",
    "111" :"FLAGS",
}

registers = [0]*7

flags_track = {
    'V':0,
    'L':0,
    'G':0,
    'E':0
}

halted = False  # this will be false until a hlt is enountered, if any instruction is encountered after the variable being true it'll throw an error

inp = []
while True:
    try:
        line = input()
    except EOFError:
        break
    inp.append(line)
variable_space = 256 - len(inp)
for i in range(variable_space):
    inp.append('0000000000000000')

def dec_to_bin(imm):
    return bin(imm)[2:]

def dec_to_bin_8(decimal):  # converts any integer into 8 bit binary representation, only valid for 8 bit numbers, i.e. 0 to 255
    binary = "{:08b}".format(decimal)
    return bin(decimal)[2:].zfill(8)

def dec_to_bin_16(decimal):  # converts any integer into 8 bit binary representation, only valid for 16 bit numbers
    return bin(decimal)[2:].zfill(16)

def bin_to_dec(imm):
    return int(imm,base = 2)

def type_b(op_instruction, reg1, imm):
    """opcode(5) reg1(3) imm(8)
    mov, ls, rs"""
    if op_instruction == "ls":
        ans = registers[int(reg1[1])]<<imm
    if op_instruction == "rs":
        ans = registers[int(reg1[1])]>>imm
    if op_instruction == "mov":
        ans = imm
    return ans

def type_c(op_instruction, reg1, reg2, flag):
    """opcode(5) unused(5) reg1(3) reg2(3)
    mov, div, not, cmp,
    flags needed for: mov, cmp"""
    if op_instruction == "mov":
        if reg1 == "FLAGS":
            imm = "0"*12
            imm+=str(flag["V"])
            imm+=str(flag["L"])
            imm += str(flag["G"])
            imm += str(flag["E"])
            ans = bin_to_dec(imm)
            return ans
        else:
            return registers[int(reg2[1])]
    if op_instruction == "div":
        quotient = registers[int(reg1[1])]//registers[int(reg2[1])]
        remainder = registers[int(reg1[1])]%registers[int(reg2[1])]
        return (quotient, remainder)
    if op_instruction == "not":
        binary = dec_to_bin_16(registers[int(reg2[1])])
        list_bin = list(binary)
        for i in range(len(list_bin)):
            if list_bin[i] == "1":
                list_bin[i] = "0"
            elif list_bin[i] == "0":
                list_bin[i] = "1"
        ans =""
        for i in list_bin:
            ans+= i
        return ans
    if op_instruction == "cmp":
        num1 = registers[int(reg1[1])]
        num2 = registers[int(reg2[1])]
        if num1 == num2:
            return "E"
        elif num1<num2:
            return "L"
        elif num1>num2:
            return "G"
