from typing import List, Optional
from pydantic import BaseModel as SCBaseModel

class GeneroBase(SCBaseModel):
    id_genero: int
    nome: str
    
    class Config:
        orm_mode = True