# tests/test_add_hl_sp.py
import pytest

from cpu import CPU
from handlers_stack_manipulation import add_hl_sp


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


def set_Z(cpu, z_before: int):
    # Only set Z; leave others untouched
    cpu.set_flags(z=1 if z_before else 0)


def flags_tuple(cpu):
    return (cpu.get_flagZ(), cpu.get_flagN(), cpu.get_flagH(), cpu.get_flagC())


def run_case(cpu, hl, sp, z_before, hl_expected, h_expected, c_expected):
    # Arrange
    cpu.set_HL(hl & 0xFFFF)
    cpu.SP = sp & 0xFFFF
    set_Z(cpu, z_before)

    # Act
    add_hl_sp(cpu)

    # Assert result
    assert cpu.get_HL() == (hl_expected & 0xFFFF), "HL result wrong"

    # Assert flags
    Z, N, H, C = flags_tuple(cpu)
    assert N == 0, "N must be cleared by ADD HL,SP"
    assert H == (1 if h_expected else 0), "H (half-carry from bit 11) wrong"
    assert C == (1 if c_expected else 0), "C (carry from bit 15) wrong"
    assert Z == (1 if z_before else 0), "Z must be unchanged by ADD HL,SP"


@pytest.mark.parametrize(
    "hl, sp, z_before, hl_expected, h_expected, c_expected",
    [
        (0x1234, 0x0001, 0, 0x1235, False, False),
        (0x1234, 0x0001, 1, 0x1235, False, False),

        # Half-carry only (carry out of bit 11)
        (0x0FFF, 0x0001, 0, 0x1000, True,  False),

        # Full carry wrap (carry out of bit 15); this edge also sets H
        (0xFFFF, 0x0001, 0, 0x0000, True,  True),

        # Carry without half-carry (bit11)
        (0x8000, 0x8000, 0, 0x0000, False, True),

        # Boundary: no half-carry, no full carry
        (0x08FF, 0x0101, 0, 0x0A00, False, False),
    ],
)

def test_add_hl_sp(cpu, hl, sp, z_before, hl_expected, h_expected, c_expected):
    run_case(cpu, hl, sp, z_before, hl_expected, h_expected, c_expected)
