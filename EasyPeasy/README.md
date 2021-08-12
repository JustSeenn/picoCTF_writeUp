# Easy Peasy
Category: Cryptography 

AUTHOR: MADSTACKS 

## Beginning
When you launch the netcat command, this is what you have
```
******************Welcome to our OTP implementation!******************
This is the encrypted flag!
5541103a246e415e036c4c5f0e3d415a513e4a560050644859536b4f57003d4c

What data would you like to encrypt? flag
Here ya go!
570d5f3b

What data would you like to encrypt?
```

So there is a flag given, that's good new but how can we decrypt it ? Let's take a look at the code

## Source Code
We have to big function to understand here and some previous 

### Previous
```
KEY_FILE = "key"
KEY_LEN = 50000
FLAG_FILE = "flag"
``` 
At this point we know that the KEY will be around 50k long, so we can forget the guessing

### Startup
```
def startup(key_location):
	flag = open(FLAG_FILE).read() 
	kf = open(KEY_FILE, "rb").read()

	start = key_location
	stop = key_location + len(flag)

	key = kf[start:stop] # We take the exact length of the flag in the key
	key_location = stop

	result = list(map(lambda p, k: "{:02x}".format(ord(p) ^ k), flag, key)) # We use a XOR on each char of the flag 
	print("This is the encrypted flag!\n{}\n".format("".join(result)))
  ```
  
  Okay, so it's a XOR which is use to encrypt our flag, great it's easy to convert. However it use the same XOR for each char of the flag, so if we find the key, we find the flag easily
  Maybe the next function will give us vulnerabilitites to find the key.
  
  ### Encrypt
  
  ```
  ui = input("What data would you like to encrypt? ").rstrip()
	if len(ui) == 0 or len(ui) > KEY_LEN:
		return -1

	start = key_location
	stop = key_location + len(ui)

	kf = open(KEY_FILE, "rb").read()

	if stop >= KEY_LEN:   
		stop = stop % KEY_LEN  # There is a loop using a modulo to return at the start of the key
		key = kf[start:] + kf[:stop] 
	else:
		key = kf[start:stop]
	key_location = stop

	result = list(map(lambda p, k: "{:02x}".format(ord(p) ^ k), ui, key))

	print("Here ya go!\n{}\n".format("".join(result)))

	return key_location
  ```
  
  The stop condition give us a really good start. 
  What mean this ? If we get the stop to be the exact KEY_LEN, then ```stop % KEY_LEN == 0 ``` and we can find the flag. 
  How do you think ?
  
  Try to do a double XOR on a string with the exact same key. You will recover the string. That's what we will use.
  
  ## Script
  
  Let's create our script now using pwntool
  ```
from pwn import *

KEY_LEN = 50000
count = 50000 - 32

r = remote("mercury.picoctf.net", 36981)


r.recvuntil("This is the encrypted flag!\n")
flag = r.recvline()
log.info(f"Flag : {flag}")
bin_flag = unhex(flag)


```
We know with the cipher flag that it will be 32 long, so the key has to be 50 000 - 32 of length. 
Let's get the flag encrypted and use unhex to convert it. 

```
r.sendlineafter("What data would you like to encrypt? ", "A" * count)
r.sendlineafter("What data would you like to encrypt? ", bin_flag)
r.recvlineS()
log.success("The flag: {}".format(unhex(r.recvlineS())))
```

The magic starts here, we start by sending ``` 'A' * (50 000 - 32) ``` to get our input equal to the KEY_LENGTH and then we send back our flag 
```
Flag : b'5541103a246e415e036c4c5f0e3d415a513e4a560050644859536b4f57003d4c\n'
[+] The flag: b'7f9da29f40499a98db220380a57746a4'
[*] Closed connection to mercury.picoctf.net port 36981
```
Wrap 7f9da29f40499a98db220380a57746a4 into picoCTF{ } to get your points !
    
