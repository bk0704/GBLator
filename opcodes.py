import handlers_ld
import handlers_stack_manipulation

ops_base = [None] * 0x100

ops_base[0x00] = {"mnemonic": "NOP", "handler": handlers_ld.nop, "length": 1, "cycles": 4, }

# LD r8, n8
ops_base[0x3E] = {"mnemonic": "LD A,n8", "handler": handlers_ld.ld_a_n8, "length": 2, "cycles": 8, }
ops_base[0x06] = {"mnemonic": "LD B,n8", "handler": handlers_ld.ld_b_n8, "length": 2, "cycles": 8, }
ops_base[0x0E] = {"mnemonic": "LD C,n8", "handler": handlers_ld.ld_c_n8, "length": 2, "cycles": 8, }
ops_base[0x16] = {"mnemonic": "LD D,n8", "handler": handlers_ld.ld_d_n8, "length": 2, "cycles": 8, }
ops_base[0x1E] = {"mnemonic": "LD E,n8", "handler": handlers_ld.ld_e_n8, "length": 2, "cycles": 8, }
ops_base[0x26] = {"mnemonic": "LD H,n8", "handler": handlers_ld.ld_h_n8, "length": 2, "cycles": 8, }
ops_base[0x2E] = {"mnemonic": "LD L,n8", "handler": handlers_ld.ld_l_n8, "length": 2, "cycles": 8, }

# LD B, r8
ops_base[0x40] = {"mnemonic": "LD B, B", "handler": handlers_ld.ld_b_b, "length": 1, "cycles": 4, }
ops_base[0x41] = {"mnemonic": "LD B, C", "handler": handlers_ld.ld_b_c, "length": 1, "cycles": 4, }
ops_base[0x42] = {"mnemonic": "LD B, D", "handler": handlers_ld.ld_b_d, "length": 1, "cycles": 4, }
ops_base[0x43] = {"mnemonic": "LD B, E", "handler": handlers_ld.ld_b_e, "length": 1, "cycles": 4, }
ops_base[0x44] = {"mnemonic": "LD B, H", "handler": handlers_ld.ld_b_h, "length": 1, "cycles": 4, }
ops_base[0x45] = {"mnemonic": "LD B, L", "handler": handlers_ld.ld_b_l, "length": 1, "cycles": 4, }
ops_base[0x47] = {"mnemonic": "LD B, A", "handler": handlers_ld.ld_b_a, "length": 1, "cycles": 4, }

# LD C, r8
ops_base[0x48] = {"mnemonic": "LD C, B", "handler": handlers_ld.ld_c_b, "length": 1, "cycles": 4, }
ops_base[0x49] = {"mnemonic": "LD C, C", "handler": handlers_ld.ld_c_c, "length": 1, "cycles": 4, }
ops_base[0x4A] = {"mnemonic": "LD B, D", "handler": handlers_ld.ld_c_d, "length": 1, "cycles": 4, }
ops_base[0x4B] = {"mnemonic": "LD B, E", "handler": handlers_ld.ld_c_e, "length": 1, "cycles": 4, }
ops_base[0x4C] = {"mnemonic": "LD B, H", "handler": handlers_ld.ld_c_h, "length": 1, "cycles": 4, }
ops_base[0x4D] = {"mnemonic": "LD B, L", "handler": handlers_ld.ld_c_l, "length": 1, "cycles": 4, }
ops_base[0x4F] = {"mnemonic": "LD B, A", "handler": handlers_ld.ld_c_a, "length": 1, "cycles": 4, }

# LD D, r8
ops_base[0x50] = {"mnemonic": "LD D, B", "handler": handlers_ld.ld_d_b, "length": 1, "cycles": 4, }
ops_base[0x51] = {"mnemonic": "LD D, C", "handler": handlers_ld.ld_d_c, "length": 1, "cycles": 4, }
ops_base[0x52] = {"mnemonic": "LD D, D", "handler": handlers_ld.ld_d_d, "length": 1, "cycles": 4, }
ops_base[0x53] = {"mnemonic": "LD D, E", "handler": handlers_ld.ld_d_e, "length": 1, "cycles": 4, }
ops_base[0x54] = {"mnemonic": "LD D, H", "handler": handlers_ld.ld_d_h, "length": 1, "cycles": 4, }
ops_base[0x55] = {"mnemonic": "LD D, L", "handler": handlers_ld.ld_d_l, "length": 1, "cycles": 4, }
ops_base[0x57] = {"mnemonic": "LD D, A", "handler": handlers_ld.ld_d_a, "length": 1, "cycles": 4, }

