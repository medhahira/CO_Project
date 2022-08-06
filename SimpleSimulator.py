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
while(halted == False):
    cycles.append(cycle)
    breakdown_ins = []
    code = inp[PC]
    opcode = code[0:5]
    op_instruction = isa[opcode][1]
    instruction_type = isa[opcode][0]
    breakdown_ins.append(code[0:5])

    if instruction_type == 'A':
        """opcode(5) unused(2) reg1(3) reg2(3) reg3(3)
            add, sub, mul, xor, or, and"""
        breakdown_ins.append(code[7:10])
        breakdown_ins.append(code[10:13])
        breakdown_ins.append(code[13:16])
        regd = encoding_reg[breakdown_ins[1]] #this is the destination register
        reg1 = encoding_reg[breakdown_ins[2]]
        reg2 = encoding_reg[breakdown_ins[3]]
        if op_instruction == "add":
            ans = registers[int(reg1[1])] + registers[int(reg2[1])]
            if ans < 0 or ans > pow(2, 16) - 1 :
                flags_track['V'] = 1
                registers[int(regd[1])] = bin_to_dec(dec_to_bin_16(ans))
            else:
                registers[int(regd[1])] = ans
        if op_instruction == "sub":
            ans = registers[int(reg1[1])] - registers[int(reg2[1])]
            if ans < 0 or ans > pow(2, 16) - 1:
                flags_track['V'] = 1
                registers[int(regd[1])] = 0
            else:
                registers[int(regd[1])] = ans
        if op_instruction == "mul":
            ans = registers[int(reg1[1])] * registers[int(reg2[1])]
            if ans < 0 or ans > pow(2, 16) - 1 :
                flags_track['V'] = 1
                registers[int(regd[1])] = bin_to_dec(dec_to_bin_16(ans))
            else:
                registers[int(regd[1])] = ans
        if op_instruction == "xor":
            ans = registers[int(reg1[1])] ^ registers[int(reg2[1])]
        if op_instruction == "or":
            ans = registers[int(reg1[1])] | registers[int(reg2[1])]
        if op_instruction == "and":
            ans = registers[int(reg1[1])] & registers[int(reg2[1])]
        flags = "000000000000" + f"{flags_track['V']}" + f"{flags_track['L']}" + f"{flags_track['G']}" + f"{flags_track['E']}"
        pcs.append(PC)
        print(dec_to_bin_8(PC), dec_to_bin_16(registers[0]), dec_to_bin_16(registers[1]), dec_to_bin_16(registers[2]), dec_to_bin_16(registers[3]), dec_to_bin_16(registers[4]), dec_to_bin_16(registers[5]), dec_to_bin_16(registers[6]), flags)

    elif instruction_type == 'B':
        """opcode(5) reg1(3) imm(8)
            movi, ls, rs"""
        breakdown_ins.append(code[5:8])
        breakdown_ins.append(code[8:16])
        regd = encoding_reg[breakdown_ins[1]]  # this is the destination register
        imm = bin_to_dec(breakdown_ins[-1])
        if op_instruction == "ls":
            ans = registers[int(reg1[1])] << imm
        if op_instruction == "rs":
            ans = registers[int(reg1[1])] >> imm
        if op_instruction == "mov":
            ans = imm
        registers[int(regd[1])] = ans
        flags = "000000000000" + f"{flags_track['V']}" + f"{flags_track['L']}" + f"{flags_track['G']}" + f"{flags_track['E']}"
        pcs.append(PC)
        print(dec_to_bin_8(PC), dec_to_bin_16(registers[0]), dec_to_bin_16(registers[1]), dec_to_bin_16(registers[2]), dec_to_bin_16(registers[3]), dec_to_bin_16(registers[4]), dec_to_bin_16(registers[5]), dec_to_bin_16(registers[6]), flags)

    elif instruction_type == 'C':
        breakdown_ins.append(code[10:13])
        breakdown_ins.append(code[13:16])
        reg1 = encoding_reg[breakdown_ins[1]]
        reg2 = encoding_reg[breakdown_ins[-1]]
        ans = type_c(op_instruction, reg1, reg2, flags_track)
        #NEED TO CONFIRM THE FLAGS INITIALIZATION
        if op_instruction == "mov":
            registers[int(reg1[1])] = ans
        elif op_instruction == "not":
            registers[int(reg1[1])] = ans
        elif op_instruction == "div":
            registers[0], registers[1] = ans
        elif op_instruction == "cmp":
            flags_track["E"] = 0
            flags_track["V"] = 0
            flags_track["G"] = 0
            flags_track["L"] = 0
            flags_track[ans] = 1
        flags = "000000000000" + f"{flags_track['V']}" + f"{flags_track['L']}" + f"{flags_track['G']}" + f"{flags_track['E']}"
        pcs.append(PC)
        print(dec_to_bin_8(PC), dec_to_bin_16(registers[0]), dec_to_bin_16(registers[1]), dec_to_bin_16(registers[2]), dec_to_bin_16(registers[3]), dec_to_bin_16(registers[4]), dec_to_bin_16(registers[5]), dec_to_bin_16(registers[6]), flags)
    elif instruction_type == 'D':
        cycles.append(cycle)
        breakdown_ins.append(code[5:8])
        breakdown_ins.append(code[8:16])
        pcs.append(bin_to_dec(breakdown_ins[2]))
        flags_track["E"] = 0
        flags_track["V"] = 0
        flags_track["G"] = 0
        flags_track["L"] = 0
        '''load and store instructions
        ld variable to register
        st register to variable
        go to memory address of variable (convert binary in the line to decimal and go to mem_addr[i]) and make changes as required (change from dec to bin/bin to dec as required)
        '''
        if op_instruction == "ld":
            val = bin_to_dec(inp[bin_to_dec(breakdown_ins[2])])
            reg = f"{breakdown_ins[1]}"
            rreg = encoding_reg[reg]
            registers[int(rreg[1])] = val
        elif op_instruction == "st":
            reg = f"{breakdown_ins[1]}"
            rreg = encoding_reg[reg]
            val = registers[int(rreg[1])]
            inp[bin_to_dec(breakdown_ins[2])] = dec_to_bin_16(val)
        flags = "000000000000" + f"{flags_track['V']}" + f"{flags_track['L']}" + f"{flags_track['G']}" + f"{flags_track['E']}"
        pcs.append(PC)
        print(dec_to_bin_8(PC), dec_to_bin_16(registers[0]), dec_to_bin_16(registers[1]), dec_to_bin_16(registers[2]), dec_to_bin_16(registers[3]), dec_to_bin_16(registers[4]), dec_to_bin_16(registers[5]), dec_to_bin_16(registers[6]), flags)
    elif instruction_type == 'E':
        breakdown_ins.append(code[8:16])
        '''
        after cmp instruction, if next instruction is jlt, check the L flag, jgt, check g flag, je check E flag.
        if the flag is = 1, jump to line number
        '''
        program_counter = PC
        pcs.append(PC)
        if op_instruction == "jmp":
            flags = "0000000000000000"
            print(dec_to_bin_8(PC), dec_to_bin_16(registers[0]), dec_to_bin_16(registers[1]), dec_to_bin_16(registers[2]), dec_to_bin_16(registers[3]), dec_to_bin_16(registers[4]), dec_to_bin_16(registers[5]), dec_to_bin_16(registers[6]), flags)
            program_counter = bin_to_dec(breakdown_ins[1])
            cycles.append(cycle)
            pcs.append(program_counter)
            PC = program_counter - 1
        elif op_instruction == "jlt":
            flags = "0000000000000000"
            print(dec_to_bin_8(PC), dec_to_bin_16(registers[0]), dec_to_bin_16(registers[1]), dec_to_bin_16(registers[2]), dec_to_bin_16(registers[3]), dec_to_bin_16(registers[4]), dec_to_bin_16(registers[5]), dec_to_bin_16(registers[6]), flags)
            if flags_track["L"] == 1:
                program_counter = bin_to_dec(breakdown_ins[1])
                PC = program_counter - 1
                cycles.append(cycle)
                pcs.append(program_counter)
        elif op_instruction == "jgt":
            flags = "0000000000000000"
            print(dec_to_bin_8(PC), dec_to_bin_16(registers[0]), dec_to_bin_16(registers[1]), dec_to_bin_16(registers[2]), dec_to_bin_16(registers[3]), dec_to_bin_16(registers[4]), dec_to_bin_16(registers[5]), dec_to_bin_16(registers[6]), flags)
            if flags_track["G"] == 1:
                program_counter = bin_to_dec(breakdown_ins[1])
                PC = program_counter - 1
                cycles.append(cycle)
                pcs.append(program_counter)
        elif op_instruction == "je":
            flags = "0000000000000000"
            print(dec_to_bin_8(PC), dec_to_bin_16(registers[0]), dec_to_bin_16(registers[1]), dec_to_bin_16(registers[2]), dec_to_bin_16(registers[3]), dec_to_bin_16(registers[4]), dec_to_bin_16(registers[5]), dec_to_bin_16(registers[6]), flags)
            if flags_track["E"] == 1:
                program_counter = bin_to_dec(breakdown_ins[1])
                PC = program_counter - 1
                cycles.append(cycle)
                pcs.append(program_counter)
        flags_track["E"] = 0
        flags_track["V"] = 0
        flags_track["G"] = 0
        flags_track["L"] = 0
       
    elif instruction_type == 'F':
        halted = True
        flags = "000000000000" + f"{flags_track['V']}" + f"{flags_track['L']}" + f"{flags_track['G']}" + f"{flags_track['E']}"
        pcs.append(PC)
        print(dec_to_bin_8(PC), dec_to_bin_16(registers[0]), dec_to_bin_16(registers[1]), dec_to_bin_16(registers[2]), dec_to_bin_16(registers[3]), dec_to_bin_16(registers[4]), dec_to_bin_16(registers[5]), dec_to_bin_16(registers[6]), flags)
        continue
    PC +=1
    cycle += 1

for line in inp:
    print(line)

plt.ylim(0, 256)
plt.xlabel("cycle number")
plt.ylabel("memory address")
plt.scatter(cycles, pcs)
plt.show()
