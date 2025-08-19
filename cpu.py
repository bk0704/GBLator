# Emulate LR35902 CPU state and lifecycle

class CPU:
    def __init__(self, bus):
        self.bus = bus # the thing with read8/write8

        # registers

        #8-bit
        self.A = 0x00 # Accumulator
        self.F = 0x00 # Flags
        self.B = 0x00
        self.C = 0x00
        self.D = 0x00
        self.E = 0x00
        self.H = 0x00
        self.L = 0x00

        # Special 16-bit
        self.PC = 0x0000
        self.SP = 0x0000

        # Control State
        self.IME = False # Interrupt Master enable: Master switch that decides if the CPU is allowed service interrupts
        self.halted = False # Shows if CPU is in halt mode
        self.stopped = False # shows if the CPU is in STOP mode (an even deeper sleep, usually triggered manually, sometimes tied to hardware like button presses or the Game Boy Color’s speed switch).
        self.ei_pending = False # a special flip-flop used for the EI instruction.

        # Timing
        self.cycles_total = 0
        self.last_instr_cycles = 0

    def reset(self, post_boot=True):
        # Use Pandocs post-boot values for DMG
        self.A = 0x01
        self.F = 0xB0
        self.B = 0x00
        self.C = 0x13
        self.D = 0x00
        self.E = 0xD8
        self.H = 0x01
        self.L = 0x4D
        self.PC = 0x0100
        self.SP = 0xFFFE

        self.IME = False
        self.halted = False
        self.stopped = False
        self.ei_pending = False

        self.cycles_total = 0
        self.last_instr_cycles = 0

        self.F &= 0xF0

    def fetch8(self):
        # Read by from memory at PC, advances PC by 1 with 16-bit Wrap
        byte = self.bus.read8(self.PC)
        self.PC += 1
        self.PC &= 0xFFFF
        return byte

    def fetch16(self):
        # Read by from memory at PC, advances PC by 1 with 16-bit Wrap
        high_byte = self.bus.read8(self.PC + 1)
        low_byte = self.bus.read8(self.PC)
        bytes = (high_byte << 8) | low_byte
        self.PC += 2
        self.PC &= 0xFFFF
        return bytes


