import pytest
from bus import Bus
from cpu import CPU
from opcodes import ops_base

# (opcode, name, mode, deltaHL)
CASES = [
    (0x22, "(HL+),A", "store", +1),  # LD (HL+),A
    (0x2A, "A,(HL+)", "load",  +1),  # LD A,(HL+)
    (0x32, "(HL-),A", "store", -1),  # LD (HL-),A
    (0x3A, "A,(HL-)", "load",  -1),  # LD A,(HL-)
]

@pytest.mark.parametrize("opcode,name,mode,delta", CASES)
def test_ld_hl_auto(opcode, name, mode, delta):
    entry = ops_base[opcode] if len(ops_base) > opcode else None
    if not entry or not entry.get("handler"):
        pytest.skip(f"{hex(opcode)} {name} not implemented")

    b = Bus()
    c = CPU(b)

    start_hl = 0xC123
    c.set_HL(start_hl)

    F_before = c.F
    pc_before = c.PC

    if mode == "store":
        c.A = 0x9A
        b.write8(start_hl, 0x00)   # prefill
    else:  # load
        c.A = 0x00
        b.write8(start_hl, 0x5E)

    # place opcode and execute
    b.write8(0x0000, opcode)
    c.step()

    # effects
    if mode == "store":
        assert b.read8(start_hl) == 0x9A, f"{name}: mem[{start_hl:#06x}] wrong"
        assert c.A == 0x9A
    else:
        assert c.A == 0x5E, f"{name}: A loaded wrong"
        assert b.read8(start_hl) == 0x5E

    expected_hl = (start_hl + delta) & 0xFFFF
    assert c.get_HL() == expected_hl, f"{name}: HL should become {expected_hl:#06x}"

    # timing & flags
    assert c.PC == ((pc_before + 1) & 0xFFFF), f"{name}: PC should advance by 1"
    assert c.last_instr_cycles == 8, f"{name}: should take 8 cycles"
    assert c.F == F_before, f"{name}: flags must be unaffected"


# Optional: quick wraparound sanity (HL increments from FFFF to 0000, or decrements from 0000 to FFFF)
@pytest.mark.parametrize("opcode,mode,delta,start_hl", [
    (0x22, "store", +1, 0xFFFF),  # (HL+),A wrap -> 0x0000
    (0x32, "store", -1, 0x0000),  # (HL-),A wrap -> 0xFFFF
])
def test_ld_hl_auto_wrap(opcode, mode, delta, start_hl):
    entry = ops_base[opcode] if len(ops_base) > opcode else None
    if not entry or not entry.get("handler"):
        pytest.skip(f"{hex(opcode)} wrap test not implemented")

    b = Bus()
    c = CPU(b)

    c.set_HL(start_hl)
    c.A = 0x77
    b.write8(start_hl, 0x00)

    b.write8(0x0000, opcode)
    c.step()

    assert b.read8(start_hl) == 0x77
    expected_hl = (start_hl + delta) & 0xFFFF
    assert c.get_HL() == expected_hl
    assert c.last_instr_cycles == 8
