import sys
​
# COMMANDS
PRINT_BEEJ     = 1  
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4  # Save a value into a register
PRINT_REGISTER = 5  # Print the value in a register
ADD            = 6  # ADD 2 registers, store the result in 1st reg
​
​# HOLDS PROGRAMS. List contains our arguments (what we expect to print)
memory = [
    PRINT_BEEJ,
    SAVE,  # SAVE 65 in R2
    65,
    2,
    SAVE,  # SAVE 20 in R3
    20,
    3,
    ADD,   # R2 + R3 == 65 + 20; Store in R2 (R2 += R3)
    2,
    3,
    PRINT_REGISTER,  # PRINT R2 (85)
    2,
    HALT
]
​
# CREATE 8 registers
register = [0] * 8  
​
pc = 0  # Program counter; memory address is 0
​
# PROCESSOR (REPL: read, eval, program/command, loop)
while True:  # While it's running
    command = memory[pc]  # Read command from our memory
​
    if command == PRINT_BEEJ:  # Evaluate command
        print("Beej!")
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2
    elif command == SAVE:
        # Save a value to a register
        num = memory[pc + 1]  # Get num from first arg
        reg = memory[pc + 2]  # Get reg index from second arg
        register[reg] = num  # Store num in correct register by reg index
        pc += 3  # B/c we have 2 args and 1 command
    elif command == PRINT_REGISTER:
        # Print the value in a register
        reg = memory[pc + 1]  # Get num from first arg
        print(register[reg])  # Print contents of that reg
        pc += 2
    elif command == ADD:
        reg_a = memory[pc + 1]  # Get 1st reg index from 1st arg
        reg_b = memory[pc + 2]  # Get 2nd reg index from 2nd arg
        register[reg_a] += register[reg_b]  # ADD 2 registers, store the result in 1st reg (reg_a) 
        pc += 3
    elif command == HALT:
        sys.exit(0)
    else:
        print(f"I did not understand that command: {command}")
        sys.exit(1)  # Exit out of the program; could do "BREAK" instead