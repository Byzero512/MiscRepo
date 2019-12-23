from pwn import *
from mypwn.mypwnlib.Exception.myExcept import *

def pack_num(num):
    try:
        if context.arch=='i386':
            return p32(num)
        elif context.arch=='amd64':
            return p64(num)
        else:
            raise contextArchError("arch must be i386 or ad64")
    except contextArchError as except1:
        print(except1)
        quit()

def myprint(payload):
    print('\033[0;33m'+payload+'\033[0m')