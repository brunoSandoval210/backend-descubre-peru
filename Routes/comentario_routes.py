from fastapi import APIRouter,Depends
from DataBase.connection import SessionLocal
from Controllers.comentarios_controllers import *
from Models.comentarios_registro import *

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
comentario_routes=APIRouter()

#Se implementara el listar los comentarios del negocio
@comentario_routes.get('s/negocio',tags=["Comentario"])
def comentarios_negocio(negocio_id:int,page:int=1, per_page:int=10,db=Depends(get_db)):
    comentarios_negocio=get_comentarios_negocio(negocio_id,page, per_page,db)
    return comentarios_negocio

#Listar Comentario por usuario
@comentario_routes.get('s', tags=["Comentario"])
def listar_comentario_usuario(usuario_id:int,db=Depends(get_db)):
    comentario = get_listar_comentario_usuario(usuario_id,db)
    return comentario

#Ingresar Comentario
@comentario_routes.post("", tags=[ "Comentario" ])
def registrar_comentarios(comentario: RegistrarComentario,db=Depends(get_db)):
    comentario_negocio_descripcion = insertar_comentario_negocio( comentario, db)
    return comentario_negocio_descripcion

#Se actualizara el comentario
@comentario_routes.put('', tags=["Comentario"])
def actualizar_comentario(comentario: comentarioDescripcionUpdate,comentarios_negocios_id:int, db=Depends(get_db)):
    comentarioActualizado = update_comentario(comentario,comentarios_negocios_id,db)
    return comentarioActualizado

#Se eliminara el comentario del negocio
@comentario_routes.delete('',tags=["Comentario"])
def eliminar_comentario(comentario_id:int,db=Depends(get_db)):
    comentario_eliminado=delete_comentario(comentario_id,db)
    return comentario_eliminado