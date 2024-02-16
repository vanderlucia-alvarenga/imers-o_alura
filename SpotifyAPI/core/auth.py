from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verify_password
from pydantic import EmailStr

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/usr/login'
)

async def autenticar(username: str, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.username == username)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None

        if not verify_password(senha, usuario.pwd):
            return None

        return usuario



def cria_token(tipo_token: str, sub: str) -> str:
    payload = {}
    zona = timezone('America/Sao_Paulo')

    payload['type'] = tipo_token
    payload['sub'] = str(sub)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def cria_token_acesso(sub: str) -> str:
    return cria_token("access_token", sub)