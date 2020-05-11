from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA256, MD5
import json
import base64
import os
from os import environ
import ipfshttpclient
IPFS_URL = environ.get("IPFS_URL", '/dns/ipfs.infura.io/tcp/5001/https')
ipfs = ipfshttpclient.connect(IPFS_URL)

def ipfs_add(file):
    url = ipfs.add_bytes(file)
    return url

def encrypt_rsa(key, public_key):
    handler = PKCS1_OAEP.new(public_key)
    return base64.encodebytes(handler.encrypt(key))

def decrypt_rsa(data, private_key):
    handler = PKCS1_OAEP.new(private_key)
    return handler.decrypt(base64.decodebytes(data))

def pad(s):
    if type(s) == str:
        return str.encode(s) + b"\0" * (AES.block_size - len(s) % AES.block_size)
    else:
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    key = pad(key)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def generate_rsa_key():
    return RSA.generate(1024, Random.new().read)

def generate_random_aes_key():
    return str(os.urandom(8))

def generate_secret_key():
    key = generate_random_aes_key()
    return MD5.new(key).hexdigest()

def hash(data):
    h = SHA256.new()
    data = json.dumps(data, separators=(',', ':')).encode()
    h.update(data)
    return h.hexdigest()