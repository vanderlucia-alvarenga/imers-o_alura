from typing import List, Optional
from pydantic import BaseModel as SCBaseModel, HttpUrl

class AlbumBase(SCBaseModel):
    
    id_album: int
    nome: str
    id_artista: int
    ano_lancamento: int
    genero: int
    
    class Config:
        orm_mode = True