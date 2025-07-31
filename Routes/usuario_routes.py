from fastapi import Depends, APIRouter, status, HTTPException
from DataBase.connection import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from Controllers.usuario_controllers import *
from typing import Annotated
from Models import usuario_registro
from datetime import timedelta
from Models.usuario_login import Token, User
from Security.function_jwt import *
from sqlalchemy.orm import Session
from Models.usuario_registro import UsuarioRegistro,UsuarioActualizar


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


usuario_routes = APIRouter()

#Validar token usuario
@usuario_routes.get("/validar/token", response_model=User, tags=["Usuarios"])
async def validar_token(current_user: User = Depends(get_current_active_user)):
    return current_user

# Listar por DNI
@usuario_routes.get("/dni", tags=["Usuarios"])
def listar_usuario_dni(usuario_dni: str, db=Depends(get_db)):
    usuarios_dni = get_listar_usuario_dni(usuario_dni, db)
    return usuarios_dni

#Listar Usuarios
@usuario_routes.get('s', tags=["Usuarios"])
def listar_usuario(page:int=1, per_page:int=10 ,db=Depends(get_db)):
    usuarios = get_listar_usuario(page,per_page,db)
    return usuarios

#Listar por id
@usuario_routes.get('', tags=["Usuarios"])
def listar_usuario_id(id_usuario: int, db=Depends(get_db)):
    usuarios_id = get_listar_usuario_id(id_usuario, db)
    return usuarios_id

# Registrar Usuario
@usuario_routes.post('', tags=["Usuarios"])
def registrar_usuario(usuario: UsuarioRegistro, db=Depends(get_db)):
    usuario_registro = get_registrar_usuario(usuario, db)
    return usuario_registro

#Login usuario
@usuario_routes.post("/login", tags=["Usuarios"])
async def login_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)
) -> Token:
    authenticated_user = authenticate_user(
        db, form_data.username, form_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW -Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": authenticated_user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")

# Editar Usuario
@usuario_routes.put('', tags=["Usuarios"])
def registrar_usuario(id_usuario:int,usuario: UsuarioActualizar, db=Depends(get_db)):
    usuario_registro = get_actualizar_usuario(id_usuario,usuario, db)
    return usuario_registro

# Eliminar usuario
@usuario_routes.delete('', tags=["Usuarios"])
def eliminar_usuario(id_usuario_eli: str, db=Depends(get_db)):
    elimi_usuarios = get_eliminar_usuario(id_usuario_eli, db)
    return elimi_usuarios

