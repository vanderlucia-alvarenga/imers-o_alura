from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.__all_models import GeneroModel
from schemas.genero_schema import GeneroBase
from models.usuario_model import UsuarioModel

from core.deps import get_session, get_current_user


router = APIRouter()

@router.get("/", response_model=List[GeneroBase])
async def get_generos(session: AsyncSession = Depends(get_session)):
    async with session as db:
        query = select(GeneroModel)
        result = await db.execute(query)
        return result.scalars().all()

@router.get("/{id_genero}", response_model=GeneroBase)
async def get_genero(id_genero: int, session: AsyncSession = Depends(get_session)):
    async with session as db:
        query = select(GeneroModel).where(GeneroModel.id_genero == id_genero)
        result = await db.execute(query)
        return result.scalars().first()

@router.post("/", response_model=GeneroBase)
async def create_genero(genero: GeneroBase, session: AsyncSession = Depends(get_session)):
    async with session as db:
        genero_db = GeneroModel(id_genero = genero.id_genero, genero = genero.genero)
        db.add(genero_db)
        await db.commit()
        await db.refresh(genero_db)
        return genero_db