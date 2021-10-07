from Crypto.Cipher import AES
from Crypto import Random

import os
import sys

# KEYIV used for encrypting KEYIV
key0 = b'\xbd4k/\xac\xf2\xfc\xff\xa6\x03\x7f\x10W\x83e\xba'
iv0 = b'\xeb\x0f1\x1c\xd8\xa5\x8d\xf5d\x97\x9aJ\xd8\xb9_\xeb'


def encrypt_it(bytefile, key=key0, iv=iv0):
    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
    return cfb_cipher.encrypt(bytefile)


def decrypt_it(bytefile):
    cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
    return cfb_decipher.decrypt(bytefile)


def readByteFile(dir):
    file = open(dir, "rb")
    data = file.read()
    file.close()
    return data


def writeByteFile(dir, data):
    file = open(dir, "wb")
    file.write(data)
    file.close()


def safe_os(cmd):
    try:
        os.system(cmd)
    except:
        pass


def keyGenerate():
    f = open("KEYIV.key", "w+")
    f.write("key = %s \n" % key)
    f.write("iv = %s \n" % iv)
    f.close()

    key_data = readByteFile("KEYIV.key")
    writeByteFile("KEYIV.key", encrypt_it(key_data))


# KEYIV used for encrypting data
key = Random.new().read(AES.block_size)
iv = Random.new().read(AES.block_size)  # initialization vector

# print ("\nKEY:", key)
# print ("IV:", iv, "\n")

safe_os('mkdir 1ORIGINAL')
safe_os('mkdir 2ENCRYPTED')
safe_os('mkdir 3DECRYPTED')

print("The program allows you to encrypt files")
print("Please put the files you want to encrypt in \'1ORIGINAL\'")

temp = input("Press \'Enter\' key to continue...")

# Creating txt with key and iv used for encryption
print("Generating KEYIV for the recipient")
keyGenerate()


print("Retrieving files in 1ORIGINAL\n")
try:
    oriFile = os.listdir("1ORIGINAL")
except:
    raise Exception(
        'Directory \'1ORIGINAL\' does not exist in the current directory')


print("Beginning Encryption...\n")

for file in oriFile:
    print("Encrypting", file)

    filedata = readByteFile("1ORIGINAL/"+file)
    writeByteFile("2ENCRYPTED/"+file+".enc", encrypt_it(filedata, key, iv))

    print("Completed encrypting", file, "\n")

print("Encryption successful\n")


print("Retrieving files in 2ENCRYPTED\n")
try:
    inFiles = os.listdir("2ENCRYPTED")
except:
    raise Exception(
        'Directory \'2ENCRYPTED\' does not exist in the current directory')


print("Beginning Decryption...\n")

for file in inFiles:
    print("Decrypting", file)

    filedata = readByteFile("2ENCRYPTED/"+file)
    writeByteFile("3DECRYPTED/"+file[:-4], decrypt_it(filedata))

    print("Completed decrypting", file, "\n")

print("Decryption successful\n")
