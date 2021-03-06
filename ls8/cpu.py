"""CPU functionality."""

import sys

# Branch-table/ Dispatch-table to simplify instruction handler. Dictionary of functions indexed by opcode value.
instruction_hash = {
    0b00000001: 'HLT',  # Halt the CPU (and exit the emulator).  should it be HLT = 01 ?
    0b10000010: 'LDI',  # Set the value of a register to an integer
    0b01000111: 'PRN',  # Print numeric value stored in the given register. Print to the console the decimal integer value that is stored in the given register
    0b10100000: 'ADD',  # Add the values in 2 reg together + store in Reg A
    0b10100010: 'MUL',  # Multipy the values in 2 reg together + store in Reg A
    0b01000101: 'PUSH',  # Push the value in given register onto top of stack
    0b01000110: 'POP',  # Pop the value at the top of stack into given register, 
    0b01010000: 'CALL',  # Calls a subroutine at the address stored in the reg
    0b00010001: 'RET'  # Return from subroutine
}

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 bytes of memory
        self.register = [0] * 8  # 8 registers of 1-byte each
        self.pc = 0  # Program counter starting at 0th block of memory
        self.sp = 7  # SP is R7
        self.operands = None
        self.operand_a = None
        self.operand_b = None
        self.methods_hash = {
            'LDI': self.execute_ldi,
            'PRN': self.execute_prn,
            'HLT': self.execute_hlt,
            'ADD': self.execute_add,
            'MUL': self.execute_mul,
            'PUSH': self.execute_push,
            'POP': self.execute_pop,
            'CALL': self.execute_call,
            'RET': self.execute_ret
        }
    
    def execute_call(self):
        # Get address of next instruction
        reg = self.pc + 2
        # Push address of next instruction onto top of stack
        self.ram[self.sp] = reg
        # Decrement SP
        self.sp -= 1
        print("Self.pc 1: ", self.pc)
        # Set PC to the address stored in the given register (which causes us to jump to that location in RAM)
        print("Self.ram 1: ", self.ram[self.pc])
        print("Self.pc 2: ", self.pc + 1)
        print("Self.ram: ", self.ram[self.pc + 1])
        self.pc = self.register[self.ram[self.pc + 1]]        
        print("Self.pc: ", self.pc)
        
        print("Register: ", self.register)
        # First instruction in the subroutine executes.
        
    def execute_ret(self):
        # Increment SP
        self.sp += 1
        # Pop the value from the top of the stack 
        val = self.ram[self.sp]
        # Store value(address) in the PC
        self.pc = val

    def execute_push(self):
        '''
        Runs `PUSH`. Stack begins at address F3 and grows downward. SP points at value at top of stack or at F4 if stack is empty. Registers R0-R6 get pushed onto the stack in that order.
        '''
        # Grab register from reg argument
        reg = self.ram[self.pc + 1]
        val = self.register[reg]
        # print("reg in push: ", self.ram[self.pc + 1])
        # print("val in push: ", self.register[reg])
        # print("sp start in push: ", self.sp)
        # Decrement SP
        self.register[self.sp] -= 1
        # print("sp end in push: ", self.sp)
        # Copy the value in the given register(from R0-R6) to the address pointed to by SP
        self.ram[self.register[self.sp]] = val
        # self.pc += 2

    def execute_pop(self):
        '''
        Runs `POP`. Registers R6-R0 are popped off the stack in that order.
        '''
        #  Grabs the value from memory at the top of stack.
        reg = self.ram[self.pc + 1]
        val = self.ram[self.register[self.sp]]
        # print("reg in pop: ", self.ram[self.pc + 1])
        # print("val in pop: ", self.register[reg])
        # print("sp start in pop: ", self.sp)
        # Copy the value from address pointed to by SP to the given register
        self.register[reg] = val
        # Increment SP
        self.register[self.sp] += 1
        # print("sp end in pop: ", self.sp)
        # self.pc += 2
    
    def execute_add(self):
        '''
        Runs alu() method passing in `ADD` as the instructional argument.
        '''
        # print('register 1', self.register)
        self.alu('ADD', self.operand_a, self.operand_b)

    def execute_mul(self):
        '''
        Runs alu() method passing in `MUL` as the instructional argument.
        '''
        # print('register 1', self.register)
        self.alu('MUL', self.operand_a, self.operand_b)
        # print('register', self.register)
        # self.pc += self.operands 

    def execute_ldi(self):
        '''
        Runs `LDI`, which sets the value of a register to an integer.
        '''
        self.register[self.operand_a] = self.operand_b  # Store value (op b) in reg 0 (op a)
        # self.pc += self.operands  # Increment pc by num of operands

    def execute_prn(self):
        '''
        Prints numeric value (decimal integer)stored in the given register to console.
        '''
        print("PRN: ", self.register[self.operand_a])
        # self.pc += self.operands

    def execute_hlt(self):
        '''
        Halts the CPU and exits the emulator.
        '''
        sys.exit()

    def handle_pc(self, IR):
        '''
        Method to make pc dynamic.
        '''
        if ((IR <<3)%256) >>7 == 1:  # Isolate `B` condition from instructions
            pass
        else:
            self.pc += self.operands + 1  # Alternative to incrementing pc in each method

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
        """Loads a program into memory."""

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
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        #elif op == "SUB": self.register[reg_a] -= self.register[reg_b]
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
            print("IR", IR)
            self.methods_hash[instruction_hash[IR]]()  # Invoke our methods_hash as a function
            self.handle_pc(IR)
            # self.pc += 1  # Increment pc by 1

