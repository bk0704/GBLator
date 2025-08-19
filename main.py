import cpu
import bus

# make the bus + cpu
bus = bus.Bus()
cpu = cpu.CPU(bus)

# preload memory
bus.write8(0x0101, 0x34)
bus.write8(0x0102, 0x12)

# set starting PC
cpu.PC = 0x0101

# 1st fetch
b1 = cpu.fetch16()
print(hex(b1), hex(cpu.PC))   # expect 0x3e, 0x101


# wraparound test
bus.write8(0xFFFF, 0xAA)
bus.write8(0x0000, 0xBB)
cpu.PC = 0xFFFF
b3 = cpu.fetch16()
print(hex(b3), hex(cpu.PC)) # expect 0x99, 0x0000

cpu.F = 0b10000000   # only bit7 set
print(cpu.getflagZ())  # expect 1

cpu.F = 0b00000000   # all clear
print(cpu.getflagZ())  # expect 0

cpu.F = 0b01000000   # bit6 set, not bit7
print(cpu.getflagZ())  # expect 0
