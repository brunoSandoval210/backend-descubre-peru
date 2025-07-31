from sqlalchemy import text
from fastapi import HTTPException
import math

# Registrar el negocio
def get_registrar_negocio(negocio, db):
    try:
        query = text(
            """
            INSERT INTO negocio(
                usuario_id,
                negocio_ruc,
                negocio_categoria_id,
                negocio_razon_social,
                negocio_numero_telefonico_asociado)
            VALUES(
                :usuario_id,
                :negocio_ruc,
                :negocio_categoria_id,
                :negocio_razon_social,
                :negocio_numero_telefonico_asociado)
            """
        )
        db.execute(query, {
            "usuario_id": negocio.usuario_id,
            "negocio_ruc": negocio.negocio_ruc,
            "negocio_categoria_id": negocio.negocio_categoria_id,
            "negocio_razon_social": negocio.negocio_razon_social,
            "negocio_numero_telefonico_asociado": negocio.negocio_numero_telefonico_asociado
        })
        db.commit()
        return {"mensaje": "El negocio se registró correctamente", "res": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al registrar el negocio", "res": False, "error": str(e)})


# Editar la empresa por el id
def get_editar_empresa(id_negocio, editar, db):
    try:
        query = text("""
            UPDATE CCP.negocio
            SET
                usuario_id = :usuario_id,
                negocio_ruc = :negocio_ruc,
                negocio_categoria_id = :negocio_categoria_id,
                negocio_razon_social = :negocio_razon_social,
                negocio_numero_telefonico_asociado = :negocio_numero_telefonico_asociado
                WHERE negocio_id = :id_negocio;""")

        db.execute(query, {
            "usuario_id": editar.usuario_id,
            "negocio_ruc": editar.negocio_ruc,
            "negocio_categoria_id": editar.negocio_categoria_id,
            "negocio_razon_social": editar.negocio_razon_social,
            "negocio_numero_telefonico_asociado": editar.negocio_numero_telefonico_asociado,
            "id_negocio": id_negocio
        })
        db.commit()
        return {"mensaje": "Usuario modificado", "res": True}

    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error en la base de datos: {str(e)}")

# Listar negocio
def get_listar_negocio(db, page, per_page):
    offset = (int(page) - 1) * int(per_page)
    try:
        query = text(
            """
            SELECT
                negocio.negocio_ruc,
                negocio.negocio_razon_social,
                negocio.negocio_numero_telefonico_asociado,
                negocio_descripcion.nd_negocio_nombre,
                negocio_descripcion.nd_negocio_descripcion,
                negocio_descripcion.nd_negocio_direccion,
                negocio_descripcion.nd_negocio_logo,
                negocio_descripcion.nd_negocio_valoracion
            FROM
                negocio
            LEFT JOIN
                negocio_descripcion ON negocio.negocio_id = negocio_descripcion.nd_negocios_id
            WHERE
                negocio.status = 1 AND negocio_descripcion.status = 1
            LIMIT :per_page OFFSET :offset;
            """
        )

        negocios = db.execute(query, {"per_page": int(per_page), "offset": offset}).fetchall()

        negocios_resultados = [{
            "Ruc": negocio.negocio_ruc,
            "Razon social": negocio.negocio_razon_social,
            "Telefono asociado": negocio.negocio_numero_telefonico_asociado,
            "Nombre del negocio": negocio.nd_negocio_nombre,
            "Descripcion del negocio": negocio.nd_negocio_descripcion,
            "Direccion": negocio.nd_negocio_direccion,
            "Logo": negocio.nd_negocio_logo,
            "Valoracion": round(negocio.nd_negocio_valoracion) if negocio.nd_negocio_valoracion else None
        } for negocio in negocios]

        return negocios_resultados

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Listar negocio por el ruc
def get_listar_negocio_ruc(negocio_ruc, db):
    try:
        query = text(
            """
                SELECT
                    negocio.negocio_ruc,
                    negocio.negocio_razon_social,
                    negocio.negocio_numero_telefonico_asociado,
                    negocio_descripcion.nd_negocio_nombre,
                    negocio_descripcion.nd_negocio_descripcion,
                    negocio_descripcion.nd_negocio_direccion,
                    negocio_descripcion.nd_negocio_logo,
                    negocio_descripcion.nd_negocio_valoracion,
                    negocio.status
                FROM
                    negocio
                LEFT JOIN
                    negocio_descripcion ON negocio.negocio_id = negocio_descripcion.nd_negocios_id
                WHERE
                    negocio_ruc = :negocio_ruc;
            """
        )

        negocio = db.execute(query, {"negocio_ruc": negocio_ruc}).fetchone()

        if negocio:
            negocio_resultados = {
                "Ruc": negocio.negocio_ruc,
                "Razon social": negocio.negocio_razon_social,
                "Telefono asociado": negocio.negocio_numero_telefonico_asociado,
                "Nombre del negocio": negocio.nd_negocio_nombre,
                "Descripcion del negocio": negocio.nd_negocio_descripcion,
                "Direccion": negocio.nd_negocio_direccion,
                "Logo": negocio.nd_negocio_logo,
                "Valoracion": round(negocio.nd_negocio_valoracion) if negocio.nd_negocio_valoracion else None,
                "Status de Negocio": negocio.status
            }
            return negocio_resultados
        else:
            return None

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Buscar negocio por Nombre
def get_obtener_negocio_nombre(nd_negocio_nombre, db):

    try:
        query = text(
            """
            SELECT
                negocio.negocio_ruc,
                negocio.negocio_razon_social,
                negocio.negocio_numero_telefonico_asociado,
                negocio_descripcion.nd_negocio_nombre,
                negocio_descripcion.nd_negocio_descripcion,
                negocio_descripcion.nd_negocio_Direccion,
                negocio_descripcion.nd_negocio_Logo,
                negocio_descripcion.nd_negocio_valoracion,
                negocio.status
            FROM
                negocio
            LEFT JOIN
                negocio_descripcion ON negocio.negocio_id = negocio_descripcion.nd_negocios_id
            WHERE
                negocio_descripcion.nd_negocio_nombre = :nd_negocio_nombre
            """
        )

        negocio = db.execute(
            query, {"nd_negocio_nombre": nd_negocio_nombre}).fetchone()

        if negocio:
            negocio_encontrado = {
                "Ruc": negocio.negocio_ruc,
                "Razon social": negocio.negocio_razon_social,
                "Telefono asociado": negocio.negocio_numero_telefonico_asociado,
                "Nombre del negocio": negocio.nd_negocio_nombre,
                "Descripcion del negocio": negocio.nd_negocio_descripcion,
                "Direccion": negocio.nd_negocio_Direccion,
                "Logo": negocio.nd_negocio_Logo,
                "Valoracion": round(negocio.nd_negocio_valoracion) if negocio.nd_negocio_valoracion else None,
                "Status de Negocio": negocio.status
            }
            return negocio_encontrado
        else:
            raise HTTPException(status_code=404, detail={
                                "mensaje": "El negocio no existe", "res": False})

    except Exception as e:
        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al obtener el negocio", "res": False, "error": str(e)})

# Eliminar negocio por el id
def get_eliminar_negocio(negocio_id, db):
    try:
        query = text(
            """
            UPDATE CCP.negocio
            SET
                status=0
            WHERE 
                negocio_id=:negocio_id;
            """
        )
        db.execute(query, {"negocio_id": negocio_id})
        db.commit()
        return {"mensaje": "El negocio se eliminó correctamente", "res": True}
    except Exception as e:

        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al eliminar el negocio", "res": False, "error": str(e)})

# Listar empresas con su descripcion por categoria
def get_negocio_categoria(categoria, nombre, page, per_page, db):
    try:
        offset = (page - 1) * per_page
        query = (
            "SELECT "
            "negocio.negocio_ruc, "
            "negocio.negocio_razon_social, "
            "negocio.negocio_numero_telefonico_asociado, "
            "negocio_descripcion.nd_negocio_nombre, "
            "negocio_descripcion.nd_negocio_descripcion, "
            "negocio_descripcion.nd_negocio_direccion, "
            "negocio_descripcion.nd_negocio_logo, "
            "negocio_descripcion.nd_negocio_valoracion "
            "FROM "
            "negocio "
            "LEFT JOIN "
            "negocio_descripcion ON negocio.negocio_id = negocio_descripcion.nd_negocios_id "
            "LEFT JOIN "    
            "negocio_categoria ON negocio.negocio_categoria_id = negocio_categoria.negocio_categoria_id "
            "WHERE "
            "negocio_categoria.descripcion = :categoria "
            "AND "
            "negocio.status = 1 "
            "AND "
            "negocio_descripcion.status = 1 "
        )

        if nombre:
            query += (
                "AND ( "
                "LOWER(negocio_descripcion.nd_negocio_nombre) LIKE LOWER(CONCAT('%', :nombre, '%')) "
                ") "
            )

        query += (
            "LIMIT :per_page OFFSET :offset "
        )

        negocios = db.execute(text(query), {"categoria": categoria, "nombre": nombre, "per_page": per_page, "offset": offset}).fetchall()
        db.commit()

        count_query = (
            "SELECT COUNT(*) AS total FROM ( "
            "SELECT 1 FROM negocio "
            "LEFT JOIN negocio_descripcion ON negocio.negocio_id = negocio_descripcion.nd_negocios_id "
            "WHERE negocio.negocio_categoria_id = :categoria "
            "AND negocio.status = 1 "
            "AND negocio_descripcion.status = 1 "
        )

        if nombre:
            count_query += (
                "AND LOWER(negocio_descripcion.nd_negocio_nombre) LIKE LOWER(CONCAT('%', :nombre, '%')) "
            )

        count_query += (
            ") AS count "
        )

        total_rows = db.execute(text(count_query), {"categoria": categoria, "nombre": nombre}).fetchone()[0]

        if negocios:
            negocios_resultados = [{
                "Ruc": negocio.negocio_ruc,
                "Razon social:": negocio.negocio_razon_social,
                "Telefono asociado": negocio.negocio_numero_telefonico_asociado,
                "Nombre": negocio.nd_negocio_nombre,
                "Descripción": negocio.nd_negocio_descripcion,
                "Direccion": negocio.nd_negocio_direccion,
                "Logo": negocio.nd_negocio_logo,
                "Valoracion": negocio.nd_negocio_valoracion
            } for negocio in negocios]
            return {
                "data": negocios_resultados,
                "total_rows": total_rows,
                "pages": math.ceil(total_rows / per_page),
            }
        else:
            raise HTTPException(status_code=404, detail={
                "mensaje": "El negocio no existe", "res": False})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#Se registra la descripcion de un negocio
def post_registrar_negocio_descripcion(negocioDescripcion, db):
    try:
        query = text(
            """
            INSERT INTO negocio_descripcion(
                nd_negocios_id,
                nd_negocio_nombre,
                nd_negocio_descripcion,
                nd_negocio_Direccion,
                nd_negocio_Logo,
                nd_negocio_ubicacion_latitud,
                nd_negocio_ubicacion_longitud
                )
            VALUES(
                :nd_negocios_id,
                :nd_negocio_nombre,
                :nd_negocio_descripcion,
                :nd_negocio_Direccion,
                :nd_negocio_Logo,
                :nd_negocio_ubicacion_latitud,
                :nd_negocio_ubicacion_longitud
                )
            """
        )

        db.execute(query, {
            "nd_negocios_id": negocioDescripcion.nd_negocios_id,
            "nd_negocio_nombre": negocioDescripcion.nd_negocio_nombre,
            "nd_negocio_descripcion": negocioDescripcion.nd_negocio_descripcion,
            "nd_negocio_Direccion": negocioDescripcion.nd_negocio_Direccion,
            "nd_negocio_Logo": negocioDescripcion.nd_negocio_Logo,
            "nd_negocio_ubicacion_latitud": negocioDescripcion.nd_negocio_ubicacion_latitud,
            "nd_negocio_ubicacion_longitud": negocioDescripcion.nd_negocio_ubicacion_longitud
        })

        db.commit()
        return {"mensaje": "La descripcion del negocio se registro correctamente", "res": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al registrar el negocio", "res": False, "error": str(e)})

# Actualizacion de la descripcion del negocio
def update_negocio_descripcion(negocio_descripcion_id, editar, db):
    try:
        query = text("""
                UPDATE CCP.negocio_descripcion
                SET
                nd_negocio_nombre = :nd_negocio_nombre,
                nd_negocio_descripcion = :nd_negocio_descripcion,
                nd_negocio_Direccion = :nd_negocio_Direccion,
                nd_negocio_Logo = :nd_negocio_Logo,
                nd_negocio_ubicacion_latitud = :nd_negocio_ubicacion_latitud,
                nd_negocio_ubicacion_longitud = :nd_negocio_ubicacion_longitud
                WHERE negocio_descripcion_id = :negocio_descripcion_id;""")

        db.execute(query, {
            "negocio_descripcion_id": negocio_descripcion_id,
            "nd_negocio_nombre":editar.nd_negocio_nombre,
            "nd_negocio_descripcion":editar.nd_negocio_descripcion,
            "nd_negocio_Direccion":editar.nd_negocio_Direccion,
            "nd_negocio_Logo":editar.nd_negocio_Logo,
            "nd_negocio_ubicacion_latitud":editar.nd_negocio_ubicacion_latitud,
            "nd_negocio_ubicacion_longitud":editar.nd_negocio_ubicacion_longitud
            })
        db.commit()
        return {"mensaje": "Descripcion del negocio ha sido modificado correctamente", "res": True}

    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error en la base de datos: {str(e)}")


def get_listar_negocio_ubicacion(nd_negocio_nombre, db):
    try:
        query = text(
            """
            SELECT
                negocio_descripcion.nd_negocio_nombre,
                negocio_descripcion.nd_negocio_direccion,
                negocio_descripcion.nd_negocio_ubicacion_latitud,
                negocio_descripcion.nd_negocio_ubicacion_longitud
            FROM
                negocio
            LEFT JOIN
                negocio_descripcion ON negocio.negocio_id = negocio_descripcion.nd_negocios_id
            WHERE
                nd_negocio_nombre = :nd_negocio_nombre AND
                negocio.status = 1 AND negocio_descripcion.status = 1;
            """
        )

        negocios = db.execute(query, {"nd_negocio_nombre": nd_negocio_nombre}).fetchall()

        negocios_resultados = [{
            "Nombre del negocio": negocio.nd_negocio_nombre,
            "Direccion": negocio.nd_negocio_direccion,
            "Long Negocio": negocio.nd_negocio_ubicacion_latitud,
            "Lat Negocio": negocio.nd_negocio_ubicacion_longitud
        } for negocio in negocios]

        return negocios_resultados

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_actualizar_negocio_ubicacion(nd_negocio_nombre, negocioUbicacion, db):
    try:
        query_update = text(
            """
            UPDATE negocio_descripcion
            SET
                nd_negocio_ubicacion_latitud = :nd_negocio_ubicacion_latitud,
                nd_negocio_ubicacion_longitud = :nd_negocio_ubicacion_longitud
            WHERE 
                nd_negocio_nombre = :nd_negocio_nombre AND status = 1;
            """
        )
        db.execute(query_update, {
            'nd_negocio_ubicacion_latitud': negocioUbicacion.nd_negocio_ubicacion_latitud,
            'nd_negocio_ubicacion_longitud': negocioUbicacion.nd_negocio_ubicacion_longitud,
            'nd_negocio_nombre': nd_negocio_nombre
        })
        db.commit()

        nuevos_parametros = {
            "Latitud": negocioUbicacion.nd_negocio_ubicacion_latitud,
            "Longitud": negocioUbicacion.nd_negocio_ubicacion_longitud
        }

        return {"mensaje": "La longitud y latitud del negocio se han actualizado correctamente", "nuevos_parametros": nuevos_parametros, "res": True}
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error en la base de datos: {str(e)}"
        )