from fastapi import APIRouter

from api.v1.endpoints import usuarios
from api.v1.endpoints import generos
from api.v1.endpoints import pais
from api.v1.endpoints import musicas

api_router = APIRouter()
api_router.include_router(usuarios.router, tags=["usuario"], prefix="/usuario")
api_router.include_router(generos.router, tags=["genero"], prefix="/genero")
api_router.include_router(pais.router, tags=["pais"], prefix="/pais")
api_router.include_router(musicas.router, tags=["musica"], prefix="/musica")
