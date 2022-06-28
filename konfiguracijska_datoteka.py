# RSA
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
# X25519
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey 
# Fernet
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def AuthRSAKlijent():
    # privatni kljuc klijenta
    private_key_server = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    pem_client = private_key_server.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
    )

    message = b"A message I want to sign"
    # potpis
    signature_server = private_key_server.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    public_key = private_key_server.public_key()
    
    # posluzitelj provjera
    public_key.verify(
        signature_server,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Posluzitelj uspjesno verificiran")

def AuthRSAServer():   
    # privatni kljuc klijenta
    private_key_client = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    pem_client = private_key_client.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
    )

    message = b"A message I want to sign"
    # potpis
    signature_client = private_key_client.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    public_key = private_key_client.public_key()
    # klijent provjera
    public_key.verify(
        signature_client,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def KeyExchangeX25519():
    client_private_key = X25519PrivateKey.generate()
    client_public_key = client_private_key.public_key()

    server_private_key = X25519PrivateKey.generate()
    server_public_key = server_private_key.public_key()

    shared_key_client = client_private_key.exchange(server_public_key)
    shared_key_server = server_private_key.exchange(client_public_key)

    if(shared_key_server == shared_key_client):
        return True

kljuc_klijent = b'nMrhMgIiAsMMEMfuPudvP4_LfA6U85NOGdAJZBdGN1Q='         
kljuc_posluzitelj =b'zjeM756A0Z69DE5jna14ff575bh2DP4-5pyFMTRXB94='     
fernet_kljuc_klijent = Fernet(kljuc_klijent)
fernet_kljuc_posluzitelj = Fernet(kljuc_posluzitelj)

print(Fernet.generate_key())

# Cha Cha poly
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
nonce = b'\xcb\x0fMz\xf7EqDg*P\x9c'
aad = None
key = b'\xe9\xc3\xb1^\xb1\xe0UKEg^\x81\x92\xab6\xb9\x9e\x18\xc5\x8a\x80\xa9 \xb1\xd1\xe6w\xa8\xe9\x01\xaal'
chacha = ChaCha20Poly1305(key)
data = b"uspjesno dobivena poruka"
ct = b"uspjesno dobivena poruka"

def ChaChaEncrypt(nonce, data, aad):
    chacha.encrypt(nonce, data, aad)
    return True

def ChaChaDecrypt(nonce, ct, aad):
    if chacha.decrypt(nonce, ct, aad) == b"uspjesno dobivena poruka":
        return True
