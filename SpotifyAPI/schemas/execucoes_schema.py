from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel as SCBaseModel, HttpUrl

class ExecucaoBase(SCBaseModel):
    id_exec: int
    id_usuario: int
    id_musica: int
    id_artista: int
    hora_exec: datetime
    
    class Config:
        orm_mode = True