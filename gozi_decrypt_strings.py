from binaryninja import BinaryReader

def decrypt_strings(secret_sauce):
    bss = bv.get_section_by_name(".bss").start
    br = BinaryReader(bv, address=bss)

    rva = bss - bv.start
    print(hex(rva))

    # TODO: Get key dynamically
    key1 = int.from_bytes(b"Apr ", "little")
    key2 = int.from_bytes(b"26 2", "little")
    key = key1 + key2 + rva + secret_sauce

    prev = 0x0
    curr = int.from_bytes(br.read(0x4), "little")
    data = b""
    for _ in range(0x400):
        if curr == 0x0:
            break
        result = (prev - key + curr & 0xffffffff).to_bytes(4, "little")
        data += result
        prev = curr
        curr = int.from_bytes(br.read(0x4), "little")
    return data

print(decrypt_strings(18))
