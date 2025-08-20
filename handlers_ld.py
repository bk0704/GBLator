def nop(cpu):
    # 0x00 return nun
    return

# LD r8, n8

def ld_a_n8(cpu):
    # LD A, n8
    value = cpu.fetch8()
    cpu.A = value

def ld_b_n8(cpu):
    # LD B, n8
    value = cpu.fetch8()
    cpu.B = value

def ld_c_n8(cpu):
    # LD C, n8
    value = cpu.fetch8()
    cpu.C = value

def ld_d_n8(cpu):
    # LD D, n8
    value = cpu.fetch8()
    cpu.D = value

def ld_e_n8(cpu):
    # LD E, n8
    value = cpu.fetch8()
    cpu.E = value

def ld_h_n8(cpu):
    # LD H, n8
    value = cpu.fetch8()
    cpu.H = value

def ld_l_n8(cpu):
    # LD L, n8
    value = cpu.fetch8()
    cpu.L = value


# LD B, r8

def ld_b_b(cpu):
    return

def ld_b_c(cpu):
    cpu.B = cpu.C

def ld_b_d(cpu):
    cpu.B = cpu.D

def ld_b_e(cpu):
    cpu.B = cpu.E

def ld_b_h(cpu):
    cpu.B = cpu.H

def ld_b_l(cpu):
    cpu.B = cpu.L