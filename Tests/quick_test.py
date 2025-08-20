import bus as bus_mod
import cpu as cpu_mod

# Program @0x0100:
# 3E 42   LD A,0x42      (8 cycles)
# 06 99   LD B,0x99      (8 cycles)
# 78      LD A,B         (4 cycles)
# 00      NOP            (4 cycles)
ROM_BYTES = [0x3E, 0x42, 0x06, 0x99, 0x78, 0x00]

def expect(name, got, want):
    if got != want:
        raise AssertionError(f"{name}: got {hex(got) if isinstance(got,int) else got} != expected {hex(want) if isinstance(want,int) else want}")
    print(f"OK: {name} == {hex(want) if isinstance(want,int) else want}")

def main():
    bus = bus_mod.Bus()
    cpu = cpu_mod.CPU(bus)

    # Load the tiny ROM into memory at 0x0100
    base = 0x0100
    for i, b in enumerate(ROM_BYTES):
        bus.write8(base + i, b)

    # Start CPU
    cpu.reset(post_boot=True)

    print("Step 1: LD A,0x42")
    cpu.step()
    expect("A", cpu.A, 0x42)
    expect("PC", cpu.PC, 0x0102)
    expect("last_instr_cycles", cpu.last_instr_cycles, 8)

    print("Step 2: LD B,0x99")
    cpu.step()
    expect("B", cpu.B, 0x99)
    expect("PC", cpu.PC, 0x0104)
    expect("last_instr_cycles", cpu.last_instr_cycles, 8)

    print("Step 3: LD A,B")
    cpu.step()
    expect("A", cpu.A, 0x99)
    expect("PC", cpu.PC, 0x0105)
    expect("last_instr_cycles", cpu.last_instr_cycles, 4)

    print("Step 4: NOP")
    cpu.step()
    expect("PC", cpu.PC, 0x0106)
    expect("last_instr_cycles", cpu.last_instr_cycles, 4)

    # Total cycles (8+8+4+4)
    expect("cycles_total", cpu.cycles_total, 24)

    print("\nAll quick tests passed ✅")

if __name__ == "__main__":
    main()
