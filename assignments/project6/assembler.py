import sys


class Assembler:
    SYMBOLS = {
                'R0': 0,
                'R1': 1,
                'R2': 2,
                'R3': 3,
                'R4': 4,
                'R5': 5,
                'R6': 6,
                'R7': 7,
                'R8': 8,
                'R9': 9,
                'R1O': 10,
                'R11': 11,
                'R12': 12,
                'R13': 13,
                'R14': 14,
                'R15': 15,
                'SCREEN': 16384,
                'KBD': 24576,
                'SP': 0,
                'LCL': 1,
                'ARG': 2,
                'THIS': 3,
                'THAT': 4
            }
    BIN_COMP = {
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            '!D': '0001101',
            '!A': '0110001',
            '-D': '0001111',
            '-A': '0110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'D+A': '0000010',
            'D-A': '0010011',
            'A-D': '0000111',
            'D&A': '0000000',
            'D|A': '0010101',
            'M': '1110000',
            '!M': '1110001',
            '-M': '1110011',
            'M+1': '1110111',
            'M-1': '1110010',
            'D+M': '1000010',
            'D-M': '1010011',
            'M-D': '1000111',
            'D&M': '1000000',
            'D|M': '1010101'
        }

    def __init__(self,filename):
        
        self.next_address = 16
        self.asm_filename = filename

        self.parse_filename()
        self.parse_instructions()

        self.write_hack_file()

    def parse_filename(self):
        filename = self.asm_filename.split('\\')[-1].replace('.asm','.hack')
        self.hack_filename = f"output\{filename}"
        print(self.hack_filename)

    def parse_lines(self):
        instructions = list()
        for line in self.instructions:
            if not (line[:2] == '//' or line == '\n'):
                line = line.replace('\n','')
                line = line.replace(' ','')
                if len(line.split('/')) > 1:
                    line = line.split('/')[0]
                instructions.append(line)
        self.instructions = instructions
    
    def find_loops(self):
        counter = 0
        for idx, val in enumerate(self.instructions):
            if val[0] == '(' and val[len(val) - 1] == ')':
                loop = val.replace('(', '').replace(')', '')
                self.SYMBOLS[loop] = idx - counter
                counter += 1
        print(f'counter : {counter}')
    def get_instructions(self):
        with  open(self.asm_filename, 'r') as asm_file:
        
            instructions = asm_file.readlines()
            # instructions.remove('\n')
        self.instructions = instructions
    

    def parse_symbol(self,symbol):
        
        if symbol not in self.SYMBOLS:
            self.SYMBOLS[symbol] = self.next_address
            self.next_address += 1

        return self.SYMBOLS[symbol]


    def int_to_bin(self,num, bit_size=16):
        bin_num = bin(num)[2:]
        return (bit_size - len(bin_num)) * '0' + bin_num


    def parse_a_instruction(self,instruction):
        address = instruction[1:]
        try:
            return self.int_to_bin(int(address))
        except ValueError:
            return self.int_to_bin(self.parse_symbol(address))

    def get_bin_comp(self,comp):
        return self.BIN_COMP[comp]

    def get_bin_dest(self,dest):
        dest_list = ['0', '0', '0']
        if not dest:
            return ''.join(dest_list)
        if 'A' in dest:
            dest_list[0] = '1'
        if 'D' in dest:
            dest_list[1] = '1'
        if 'M' in dest:
            dest_list[2] = '1'
        return ''.join(dest_list)


    def get_bin_jmp(self,jmp):
        if not jmp:
            return '000'
        return {
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
        }[jmp]

    
    def parse_c_instruction(self,instruction):
        bin_output = '111'
        dest = None
        jmp = None

        if '=' in instruction:
            [dest, instruction] = instruction.split('=')
        if ';' in instruction:
            [comp, jmp] = instruction.split(';')
        else:
            comp = instruction

        bin_output += self.get_bin_comp(comp)
        bin_output += self.get_bin_dest(dest)
        bin_output += self.get_bin_jmp(jmp)
        return bin_output

    def parse_instructions(self):

        self.get_instructions()
        print(self.instructions)
        self.parse_lines()
        print(len(self.instructions))
        self.find_loops()
        hack_instructions = list()
        for inst in self.instructions:
            if inst[0] == '(':
                continue

            elif inst[0] == '@':
                binary_instruction = self.parse_a_instruction(inst)
            else:
                binary_instruction = self.parse_c_instruction(inst)
            hack_instructions.append(binary_instruction)
        self.hack_instructions = hack_instructions
        print(len(self.hack_instructions))
    def write_hack_file(self):
        with open(self.hack_filename,'w') as hack_file:
            hack_file.write('\n'.join(self.hack_instructions))


if __name__ == '__main__':
    filename =  sys.argv[1]
    assembler = Assembler(filename)