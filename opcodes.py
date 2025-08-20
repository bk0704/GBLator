from handlers_ld import (nop, ld_a_n8, ld_b_n8, ld_c_n8, ld_d_n8, ld_e_n8, ld_h_n8,
                         ld_l_n8, ld_b_b, ld_b_c, ld_b_d, ld_b_e, ld_b_h, ld_b_l, ld_b_a,
                         ld_c_b, ld_c_c, ld_c_d, ld_c_e, ld_c_h, ld_c_l, ld_c_a,
                         ld_d_b, ld_d_c, ld_d_d, ld_d_e, ld_d_h, ld_d_l, ld_d_a,
                         ld_e_b, ld_e_c, ld_e_d, ld_e_e, ld_e_h, ld_e_l, ld_e_a,
                         ld_h_b, ld_h_c, ld_h_d, ld_h_e, ld_h_h, ld_h_l, ld_h_a,
                         ld_l_b, ld_l_c, ld_l_d, ld_l_e, ld_l_h, ld_l_l, ld_l_a,)

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

# LD B, r8
ops_base[0x40] = {"mnemonic": "LD B, B", "handler": ld_b_b, "length": 1, "cycles": 4,}
ops_base[0x41] = {"mnemonic": "LD B, C", "handler": ld_b_c, "length": 1, "cycles": 4,}
ops_base[0x42] = {"mnemonic": "LD B, D", "handler": ld_b_d, "length": 1, "cycles": 4,}
ops_base[0x43] = {"mnemonic": "LD B, E", "handler": ld_b_e, "length": 1, "cycles": 4,}
ops_base[0x44] = {"mnemonic": "LD B, H", "handler": ld_b_h, "length": 1, "cycles": 4,}
ops_base[0x45] = {"mnemonic": "LD B, L", "handler": ld_b_l, "length": 1, "cycles": 4,}
ops_base[0x47] = {"mnemonic": "LD B, A", "handler": ld_b_a, "length": 1, "cycles": 4,}

# LD C, r8
ops_base[0x48] = {"mnemonic": "LD C, B", "handler": ld_c_b, "length": 1, "cycles": 4,}
ops_base[0x49] = {"mnemonic": "LD C, C", "handler": ld_c_c, "length": 1, "cycles": 4,}
ops_base[0x4A] = {"mnemonic": "LD B, D", "handler": ld_c_d, "length": 1, "cycles": 4,}
ops_base[0x4B] = {"mnemonic": "LD B, E", "handler": ld_c_e, "length": 1, "cycles": 4,}
ops_base[0x4C] = {"mnemonic": "LD B, H", "handler": ld_c_h, "length": 1, "cycles": 4,}
ops_base[0x4D] = {"mnemonic": "LD B, L", "handler": ld_c_l, "length": 1, "cycles": 4,}
ops_base[0x4F] = {"mnemonic": "LD B, A", "handler": ld_c_a, "length": 1, "cycles": 4,}

# LD D, r8
ops_base[0x50] = {"mnemonic": "LD D, B", "handler": ld_d_b, "length": 1, "cycles": 4,}
ops_base[0x51] = {"mnemonic": "LD D, C", "handler": ld_d_c, "length": 1, "cycles": 4,}
ops_base[0x52] = {"mnemonic": "LD D, D", "handler": ld_d_d, "length": 1, "cycles": 4,}
ops_base[0x53] = {"mnemonic": "LD D, E", "handler": ld_d_e, "length": 1, "cycles": 4,}
ops_base[0x54] = {"mnemonic": "LD D, H", "handler": ld_d_h, "length": 1, "cycles": 4,}
ops_base[0x55] = {"mnemonic": "LD D, L", "handler": ld_d_l, "length": 1, "cycles": 4,}
ops_base[0x57] = {"mnemonic": "LD D, A", "handler": ld_d_a, "length": 1, "cycles": 4,}

# LD E, r8
ops_base[0x58] = {"mnemonic": "LD E, B", "handler": ld_e_b, "length": 1, "cycles": 4,}
ops_base[0x59] = {"mnemonic": "LD E, C", "handler": ld_e_c, "length": 1, "cycles": 4,}
ops_base[0x5A] = {"mnemonic": "LD E, D", "handler": ld_e_d, "length": 1, "cycles": 4,}
ops_base[0x5B] = {"mnemonic": "LD E, E", "handler": ld_e_e, "length": 1, "cycles": 4,}
ops_base[0x5C] = {"mnemonic": "LD E, H", "handler": ld_e_h, "length": 1, "cycles": 4,}
ops_base[0x5D] = {"mnemonic": "LD E, L", "handler": ld_e_l, "length": 1, "cycles": 4,}
ops_base[0x5F] = {"mnemonic": "LD E, A", "handler": ld_e_a, "length": 1, "cycles": 4,}

# LD H, r8
ops_base[0x60] = {"mnemonic": "LD H, B", "handler": ld_h_b, "length": 1, "cycles": 4,}
ops_base[0x61] = {"mnemonic": "LD H, C", "handler": ld_h_c, "length": 1, "cycles": 4,}
ops_base[0x62] = {"mnemonic": "LD H, D", "handler": ld_h_d, "length": 1, "cycles": 4,}
ops_base[0x63] = {"mnemonic": "LD H, E", "handler": ld_h_e, "length": 1, "cycles": 4,}
ops_base[0x64] = {"mnemonic": "LD H, H", "handler": ld_h_h, "length": 1, "cycles": 4,}
ops_base[0x65] = {"mnemonic": "LD H, L", "handler": ld_h_l, "length": 1, "cycles": 4,}
ops_base[0x67] = {"mnemonic": "LD H, A", "handler": ld_h_a, "length": 1, "cycles": 4,}


# LD L, r8
ops_base[0x68] = {"mnemonic": "LD L, B", "handler": ld_l_b, "length": 1, "cycles": 4,}
ops_base[0x69] = {"mnemonic": "LD L, C", "handler": ld_l_c, "length": 1, "cycles": 4,}
ops_base[0x6A] = {"mnemonic": "LD L, D", "handler": ld_l_d, "length": 1, "cycles": 4,}
ops_base[0x6B] = {"mnemonic": "LD L, E", "handler": ld_l_e, "length": 1, "cycles": 4,}
ops_base[0x6C] = {"mnemonic": "LD L, H", "handler": ld_l_h, "length": 1, "cycles": 4,}
ops_base[0x6D] = {"mnemonic": "LD L, L", "handler": ld_l_l, "length": 1, "cycles": 4,}
ops_base[0x6F] = {"mnemonic": "LD L, A", "handler": ld_l_a, "length": 1, "cycles": 4,}