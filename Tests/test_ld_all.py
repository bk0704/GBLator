import pytest
from bus import Bus
from cpu import CPU
from opcodes import ops_base

# --------------------------
# Helpers
# --------------------------

def has_op(opc):
    return (len(ops_base) > opc) and ops_base[opc] and ops_base[opc].get("handler")

def seed_rom(bus, *bytes_):
    for i, b in enumerate(bytes_):
        bus.write8(i, b & 0xFF)

# --------------------------
# LD r8, n8  (A,B,C,D,E,H,L)
# --------------------------

@pytest.mark.parametrize("opc,reg", [
    (0x3E, "A"), (0x06, "B"), (0x0E, "C"),
    (0x16, "D"), (0x1E, "E"), (0x26, "H"),
    (0x2E, "L"),
])
@pytest.mark.parametrize("imm", [0x00, 0x42, 0x7F, 0x80, 0xFF])
def test_ld_r8_n8(opc, reg, imm):
    if not has_op(opc): pytest.skip(f"{hex(opc)} LD {reg},n8 not implemented")
    b, c = Bus(), CPU(Bus())
    c = CPU(b)
    seed_rom(b, opc, imm)
    F_before, pc_before = c.F, c.PC
    c.step()
    assert getattr(c, reg) == imm
    assert c.PC == ((pc_before + 2) & 0xFFFF)
    assert c.last_instr_cycles == 8
    assert c.F == F_before

# --------------------------
# LD r16, n16  (BC,DE,HL,SP)
# --------------------------

@pytest.mark.parametrize("opc,name,getter", [
    (0x01, "BC", "get_BC"),
    (0x11, "DE", "get_DE"),
    (0x21, "HL", "get_HL"),
    (0x31, "SP", None),
])
@pytest.mark.parametrize("val", [0x0000, 0x1234, 0xBEEF, 0xFFFF])
def test_ld_r16_n16(opc, name, getter, val):
    if not has_op(opc): pytest.skip(f"{hex(opc)} LD {name},n16 not implemented")
    b, c = Bus(), CPU(Bus())
    c = CPU(b)
    lo, hi = val & 0xFF, (val >> 8) & 0xFF
    seed_rom(b, opc, lo, hi)
    F_before, pc_before = c.F, c.PC
    c.step()
    got = c.SP if getter is None else getattr(c, getter)()
    assert (got & 0xFFFF) == val & 0xFFFF
    assert c.PC == ((pc_before + 3) & 0xFFFF)
    assert c.last_instr_cycles == 12
    assert c.F == F_before

# --------------------------
# LD r8, [HL]
# --------------------------

@pytest.mark.parametrize("opc,reg", [
    (0x46, "B"), (0x4E, "C"), (0x56, "D"),
    (0x5E, "E"), (0x66, "H"), (0x6E, "L"),
    (0x7E, "A"),
])
def test_ld_r8_from_hl(opc, reg):
    if not has_op(opc): pytest.skip(f"{hex(opc)} LD {reg},[HL] not implemented")
    b, c = Bus(), CPU(Bus())
    c = CPU(b)
    hl, val = 0xC123, 0xAB
    c.set_HL(hl)
    b.write8(hl, val)
    seed_rom(b, opc)
    pc_before, F_before = c.PC, c.F
    c.step()
    assert getattr(c, reg) == val
    assert c.PC == ((pc_before + 1) & 0xFFFF)
    assert c.last_instr_cycles == 8
    assert c.F == F_before

# --------------------------
# LD [HL], r8
# --------------------------

