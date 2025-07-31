from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime,date
from DataBase.connection import SessionLocal, engine
from pydantic import BaseModel

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UsuarioRegistro(BaseModel):
    usuario_nombres: str
    usuario_apellidos: str
    usuario_fecha_de_nacimiento: date
    usuario_dni: int
    usuario_tipo_usuario_id: int
    usuario_email: str
    usuario_password: str

class UsuarioActualizar(BaseModel):
    usuario_nombres: str
    usuario_apellidos: str
    usuario_fecha_de_nacimiento: date
    usuario_dni: int
    usuario_tipo_usuario_id: int
    usuario_email: str
    usuario_password: str



