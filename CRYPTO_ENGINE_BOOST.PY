import hashlib
import hmac
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
class CryptoEngine:
    def __init__(self):
        self.backend = default_backend()
    def generate_key(self):
        return os.urandom(32)
    def encrypt_aes_gcm(self, plaintext, key):
        cipher = Cipher(algorithms.AES(key), modes.GCM(b'\x00'*12), backend=self.backend)
        encryptor = cipher.encryptor()
        ct = encryptor.update(plaintext) + encryptor.finalize()
        return ct + encryptor.tag
    def decrypt_aes_gcm(self, ciphertext, key):
        cipher = Cipher(algorithms.AES(key), modes.GCM(ciphertext[-16:], ciphertext[:-16]), backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext[:-16]) + decryptor.finalize()
    def encrypt_rsa_oaep(self, plaintext, pubkey):
        from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
        from cryptography.hazmat.primitives import serialization
        pubkey = serialization.load_pem_public_key(pubkey, backend=self.backend)
        encryptor = pubkey.encryptor(
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashlib.sha256()),
                algorithm=hashlib.sha256(),
                label=None
            )
        )
        return encryptor.update(plaintext)
    def decrypt_rsa_oaep(self, ciphertext, privkey):
        from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
        from cryptography.hazmat.primitives import serialization
        privkey = serialization.load_pem_private_key(privkey, password=None, backend=self.backend)
        decryptor = privkey.decryptor(
            asym_padding.OAEP
**CONTINUING CIPHER IMPLEMENTATION**
```python
(
    mgf=asym_padding.MGF1(algorithm=hashlib.sha256()),
    algorithm=hashlib.sha256(),
    label=None
)
)
return decryptor.update(ciphertext)
def sign_data_hmac(self, data, key):
    return hmac.new(key, data, hashlib.sha256).digest()
def verify_signature_hmac(self, signature, data, key):
    expected_signature = self.sign_data_hmac(data, key)
    return hmac.compare_digest(expected_signature, signature)
def sign_data_rsa(self, data, privkey):
    from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
    from cryptography.hazmat.primitives import serialization
    privkey = serialization.load_pem_private_key(privkey, password=None, backend=self.backend)
    signer = privkey.signer(
        asym_padding.PSS(
            mgf=asym_padding.MGF1(algorithm=hashlib.sha256()),
            salt_length=asym_padding.PSS.MAX_LENGTH
        ),
        hashlib.sha256()
    )
    return signer.update(data).finalize()
def verify_signature_rsa(self, signature, data, pubkey):
    from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
    from cryptography.hazmat.primitives import serialization
    pubkey = serialization.load_pem_public_key(pubkey, backend=self.backend)
    verifier = pubkey.verifier(
        asym_padding.PSS(
            mgf=asym_padding.MGF1(algorithm=hashlib.sha256()),
            salt_length=asym_padding.PSS.MAX_LENGTH
        ),
        hashlib.sha256()
    )
    verifier.update(data)
    verifier.verify(signature)
