import pytest
from cpu import CPU
from bus import Bus
from opcodes import ops_base

def setup_cpu_with_hl(val):
    bus = Bus()
    cpu = CPU(bus)
    cpu.set_HL(0x1234)     # HL points to 0x1234
    bus.mem[0x1234] = val  # memory at HL = val
    return cpu

def test_ld_r8_from_hl():
    # LD B, [HL]
    cpu = setup_cpu_with_hl(0x42)
    cpu.bus.mem[0x0000] = 0x46  # opcode LD B,[HL]
    cpu.step()
    assert cpu.B == 0x42, f"B after LD B,[HL]: {cpu.B:#04x}"

    # LD C, [HL]
    cpu = setup_cpu_with_hl(0x43)
    cpu.bus.mem[0x0000] = 0x4E  # opcode LD C,[HL]
    cpu.step()
    assert cpu.C == 0x43, f"C after LD C,[HL]: {cpu.C:#04x}"

    # LD D, [HL]
    cpu = setup_cpu_with_hl(0x44)
    cpu.bus.mem[0x0000] = 0x56  # opcode LD D,[HL]
    cpu.step()
    assert cpu.D == 0x44, f"D after LD D,[HL]: {cpu.D:#04x}"

    # LD E, [HL]
    cpu = setup_cpu_with_hl(0x45)
    cpu.bus.mem[0x0000] = 0x5E  # opcode LD E,[HL]
    cpu.step()
    assert cpu.E == 0x45, f"E after LD E,[HL]: {cpu.E:#04x}"

    # LD H, [HL]
    cpu = setup_cpu_with_hl(0x46)
    cpu.bus.mem[0x0000] = 0x66  # opcode LD H,[HL]
    cpu.step()
    assert cpu.H == 0x46, f"H after LD H,[HL]: {cpu.H:#04x}"

    # LD L, [HL]
    cpu = setup_cpu_with_hl(0x47)
    cpu.bus.mem[0x0000] = 0x6E  # opcode LD L,[HL]
    cpu.step()
    assert cpu.L == 0x47, f"L after LD L,[HL]: {cpu.L:#04x}"

    # LD A, [HL]
    cpu = setup_cpu_with_hl(0x48)
    cpu.bus.mem[0x0000] = 0x7E  # opcode LD A,[HL]
    cpu.step()
    assert cpu.A == 0x48, f"A after LD A,[HL]: {cpu.A:#04x}"
