from typing import List, Optional
from pydantic import BaseModel as SCBaseModel, HttpUrl

class UsuarioBase(SCBaseModel):
    
    id_usuario: int
    nome: str
    username: str
    pwd: str
    
    class Config:
        orm_mode = True
        
class UsuarioLogin(SCBaseModel):
    
    username: str
    pwd: str
    
    class Config:
        orm_mode = True