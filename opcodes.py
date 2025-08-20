ops_base = [None] * 0x100

def nop(cpu):
    # 0x00 return nun
    return

def ld_a_n8(cpu):
    # LD A, n8
    value = cpu.fetch8()
    cpu.A = value

def ld_b_n8(cpu):
    # LD B, n8
    value = cpu.fetch8()
    cpu.B = value

ops_base[0x00] = {
    "mnemonic": "NOP",
    "handler": nop,
    "length": 1,
    "cycles": 4,
}

ops_base[0x3E] = {
    "mnemonic": "LD A,n8",
    "handler": ld_a_n8,
    "length": 2,
    "cycles": 8,
}

ops_base[0x06] = {
    "mnemonic": "LD B,d8",
    "handler": ld_b_n8,
    "length": 2,
    "cycles": 8,
}