@pytest.mark.parametrize("opc,reg", [
    (0x70, "B"), (0x71, "C"), (0x72, "D"),
    (0x73, "E"), (0x74, "H"), (0x75, "L"),
    (0x77, "A"),
])
def test_ld_hl_from_r8(opc, reg):
    if not has_op(opc): pytest.skip(f"{hex(opc)} LD [HL],{reg} not implemented")
    b, c = Bus(), CPU(Bus())
    c = CPU(b)

    # Seed HL first, then seed the source register.
    # NOTE: If reg is H or L, this will CHANGE HL.
    c.set_HL(0xC124)
    val = 0x9A
    setattr(c, reg, val)

    # Use the LIVE HL after setting the source register.
    hl_addr = c.get_HL()

    # Prefill memory at the actual target address so we can see the change.
    b.write8(hl_addr, 0x00)

    seed_rom(b, opc)
    pc_before, F_before = c.PC, c.F
    c.step()

    # Assert the write happened at the correct (possibly changed) address.
    assert b.read8(hl_addr) == val
    assert getattr(c, reg) == val
    assert c.PC == ((pc_before + 1) & 0xFFFF)
    assert c.last_instr_cycles == 8
    assert c.F == F_before

# --------------------------
# LD [HL], n8
# --------------------------

@pytest.mark.parametrize("imm", [0x00, 0x7E, 0xFF])
def test_ld_hl_n8(imm):
    if not has_op(0x36): pytest.skip("0x36 LD [HL],n8 not implemented")
    b, c = Bus(), CPU(Bus())
    c = CPU(b)
    hl = 0xC200
    c.set_HL(hl)
    b.write8(hl, 0x00)
    seed_rom(b, 0x36, imm)
    pc_before, F_before = c.PC, c.F
    c.step()
    assert b.read8(hl) == imm
    assert c.PC == ((pc_before + 2) & 0xFFFF)
    assert c.last_instr_cycles == 12
    assert c.F == F_before

# --------------------------
# LD [r16], A   and   LD A, [r16]   (BC/DE)
# --------------------------

@pytest.mark.parametrize("store_opc,load_opc,getter_name", [
    (0x02, 0x0A, "get_BC"),
    (0x12, 0x1A, "get_DE"),
])
def test_ld_r16_ptr(store_opc, load_opc, getter_name):
    # store: (r16),A
    if has_op(store_opc):
        b, c = Bus(), CPU(Bus())
        c = CPU(b)
        addr, val = 0xC345, 0x77
        getattr(c, f"set_{getter_name.split('_')[1]}")(addr)  # set_BC or set_DE
        c.A = val
        b.write8(addr, 0x00)
        seed_rom(b, store_opc)
        pc_before, F_before = c.PC, c.F
        c.step()
        assert b.read8(addr) == val
        assert c.PC == ((pc_before + 1) & 0xFFFF)
        assert c.last_instr_cycles == 8
        assert c.F == F_before
    else:
        pytest.skip(f"{hex(store_opc)} not implemented")

    # load: A,(r16)
    if has_op(load_opc):
        b, c = Bus(), CPU(Bus())
        c = CPU(b)
        addr, val = 0xC456, 0x5E
        getattr(c, f"set_{getter_name.split('_')[1]}")(addr)
        b.write8(addr, val)
        c.A = 0x00
        seed_rom(b, load_opc)
        pc_before, F_before = c.PC, c.F
        c.step()
        assert c.A == val
        assert b.read8(addr) == val
        assert c.PC == ((pc_before + 1) & 0xFFFF)
        assert c.last_instr_cycles == 8
        assert c.F == F_before
    else:
        pytest.skip(f"{hex(load_opc)} not implemented")

# --------------------------
# LD [n16], A   and   LD A, [n16]
# --------------------------

@pytest.mark.parametrize("opc,name,is_store", [
    (0xEA, "LD (n16),A", True),
    (0xFA, "LD A,(n16)", False),
])
@pytest.mark.parametrize("addr,val", [(0xC000, 0x00), (0xD123, 0xFF)])
def test_ld_abs_n16(opc, name, is_store, addr, val):
    if not has_op(opc): pytest.skip(f"{name} not implemented")
    b, c = Bus(), CPU(Bus())
    c = CPU(b)
    seed_rom(b, opc, addr & 0xFF, (addr >> 8) & 0xFF)
    F_before, pc_before = c.F, c.PC
    if is_store:
        c.A = val
        b.write8(addr, 0x00)
    else:
        c.A = 0x00
        b.write8(addr, val)
    c.step()
    if is_store:
        assert b.read8(addr) == val
        assert c.A == val
    else:
        assert c.A == val
        assert b.read8(addr) == val
    assert c.PC == ((pc_before + 3) & 0xFFFF)
    assert c.last_instr_cycles == 16
    assert c.F == F_before

