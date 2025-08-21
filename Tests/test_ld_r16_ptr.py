import pytest
from bus import Bus
from cpu import CPU
from opcodes import ops_base

# (opcode, name, pair_getter) — pair_getter returns current 16-bit address from CPU
CASES = [
    (0x02, "(BC),A", "get_BC"),  # store A -> [BC]
    (0x0A, "A,(BC)", "get_BC"),  # load  [BC] -> A
    (0x12, "(DE),A", "get_DE"),  # store A -> [DE]
    (0x1A, "A,(DE)", "get_DE"),  # load  [DE] -> A
]

@pytest.mark.parametrize("opcode,name,pair_getter", CASES)
def test_ld_r16_pointer(opcode, name, pair_getter):
    entry = ops_base[opcode] if len(ops_base) > opcode else None
    if not entry or not entry.get("handler"):
        pytest.skip(f"{hex(opcode)} ({name}) not implemented")

    b = Bus()
    c = CPU(b)

    # Choose addresses & values
    addr = 0xC123
    A_seed = 0x9A
    mem_seed = 0x5E

    # Seed the target pair (BC/DE)
    getattr(c, f"set_{pair_getter.split('_')[1]}")(addr)  # set_BC or set_DE via getter name trick

    # Common: flags shouldn't change
    F_before = c.F

    # Place opcode at PC=0
    b.write8(0x0000, opcode)
    pc_before = c.PC

    if opcode in (0x02, 0x12):  # (BC|DE),A => store A into memory at pair
        c.A = A_seed
        b.write8(addr, 0x00)  # prefill to check change
        c.step()

        assert b.read8(addr) == A_seed, f"{name}: mem[{addr:#06x}] wrong"
        assert c.A == A_seed, f"{name}: A must remain unchanged"
    else:  # A,(BC|DE) => load memory at pair into A
        c.A = 0x00
        b.write8(addr, mem_seed)
        c.step()

        assert c.A == mem_seed, f"{name}: A loaded wrong"
        assert b.read8(addr) == mem_seed, f"{name}: memory must remain unchanged"

    # PC & timing
    assert c.PC == ((pc_before + 1) & 0xFFFF), f"{name}: PC should advance by 1"
    assert c.last_instr_cycles == 8, f"{name}: should take 8 cycles"
    assert c.F == F_before, f"{name}: flags must be unaffected"
