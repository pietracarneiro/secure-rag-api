import bcrypt
import jwt
from datetime import datetime, timedelta

# ATENÇÃO: Em produção, isso nunca fica direto no código (hardcoded). 
# Guardamos em variáveis de ambiente, mas para o nosso estudo, usaremos assim:
SECRET_KEY = "uma_chave_super_secreta_e_longa_para_o_nosso_projeto_rag"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    """Transforma a senha limpa em um hash seguro usando bcrypt nativo"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha digitada bate com o hash salvo"""
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def create_access_token(data: dict) -> str:
    """Gera o crachá digital (Token JWT) assinado pela API"""
    to_encode = data.copy()
    # Define quando o crachá vai expirar
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Criptografa os dados e assina com a nossa chave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt