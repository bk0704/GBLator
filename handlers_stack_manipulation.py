# ADD HL, SP

def add_hl_sp(cpu):
    # Read operands
    hl = cpu.get_HL()
    sp = cpu.SP

    # Flag precompute (from original values)
    half_carry = ((hl & 0x0FFF) + (sp & 0x0FFF)) > 0x0FFF   # carry from bit 11
    carry      = (hl + sp) > 0xFFFF                         # carry from bit 15

    # Write result
    cpu.set_HL((hl + sp) & 0xFFFF)

    # Update flags (Z unchanged)
    cpu.set_flags(n=0, h=1 if half_carry else 0, c=1 if carry else 0)


# ADD SP, e8
def add_sp_e8(cpu):
    e8 = cpu.fetch_e8()       # signed 8-bit
    old_sp = cpu.SP

    result = (old_sp + e8) & 0xFFFF

    half_carry = ((old_sp & 0xF) + (e8 & 0xF)) > 0xF
    carry = ((old_sp & 0xFF) + (e8 & 0xFF)) > 0xFF

    cpu.SP = result
    cpu.set_flags(z=0, n=0, h=half_carry, c=carry)

# INC/DEC SP
def inc_sp(cpu):
    cpu.SP = (cpu.SP + 1) & 0xFFFF

def dec_sp(cpu):
    cpu.SP = (cpu.SP - 1) & 0xFFFF
