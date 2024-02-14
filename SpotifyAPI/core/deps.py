from typing import Generator, List, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, EmailStr
from core.database import Session as Session
from models.usuario_model import UsuarioModel
from core.auth import oauth2_scheme
from core.configs import settings

async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> UsuarioModel:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM], options={"verify_aud": False})
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credenciais Inválidas")
    token_data = TokenData(email=username)

    async with session as db:
        query = select(UsuarioModel).filter(UsuarioModel.username == token_data.id)

        result = await db.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario ou senha Incorreta")
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro na autenticação")

    finally:
        if usuario:
            return usuario
        raise httpException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> UsuarioModel:
    if not current_user.ativo:
        raise HTTPException(status_code=status.400_BAD_REQUEST, detail="Usuário Inativo")
    return current_user