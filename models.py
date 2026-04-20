from pydantic import BaseModel

# User register karne ka structure
# Jab koi register kare toh yeh data bhejega
class UserRegister(BaseModel):
    username: str
    password: str

# User login karne ka structure
class UserLogin(BaseModel):
    username: str
    password: str

# Task banane ka structure
# Jab koi nayi task add kare toh yeh data bhejega
class TaskCreate(BaseModel):
    title: str
    description: str

# Task update karne ka structure
# Task complete karna ya title change karna
class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool