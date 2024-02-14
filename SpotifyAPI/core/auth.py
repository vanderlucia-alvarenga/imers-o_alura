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
from core.security import verificar_senha
from pydantic import EmailStr

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/usr/login'
)

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as sess:
        try:
            query = select(UsuarioModel).filter(UsuarioModel.email == email)
            result = await sess.execute(query)
            usuario: UsuarioModel = result.scalar().unique().one_or_none()

            if not usuario:
                return None
            if not verificar_senha(senha, usuario.senha): return None

        except Exception as e:
            raise HTTPException(status_code=status.500_INTERNAL_SERVER_ERROR, detail="Erro ao autenticar o usuário")
        finally:
            return usuario


def cria_token(tipo_token: str, sub: str) -> str:
    payload = {}
    zona = timezone('America/Sao_Paulo')

    payload['type'] = tipo_token
    payload['sub'] = str(sub)
    return jwt.encode(payload, settings.JWT_secret, algorithm=settings.ALGORITHM)

def cria_token_acesso(email: str) -> str:
    return cria_token("access_token", email)