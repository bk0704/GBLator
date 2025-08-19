class Bus:
    def __init__(self):
        self.mem = bytearray(65536) # 64KB memory

    def read8(self, address):
        # Masks address to 16-bit and returns byte
        address &= 0xFFFF
        byte = self.mem[address]
        return byte

    def write8(self, address, byte):
        address &= 0xFFFF #Mask Address to 16-bit
        byte &= 0xFF # Mask address to 8-bit
        self.mem[address] = byte # Store the byte in address




