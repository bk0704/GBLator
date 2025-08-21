import pytest
from bus import Bus
from cpu import CPU
from opcodes import ops_base

IMMEDIATES = [0x00, 0x7F, 0x80, 0xAB, 0xFF]

@pytest.mark.parametrize("imm8", IMMEDIATES)
def test_ld_hl_n8(imm8):
    # Skip cleanly if opcode not wired yet
    entry = ops_base[0x36] if len(ops_base) > 0x36 else None
    if not entry or not entry.get("handler"):
        pytest.skip("0x36 (LD [HL], n8) not implemented")

    b = Bus()
    c = CPU(b)

    # Set HL to a known address; prefill memory and flags
    hl_addr = 0x1234
    c.set_HL(hl_addr)
    b.write8(hl_addr, 0x00)
    F_before = c.F

    # Put opcode + immediate at PC=0 and execute
    b.write8(0x0000, 0x36)      # LD [HL], n8
    b.write8(0x0001, imm8)      # immediate byte

    pc_before = c.PC
    c.step()

    # Assertions
    assert b.read8(hl_addr) == imm8, \
        f"mem[{hl_addr:#06x}] = {b.read8(hl_addr):#04x}, expected {imm8:#04x}"
    assert c.PC == ((pc_before + 2) & 0xFFFF), "PC should advance by 2"
    assert c.last_instr_cycles == 12, "LD [HL],n8 should take 12 cycles"
    assert c.F == F_before, "Flags must be unaffected by LD [HL],n8"

