from fastapi import APIRouter, Depends
from Controllers.valoracion_controllers import *
from DataBase.connection import SessionLocal
from Models.valoracion import *


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


valoracion_routes = APIRouter()

# Registro de la valoración del negocio
@valoracion_routes.post('', tags=["Valoracion"])
def registrar_valoracion(valoracion: valoracion, db=Depends(get_db)):
    registro_de_valoración = post_registrar_valoracion(valoracion, db)
    return registro_de_valoración

# Actualización de la valoracion
@valoracion_routes.put('/Update', tags=["Valoracion"])
def actualizar_valoracion(valoracion_id: int, valoracion: valoracionUpdate, db=Depends(get_db)):
    valoracion_actualizada = update_valoracion(valoracion_id, valoracion, db)
    return valoracion_actualizada
