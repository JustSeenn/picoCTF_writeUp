from pwn import *

KEY_LEN = 50000
MAX_CHUNK = 1000

r = remote("mercury.picoctf.net", 36981)


r.recvuntil("This is the encrypted flag!\n")
flag = r.recvline()
log.info(f"Flag : {flag}")
bin_flag = unhex(flag)
count = 50000 - 32


r.sendlineafter("What data would you like to encrypt? ", "A" * count)
r.sendlineafter("What data would you like to encrypt? ", bin_flag)
r.recvlineS()
log.success("The flag: {}".format(unhex(r.recvlineS())))


