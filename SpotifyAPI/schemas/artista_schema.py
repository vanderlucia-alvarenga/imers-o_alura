from typing import List, Optional
from pydantic import BaseModel as SCBaseModel, HttpUrl

class ArtistaBase(SCBaseModel):
    id_artista: int
    nome: str
    id_pais: int
    id_genero: int
    
    class Config:
        orm_mode = True
        