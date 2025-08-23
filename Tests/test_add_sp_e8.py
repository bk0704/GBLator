# tests/test_add_sp_e8.py
import pytest

from cpu import CPU
from handlers_stack_manipulation import add_sp_e8


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


def preload_imm(cpu, imm_u8):
    """Place the immediate at PC for fetch_e8()/fetch8() to read."""
    cpu.bus.write8(cpu.PC, imm_u8 & 0xFF)


def flags(cpu):
    return cpu.get_flagZ(), cpu.get_flagN(), cpu.get_flagH(), cpu.get_flagC()


@pytest.mark.parametrize(
    "sp_start, imm_u8, sp_expected, h_expected, c_expected",
    [
        # +1, no half-carry, no carry
        (0x1000, 0x01, 0x1001, False, False),

        # +1, half-carry from low nibble (0x...F + 1)
        (0x100F, 0x01, 0x1010, True,  False),

        # +1, byte carry (0x..FF + 1)
        (0x10FF, 0x01, 0x1100, True, True),

        # -1 (0xFF), borrow but flags are computed via low-byte add rules
        (0x0000, 0xFF, 0xFFFF, False, False),

        # -1 from 0x0001 -> 0x0000, should set both H and C
        (0x0001, 0xFF, 0x0000, True,  True),

        # -128 (0x80), no half-carry, no carry
        (0xFF00, 0x80, 0xFE80, False, False),
    ],
)
def test_add_sp_e8(cpu, sp_start, imm_u8, sp_expected, h_expected, c_expected):
    # Arrange
    cpu.SP = sp_start & 0xFFFF
    cpu.PC = 0x2000
    preload_imm(cpu, imm_u8)

    # Seed flags to ensure Z/N are actively cleared by the op
    cpu.set_flags(z=1, n=1, h=0, c=0)
    pc_before = cpu.PC

    # Act
    add_sp_e8(cpu)

    # Assert SP and PC advance by 1 (the immediate)
    assert cpu.SP == sp_expected & 0xFFFF
    assert cpu.PC == ((pc_before + 1) & 0xFFFF)

    # Assert flags
    Z, N, H, C = flags(cpu)
    assert Z == 0, "ADD SP,e8 must clear Z"
    assert N == 0, "ADD SP,e8 must clear N"
    assert H == (1 if h_expected else 0), "Half-carry (low nibble) incorrect"
    assert C == (1 if c_expected else 0), "Carry (low byte) incorrect"
