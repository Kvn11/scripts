from binaryninja import BinaryReader
import re

def xor_decrypt(data_addr):
    br = BinaryReader(bv, address=data_addr)
    data = br.read(0x80)
    config = b""
    for i in range(0x20):
        config += (data[i] ^ data[i + 0x40]).to_bytes(1, "little")
    return config

def extract_url_from_bytes(byte_string):
    extracted_ascii = b""
    for byte in byte_string:
        if 32 <= byte <= 126:
            extracted_ascii += bytes([byte])
    extracted_ascii = extracted_ascii.decode("utf-8")
    pattern = re.compile('.*com')
    url = pattern.search(extracted_ascii)
    return url.group(0)
    
config = xor_decrypt(0x7ffc97718000)
url = extract_url_from_bytes(config)
print(f"[*] C2 Address -> {url}")
