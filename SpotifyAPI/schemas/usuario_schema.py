from typing import List, Optional
from pydantic import BaseModel as SCBaseModel, HttpUrl

class UsuarioBase(SCBaseModel):
    
    id_usuario: int
    nome: str
    username: str
    password: str
    
    class Config:
        orm_mode = True