# LD E, r8
ops_base[0x58] = {"mnemonic": "LD E, B", "handler": handlers_ld.ld_e_b, "length": 1, "cycles": 4, }
ops_base[0x59] = {"mnemonic": "LD E, C", "handler": handlers_ld.ld_e_c, "length": 1, "cycles": 4, }
ops_base[0x5A] = {"mnemonic": "LD E, D", "handler": handlers_ld.ld_e_d, "length": 1, "cycles": 4, }
ops_base[0x5B] = {"mnemonic": "LD E, E", "handler": handlers_ld.ld_e_e, "length": 1, "cycles": 4, }
ops_base[0x5C] = {"mnemonic": "LD E, H", "handler": handlers_ld.ld_e_h, "length": 1, "cycles": 4, }
ops_base[0x5D] = {"mnemonic": "LD E, L", "handler": handlers_ld.ld_e_l, "length": 1, "cycles": 4, }
ops_base[0x5F] = {"mnemonic": "LD E, A", "handler": handlers_ld.ld_e_a, "length": 1, "cycles": 4, }

# LD H, r8
ops_base[0x60] = {"mnemonic": "LD H, B", "handler": handlers_ld.ld_h_b, "length": 1, "cycles": 4, }
ops_base[0x61] = {"mnemonic": "LD H, C", "handler": handlers_ld.ld_h_c, "length": 1, "cycles": 4, }
ops_base[0x62] = {"mnemonic": "LD H, D", "handler": handlers_ld.ld_h_d, "length": 1, "cycles": 4, }
ops_base[0x63] = {"mnemonic": "LD H, E", "handler": handlers_ld.ld_h_e, "length": 1, "cycles": 4, }
ops_base[0x64] = {"mnemonic": "LD H, H", "handler": handlers_ld.ld_h_h, "length": 1, "cycles": 4, }
ops_base[0x65] = {"mnemonic": "LD H, L", "handler": handlers_ld.ld_h_l, "length": 1, "cycles": 4, }
ops_base[0x67] = {"mnemonic": "LD H, A", "handler": handlers_ld.ld_h_a, "length": 1, "cycles": 4, }


# LD L, r8
ops_base[0x68] = {"mnemonic": "LD L, B", "handler": handlers_ld.ld_l_b, "length": 1, "cycles": 4, }
ops_base[0x69] = {"mnemonic": "LD L, C", "handler": handlers_ld.ld_l_c, "length": 1, "cycles": 4, }
ops_base[0x6A] = {"mnemonic": "LD L, D", "handler": handlers_ld.ld_l_d, "length": 1, "cycles": 4, }
ops_base[0x6B] = {"mnemonic": "LD L, E", "handler": handlers_ld.ld_l_e, "length": 1, "cycles": 4, }
ops_base[0x6C] = {"mnemonic": "LD L, H", "handler": handlers_ld.ld_l_h, "length": 1, "cycles": 4, }
ops_base[0x6D] = {"mnemonic": "LD L, L", "handler": handlers_ld.ld_l_l, "length": 1, "cycles": 4, }
ops_base[0x6F] = {"mnemonic": "LD L, A", "handler": handlers_ld.ld_l_a, "length": 1, "cycles": 4, }

# LD A, r8
ops_base[0x78] = {"mnemonic": "LD A, B", "handler": handlers_ld.ld_a_b, "length": 1, "cycles": 4, }
ops_base[0x79] = {"mnemonic": "LD A, C", "handler": handlers_ld.ld_a_c, "length": 1, "cycles": 4, }
ops_base[0x7A] = {"mnemonic": "LD A, D", "handler": handlers_ld.ld_a_d, "length": 1, "cycles": 4, }
ops_base[0x7B] = {"mnemonic": "LD A, E", "handler": handlers_ld.ld_a_e, "length": 1, "cycles": 4, }
ops_base[0x7C] = {"mnemonic": "LD A, H", "handler": handlers_ld.ld_a_h, "length": 1, "cycles": 4, }
ops_base[0x7D] = {"mnemonic": "LD A, L", "handler": handlers_ld.ld_a_l, "length": 1, "cycles": 4, }
ops_base[0x7F] = {"mnemonic": "LD A, A", "handler": handlers_ld.ld_a_a, "length": 1, "cycles": 4, }

# LD r8, [HL]
ops_base[0x46] = {"mnemonic": "LD B,[HL]", "handler": handlers_ld.ld_b_hl, "length": 1, "cycles": 8, }
ops_base[0x4E] = {"mnemonic": "LD C,[HL]", "handler": handlers_ld.ld_c_hl, "length": 1, "cycles": 8, }
ops_base[0x56] = {"mnemonic": "LD D,[HL]", "handler": handlers_ld.ld_d_hl, "length": 1, "cycles": 8, }
ops_base[0x5E] = {"mnemonic": "LD E,[HL]", "handler": handlers_ld.ld_e_hl, "length": 1, "cycles": 8, }
ops_base[0x66] = {"mnemonic": "LD H,[HL]", "handler": handlers_ld.ld_h_hl, "length": 1, "cycles": 8, }
ops_base[0x6E] = {"mnemonic": "LD L,[HL]", "handler": handlers_ld.ld_l_hl, "length": 1, "cycles": 8, }
ops_base[0x7E] = {"mnemonic": "LD A,[HL]", "handler": handlers_ld.ld_a_hl, "length": 1, "cycles": 8, }

