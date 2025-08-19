import cpu
import bus

# make the bus + cpu
bus = bus.Bus()
cpu = cpu.CPU(bus)

print("=== Test fetch8 ===")
bus.write8(0x0100, 0xAB)
cpu.PC = 0x0100
val = cpu.fetch8()
print("fetch8 ->", hex(val), " PC =", hex(cpu.PC))  # expect 0xAB, PC=0x0101

print("\n=== Test fetch16 ===")
bus.write8(0x0100, 0x34)  # low
bus.write8(0x0101, 0x12)  # high
cpu.PC = 0x0100
val16 = cpu.fetch16()
print("fetch16 ->", hex(val16), " PC =", hex(cpu.PC))  # expect 0x1234, PC=0x0102

print("\n=== Test wraparound ===")
bus.write8(0xFFFF, 0xCD)
bus.write8(0x0000, 0xAB)
cpu.PC = 0xFFFF
val16_wrap = cpu.fetch16()
print("fetch16 wrap ->", hex(val16_wrap), " PC =", hex(cpu.PC))  # expect 0xABCD, PC=0x0001

print("\n=== Test flags ===")
cpu.F = 0b10100000  # Z=1, N=0, H=1, C=0
print("Z:", cpu.get_flagZ())  # expect 1
print("N:", cpu.get_flagN())  # expect 0
print("H:", cpu.get_flagH())  # expect 1
print("C:", cpu.get_flagC())  # expect 0

