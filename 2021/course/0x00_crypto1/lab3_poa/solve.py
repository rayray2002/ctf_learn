from pwn import *
from tqdm import tqdm

def xor(x, y):
    return bytes(a ^ b for a, b in zip(x, y))


r = remote("edu-ctf.csie.org", 42070, level="info")

r.recvuntil("cipher = ")
cipher = r.recvline().strip().decode()
print(cipher)

cipher = bytes.fromhex(cipher)
iv = cipher[:16]
flag = b""
print(f"iv = {iv.hex()}")
for block in [cipher[16:32], cipher[32:48]]:
    print(f"block = {block.hex()}")

    correct = b""
    for i in tqdm(range(16)):
        # print(i)
        for j in range(256):
            iv_new = b"\x00" * (15 - i) + bytes([j]) + correct
            # print(f"iv_new = {iv_new.hex()}")
            pl = iv_new + block
            r.sendlineafter("cipher = ", pl.hex())
            resp = r.recvline().strip().decode()
            if resp == "YESSSSSSSS":
                correct = bytes([j ^ 0x80]) + correct
                # print(correct.hex())
                break
    flag += xor(iv, correct)
    print(flag)
    iv = block
