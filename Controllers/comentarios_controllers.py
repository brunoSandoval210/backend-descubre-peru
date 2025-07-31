from fastapi import HTTPException
from sqlalchemy import text
from datetime import datetime
from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy.sql import text
from fastapi import HTTPException
from DataBase.connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Registrar un comentario
def insertar_comentario_negocio(comentario, db):
    try:
        # Verificar si el negocio existe
        query_busqueda = text("""
                            SELECT
                                negocio_id
                            FROM
                                negocio
                            WHERE
                                negocio_id = :negocio_id
                            """)
        resultado = db.execute(query_busqueda, {"negocio_id": comentario.negocio_id}).fetchone()

        if resultado:
            # El negocio existe, insertar la descripción
            query_insertar = text("""
                                INSERT INTO
                                comentarios_negocios
                                (
                                comentarios_negocios_negocio_id,
                                comentarios_negocios_usuario_id,
                                comentario_negocio_descripcion
                                )
                                VALUES
                                (
                                :negocio_id,
                                :usuario_id,
                                :descripcion
                                )
                                """)
            db.execute(query_insertar, {"negocio_id": comentario.negocio_id,"usuario_id": comentario.usuario_id, "descripcion": comentario.descripcion})
            db.commit()
            return {"mensaje": "Descripción insertada correctamente", "res": True}
        else:
            return {"mensaje": "No se encontró el negocio con el ID proporcionado", "res": False}

    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error en la base de datos: {str(e)}"
        )


#Se listara los comentarios hechos por el usuario
def get_listar_comentario_usuario(usuario_id,db):
    try:
        query = text(
                """SELECT
                        CN.comentario_negocio_descripcion,
                        ND.nd_negocio_nombre,
                        U.usuario_nombres
                    FROM
                        comentarios_negocios as CN
                    INNER JOIN
                        usuario AS U ON U.usuario_id = CN.comentarios_negocios_usuario_id
                    INNER JOIN
                        negocio_descripcion AS ND ON ND.negocio_descripcion_id = CN.comentarios_negocios_negocio_id
                    where
                    CN.status=1 
                    AND
                    U.usuario_id=:usuario_id;""")

        usuarios = db.execute(query, {"usuario_id": usuario_id}).fetchall()
        if usuarios:
            usuarios_resultados = [{
                "Comentario del usuario": usuarios.comentario_negocio_descripcion,
                "Nombre del negocio": usuarios.nd_negocio_nombre,
                "Nombre de usuario": usuarios.usuario_nombres
            }for usuarios in usuarios]
            return usuarios_resultados
        else:
            raise HTTPException(status_code=404, detail={
                                "mensaje": "El negocio no existe", "res": False})
    except Exception as e:
        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al listar los comentarios del usuario", "res": False, "error": str(e)})


#Se implementara el listar los comentarios del negocio
def get_comentarios_negocio(negocio_id,page, per_page,db):
    try:
        offset = (int(page) - 1) * int(per_page)
        query=text("""       
                SELECT 
                    usuario.usuario_nombres,
                    usuario.usuario_apellidos,
                    usuario.usuario_email,
                    negocio_descripcion.nd_negocio_nombre,
                    comentarios_negocios.comentario_negocio_descripcion
                FROM 
                    comentarios_negocios
                JOIN
                    usuario ON comentarios_negocios.comentarios_negocios_usuario_id=usuario.usuario_id
                JOIN 
                    negocio_descripcion ON  comentarios_negocios.comentarios_negocios_negocio_id=negocio_descripcion.nd_negocios_id
                WHERE 
                    comentarios_negocios.comentarios_negocios_negocio_id = :negocio_id
                AND 
                    comentarios_negocios.status = 1
                AND
                    usuario.status=1
                AND
                    negocio_descripcion.status =1
                LIMIT 
                    :per_page OFFSET :offset;
                """)
        comentarios=db.execute(query,{"negocio_id":negocio_id,"per_page": int(per_page), "offset": offset}).fetchall()
        if comentarios:
            comentarios_resultado=[{
                "Nombres":comentario.usuario_nombres,
                "Apellidos":comentario.usuario_apellidos,
                "Email":comentario.usuario_email,
                "Nombre de la empresa":comentario.nd_negocio_nombre,
                "Comentario":comentario.comentario_negocio_descripcion
            } for comentario in comentarios]
 
        return comentarios_resultado
    except Exception as e:
        raise HTTPException(status_code=400,detail={"mensaje":"Error al listar los comentarios del negocio","res":False,"error":str(e)})


#Se eliminara el comentario del negocio
def delete_comentario(comentario_id,db):
    try:
        query=text(""" 
                    UPDATE 
                        comentarios_negocios
                    SET 
                        status = 0
                    WHERE 
                        comentarios_negocios_id = :comentario_id
                
                """)
        db.execute(query,{"comentario_id":comentario_id})
        db.commit()
        return {"message":"Comentario eliminado","res":True}
    except Exception as e:
        raise HTTPException(status_code=400,detail={
            "mensaje": "Error al eliminar el comentario del negocio","res":False,"error":str(e)})


#Actualizar comentario negocio
def update_comentario(comentario,comentarios_negocios_id, db):
    try:  
        # Actualizar el comentario del negocio específico
        query_editar = text("""
                        UPDATE  
                            comentarios_negocios
                        SET
                            comentario_negocio_descripcion = :descripcion
                        WHERE
                            comentarios_negocios_id = :comentarios_negocios_id
                        """)
        db.execute(query_editar, {
            "descripcion": comentario.descripcion,
            "comentarios_negocios_id": comentarios_negocios_id
        })
        db.commit()
        return {"message": "Se actualizó correctamente el comentario", 'data': comentario}
    
    except IntegrityError as ie:
        db.rollback()
        raise HTTPException(status_code=422, detail={"message": "Error de integridad al actualizar comentario", "res": False, "error": str(ie)})
    except DatabaseError as de:
        db.rollback()
        raise HTTPException(status_code=500, detail={"message": "Error de base de datos al actualizar comentario", "res": False, "error": str(de)})