# LD [HL], r8
ops_base[0x70] = {"mnemonic": "LD [HL],B", "handler": handlers_ld.ld_hl_b, "length": 1, "cycles": 8}
ops_base[0x71] = {"mnemonic": "LD [HL],C", "handler": handlers_ld.ld_hl_c, "length": 1, "cycles": 8}
ops_base[0x72] = {"mnemonic": "LD [HL],D", "handler": handlers_ld.ld_hl_d, "length": 1, "cycles": 8}
ops_base[0x73] = {"mnemonic": "LD [HL],E", "handler": handlers_ld.ld_hl_e, "length": 1, "cycles": 8}
ops_base[0x74] = {"mnemonic": "LD [HL],H", "handler": handlers_ld.ld_hl_h, "length": 1, "cycles": 8}
ops_base[0x75] = {"mnemonic": "LD [HL],L", "handler": handlers_ld.ld_hl_l, "length": 1, "cycles": 8}
ops_base[0x77] = {"mnemonic": "LD [HL],A", "handler": handlers_ld.ld_hl_a, "length": 1, "cycles": 8}

# LD r16, n16
ops_base[0x01] = {"mnemonic": "LD BC,n16", "handler": handlers_ld.ld_bc_n16, "length": 3, "cycles": 12, }
ops_base[0x11] = {"mnemonic": "LD DE,n16", "handler": handlers_ld.ld_de_n16, "length": 3, "cycles": 12, }
ops_base[0x21] = {"mnemonic": "LD HL,n16", "handler": handlers_ld.ld_hl_n16, "length": 3, "cycles": 12, }
ops_base[0x31] = {"mnemonic": "LD SP,n16", "handler": handlers_ld.ld_sp_n16, "length": 3, "cycles": 12, }

# LD [HL], n8
ops_base[0x36] = {"mnemonic": "LD [HL],n8", "handler": handlers_ld.ld_hl_n8, "length": 2, "cycles": 12, }

# LD [r16], A
ops_base[0x02] = {"mnemonic": "LD [BC],A", "handler": handlers_ld.ld_bc_a, "length": 1, "cycles": 8, }
ops_base[0x12] = {"mnemonic": "LD [DE],A", "handler": handlers_ld.ld_de_a, "length": 1, "cycles": 8, }

# LD A, [r16]
ops_base[0x0A] = {"mnemonic": "LD A,[BC]", "handler": handlers_ld.ld_a_bc, "length": 1, "cycles": 8, }
ops_base[0x1A] = {"mnemonic": "LD A,[DE]", "handler": handlers_ld.ld_a_de, "length": 1, "cycles": 8, }

# LD [HL+/-], A
ops_base[0x22] = {"mnemonic": "LD [HL+],A", "handler": handlers_ld.ld_hl_plus_a, "length": 1, "cycles": 8, }
ops_base[0x32] = {"mnemonic": "LD [HL-],A", "handler": handlers_ld.ld_hl_minus_a, "length": 1, "cycles": 8, }

# LD A, [HL+/-]
ops_base[0x2A] = {"mnemonic": "LD A,[HL+]", "handler": handlers_ld.ld_a_hl_plus, "length": 1, "cycles": 8, }
ops_base[0x3A] = {"mnemonic": "LD A,[HL-]", "handler": handlers_ld.ld_a_hl_minus, "length": 1, "cycles": 8, }

# LD n16, A
ops_base[0xFA] = {"mnemonic": "LD n16,A", "handler": handlers_ld.ld_a_n16, "length": 3, "cycles": 16, }

# LDH A, n16
ops_base[0xEA] = {"mnemonic": "LDH A,n16", "handler": handlers_ld.ld_n16_a, "length": 3, "cycles": 16, }

# LDH n16, A
ops_base[0xE0] = {"mnemonic": "LDH n16,A", "handler": handlers_ld.ldh_n16_a, "length": 2, "cycles": 12, }

# LDH A, n16
ops_base[0xF0] = {"mnemonic": "LDH A,n16", "handler": handlers_ld.ldh_a_n16, "length": 2, "cycles": 12, }

# LDH A, C
ops_base[0xF2] = {"mnemonic": "LDH A,C", "handler": handlers_ld.ldh_a_c, "length": 1, "cycles": 8, }

# LDH C, A
ops_base[0xE2] = {"mnemonic": "LDH C,A", "handler": handlers_ld.ldh_c_a, "length": 1, "cycles": 8, }

# ADD HL, SP
ops_base[0x39] = {"mnemonic": "ADD HL, SP", "handler": handlers_stack_manipulation.add_hl_sp, "length": 1, "cycles": 8}

# ADD SP, e8
ops_base[0xE8] = {"mnemonic": "ADD SP, e8", "handler": handlers_stack_manipulation.add_sp_e8, "length": 2, "cycles": 16}



