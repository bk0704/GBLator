from handlers_ld import (nop, ld_a_n8, ld_b_n8, ld_c_n8, ld_d_n8, ld_e_n8, ld_h_n8,
                         ld_l_n8, ld_b_b, ld_b_c, ld_b_d, ld_b_e, ld_b_h, ld_b_l)

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

#LD B, r8
ops_base[0x40] = {"mnemonic": "LD B, B", "handler": ld_b_b, "length": 1, "cycles": 4,}
ops_base[0x41] = {"mnemonic": "LD B, C", "handler": ld_b_c, "length": 1, "cycles": 4,}
ops_base[0x42] = {"mnemonic": "LD B, D", "handler": ld_b_d, "length": 1, "cycles": 4,}
ops_base[0x43] = {"mnemonic": "LD B, E", "handler": ld_b_e, "length": 1, "cycles": 4,}
ops_base[0x44] = {"mnemonic": "LD B, H", "handler": ld_b_h, "length": 1, "cycles": 4,}
ops_base[0x45] = {"mnemonic": "LD B, L", "handler": ld_b_l, "length": 1, "cycles": 4,}


