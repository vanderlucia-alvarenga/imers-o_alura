from typing import List, Optional
from pydantic import BaseModel as SCBaseModel, HttpUrl

class PaisBase(SCBaseModel):
        
        id_pais: int
        nome: str
        
        class Config:
            orm_mode = True