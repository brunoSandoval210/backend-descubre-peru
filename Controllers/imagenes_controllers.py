from sqlalchemy import text
from fastapi import HTTPException


# Listar imagen por el id
def get_listar_imagen_id(id_imagen, db):

    try:
        query = text(
            """SELECT
                    imagenes_registro_nombre, 
                    imagenes_registro_type, 
                    imagenes_registro_url,
                    imagenes_registro_public_id
                FROM 
                    imagenes_registro
                WHERE 
                    imagenes_registro_id=:id_imagen;""")

        usuarios = db.execute(query, {"id_imagen": id_imagen}).fetchone()

        if usuarios:
            imagen_encontrado = {
                "Nombre": usuarios.imagenes_registro_nombre,
                "type": usuarios.imagenes_registro_type,
                "url": usuarios.imagenes_registro_url,
                "public id": usuarios.imagenes_registro_public_id
            }

            return imagen_encontrado
        else:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado")

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Listar imagenes


def get_listar_imagenes(db):
    try:
        query = text("""
                    SELECT
                        imagenes_registro_id,
                        imagenes_registro_nombre,
                        imagenes_registro_type,
                        imagenes_registro_url,
                        imagenes_registro_public_id
                    FROM 
                        imagenes_registro
                    WHERE 
                        status=1
                        """)
        imagenes = db.execute(query).fetchall()
        imagenes_resultados = [{
            "Id": imagen.imagenes_registro_id,
            "Nombre": imagen.imagenes_registro_nombre,
            "Tipo": imagen.imagenes_registro_type,
            "Url": imagen.imagenes_registro_url,
            "Public id": imagen.imagenes_registro_public_id
        } for imagen in imagenes]
        return imagenes_resultados
    except Exception as e:
        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al listar las imagenes", "res": False, "error": str(e)})

# Registrar imagen en la base de datos


def post_guardar_imagen_db(imagenRegistro, db):
    try:
        query = text("""
                    INSERT INTO 
                        imagenes_registro
                        (
                        imagenes_registro_nombre,
                        imagenes_registro_public_id,
                        imagenes_registro_url,
                        imagenes_registro_type,
                        imagenes_registro_negocio_id,
                        imagenes_registro_usuario_id
                        )
                    VALUES(
                        :nombre,
                        :public_id,
                        :url,
                        :type,
                        :negocio_id,
                        :usuario_id
                        )
                    """)
        db.execute(query, {
            "nombre": imagenRegistro.nombre,
            "public_id": imagenRegistro.public_id,
            "url": imagenRegistro.url,
            "type": imagenRegistro.type,
            "negocio_id": imagenRegistro.negocio_id,
            "usuario_id": imagenRegistro.usuario_id

        })
        db.commit()
        return {"mensaje": "Imagen registrada correctamente", "res": True}

    except Exception as e:
        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al registrar la imagen", "res": False, "error": str(e)})

# Actualizar imagen


def put_actualizar_imagen_db(public_id, imagen_actualizar, db):
    try:
        query = text("""
                    UPDATE 
                        imagenes_registro
                    SET
                        imagenes_registro_nombre =:nombre,
                        imagenes_registro_public_id = :public__id,
                        imagenes_registro_url = :url,
                        imagenes_registro_type = :type,
                    WHERE
                        imagenes_registro_id=:id_imagen""")
        db.execute(query, {
            "nombre": imagen_actualizar.nombre,
            "public__id": imagen_actualizar.public_id,
            "url": imagen_actualizar.url,
            "type": imagen_actualizar.type,
            "id_imagen": public_id
        })
        db.commit()
        return {"mensaje": "Imagen actualizada correctamente", "res": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al actualizar la imagen", "res": False, "error": str(e)})


def delete_imagen_db(imagen_id, db):
    try:

        query_status = text("""
            SELECT status FROM imagenes_registro
            WHERE imagenes_registro_id = :id_imagenes_registro_id
        """)
        status_result = db.execute(
            query_status, {"id_imagenes_registro_id": imagen_id}).fetchone()

        if status_result is None:
            raise HTTPException(status_code=404, detail={
                "mensaje": "La imagen no fue encontrada", "res": False})

        status = status_result[0]

        if status == 0:
            return {"mensaje": "La imagen ya ha sido eliminada", "res": False}
        elif status == 1:
            query = text("""
                    UPDATE 
                        imagenes_registro
                    SET
                        status = 0
                    WHERE
                        imagenes_registro_id=:imagenes_registro_id""")
            db.execute(query, {
                "imagenes_registro_id": imagen_id
            })
            db.commit()
            return {"mensaje": "Imagen eliminada correctamente", "res": True}

    except Exception as e:
        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al eliminar la imagen", "res": False, "error": str(e)})
