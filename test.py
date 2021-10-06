import pefile
from OpenSSL import crypto
from OpenSSL.crypto import _lib, _ffi, X509


def get_certificates(self):
    certs = _ffi.NULL
    if self.type_is_signed():
        certs = self._pkcs7.d.sign.cert
    elif self.type_is_signedAndEnveloped():
        certs = self._pkcs7.d.signed_and_enveloped.cert

    pycerts = []
    for i in range(_lib.sk_X509_num(certs)):
        pycert = X509.__new__(X509)
        pycert._x509 = _lib.sk_X509_value(certs, i)
        pycerts.append(pycert)

    if not pycerts:
        return None
    return tuple(pycerts)


SignedFile = "/home/whydoyoucare/freelancer/python-pe-inmemory-exec/testfiles/hh7.golden.exe"

pe = pefile.PE(SignedFile)

address = pe.OPTIONAL_HEADER.DATA_DIRECTORY[
    pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
].VirtualAddress
size = pe.OPTIONAL_HEADER.DATA_DIRECTORY[
    pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
].Size

if address == 0:
    print("Error: source file not signed")
else:
    signature = pe.write()[address + 8:]

    pkcs = crypto.load_pkcs7_data(crypto.FILETYPE_ASN1, bytes(signature))
    certs = get_certificates(pkcs)

    for cert in certs:
        c = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        a = crypto.load_certificate(crypto.FILETYPE_PEM, c)
        # get data from parsed cert
        print(a.get_subject())
