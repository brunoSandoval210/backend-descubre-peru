from sqlalchemy import text
from fastapi import HTTPException,status,Depends
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from Models.usuario_login import TokenData,User
from DataBase.connection import SessionLocal
from os import getenv

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuario/login")

ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, email: str):
    query = text(
        """SELECT 
                usuario_nombres AS nombres,
                usuario_apellidos AS apellidos,
                usuario_email AS email,
                usuario_dni,
                usuario_password AS contrasena,
                status 
            FROM 
                usuario 
            WHERE 
                usuario_email = :usuario_email
            AND status = 1 """)
    usuario = db.execute(query, {"usuario_email": email}).fetchone()
    
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

def authenticate_user(db,email: str, contrasena: str):

   
    usuario_credenciales=get_user(db,email)
    if usuario_credenciales is None:
        return False
    if not verify_password(contrasena, usuario_credenciales.contrasena):
        return False
    return usuario_credenciales


def create_access_token(data: dict, expires_delta: timedelta | None=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, getenv("SECRET_KEY"), algorithms=[getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db=next(get_db())
    user = get_user(db, email=token_data.username)

    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.status == 0:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
