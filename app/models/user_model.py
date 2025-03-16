from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id:str
    email:str
    password:str
    full_name:str
    role:str = "user"
    created_at:int = int(datetime.timestamp(datetime.now()))

