from fastapi import APIRouter, Depends
from DataBase.connection import SessionLocal
from Controllers.categoria_controller import *
from Models.categoria import *

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
categoria_routes = APIRouter()


@categoria_routes.get('s', tags=["Categoria"])
def traer_categorias(db=Depends(get_db)):
    categorias = get_traer_categorias(db)
    return categorias

@categoria_routes.post('', tags=["Categoria"])
def registrar_categoria(categoria: CategoriaRegistro, db=Depends(get_db)):
    categoria_registrada = post_registrar_categoria(db, categoria)
    return categoria_registrada

@categoria_routes.put('', tags=["Categoria"])
def actualizar_categoria(id_categoria: int, categoria: CategoriaRegistro, db=Depends(get_db)):
    categoria_actualizada = put_actualizar_categoria(db, id_categoria, categoria)
    return categoria_actualizada

@categoria_routes.delete('', tags=["Categoria"])
def eliminar_categoria(id_categoria: int, db=Depends(get_db)):
    categoria_eliminada = delete_categoria(db, id_categoria)
    return categoria_eliminada
