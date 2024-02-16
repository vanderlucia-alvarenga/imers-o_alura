from typing import List, Optional
from pydantic import BaseModel as SCBaseModel, HttpUrl

class PaisBase(SCBaseModel):
        
        id_pais: int
        pais: str
        
        class Config:
            orm_mode = True