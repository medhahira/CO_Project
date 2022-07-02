import sys

isa = {
    #instruction: [type, Opcode]
    "add":["A", "10000"],
    "sub":["A", "10001"],
    "movi":["B", "10010"],
    "movr":["C", "10011"],
    "ld":["D", "10100"],
    "st":["D", "10101"],
    "mul":["A", "10110"],
    "div":["C", "10111"],
    "rs":["B", "11000"],
    "ls":["B", "11001"],
    "xor":["A", "11010"],
    "or":["A", "11011"],
    "and":["A", "11100"],
    "not":["C", "11101"],
    "cmp":["C", "11110"],
    "jmp":["E", "11111"],
    "jlt":["E", "01100"],
    "jgt":["E", "01101"],
    "je":["E", "01111"],
    "hlt":["F", "01010"],
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
immediate = {
    "A": 0,
    "B": 1,
    "C": 0,
    "D": 0,
    "E": 0,
    "F": 0,
}
unused = {
    "A": 2,
    "B": 0,
    "C": 5,
    "D": 0,
    "E": 3,
    "F": 11,
}
input = {
    "A": 4,
    "B": 3,
    "C": 3,
    "D": 3,
    "E": 2,
    "F": 1,
}
mem_addr = {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 1,
    "E": 1,
    "F": 0,
}
number_of_regs = {
    "A": 3,
    "B": 1,
    "C": 2,
    "D": 1,
    "E": 0,
    "F": 0,
}
type_include = {
    "A" : ["op", "reg", "reg", "reg"],
    "B" : ["op", "reg", "imm"],
    "C" : ["op", "reg", "reg"],
    "D" : ["op", "reg", "mem"],
    "E" : ["op", "mem"],
    "F" : ["op"],
    "var": ["declaration", "variable"]
}
#for loop to store :

reg_bits = 3
op_code_bits = 5
imm_bits = 8
mem_addr_bits = 8
convert = ""
isa_flag = False

assembly= []
for line in sys.stdin:
    if 'hlt' == line.rstrip():
        convert = ""
        if "hlt" in isa.keys():
            convert += isa["hlt"][1]
            isa_flag = True
            if isa["hlt"][0] in unused.keys():
                for k in range(unused[isa["hlt"][0]]):
                    convert += "0"
            print(convert)
        break
    assembly.append(line)
#print(assembly)
def convertor(dec):
    j = []
    while dec >= 1:
        j.append(int(dec % 2))
        dec = dec//2
    j.reverse()
    ans = ""
    len = 0
    for i in j:
        ans += str(i)
        len += 1
    answer = ""
    for i in range(8-len):
        answer += "0"
    answer += ans
    return answer


for i in isa.keys():
    for j in assembly:
        if i in j:
            convert += isa[i][1]
            isa_flag = True
            if isa[i][0] in unused.keys():
                for k in range(unused[isa[i][0]]):
                    convert += "0"

variables = []
for i in assembly:
    j = i.strip().split(" ")
    #print(j)
    if j[0] == "mov":
        if "$" in j[2]:
            j[0] = "movi"
        else:
            j[0] = "movr"
    if j[0] == "var":
        if len(j) == len(type_include[j[0]]):
            variables.append(j[1])
        else:
            print("ERROR, instruction is incomplete")
    elif j[0] in isa.keys():
        if len(j) == len(type_include[isa[j[0]][0]]):
            convert = ""
            for k in range(len(type_include[isa[j[0]][0]])):
                if type_include[isa[j[0]][0]][k].strip() == "op":
                    convert += isa[j[0]][1]
                    for m in range(unused[isa[j[0]][0]]):
                        convert+="0"
                if type_include[isa[j[0]][0]][k].strip() == "reg":
                    convert+=regs[j[k]]
                if type_include[isa[j[0]][0]][k].strip() == "imm":
                    if "$" in j[k]:
                        c = j[k].index("$")
                        num = (j[k][c+1:])
                        ans = ""
                        for m in num:
                            ans += m
                        answer = int(ans)
                        convert += convertor(answer)
                if type_include[isa[j[0]][0]][k].strip() == "mem":
                    if j[k] in variables:
                        addr = len(assembly)+1-variables.index(j[k])-1
                        convert += convertor(addr)
                    else:
                        print("ERROR, undefined variable used")

            print(convert)
        else:
            print("ERROR, length of instruction is insufficient")
    else:
        print("ERROR, undefined instruction")
