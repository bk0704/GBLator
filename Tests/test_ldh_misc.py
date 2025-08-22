import pytest
from bus import Bus
from cpu import CPU
from opcodes import ops_base

# ---- Test LD (n16),A and LD A,(n16) ----

@pytest.mark.parametrize("opcode,name,is_store", [
    (0xEA, "LD (n16),A", True),   # store A -> [a16]
    (0xFA, "LD A,(n16)", False),  # load  A <- [a16]
])
@pytest.mark.parametrize("addr,val", [
    (0xC000, 0x00),
    (0xD123, 0xFF),
])
def test_ld_abs_n16(opcode, name, is_store, addr, val):
    entry = ops_base[opcode] if len(ops_base) > opcode else None
    if not entry or not entry.get("handler"):
        pytest.skip(f"{name} not implemented")

    b = Bus()
    c = CPU(b)

    # Place opcode + 16-bit little-endian address at PC=0
    b.write8(0x0000, opcode)
    b.write8(0x0001, addr & 0xFF)        # low
    b.write8(0x0002, (addr >> 8) & 0xFF) # high

    F_before = c.F
    pc_before = c.PC

    if is_store:
        c.A = val
        b.write8(addr, 0x00)  # prefill so we can see the change
    else:
        c.A = 0x00
        b.write8(addr, val)

    c.step()

    if is_store:
        assert b.read8(addr) == val, f"{name}: mem[{addr:#06x}] wrong"
        assert c.A == val, f"{name}: A must remain unchanged"
    else:
        assert c.A == val, f"{name}: A loaded wrong"
        assert b.read8(addr) == val, f"{name}: memory must remain unchanged"

    # PC advance: opcode + 2-byte immediate
    assert c.PC == ((pc_before + 3) & 0xFFFF), f"{name}: PC should advance by 3"
    # Cycles: 16
    assert c.last_instr_cycles == 16, f"{name}: should take 16 cycles"
    # Flags unaffected
    assert c.F == F_before, f"{name}: flags must be unaffected"


# ---- Test LDH (n8),A and LDH A,(n8) ----

@pytest.mark.parametrize("opcode,name,is_store", [
    (0xE0, "LDH (n8),A", True),   # store A -> [0xFF00 + n8]
    (0xF0, "LDH A,(n8)", False),  # load  A <- [0xFF00 + n8]
])
@pytest.mark.parametrize("offset,val", [
    (0x00, 0x12),
    (0x80, 0xA5),
    (0xFF, 0x7E),
])
def test_ldh_n8(opcode, name, is_store, offset, val):
    entry = ops_base[opcode] if len(ops_base) > opcode else None
    if not entry or not entry.get("handler"):
        pytest.skip(f"{name} not implemented")

    b = Bus()
    c = CPU(b)

    addr = 0xFF00 + (offset & 0xFF)

    # Place opcode + 8-bit immediate
    b.write8(0x0000, opcode)
    b.write8(0x0001, offset & 0xFF)

    F_before = c.F
    pc_before = c.PC

    if is_store:
        c.A = val
        b.write8(addr, 0x00)
    else:
        c.A = 0x00
        b.write8(addr, val)

    c.step()

    if is_store:
        assert b.read8(addr) == val, f"{name}: mem[{addr:#06x}] wrong"
        assert c.A == val
    else:
        assert c.A == val, f"{name}: A loaded wrong"
        assert b.read8(addr) == val

    # PC advance: opcode + 1-byte immediate
    assert c.PC == ((pc_before + 2) & 0xFFFF), f"{name}: PC should advance by 2"
    # Cycles: 12
    assert c.last_instr_cycles == 12, f"{name}: should take 12 cycles"
    # Flags unaffected
    assert c.F == F_before, f"{name}: flags must be unaffected"


# ---- Test LDH (C),A and LDH A,(C) ----

@pytest.mark.parametrize("opcode,name,is_store", [
    (0xE2, "LDH (C),A", True),   # store A -> [0xFF00 + C]
    (0xF2, "LDH A,(C)", False),  # load  A <- [0xFF00 + C]
])
@pytest.mark.parametrize("C,val", [
    (0x00, 0x34),
    (0x7F, 0xC3),
    (0xFF, 0x9A),
])
def test_ldh_c(opcode, name, is_store, C, val):
    entry = ops_base[opcode] if len(ops_base) > opcode else None
    if not entry or not entry.get("handler"):
        pytest.skip(f"{name} not implemented")

    b = Bus()
    c = CPU(b)

    c.C = C & 0xFF
    addr = 0xFF00 + c.C

    b.write8(0x0000, opcode)
    F_before = c.F
    pc_before = c.PC

    if is_store:
        c.A = val
        b.write8(addr, 0x00)
    else:
        c.A = 0x00
        b.write8(addr, val)

    c.step()

    if is_store:
        assert b.read8(addr) == val, f"{name}: mem[{addr:#06x}] wrong"
        assert c.A == val
    else:
        assert c.A == val, f"{name}: A loaded wrong"
        assert b.read8(addr) == val

    # PC advance: opcode only
    assert c.PC == ((pc_before + 1) & 0xFFFF), f"{name}: PC should advance by 1"
    # Cycles: 8
    assert c.last_instr_cycles == 8, f"{name}: should take 8 cycles"
    # Flags unaffected
    assert c.F == F_before, f"{name}: flags must be unaffected"
