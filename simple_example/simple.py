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
# ​# HOLDS PROGRAMS. List contains our arguments (what we expect to print)
# memory = [
#     PRINT_BEEJ,
#     SAVE,  # SAVE 65 in R2
#     65,
#     2,
#     SAVE,  # SAVE 20 in R3
#     20,
#     3,
#     ADD,   # R2 + R3 == 65 + 20; Store in R2 (R2 += R3)
#     2,
#     3,
#     PRINT_REGISTER,  # PRINT R2 (85)
#     2,
#     HALT
# ]

memory = [0] * 256  # Can only store 256 bytes of memory b/c we have an 8-bit emulator. All of our values are 8 bits. This creates our stack, which uses the highest bits of RAM.
​
# CREATE 8 registers of 1-byte each
register = [0] * 8  
​
pc = 0  # Program counter; memory address is 0 (PC is at the 0th block of memory to start)
sp = 7  # Stack pointer is R7

# Think of this as loading our file off of a disk (which is slow) and into memory to speed up the accessing of it
​def load_memory(filename):
    try:
        address = 0
        # Open the file
        with open(filename) as f:
            # Read all the lines
            for line in f:
                # Parse out comments ('#') and remove white space
                comment_split = line.strip().split("#")
​
                # Cast the numbers from strings to ints. remove white space
                value = comment_split[0].strip()
​
                # Ignore blank lines
                if value == "":
                    continue
​
                num = int(value)
                memory[address] = num  # Set memory address to the num
                address += 1
​
    except FileNotFoundError:  # Error handling
        print("File not found")
        sys.exit(2)
​
​
if len(sys.argv) != 2:
    print("ERROR: Must have file name")
    sys.exit(1)
​
load_memory(sys.argv[1])


# PROCESSOR (REPL: read, eval, program/command, loop)
while True:  # While it's running
    command = memory[pc]  # Read command from our memory
    print('memory', memory)
    print('register', register)

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
    elif command == PUSH:
        # Grab reg from reg argument
        reg = memory[pc + 1]
        val = register[reg]
        # Decrement SP
        register[SP] -= 1
        # Copy the value in the given reg to the address SP points to.
        memory[register[SP]] = val
        pc += 2
    elif command == POP:
        # Grab the value from memory at the top of Stack
        reg = memory[pc + 1]
        val = memory[register[SP]]
        #  Copy the value from the address pointed to by SP into the given reg.
        register[reg] = val
        # Increment SP
        register[SP] += 1
        pc += 2
    elif command == HALT:
        sys.exit(0)
    else:
        print(f"I did not understand that command: {command}")
        sys.exit(1)  # Exit out of the program; could do "BREAK" instead