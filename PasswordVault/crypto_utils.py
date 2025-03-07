import os
import logging
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Chave de desenvolvimento (APENAS PARA DESENVOLVIMENTO)
DEV_KEY = b'vFi6GxDWqjqHlrKm9jxmZ4v2VAFWj4bGuvjR_iVgMFE='

def get_encryption_key():
    """Get or create the encryption key"""
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        logger.warning("ENCRYPTION_KEY não encontrada nas variáveis de ambiente. Usando chave de desenvolvimento.")
        key = DEV_KEY
    return key if isinstance(key, bytes) else key.encode()

def initialize_fernet():
    """Initialize the Fernet instance with proper error handling"""
    try:
        key = get_encryption_key()
        return Fernet(key)
    except Exception as e:
        logger.error(f"Erro ao inicializar Fernet: {str(e)}")
        raise Exception("Falha ao inicializar o sistema de criptografia")

# Initialize Fernet instance
fernet = initialize_fernet()

def encrypt_password(password):
    """Encrypt a password using Fernet (AES)"""
    try:
        if not password:
            raise ValueError("A senha não pode estar vazia")
        encrypted = fernet.encrypt(password.encode())
        logger.debug("Senha criptografada com sucesso")
        return encrypted.decode()
    except Exception as e:
        logger.error(f"Erro na criptografia: {str(e)}")
        raise Exception(f"Falha ao criptografar a senha: {str(e)}")

def decrypt_password(encrypted_password):
    """Decrypt a password using Fernet (AES)"""
    try:
        if not encrypted_password:
            raise ValueError("A senha criptografada não pode estar vazia")
        decrypted = fernet.decrypt(encrypted_password.encode())
        logger.debug("Senha descriptografada com sucesso")
        return decrypted.decode()
    except Exception as e:
        logger.error(f"Erro na descriptografia: {str(e)}")
        raise Exception(f"Falha ao descriptografar a senha: {str(e)}")