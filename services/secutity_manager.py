import bcrypt
from cryptography import Fernet
import base64
import hashlib

class SecurityManager:
    @staticmethod #metodo che prende la password e genera una password hashata e poi vi aggiunge il salt
    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        hashed= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        return hashed.decode('utf-8')

    @staticmethod # metodo per confrontare gli hash
    def verify_password(password: str, password_hash) -> bool:
        password_bytes = password.encode('utf-8')
        hash_bytes = password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)

    @staticmethod #metodo per generare una chiave di cifratura
    def generate_key(master_password:str)->bytes:
        digest = hashlib.sha256(master_password.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(digest)

    @staticmethod #metodo per cifrare password
    def encrypt_password(plain_password:str, master_password:str)->str:
        #creazione della chiave
        key=SecurityManager.generate_key(master_password)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(plain_password.encode('utf-8'))
        return encrypted.decode('utf-8')

    @staticmethod #metodo per decifrare la password
    def decrypt_password(encrypted_password:str, master_password:str)->str:
        key=SecurityManager.generate_key(master_password)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_password.encode('utf-8'))
        return decrypted.decode('utf-8')
