from sqlalchemy import text
from fastapi import HTTPException

def get_traer_categorias(db):
    try:
        query = text("""
                    SELECT 
                        negocio_categoria_id,descripcion 
                    FROM 
                        negocio_categoria 
                    WHERE 
                        status=1""")
        categorias = db.execute(query).fetchall()
        categorias_result = [{
            "id": categorias.negocio_categoria_id,
            "nombre": categorias.descripcion
        } for categorias in categorias]
     
        return categorias_result
    except Exception as e:
        raise HTTPException(status_code=404, detail={"mensaje": "Error al obtener las categorias", "error": str(e) ,"res": False})
    
def post_registrar_categoria(db, categoria):
    try:
        query = text("""
                     INSERT INTO negocio_categoria (descripcion) VALUES(:descripcion)""")
        db.execute(query, {"descripcion": categoria.descripcion})
        db.commit()
        return {"mensaje": "Categoria registrada", "res": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail={"mensaje": "Error al registrar la categoria", "error": str(e) ,"res": False})
    
def put_actualizar_categoria(db,id_categoria, categoria):
    try:
        query = text("""
                        UPDATE negocio_categoria SET descripcion=:descripcion WHERE negocio_categoria_id=:id_categoria""")
        db.execute(query, {"descripcion": categoria.descripcion, "id_categoria": id_categoria})
        db.commit()
        return {"mensaje": "Categoria actualizada", "res": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail={"mensaje": "Error al actualizar la categoria", "error": str(e) ,"res": False})
    
def delete_categoria(db, id_categoria):
    try:
        query = text("""
                     UPDATE negocio_categoria SET status=0 WHERE negocio_categoria_id=:id_categoria""")
        db.execute(query, {"id_categoria": id_categoria})
        db.commit()
        return {"mensaje": "Categoria eliminada", "res": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail={"mensaje": "Error al eliminar la categoria", "error": str(e) ,"res": False})