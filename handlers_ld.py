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

def ld_b_a(cpu):
    cpu.B = cpu.A

# LD C, r8
def ld_c_b(cpu):
    cpu.C = cpu.B

def ld_c_c(cpu):
    return

def ld_c_d(cpu):
    cpu.C = cpu.D

def ld_c_e(cpu):
    cpu.C = cpu.E

def ld_c_h(cpu):
    cpu.C = cpu.H

def ld_c_l(cpu):
    cpu.C = cpu.L

def ld_c_a(cpu):
    cpu.C = cpu.A

# LD D, r8

def ld_d_b(cpu):
    cpu.D = cpu.B
def ld_d_c(cpu):
    cpu.D = cpu.C
def ld_d_d(cpu):
    return
def ld_d_e(cpu):
    cpu.D = cpu.E
def ld_d_h(cpu):
    cpu.D = cpu.H
def ld_d_l(cpu):
    cpu.D = cpu.L
def ld_d_a(cpu):
    cpu.D = cpu.A

# LD E, r8
def ld_e_b(cpu):
    cpu.E = cpu.B
def ld_e_c(cpu):
    cpu.E = cpu.C
def ld_e_d(cpu):
    cpu.E = cpu.D
def ld_e_e(cpu):
    return
def ld_e_h(cpu):
    cpu.E = cpu.H
def ld_e_l(cpu):
    cpu.E = cpu.L
def ld_e_a(cpu):
    cpu.E = cpu.A

# LD H, r8
def ld_h_b(cpu):
    cpu.H = cpu.B
def ld_h_c(cpu):
    cpu.H = cpu.C
def ld_h_d(cpu):
    cpu.H = cpu.D
def ld_h_e(cpu):
    cpu.H = cpu.E
def ld_h_h(cpu):
    return
def ld_h_l(cpu):
    cpu.H = cpu.L
def ld_h_a(cpu):
    cpu.H = cpu.A

# LD L, r8
def ld_l_b(cpu):
    cpu.L = cpu.B
def ld_l_c(cpu):
    cpu.L = cpu.C
def ld_l_d(cpu):
    cpu.L = cpu.D
def ld_l_e(cpu):
    cpu.L = cpu.E
def ld_l_h(cpu):
    cpu.L = cpu.H
def ld_l_l(cpu):
    return
def ld_l_a(cpu):
    cpu.L = cpu.A