# --------------------------
# LDH [n8], A   and   LDH A, [n8]
# --------------------------

@pytest.mark.parametrize("opc,name,is_store", [
    (0xE0, "LDH (n8),A", True),
    (0xF0, "LDH A,(n8)", False),
])
@pytest.mark.parametrize("off,val", [(0x00, 0x12), (0x80, 0xA5), (0xFF, 0x7E)])
def test_ldh_n8(opc, name, is_store, off, val):
    if not has_op(opc): pytest.skip(f"{name} not implemented")
    b, c = Bus(), CPU(Bus())
    c = CPU(b)
    addr = 0xFF00 + (off & 0xFF)
    seed_rom(b, opc, off & 0xFF)
    F_before, pc_before = c.F, c.PC
    if is_store:
        c.A = val
        b.write8(addr, 0x00)
    else:
        c.A = 0x00
        b.write8(addr, val)
    c.step()
    if is_store:
        assert b.read8(addr) == val
        assert c.A == val
    else:
        assert c.A == val
        assert b.read8(addr) == val
    assert c.PC == ((pc_before + 2) & 0xFFFF)
    assert c.last_instr_cycles == 12
    assert c.F == F_before

# --------------------------
# LDH [C], A   and   LDH A, [C]
# --------------------------

@pytest.mark.parametrize("opc,name,is_store", [
    (0xE2, "LDH (C),A", True),
    (0xF2, "LDH A,(C)", False),
])
@pytest.mark.parametrize("C,val", [(0x00, 0x34), (0x7F, 0xC3), (0xFF, 0x9A)])
def test_ldh_c(opc, name, is_store, C, val):
    if not has_op(opc): pytest.skip(f"{name} not implemented")
    b, c = Bus(), CPU(Bus())
    c = CPU(b)
    c.C = C & 0xFF
    addr = 0xFF00 + c.C
    seed_rom(b, opc)
    F_before, pc_before = c.F, c.PC
    if is_store:
        c.A = val
        b.write8(addr, 0x00)
    else:
        c.A = 0x00
        b.write8(addr, val)
    c.step()
    if is_store:
        assert b.read8(addr) == val
        assert c.A == val
    else:
        assert c.A == val
        assert b.read8(addr) == val
    assert c.PC == ((pc_before + 1) & 0xFFFF)
    assert c.last_instr_cycles == 8
    assert c.F == F_before

# --------------------------
# HL auto-inc/dec variants
# --------------------------

@pytest.mark.parametrize("opc,name,mode,delta", [
    (0x22, "LD (HL+),A", "store", +1),
    (0x2A, "LD A,(HL+)", "load",  +1),
    (0x32, "LD (HL-),A", "store", -1),
    (0x3A, "LD A,(HL-)", "load",  -1),
])
def test_ld_hl_auto(opc, name, mode, delta):
    if not has_op(opc): pytest.skip(f"{name} not implemented")
    b, c = Bus(), CPU(Bus())
    c = CPU(b)
    start_hl = 0xC500
    c.set_HL(start_hl)
    F_before, pc_before = c.F, c.PC
    if mode == "store":
        c.A = 0x77
        b.write8(start_hl, 0x00)
    else:
        c.A = 0x00
        b.write8(start_hl, 0x5E)
    seed_rom(b, opc)
    c.step()
    if mode == "store":
        assert b.read8(start_hl) == 0x77
        assert c.A == 0x77
    else:
        assert c.A == 0x5E
        assert b.read8(start_hl) == 0x5E
    expected_hl = (start_hl + delta) & 0xFFFF
    assert c.get_HL() == expected_hl
    assert c.PC == ((pc_before + 1) & 0xFFFF)
    assert c.last_instr_cycles == 8
    assert c.F == F_before
