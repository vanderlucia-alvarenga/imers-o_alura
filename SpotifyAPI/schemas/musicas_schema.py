from typing import List, Optional
from pydantic import BaseModel as SCBaseModel, HttpUrl

class MusicaBase(SCBaseModel):
    id_musica: int
    nome: str
    duracao: int
    id_album: int
    id_artista: int
    
    class Config:
        orm_mode = True