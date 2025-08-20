import bus as bus_mod
import cpu as cpu_mod
import opcodes as opcodes_mod

# Always present in your current code:
#   0x3E LD A,n8
#   0x06 LD B,n8
#   0x0E LD C,n8
#   0x16 LD D,n8
#   0x1E LD E,n8
#   0x26 LD H,n8
#   0x2E LD L,n8
#   0x00 NOP
#
# Optionally present (if you added them):
#   0x40 LD B,B
#   0x41 LD B,C
#   0x42 LD B,D
#   0x43 LD B,E
#   0x44 LD B,H
#   0x45 LD B,L

def expect(name, got, want):
    if got != want:
        g = hex(got) if isinstance(got, int) else got
        w = hex(want) if isinstance(want, int) else want
        raise AssertionError(f"{name}: got {g} != expected {w}")
    print(f"OK: {name} == {hex(want) if isinstance(want,int) else want}")

def main():
    b = bus_mod.Bus()
    c = cpu_mod.CPU(b)

    # Build a ROM dynamically so we can include optional LD B,r if available.
    ROM = []
    # Seed distinct values in all 8-bit regs using LD r,n8 (8 cycles each)
    ROM += [0x3E, 0x42]  # LD A,0x42
    ROM += [0x06, 0x11]  # LD B,0x11
    ROM += [0x0E, 0x22]  # LD C,0x22
    ROM += [0x16, 0x33]  # LD D,0x33
    ROM += [0x1E, 0x44]  # LD E,0x44
    ROM += [0x26, 0x55]  # LD H,0x55
    ROM += [0x2E, 0x66]  # LD L,0x66
    ROM += [0x00]        # NOP (4 cycles)

    # Optional LD B,r group (4 cycles each). Only append if handler exists.
    base_ops = opcodes_mod.ops_base
    ld_b_r_opcodes = []
    for opc in (0x40, 0x41, 0x42, 0x43, 0x44, 0x45):
        entry = base_ops[opc]
        if entry is not None and entry.get("handler"):
            ld_b_r_opcodes.append(opc)

    ROM += ld_b_r_opcodes

    # Load ROM at 0x0100
    base_addr = 0x0100
    for i, byte in enumerate(ROM):
        b.write8(base_addr + i, byte)

    # Reset and run
    c.reset(post_boot=True)

    # --- Step through the mandatory LD r,n8 + NOP sequence ---
    # 1: LD A,0x42
    c.step()
    expect("A after LD A,n8", c.A, 0x42)
    expect("PC after step 1", c.PC, 0x0102)
    expect("last_instr_cycles step 1", c.last_instr_cycles, 8)

    # 2: LD B,0x11
    c.step()
    expect("B after LD B,n8", c.B, 0x11)
    expect("PC after step 2", c.PC, 0x0104)
    expect("last_instr_cycles step 2", c.last_instr_cycles, 8)

    # 3: LD C,0x22
    c.step()
    expect("C after LD C,n8", c.C, 0x22)
    expect("PC after step 3", c.PC, 0x0106)
    expect("last_instr_cycles step 3", c.last_instr_cycles, 8)

    # 4: LD D,0x33
    c.step()
    expect("D after LD D,n8", c.D, 0x33)
    expect("PC after step 4", c.PC, 0x0108)
    expect("last_instr_cycles step 4", c.last_instr_cycles, 8)

    # 5: LD E,0x44
    c.step()
    expect("E after LD E,n8", c.E, 0x44)
    expect("PC after step 5", c.PC, 0x010A)
    expect("last_instr_cycles step 5", c.last_instr_cycles, 8)

    # 6: LD H,0x55
    c.step()
    expect("H after LD H,n8", c.H, 0x55)
    expect("PC after step 6", c.PC, 0x010C)
    expect("last_instr_cycles step 6", c.last_instr_cycles, 8)

    # 7: LD L,0x66
    c.step()
    expect("L after LD L,n8", c.L, 0x66)
    expect("PC after step 7", c.PC, 0x010E)
    expect("last_instr_cycles step 7", c.last_instr_cycles, 8)

    # 8: NOP
    c.step()
    expect("PC after step 8 (NOP)", c.PC, 0x010F)
    expect("last_instr_cycles step 8", c.last_instr_cycles, 4)

    # Base cycles so far: 7 * 8 + 4 = 60
    base_cycles = 7 * 8 + 4
    expect("cycles_total after base LDs", c.cycles_total, base_cycles)

    # --- Optional LD B,r checks (if those handlers exist) ---
    # Note: at this point registers have: B=0x11, C=0x22, D=0x33, E=0x44, H=0x55, L=0x66
    # Execute each appended opcode and assert B matches the source.
    for opc in ld_b_r_opcodes:
        before_pc = c.PC
        c.step()
        # Each LD B,r is 1 byte, 4 cycles, PC should +1
        expect(f"PC after LD B,? opcode {hex(opc)}", c.PC, (before_pc + 1) & 0xFFFF)
        expect("last_instr_cycles for LD B,?", c.last_instr_cycles, 4)

        if opc == 0x40:  # LD B,B (no change)
            expect("B after LD B,B", c.B, c.B)
        elif opc == 0x41:  # LD B,C
            expect("B after LD B,C", c.B, 0x22)
        elif opc == 0x42:  # LD B,D
            expect("B after LD B,D", c.B, 0x33)
        elif opc == 0x43:  # LD B,E
            expect("B after LD B,E", c.B, 0x44)
        elif opc == 0x44:  # LD B,H
            expect("B after LD B,H", c.B, 0x55)
        elif opc == 0x45:  # LD B,L
            expect("B after LD B,L", c.B, 0x66)

    # Final cycles check
    expect("final cycles_total",
           c.cycles_total,
           base_cycles + 4 * len(ld_b_r_opcodes))

    print("\nAll tests for current opcodes passed ✅")

if __name__ == "__main__":
    main()
