import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {}
        self.reg = [0] * 8
        self.pc = -1

    # Increases the PC counter
    @property
    def counter(self):
        self.pc += 1
        return self.pc

    def load(self, file: str):
        """Load a program into memory."""

        # with - ensures that a resource is "cleaned up" when the code that uses it finishes running
        with open(file, 'r') as file:
            for line in file:
                line = line.split("#")[0]

                if line:
                    # Converts the String into an int with base 2
                    binary = int(line, 2)
                    self.ram_load(binary)

    # Loads ram given a value
    def ram_load(self, value):
        address = len(self.ram.values())
        self.ram[address] = value

    # Reads ram given address
    def ram_read(self, address):
        return self.ram[address]

    # Register read given register
    def reg_read(self, register):
        return self.reg[register]

    # Register write given register and value
    def reg_write(self, register, value):
        self.reg[register] = value

    def alu(self, operation, reg_a, reg_b):
        """ALU operations."""

        if operation == "MUL":
            self.reg_write(reg_a, self.reg[reg_a] * self.reg[reg_b])

        else:
            raise Exception("Unsupported operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.counter,
            self.ram_read(self.counter),
            self.ram_read(self.counter + 1),
            self.ram_read(self.counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010  # 130
        PRN = 0b01000111  # 71
        MUL = 0b10100010  # 162
        HLT = 0b00000001  # 1

        running = True

        while running:
            IR  = self.ram_read(self.counter)

            # LDI: load "immediate", store a value in a register, or "set this register to this value".
            if IR == LDI:
                reg_a = self.ram_read(self.counter)
                value = self.ram_read(self.counter)
                self.reg_write(reg_a, value)

            # PRN: a pseudo-instruction that prints the numeric value stored in a register.
            elif IR == PRN:
                reg_a = self.ram_read(self.counter)
                value = self.reg_read(reg_a)
                print(value)

            # Multiplys
            elif IR == MUL:
                reg_a = self.ram_read(self.counter)
                reg_b = self.ram_read(self.counter)
                self.alu("MUL", reg_a, reg_b)

            # Stop running
            elif IR == HLT:
                running = False

            else:
                raise Exception("Unsupported instruction")
