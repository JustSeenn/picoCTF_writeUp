# ARMssembly 0 
Category: Reverse Engineering

AUTHOR: Dylan McGuire

## Beginning

This CTF is a really good introduction to ARMv8, all you have to do is sit in your chair and try to understand where the code is going.
It's exactly what will do by peeling each line and function.

This script is compose with 4 function and a main. Something strange at first is that we can see ``` bl atoi ``` but we don't have this one.
In french "à toi" mean "your turn" so i guess it's where we will put our inputs (266134863 & 1592237099) in my case, we don't have to worry about it so.

## Source code
Let's start with the main function 

```
main:
        stp     x29, x30, [sp, -48]!
        add     x29, sp, 0
        str     x19, [sp, 16]
        str     w0, [x29, 44]
        str     x1, [x29, 32]
        ldr     x0, [x29, 32]
        add     x0, x0, 8
        ldr     x0, [x0]
        bl      atoi
        mov     w19, w0            ** w19 = 266134863 ** 
        ldr     x0, [x29, 32]
        add     x0, x0, 16
        ldr     x0, [x0]
        bl      atoi
        mov     w1, w0             ** w1 = 1592237099 **
        mov     w0, w19            ** w0 = 266134863 **
        bl      func1
        mov     w1, w0
        adrp    x0, .LC0
        add     x0, x0, :lo12:.LC0
        bl      printf
        mov     w0, 0
        ldr     x19, [sp, 16]
        ldp     x29, x30, [sp], 48
        ret
        .size   main, .-main
        .ident  "GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
        .section        .note.GNU-stack,"",@progbits

```

Until the ``` bl func1 ``` we can just focus and which inputs we have. After each "atoi" function, the argument will be stock in the w0 register. The instruction ``` mov a,b ``` copy the value of b into the a register. So by knowing that we can undertand my comments and where are registered our 2 arguments.

Let's take a look to the func1.

```
func1:
        sub     sp, sp, #16
        str     w0, [sp, 12]   # [sp,12] = 266134863
        str     w1, [sp, 8]    # [sp,8] = 1592237099
        ldr     w1, [sp, 12]
        ldr     w0, [sp, 8]
        cmp     w1, w0
        bls     .L2
        ldr     w0, [sp, 12]
        b       .L3

```

The first line here mean that we give us a bit of space to register our variables, the instruction ``` sub sp,sp,#16 ``` mean that we put the stack pointer 2 bytes behind his initial value.
sub a,b,c mean a = b - c for another example.

Here we have the two most importants instruction  ``` str w0, [sp, 12] ```and ```str w1, [sp, 8]``` "str" is for storage, so here we store w0 at the space [sp,12] and w1 at [sp,8] like that we can recover them whenever we want to.

"ldr" at the opposite is for "loader" so to recover our values. At this points w1 = 266134863 and w0 = 1592237099.

Before talking about the cmp instruction i have to give a little explanation about how ARM and flags work (yes flags are everywhere).
Each time you will see a "cmp" instruction it will compare the values next to. In our example w1 and w0, and it will do a little substraction of them. This substraction will turn on flags depends on the result. 

```
N: Negative

The N flag is set by an instruction if the result is negative. In practice, N is set to the two's complement sign bit of the result (bit 31).

Z: Zero

The Z flag is set if the result of the flag-setting instruction is zero.

C: Carry (or Unsigned Overflow)

The C flag is set if the result of an unsigned operation overflows the 32-bit result register. This bit can be used to implement 64-bit unsigned arithmetic, for example.

V: (Signed) Overflow

The V flag works the same as the C flag, but for signed operations. For example, 0x7fffffff is the largest positive two's complement integer that can be represented in 32 bits, so 0x7fffffff + 0x7fffffff triggers a signed overflow, but not an unsigned overflow (or carry): the result, 0xfffffffe, is correct if interpreted as an unsigned quantity, but represents a negative value (-2) if interpreted as a signed quantity.


```
* https://community.arm.com/developer/ip-products/processors/b/processors-ip-blog/posts/condition-codes-1-condition-flags-and-codes * 

Of course they are not useless, so we will use these flags to see the result of our compare. 
```
	cmp  w1, w0    cmp #266134863,#1592237099
    bls  .L2

```

So here the "bls" instruction will be directly impacted by the flags. In fact it's the "ls" which is intresting because it mean "lower or same" so if w1 is lower or equal to w0 it will call the .L2 function, it's our case.

```
 .L2:
     ldr w0, [sp, 8]  # w0 = 1592237099

```

Very easy function here because it do only one thing so i will not explain that a lot.
After that it slide right behind and the code execute the .L3 function

```
 .L3:
       add  sp, sp, 16
       ret
        .size   func1, .-func1
        .section        .rodata
        .align  3

```
Lot of scary things here but don't worry it's only a "return" function. 
So after that we are back to the main with w0 = w1 = 1592237099

```
	mov w1, w0
    adrp x0, .LC0
    add x0, x0, :lo12:.LC0
    bl  printf

```
These are the lasted important line to finish this CTF, as we know w1 = w0 so moving w0 into w1 is useless here. The two other lines are here to prepare the printf by calling the function LC0 which get in shape the print.
And then we call the printf with w0 = 1592237099.
In ARM w0 is alway the variable which is tranfer to a function at another. We use it like that. So we will print w0.


## Final
To conclude use any website to convert the value into HEX and put it in lowercase. After that wrap it around picoCTF{} and you have your flag.