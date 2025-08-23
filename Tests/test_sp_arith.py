# Tests/test_sp_arith.py
import pytest

from cpu import CPU
from handlers_stack_manipulation import add_hl_sp, add_sp_e8, inc_sp, dec_sp


class FakeBus:
    def __init__(self, size=0x10000):
        self.mem = bytearray(size)

    def read8(self, addr):
        return self.mem[addr & 0xFFFF]

    def write8(self, addr, value):
        self.mem[addr & 0xFFFF] = value & 0xFF


@pytest.fixture
def cpu():
    return CPU(FakeBus())


# ---------- ADD HL, SP ----------
def _set_Z(cpu, val):  # only Z; others untouched
    cpu.set_flags(z=1 if val else 0)

def _flags(cpu):
    return cpu.get_flagZ(), cpu.get_flagN(), cpu.get_flagH(), cpu.get_flagC()

@pytest.mark.parametrize(
    "hl, sp, z_before, hl_expected, h_expected, c_expected",
    [
        (0x1234, 0x0001, 0, 0x1235, False, False),
        (0x1234, 0x0001, 1, 0x1235, False, False),
        (0x0FFF, 0x0001, 0, 0x1000, True,  False),  # half-carry only (bit11)
        (0xFFFF, 0x0001, 0, 0x0000, True,  True),   # wrap, sets H & C
        (0x8000, 0x8000, 0, 0x0000, False, True),   # carry without half-carry
        (0x08FF, 0x0101, 0, 0x0A00, False, False),  # boundary, no H/C
    ],
)
def test_add_hl_sp(cpu, hl, sp, z_before, hl_expected, h_expected, c_expected):
    cpu.set_HL(hl & 0xFFFF)
    cpu.SP = sp & 0xFFFF
    _set_Z(cpu, z_before)

    add_hl_sp(cpu)

    assert cpu.get_HL() == (hl_expected & 0xFFFF)
    Z, N, H, C = _flags(cpu)
    assert N == 0
    assert H == (1 if h_expected else 0)
    assert C == (1 if c_expected else 0)
    assert Z == (1 if z_before else 0)  # Z unchanged


# ---------- ADD SP, e8 ----------
def _preload_imm(cpu, imm_u8):
    cpu.bus.write8(cpu.PC, imm_u8 & 0xFF)

@pytest.mark.parametrize(
    "sp_start, imm_u8, sp_expected, h_expected, c_expected",
    [
        (0x1000, 0x01, 0x1001, False, False),  # +1
        (0x100F, 0x01, 0x1010, True,  False),  # +1 half-carry (nibble)
        (0x10FF, 0x01, 0x1100, True,  True),   # +1 byte carry & nibble H
        (0x0000, 0xFF, 0xFFFF, False, False),  # -1
        (0x0001, 0xFF, 0x0000, True,  True),   # -1: 0x01+0xFF = 0x100 => H,C
        (0xFF00, 0x80, 0xFE80, False, False),  # -128
    ],
)
def test_add_sp_e8(cpu, sp_start, imm_u8, sp_expected, h_expected, c_expected):
    cpu.SP = sp_start & 0xFFFF
    cpu.PC = 0x2000
    _preload_imm(cpu, imm_u8)

    # Seed flags so we can verify Z/N cleared and H/C set correctly
    cpu.set_flags(z=1, n=1, h=0, c=0)
    pc_before = cpu.PC

    add_sp_e8(cpu)

    assert cpu.SP == (sp_expected & 0xFFFF)
    assert cpu.PC == ((pc_before + 1) & 0xFFFF)  # immediate consumed

    Z, N, H, C = _flags(cpu)
    assert Z == 0
    assert N == 0
    assert H == (1 if h_expected else 0)
    assert C == (1 if c_expected else 0)


# ---------- INC SP / DEC SP ----------
def test_inc_sp_wrap_and_flags(cpu):
    cpu.SP = 0xFFFF
    # Seed flags to confirm no changes
    cpu.set_flags(z=1, n=0, h=1, c=0)

    inc_sp(cpu)

    assert cpu.SP == 0x0000
    Z, N, H, C = _flags(cpu)
    assert (Z, N, H, C) == (1, 0, 1, 0)  # unchanged

def test_dec_sp_wrap_and_flags(cpu):
    cpu.SP = 0x0000
    cpu.set_flags(z=0, n=1, h=0, c=1)

    dec_sp(cpu)

    assert cpu.SP == 0xFFFF
    Z, N, H, C = _flags(cpu)
    assert (Z, N, H, C) == (0, 1, 0, 1)  # unchanged
