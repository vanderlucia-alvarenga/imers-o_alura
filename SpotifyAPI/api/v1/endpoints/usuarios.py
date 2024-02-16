from typing import List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioBase, UsuarioLogin
from core.deps import get_session, get_current_user
from core.security import get_hashed_password, verify_password
from core.auth import autenticar, cria_token_acesso

router = APIRouter()

# Criando o Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(username=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": cria_token_acesso(sub=usuario.id_usuario), "token_type": "bearer"}, status_code=status.HTTP_200_OK)

# Retornando o usuário logado
@router.get("/me", response_model=UsuarioBase)
async def me(usuario: UsuarioBase = Depends(get_current_user)):
    return usuario

# Retornando todos os usuários
@router.get("/", response_model=List[UsuarioBase])
async def get_usuarios(session: AsyncSession = Depends(get_session)):
    async with session as db:
        query = select(UsuarioModel)
        result = await db.execute(query)
        return result.scalars().all()

# Criando o Registro
@router.post("/signup", response_model=UsuarioBase)
async def signup(usuario: UsuarioBase, session: AsyncSession = Depends(get_session)):
    try:
        async with session as db:
            usuario_db = UsuarioModel(id_usuario = usuario.id_usuario,nome = usuario.nome, username = usuario.username, pwd = get_hashed_password(usuario.pwd))
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

