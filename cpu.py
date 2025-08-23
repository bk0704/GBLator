# Emulate LR35902 CPU state and lifecycle

import opcodes

FLAG_Z = 0x80  # bit 7
FLAG_N = 0x40  # bit 6
FLAG_H = 0x20  # bit 5
FLAG_C = 0x10  # bit 4


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
        self.PC = (self.PC + 1) & 0xFFFF
        return byte

    def fetch16(self):
        # Read little-endian 16-bit at PC (low, then high), advance PC by 2 (16-bit wrap)
        low_byte = self.bus.read8(self.PC)
        high_byte = self.bus.read8(self.PC + 1 & 0xFFFF)
        bytes = (high_byte << 8) | low_byte
        self.PC += 2
        self.PC &= 0xFFFF
        return bytes

    def get_flagZ(self):
        return (self.F >> 7) & 1

    def get_flagN(self):
        return (self.F >> 6) & 1

    def get_flagH(self):
        return (self.F >> 5) & 1

    def get_flagC(self):
        return (self.F >> 4) & 1

    def set_flags(self, z=None, n=None, h=None, c=None):
        f = self.F

        M = 0
        if z is not None: M |= FLAG_Z
        if n is not None: M |= FLAG_N
        if h is not None: M |= FLAG_H
        if c is not None: M |= FLAG_C

        V = 0
        if z: V |= FLAG_Z
        if n: V |= FLAG_N
        if h: V |= FLAG_H
        if c: V |= FLAG_C

        f = (f & ~M) | V
        self.F = f & 0xF0  # low nibble always 0

    def get_AF(self):
        return (self.A << 8) | self.F

    def set_AF(self, value):
        value &= 0xFFFF
        a = value >> 8
        f = value & 0xFF
        f &= 0xF0
        self.A = a
        self.F = f

    def get_BC(self):
        return (self.B << 8) | self.C

    def set_BC(self, value):
        value &= 0xFFFF
        b = value >> 8
        c = value & 0xFF
        self.B = b
        self.C = c

    def get_DE(self):
        return (self.D << 8) | self.E

    def set_DE(self, value):
        value &= 0xFFFF
        d = value >> 8
        e = value & 0xFF
        self.D = d
        self.E = e

    def get_HL(self):
        return (self.H << 8) | self.L

    def set_HL(self, value):
        value &= 0xFFFF
        h = value >> 8
        l = value & 0xFF
        self.H = h
        self.L = l

    def r8(self, i):
        if i == 0:
            return self.B
        elif i == 1:
            return self.C
        elif i == 2:
            return self.D
        elif i == 3:
            return self.E
        elif i == 4:
            return self.H
        elif i == 5:
            return self.L
        elif i == 6:
            return self.bus.read8(self.get_HL())
        elif i == 7:
            return self.A
        else:
            raise ValueError("Invalid r8 index")

    def set_r8(self, i, value):
        value = value & 0xFF
        if i == 0:
            self.B = value
        elif i == 1:
            self.C = value
        elif i == 2:
            self.D = value
        elif i == 3:
            self.E = value
        elif i == 4:
            self.H = value
        elif i == 5:
            self.L = value
        elif i == 6:
            self.bus.write8(self.get_HL(), value)
        elif i == 7:
            self.A = value
        else:
            raise ValueError("Invalid r8 index")

    def r16(self, i):
        if i == 0:
            return self.get_BC()
        elif i == 1:
            return self.get_DE()
        elif i == 2:
            return self.get_HL()
        elif i == 3:
            return self.SP
        else:
            raise ValueError("Invalid r16 index")

    def set_r16(self, i, value):
        value &= 0xFFFF
        if i == 0:
            self.set_BC(value)
        elif i == 1:
            self.set_DE(value)
        elif i == 2:
            self.set_HL(value)
        elif i == 3:
            self.SP = value
        else:
            raise ValueError("Invalid r16 index")

    def fetch_e8(self):
        # Fetch the next byte and interpret it as a signed 8-bit immediate
        imm = self.fetch8()
        return imm - 0x100 if imm & 0x80 else imm

    def step(self):
        op = self.fetch8()
        entry = opcodes.ops_base[op]
        handler = entry["handler"]
        if entry == None or handler == None:
            self.last_instr_cycles = 0
        pc_before = self.PC
        handler(self)
        if self.PC == pc_before:
            self.PC += entry["length"] - 1
            self.PC &= 0xFFFF
        cycles = entry["cycles"]
        self.last_instr_cycles = cycles
        self.cycles_total += cycles