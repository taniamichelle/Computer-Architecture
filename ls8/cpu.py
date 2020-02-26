"""CPU functionality."""

import sys

instruction_hash = {
    0b00000001: 'HLT',  # Halt the CPU (and exit the emulator).  should it be HLT = 01 ?
    0b10000010: 'LDI',  # Set the value of a register to an integer
    0b01000111: 'PRN'  # Print numeric value stored in the given register. Print to the console the decimal integer value that is stored in the given register
}

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 bytes of memory
        self.register = [0] * 8  # 8 registers of 1-byte each
        self.pc = 0  # Program counter starting at 0th block of memory
        self.operands = None
        self.operand_a = None
        self.operand_b = None
        self.methods_hash = {
            'LDI': self.execute_ldi,
            'PRN': self.execute_prn,
            'HLT': self.execute_hlt
        }
    
    def execute_ldi(self):
        self.register[self.operand_a] = self.operand_b  # Store value (op b) in reg 0 (op a)
        self.pc += self.operands  # Increment pc by num of operands

    def execute_prn(self):
        print("Print: 1 operand", self.register[self.operand_a])
        self.pc += self.operands

    def execute_hlt(self):
        sys.exit()
    def ram_read(self, MAR):
        '''
        Accepts the address to read and returns the value stored there.
        '''
        return self.ram[MAR]                  

    def ram_write(self, MAR, MDR):
        '''
        Accepts a value to write and the address to write it to.
        '''
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.strip().split("#")
                    value = comment_split[0].strip()
                    if value == "":
                        continue
                    num = int(value, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print("File not found.")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
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
            print(" %02X" % self.register[i], end='')

        print()


    def run(self):
        """
        Reads the memory address stored in `PC` and stores the result in `IR`. Runs the CPU. 
        """

        while True:
            IR = self.ram_read(self.pc)  # Read and store memory address stored in reg `PC` as IR
            self.operands = IR >> 6  # Right-shift IR by 6 so that the high bits (containing # operands) are rightmost

            if self.operands == 1:  # If 1 argument (operand)
                self.operand_a = self.ram_read(self.pc+1)
            elif self.operands == 2:  # If 2 arguments
                self.operand_a = self.ram_read(self.pc+1)
                self.operand_b = self.ram_read(self.pc+2)
            
            self.methods_hash[instruction_hash[IR]]()  # Invoke our methods_hash as a function

            self.pc += 1  # Increment pc by 1

