from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.musicas_model import MusicaModel
from schemas.musicas_schema import MusicaBase
from models.usuario_model import UsuarioModel

from core.deps import get_session, get_current_user

router = APIRouter()

@router.get("/", response_model=List[MusicaBase])
async def get_musicas(session: AsyncSession = Depends(get_session)):
    async with session as db:
        query = select(MusicaModel)
        result = await db.execute(query)
        return result.scalars().all()

@router.get("/{id_musica}", response_model=MusicaBase)
async def get_musica(id_musica: int, session: AsyncSession = Depends(get_session)):
    async with session as db:
        query = select(MusicaModel).where(MusicaModel.id_musica == id_musica)
        result = await db.execute(query)
        return result.scalars().first()

@router.post("/", response_model=MusicaBase)
async def create_musica(musica: MusicaBase, session: AsyncSession = Depends(get_session), usuario: UsuarioModel = Depends(get_current_user)):
    async with session as db:
        musica_db = MusicaModel(id_musica = musica.id_musica, nome = musica.nome, artista = musica.artista, genero = musica.genero, pais = musica.pais, usuario = usuario)
        db.add(musica_db)
        await db.commit()
        await db.refresh(musica_db)
        return musica_db
    

# Busca musica por artista
@router.get("/artista/{artista}", response_model=List[MusicaBase])
async def get_musica_artista(artista: str, session: AsyncSession = Depends(get_session)):
    async with session as db:
        query = select(MusicaModel).where(MusicaModel.id_artista == artista)
        result = await db.execute(query)
        return result.scalars().all()

# Busca musica por genero
@router.get("/genero/{genero}", response_model=List[MusicaBase])
async def get_musica_genero(genero: str, session: AsyncSession = Depends(get_session)):
    async with session as db:
        query = select(MusicaModel).where(MusicaModel.id_genero == genero).join(genero)
        result = await db.execute(query)
        return result.scalars().all()