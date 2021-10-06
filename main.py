import sys
from pefile import PE

# Catch all input arguments


def main(pename):

    pe = PE(pename)

    verinfo = pe.VS_FIXEDFILEINFO
    filever = (verinfo.FileVersionMS >> 16, verinfo.FileVersionMS & 0xFFFF,
               verinfo.FileVersionLS >> 16, verinfo.FileVersionLS & 0xFFFF)
    prodver = (verinfo.ProductVersionMS >> 16, verinfo.Product5VersionMS & 0xFFFF,
               verinfo.ProductVersionLS >> 16, verinfo.ProductVersionLS & 0xFFFF)


def t(filename):
    from ecdsa import SigningKey
    private_key = SigningKey.generate() # uses NIST192p
    signature = private_key.sign(b"Educative authorizes this shot")
    print(signature)
    public_key = private_key.verifying_key
    
    print("Verified:", public_key.verify(signature, b"Educative authorizes this shot"))
main("/home/whydoyoucare/freelancer/python-pe-inmemory-exec/testfiles/hh7.golden.exe")
