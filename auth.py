from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Yeh secret key hai — token banane mein use hoti hai
# Real project mein yeh .env file mein hoti hai
SECRET_KEY = "taskflow-secret-key-123"

# Token banane ka algorithm
ALGORITHM = "HS256"

# Token kitne minutes tak valid rahega
TOKEN_EXPIRE_MINUTES = 30

# Password hashing ka setup
# bcrypt — sabse secure hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    # Plain password ko hash mein badlo
    # "ranjit123" → "$2b$12$xyz..." jaisa ban jaata hai
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    # Login mein — plain password aur hashed compare karo
    # Sahi hai toh True, galat hai toh False
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    # Token banao — user ka data andar hoga
    to_encode = data.copy()

    # Token expire time set karo
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Token encode karo aur return karo
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        # Token decode karo — data nikalo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Token galat ya expire ho gaya
        return None