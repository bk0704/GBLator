import pytest
from bus import Bus
from cpu import CPU
from opcodes import ops_base

CASES = [
    (0x70, "B"),  # LD [HL],B
    (0x71, "C"),  # LD [HL],C
    (0x72, "D"),  # LD [HL],D
    (0x73, "E"),  # LD [HL],E
    (0x74, "H"),  # LD [HL],H
    (0x75, "L"),  # LD [HL],L
    (0x77, "A"),  # LD [HL],A
]

@pytest.mark.parametrize("opcode,src_attr", CASES)
def test_ld_hl_r8(opcode, src_attr):
    entry = ops_base[opcode]
    if not entry or not entry.get("handler"):
        pytest.skip(f"{hex(opcode)} (LD [HL],{src_attr}) not implemented")

    bus = Bus()
    cpu = CPU(bus)

    # Seed HL and source register
    cpu.set_HL(0x1234)
    setattr(cpu, src_attr, 0x9A)
    # IMPORTANT: for H/L cases, HL may have changed now. Use the live address:
    hl_addr = cpu.get_HL()

    # Pre-fill current [HL] so we can see the change
    bus.write8(hl_addr, 0x00)

    # Execute
    cpu.bus.mem[0x0000] = opcode
    pc_before = cpu.PC
    cpu.step()

    # Assert write at the actual HL
    assert bus.read8(hl_addr) == 0x9A
    assert cpu.PC == ((pc_before + 1) & 0xFFFF)
    assert cpu.last_instr_cycles == 8
    assert getattr(cpu, src_attr) == 0x9A









