import pytest
from bus import Bus
from cpu import CPU
from opcodes import ops_base

# (opcode, human_name, getter_attr) — SP uses cpu.SP directly
CASES = [
    (0x01, "BC", "get_BC"),  # LD BC, n16
    (0x11, "DE", "get_DE"),  # LD DE, n16
    (0x21, "HL", "get_HL"),  # LD HL, n16
    (0x31, "SP", None),      # LD SP, n16
]

# A couple of representative 16-bit values to try (little-endian in memory)
IMMEDIATES = [0x1234, 0xBEEF]

@pytest.mark.parametrize("opcode,name,getter", CASES)
@pytest.mark.parametrize("imm16", IMMEDIATES)
def test_ld_r16_n16(opcode, name, getter, imm16):
    entry = ops_base[opcode]
    if not entry or not entry.get("handler"):
        pytest.skip(f"{hex(opcode)} (LD {name}, n16) not implemented")

    b = Bus()
    c = CPU(b)

    # Place opcode and little-endian immediate at PC=0
    lo = imm16 & 0xFF
    hi = (imm16 >> 8) & 0xFF
    b.write8(0x0000, opcode)
    b.write8(0x0001, lo)
    b.write8(0x0002, hi)

    F_before = c.F
    pc_before = c.PC

    c.step()

    # Read the destination pair
    if getter is None:  # SP
        got = c.SP & 0xFFFF
    else:
        got = getattr(c, getter)() & 0xFFFF

    assert got == (imm16 & 0xFFFF), \
        f"LD {name},n16 loaded {got:#06x}, expected {imm16:#06x}"

    # PC should advance by 3 (opcode + 2 bytes)
    assert c.PC == ((pc_before + 3) & 0xFFFF), \
        f"PC advanced to {c.PC:#06x}, expected {(pc_before + 3) & 0xFFFF:#06x}"

    # Cycles should be 12
    assert c.last_instr_cycles == 12, \
        f"Cycles {c.last_instr_cycles}, expected 12"

    # Flags unaffected
    assert c.F == F_before, "F should not change for LD r16,n16"
