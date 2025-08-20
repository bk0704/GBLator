import bus as bus_mod
import cpu as cpu_mod

# Program @0x0100:
# 3E 42   LD A,0x42      (8 cycles)
# 06 99   LD B,0x99      (8 cycles)
# 00      NOP            (4 cycles)
ROM = [0x3E, 0x42, 0x06, 0x99, 0x00]

def expect(name, got, want):
    if got != want:
        raise AssertionError(f"{name}: got {hex(got) if isinstance(got,int) else got} != expected {hex(want) if isinstance(want,int) else want}")
    print(f"OK: {name} == {hex(want) if isinstance(want,int) else want}")

def main():
    b = bus_mod.Bus()
    c = cpu_mod.CPU(b)

    # Load the tiny ROM into memory at 0x0100
    base = 0x0100
    for i, byte in enumerate(ROM):
        b.write8(base + i, byte)

    # Start CPU in post-boot state
    c.reset(post_boot=True)

    # ---- Step 1: LD A,0x42 ----
    c.step()
    expect("A after LD A,n8", c.A, 0x42)
    expect("PC after step 1", c.PC, 0x0102)
    expect("last_instr_cycles step 1", c.last_instr_cycles, 8)

    # ---- Step 2: LD B,0x99 ----
    c.step()
    expect("B after LD B,n8", c.B, 0x99)
    expect("PC after step 2", c.PC, 0x0104)
    expect("last_instr_cycles step 2", c.last_instr_cycles, 8)

    # ---- Step 3: NOP ----
    c.step()
    expect("PC after step 3", c.PC, 0x0105)
    expect("last_instr_cycles step 3", c.last_instr_cycles, 4)

    # ---- Totals ----
    expect("cycles_total", c.cycles_total, 8 + 8 + 4)

    print("\nAll LD-basic tests passed ✅")

if __name__ == "__main__":
    main()
