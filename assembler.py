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

