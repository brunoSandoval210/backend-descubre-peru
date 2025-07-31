from fastapi import APIRouter, Depends
from DataBase.connection import SessionLocal
from Controllers.negocio_controllers import *
from Models.negocio_registro import *


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


negocio_routes = APIRouter()

# GET
# Listar empresas con su descripcion por categoria
@negocio_routes.get('/categoria', tags=["Negocio"])
def lista_negocio_categoria(categoria: str, nombre: str = None, page:int=1, per_page:int=10 ,db=Depends(get_db)):
    negocios = get_negocio_categoria(categoria, nombre,page,per_page,db)
    return negocios


# Buscar negocio por el nombre
@negocio_routes.get('/nombre', tags=["Negocio"])
def obtener_negocio(negocio_nombre: str, db=Depends(get_db)):
    negocio = get_obtener_negocio_nombre(negocio_nombre, db)
    return negocio

# Listar Negocio por RUC/RUC
@negocio_routes.get('/RUC', tags=["Negocio"])
def listar_negocio_por_ruc(negocio_ruc: str, db=Depends(get_db)):
    negocios_ruc = get_listar_negocio_ruc(negocio_ruc, db)
    return negocios_ruc

# Listar Negocio
@negocio_routes.get('s', tags=["Negocio"])
def listar_negocio(db=Depends(get_db), page:int=1, per_page:int=10):
    lista_negocio = get_listar_negocio(db, page, per_page)
    return lista_negocio

# POST
# Registrar Negocio
@negocio_routes.post('', tags=["Negocio"])
def registrar_negocio(negocio: NegocioRegistro, db=Depends(get_db)):
    negocio_registrado = get_registrar_negocio(negocio, db)
    return negocio_registrado

# Registrar descripcion del negocio
@negocio_routes.post('/descripcion', tags=["Negocio"])
def registrar_negocio_descripcion(negocioDescripcion: negocioDescripcionRegistro, db=Depends(get_db)):
    negocio_decripcion_registrado = post_registrar_negocio_descripcion(
        negocioDescripcion, db)
    return negocio_decripcion_registrado

# PUT
# Editar empresa
@negocio_routes.put('', tags=["Negocio"])
def editar_empresa(id_negocio: int, editar: edit_empresa, db=Depends(get_db)):
    empresa_edit = get_editar_empresa(id_negocio, editar, db)
    return empresa_edit

# Actualizacion de descripcion del negocio
@negocio_routes.put('/descripcion', tags=["Negocio"])
def actualizar_negocio_descripcion(negocio_descripcion_id: int, negocioDescripcion: negocioDescripcionUpdate, db=Depends(get_db)):
    negocio_descripcion_actualizado = update_negocio_descripcion(
        negocio_descripcion_id, negocioDescripcion, db)
    return negocio_descripcion_actualizado

# DELETE
# Eliminar negocio
@negocio_routes.delete('', tags=["Negocio"])
def eliminar_negocio(negocio_id: str, db=Depends(get_db)):
    negocio_eliminado = get_eliminar_negocio(negocio_id, db)
    return negocio_eliminado

@negocio_routes.get('/ubicacion', tags=["Negocio"])
def listar_negocio_ubicacion(negocio_nombre: str, db=Depends(get_db)):
    lista_negocio_ub = get_listar_negocio_ubicacion(negocio_nombre,db)
    return lista_negocio_ub

@negocio_routes.post('/ubicacion', tags=["Negocio"])
def actualizar_negocio_ubicacion(negocio_nombre: str, negocioUbicacion: negocioUbicacion, db=Depends(get_db)) :
    actualizar_negocio_ub = get_actualizar_negocio_ubicacion(negocio_nombre, negocioUbicacion, db)
    return actualizar_negocio_ub