from typing import List, Optional

from fastapi  import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.__all_models import PaisModel
from schemas.pais_schema import PaisBase
from models.usuario_model import UsuarioModel
from core.deps import get_session, get_current_user

router = APIRouter()

@router.get("/", response_model=List[PaisBase])
async def get_paises(session: AsyncSession = Depends(get_session), usuario: UsuarioModel = Depends(get_current_user)):
    async with session as db:
        query = select(PaisModel)
        result = await db.execute(query)
        return result.scalars().all()
    
@router.get("/{id_pais}", response_model=PaisBase)
async def get_pais(id_pais: int, session: AsyncSession = Depends(get_session)):
    async with session as db:
        query = select(PaisModel).where(PaisModel.id_pais == id_pais)
        result = await db.execute(query)
        return result.scalars().first()

@router.post("/", response_model=PaisBase)
async def create_pais(pais: PaisBase, session: AsyncSession = Depends(get_session), usuario: UsuarioModel = Depends(get_current_user)):
    async with session as db:
        pais_db = PaisModel(id_pais = pais.id_pais, pais = pais.pais)
        db.add(pais_db)
        await db.commit()
        await db.refresh(pais_db)
        return pais_db