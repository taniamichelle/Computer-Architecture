"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, memory, registers, pc= 0):
        """Construct a new CPU."""
        self.memory = [0] * 256  # 256 bytes of memory
        self.registers = [0] * 8  # 8 registers of 1-byte each
        self.pc = pc  # Program counter starting at 0th block of memory

    def ram_read(self, MAR):
        '''
        Accepts the address to read and returns the value stored there.
        '''
        self.MAR = MAR

        self.load()

        with open(program) as p:
            for line in p:
                comment_split = line.strip().split("#")

                value = comment_split[0].strip()

                if value == "":
                    continue

                num = int(value)
                memory[address] = num
                address += 1
                    

    def ram_write(self, value, MDR):
        '''
        Accepts a value to write, and the address to write it to
        '''
        self.value = value
        self.MDR = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self, instruction):
        """
        Reads the memory address stored in `PC` and stores the result in `IR`. Runs the CPU. 
        """
        self.load()

        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)
        
        # 'L' = operand_a < operand_b
        # 'G' = operand_a > operand_b
        # 'E' = operand_a == operand_b
    
        while True:
            instruction = memory[pc]
            if instruction == 'L':
                pc += 1
            else:
                pc = 0
            if instruction == 'G':
                pc += 1
            else:
                pc = 0
            if instruction == 'E':
                pc += 1
            else:
                pc = 0
