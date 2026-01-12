from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd.hash(password)

def verify_password(password, hashed):
    return pwd.verify(password, hashed)
