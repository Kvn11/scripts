from binaryninja import Transform, BinaryReader

FILENAME = ""
ADDR_OF_DATA = 0x7fff7a1a9040
KEY = 0x11c742c6

def get_data(hexstream_addr):
    br = BinaryReader(bv, address=hexstream_addr)
    data = ""
    curr = br.read(2)
    while curr != b"\x00\x00":
        data += curr.decode("utf-8")
        curr = br.read(2)
    data = bytes.fromhex(data)
    return data

def rc4_decrypt(data, key=KEY):
    key = key.to_bytes(4, byteorder="little")
    rc4 = Transform["RC4"]
    return rc4.encode(data, {"key": key})

def xor_decrypt(data, key=KEY):
    data = bytearray(data)
    key = key.to_bytes(4, byteorder="little")
    for i in range(len(data) - 1):
        b = data[i] ^ key[i % len(key)]
        b -= data[i + 1]
        b &= b & 0xFF
        data[i] = b
    return data

def unpack(hexstream_addr):
    data = get_data(hexstream_addr)
    data = rc4_decrypt(data)
    data = xor_decrypt(data)
    with open(FILENAME, "wb") as f:
        f.write(data)
    return True

unpack(ADDR_OF_DATA)
