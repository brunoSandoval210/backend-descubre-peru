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

#Registrar Comentario
class RegistrarComentario(BaseModel):
    negocio_id: int
    usuario_id: int
    descripcion: str

#Actualizar comentario
class comentarioDescripcionUpdate(BaseModel):
    descripcion: str