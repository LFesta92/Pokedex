import base64
import hashlib

import bcrypt
from cryptography.fernet import Fernet


# Racchiude le utility di sicurezza usate per utenti e credenziali.
class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        # Usa bcrypt con salt automatico per evitare password prevedibili.
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, password_hash) -> bool:
        # Confronta la password inserita con l'hash salvato nel database.
        password_bytes = password.encode("utf-8")
        hash_bytes = password_hash.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hash_bytes)

    @staticmethod
    def generate_key(master_password: str) -> bytes:
        # Deriva una chiave simmetrica semplice a partire da una password master.
        digest = hashlib.sha256(master_password.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(digest)

    @staticmethod
    def encrypt_password(plain_password: str, master_password: str) -> str:
        # Utile se in futuro serviranno credenziali cifrate recuperabili.
        key = SecurityManager.generate_key(master_password)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(plain_password.encode("utf-8"))
        return encrypted.decode("utf-8")

    @staticmethod
    def decrypt_password(encrypted_password: str, master_password: str) -> str:
        # Decifra il valore solo se viene usata la stessa password master.
        key = SecurityManager.generate_key(master_password)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_password.encode("utf-8"))
        return decrypted.decode("utf-8")
