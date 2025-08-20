import bus as bus_mod
import cpu as cpu_mod

# Program @ 0x0100:
# 3E 42   LD A,0x42
# 06 11   LD B,0x11
# 0E 22   LD C,0x22
# 16 33   LD D,0x33
# 1E 44   LD E,0x44
# 26 55   LD H,0x55
# 2E 66   LD L,0x66
# 00      NOP
ROM = [
    0x3E, 0x42,
    0x06, 0x11,
    0x0E, 0x22,
    0x16, 0x33,
    0x1E, 0x44,
    0x26, 0x55,
    0x2E, 0x66,
    0x00,
]

def expect(name, got, want):
    if got != want:
        raise AssertionError(f"{name}: got {hex(got) if isinstance(got,int) else got} != expected {hex(want) if isinstance(want,int) else want}")
    print(f"OK: {name} == {hex(want) if isinstance(want,int) else want}")

def main():
    b = bus_mod.Bus()
    c = cpu_mod.CPU(b)

    # Load ROM at 0x0100
    base = 0x0100
    for i, byte in enumerate(ROM):
        b.write8(base + i, byte)

    c.reset(post_boot=True)

    # Step through each instruction and check effects
    print("Step 1: LD A,0x42")
    c.step()
    expect("A", c.A, 0x42)
    expect("PC", c.PC, 0x0102)
    expect("last_instr_cycles", c.last_instr_cycles, 8)

    print("Step 2: LD B,0x11")
    c.step()
    expect("B", c.B, 0x11)
    expect("PC", c.PC, 0x0104)
    expect("last_instr_cycles", c.last_instr_cycles, 8)

    print("Step 3: LD C,0x22")
    c.step()
    expect("C", c.C, 0x22)
    expect("PC", c.PC, 0x0106)
    expect("last_instr_cycles", c.last_instr_cycles, 8)

    print("Step 4: LD D,0x33")
    c.step()
    expect("D", c.D, 0x33)
    expect("PC", c.PC, 0x0108)
    expect("last_instr_cycles", c.last_instr_cycles, 8)

    print("Step 5: LD E,0x44")
    c.step()
    expect("E", c.E, 0x44)
    expect("PC", c.PC, 0x010A)
    expect("last_instr_cycles", c.last_instr_cycles, 8)

    print("Step 6: LD H,0x55")
    c.step()
    expect("H", c.H, 0x55)
    expect("PC", c.PC, 0x010C)
    expect("last_instr_cycles", c.last_instr_cycles, 8)

    print("Step 7: LD L,0x66")
    c.step()
    expect("L", c.L, 0x66)
    expect("PC", c.PC, 0x010E)
    expect("last_instr_cycles", c.last_instr_cycles, 8)

    print("Step 8: NOP")
    c.step()
    expect("PC", c.PC, 0x010F)
    expect("last_instr_cycles", c.last_instr_cycles, 4)

    # Totals: 7 LDs (8 cycles each) + 1 NOP (4 cycles) = 60
    expect("cycles_total", c.cycles_total, 7*8 + 4)

    print("\nAll current LD-opcode tests passed ✅")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
