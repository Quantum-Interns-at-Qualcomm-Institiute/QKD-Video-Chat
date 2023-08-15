from Crypto.Cipher import AES
import hashlib

def encrypt(data, key):
    cipher = AES.new(hashlib.sha256(key).digest(), AES.MODE_ECB)
    return cipher.encrypt(data)

def decrypt(data, key):
    cipher = AES.new(hashlib.sha256(key).digest(), AES.MODE_ECB)
    return cipher.decrypt(data)
