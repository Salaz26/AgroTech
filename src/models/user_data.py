# src/models/user_data.py
from pydantic import BaseModel

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    email: str