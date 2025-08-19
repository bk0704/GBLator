import cpu
import bus as bus_mod

# setup
bus = bus_mod.Bus()
c = cpu.CPU(bus)

# helpers to make failures obvious
def check(name, got, expect):
    if got != expect:
        raise AssertionError(f"{name}: got {hex(got)} != expected {hex(expect)}")
    print(f"OK: {name} == {hex(expect)}")

print("=== seed register pairs ===")
c.set_BC(0x1234)
c.set_DE(0xABCD)
c.set_HL(0xC000)
c.SP = 0xFFFE

# ---- r16 reads ----
print("\n=== r16 reads ===")
check("r16(0) BC", c.r16(0), 0x1234)
check("r16(1) DE", c.r16(1), 0xABCD)
check("r16(2) HL", c.r16(2), 0xC000)
check("r16(3) SP", c.r16(3), 0xFFFE)

# ---- r16 writes ----
print("\n=== r16 writes ===")
c.set_r16(0, 0x5555)       # BC
check("get_BC()", c.get_BC(), 0x5555)

c.set_r16(1, 0x89AB)       # DE
check("get_DE()", c.get_DE(), 0x89AB)

c.set_r16(2, 0xCAFE)       # HL
check("get_HL()", c.get_HL(), 0xCAFE)

c.set_r16(3, 0x8001)       # SP
check("SP", c.SP, 0x8001)

# ---- masking & bounds ----
print("\n=== masking ===")
c.set_r16(0, 0x1_2345)     # >16-bit should wrap to 0x2345
check("BC masked", c.get_BC(), 0x2345)

c.set_r16(3, -1)           # negative should wrap to 0xFFFF (if you mask)
check("SP masked", c.SP & 0xFFFF, 0xFFFF)

print("\nALL r16 tests passed ✅")
