"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 bytes of memory
        self.register = [0] * 8  # 8 registers of 1-byte each
        self.pc = 0  # Program counter starting at 0th block of memory

    def ram_read(self, MAR):
        '''
        Accepts the address to read and returns the value stored there.
        '''
        # self.MAR = MAR

        return self.ram[MAR]                  

    def ram_write(self, MAR, MDR):
        '''
        Accepts a value to write and the address to write it to.
        '''
        # self.MAR = MAR  # RAM address
        # self.MDR = MDR  # Data being saved
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # STEP 7: Un-hardcode the machine code
        # For now, we've just hardcoded a program:
        # Loading program(s) into RAM
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        # with open(program) as p:
        #     for line in p:
        #         comment_split = line.strip().split("#")

        #         value = comment_split[0].strip()

        #         if value == "":
        #             continue

        #         num = int(value)
        #         memory[address] = num
        #         address += 1
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

    # # COMMANDS
    # HLT = 0b00000001  # Halt the CPU (and exit the emulator).  should it be HLT = 01 ?
    # LDI = 0b10000010 00000rrr iiiiiiii  # Set the value of a register to an integer.  should it be LDI = 82 0r ii ?
    # PRN = 0b01000111 00000rrr  # Print numeric value stored in the given register. Print to the console the decimal integer value that is stored in the given register. should it be PRN = 47 0r ?

# Print to the console the decimal integer value that is stored in the given register.

    # STEP 3: Implement `run()` method
    def run(self):
        """
        Reads the memory address stored in `PC` and stores the result in `IR`. Runs the CPU. 
        """

        while True:
            IR = self.ram_read(self.pc)
            operands = IR >> 6
            # if operands == 0:  # If no arguments in IR
            #     pass
            if operands == 1:  # If 1 argument
                operand_a = self.ram_read(self.pc+1)
            elif operands == 2:  # If 2 arguments
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)
            if IR == 0b10000010:
                self.register[operand_a] = operand_b
                self.pc += operands
            elif IR == 0b01000111:
                print("Print: 1 operand", self.register[operand_a])
                self.pc += operands
            elif IR == 0b00000001:
                break
            self.pc += 1 
            # STEP 4: Exit loop if `HLT` instruction encountered.
            # STEP 5: Add `LDI` instruction
            # STEP 6: Add `PRN` instruction

