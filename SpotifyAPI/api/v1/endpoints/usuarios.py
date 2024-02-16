from typing import List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import Oauth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.ext import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioBase
from core.deps import get_session, get_current_user
from core.security import get_hashed_password, verify_password
from core.auth import autenticar, cria_token_acesso

router = APIRouter()

# Criando o Login
@router.post("/login", response_model=UsuarioBase)
def login(form_data: Oauth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    usuario = autenticar(session, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    return usuario

# Criando o Registro
@router.post("/signup", response_model=UsuarioBase)
async def signup(usuario: UsuarioBase, session: AsyncSession = Depends(get_session)):
    try:
        async with session as db:
            usuario_db = UsuarioModel(**usuario.dict(), password=get_hashed_password(usuario.password))
            db.add(usuario_db)
            await db.commit()
            await db.refresh(usuario_db)
            return usuario_db
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário já cadastrado")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# Criando o Logout
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
    return {"detail": "Deslogado com sucesso"}

