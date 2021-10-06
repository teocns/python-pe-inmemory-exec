
from io import BytesIO
from itertools import cycle

from config import ENCRYPTION_KEY


def xore(data, key):
    return bytes(a ^ b for a, b in zip(data, cycle(key)))


def encrypt(data: bytes):
    with BytesIO(data) as f:
        return xore(f.read(), ENCRYPTION_KEY)


def unencrypt(data: bytes):
    with BytesIO(data) as f:
        return xore(f.read(), ENCRYPTION_KEY)
