import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8 # Number of registers
        self.ram = [0] * 256     # Bytes
        self.pc = 0              # Program Counter
        self.address = 0
        self.stack = []

        # operations
        self.operations = {
            "00000001": {"advance": 0, "opCode": "HLT"}, # Halt
            "10000010": {"advance": 2, "opCode": "LDI"}, # Save
            "10100010": {"advance": 2, "opCode": "MUL"}, # Multiply
            "01000110": {"advance": 1, "opCode": "POP"}, # Pop
            "01000111": {"advance": 1, "opCode": "PRN"}, # Print
            "01000101": {"advance": 1, "opCode": "PUSH"} # Push
        }

    # Loads the file and adds each line
    def load(self, file: str):
        """Load a program into memory."""

        program = None

        # with - ensures that a resource is "cleaned up" when the code that uses it finishes running
        with open(file, 'r') as file:
            program = file.readlines()
        for instruction in program:
            if "#" in instruction:
                instruction = instruction[: instruction.index("#")].strip()

            self.ram[self.address] = instruction
            self.address += 1

    # Loads ram given a value
    def ram_load(self, value):
        address = len(self.ram.values())
        self.ram[address] = value

    # Reads ram given address
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    # Register read given register
    def reg_read(self, register):
        return self.reg[register]

    # Register write given register and value
    def reg_write(self, register, value):
        self.reg[register] = value

    def alu(self, operation, reg_a, reg_b):
        """ALU operations."""

        if operation == "LDI":
            self.registers[reg_a] = reg_b
        elif operation == "PRN":
            print(self.registers[reg_a])
        elif operation == "MUL":
            self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b]
        elif operation == "PUSH":
            self.stack.append(self.registers[reg_a])
        elif operation == "POP":
            self.registers[reg_a] = self.stack.pop()
        else:
            raise Exception("Unsupported operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def run(self):
        """Run the CPU."""

        running = True

        while self.pc <= self.address:
            # IR = Instruction Register
            IR = self.ram_read(self.pc)
            objMap = self.operations[IR]
            op = objMap["opCode"]

            if op == "HLT":
                return

            operand_a = int(self.ram_read(self.pc + 1), 2)
            operand_b = int(self.ram_read(self.pc + 2), 2)

            self.alu(op, operand_a, operand_b)
            self.pc += 1 + objMap["advance"]
