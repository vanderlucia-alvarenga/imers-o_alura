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

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

async def get_session() -> Generator: # type: ignore
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

    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro na autenticação")
    
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario ou senha Incorreta")

    finally:
        if usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")

    return usuario
