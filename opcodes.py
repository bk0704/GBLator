from handlers_ld import nop, ld_a_n8, ld_b_n8, ld_c_n8, ld_d_n8, ld_e_n8, ld_h_n8, ld_l_n8

ops_base = [None] * 0x100

ops_base[0x00] = {"mnemonic": "NOP", "handler": nop, "length": 1, "cycles": 4, }

# LD r8, n8
ops_base[0x3E] = {"mnemonic": "LD A,n8", "handler": ld_a_n8, "length": 2, "cycles": 8,}
ops_base[0x06] = {"mnemonic": "LD B,n8", "handler": ld_b_n8, "length": 2, "cycles": 8,}
ops_base[0x0E] = {"mnemonic": "LD C,n8", "handler": ld_c_n8, "length": 2, "cycles": 8,}
ops_base[0x16] = {"mnemonic": "LD D,n8", "handler": ld_d_n8, "length": 2, "cycles": 8,}
ops_base[0x1E] = {"mnemonic": "LD E,n8", "handler": ld_e_n8, "length": 2, "cycles": 8,}
ops_base[0x26] = {"mnemonic": "LD H,n8", "handler": ld_h_n8, "length": 2, "cycles": 8,}
ops_base[0x2E] = {"mnemonic": "LD L,n8", "handler": ld_l_n8, "length": 2, "cycles": 8,}

