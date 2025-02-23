from cryptography.fernet import Fernet

class EncryptionManager:
    def __init__(self, key=None):
        if key is None:
            key = Fernet.generate_key()
        self.cipher = Fernet(key)

    def encrypt_data(self, data):
        return self.cipher.encrypt(data.encode('utf-8')).decode('utf-8')

    def decrypt_data(self, token):
        return self.cipher.decrypt(token.encode('utf-8')).decode('utf-8')
