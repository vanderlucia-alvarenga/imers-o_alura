from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> bool:
    return CRIPTO.verify(plain_password, hashed_password)

def get_hashed_password(password: str) -> str:
    return CRIPTO.hash(password)
