from fastapi import APIRouter, Depends, File, UploadFile
from DataBase.connection import SessionLocal
from Controllers.imagenes_controllers import *
from Services.Cloudinary import *
from Models.imagen import *
from typing import Optional
import uuid


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


imagenes_routes = APIRouter()


# Listar por id
@imagenes_routes.get('', tags=["Imagenes"])
def listar_imagen_id(id_imagen: int, db=Depends(get_db)):
    imagen_id = get_listar_imagen_id(id_imagen, db)
    return imagen_id

# Listar imagenes


@imagenes_routes.get("es", tags=["Imagenes"])
def listar_imagenes(db=Depends(get_db)):
    imagenes = get_listar_imagenes(db)
    return imagenes

# Guardar imagen


@imagenes_routes.post('', tags=["Imagenes"])
async def subir_imagen(
    negocio_id: Optional[int] = None,
    usuario_id: Optional[int] = None,
    imagen: UploadFile = File(...),
    carpeta: str = "",
    db=Depends(get_db)
):
    resultado_subida = post_guardar_imagen(imagen.file, carpeta)
    public_id = resultado_subida.get('public_id')
    nombre = str(uuid.uuid4()) + "_"+imagen.filename
    url = resultado_subida.get('url')
    type = resultado_subida.get('type')

    imagenRegistro = ImagenRegistro(
        nombre=nombre,
        public_id=public_id,
        url=url,
        type=type,
        negocio_id=negocio_id,
        usuario_id=usuario_id
    )
    imagen_db = post_guardar_imagen_db(imagenRegistro, db)
    return imagen_db

# Actualizar imagen


@imagenes_routes.put('', tags=["Imagenes"])
async def actualizar_imagen(public_id: str, imagen: UploadFile = File(...), db=Depends(get_db)):
    resultado_subida = put_actualizar_imagen(public_id, imagen.file)
    publicid = resultado_subida.get('public_id')
    url = resultado_subida.get('url')
    type = resultado_subida.get('type')
    nuevonombre = str(uuid.uuid4()) + "_"+imagen.filename
    imagen_actualizar = ImagenActualizar(
        nombre=nuevonombre,
        public_id=publicid,
        url=url,
        type=type,
    )
    actualizarImagen = put_actualizar_imagen_db(
        public_id, imagen_actualizar, db)
    return actualizarImagen

# Eliminar imagen


@imagenes_routes.delete('', tags=["Imagenes"])
async def actualizar_imagen(public_id: str):
    resultado_subida = delete_eliminar_imagen(public_id)
    return resultado_subida


@imagenes_routes.delete('/deleteBD', tags=["Imagenes"])
def eliminar_imagen(imagen_id: str, db=Depends(get_db)):
    imagen_eliminada = delete_imagen_db(imagen_id, db)
    return imagen_eliminada
