from sqlalchemy.exc import IntegrityError, OperationalError
from fastapi import HTTPException
from sqlalchemy import text
from DataBase.connection import SessionLocal
from Security.function_jwt import get_password_hash
import math

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Listar usuarios
def get_listar_usuario(page, per_page,db):
    try:
        offset = (page - 1) * per_page
        query = text(
            """SELECT
                    usuario_id,
                    usuario_nombres,
                    usuario_apellidos,
                    usuario_fecha_de_nacimiento,
                    usuario_email,
                    usuario_dni,
                    tipo_usuario.tipo_usuario_descripcion
                FROM
                    usuario AS U
                JOIN
                    tipo_usuario ON U.usuario_tipo_usuario_id = tipo_usuario.tipo_usuario_id
                WHERE
                    U.status = 1
                LIMIT :per_page OFFSET :offset ;""")

        usuarios = db.execute(query,{"per_page":per_page,"offset":offset}).fetchall()

        usuarios_listado = []
        for usuario in usuarios:
            usuarios_resultados = {
                "Id": usuario.usuario_id,
                "Nombres": usuario.usuario_nombres,
                "Apellidos": usuario.usuario_apellidos,
                "Fecha de nacimiento": usuario.usuario_fecha_de_nacimiento,
                "Email": usuario.usuario_email,
                "Dni": usuario.usuario_dni,
                "Tipo de usuario": usuario.tipo_usuario_descripcion
            }
            usuarios_listado.append(usuarios_resultados)

        return usuarios_listado

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

#Registar usuario por el id
def get_listar_usuario_id(id_usuario, db):

    try:
        query = text(
            """SELECT
                    usuario_nombres,
                    usuario_apellidos,
                    usuario_fecha_de_nacimiento,
                    usuario_email,
                    usuario_dni,
                    tipo_usuario.tipo_usuario_descripcion
                FROM 
                    usuario AS U
                JOIN
                    tipo_usuario ON U.usuario_tipo_usuario_id = tipo_usuario.tipo_usuario_id
                WHERE 
                    U.usuario_id=:id_usuario
                AND 
                    U.status = 1;""")

        usuarios = db.execute(query, {"id_usuario": id_usuario}).fetchone()

        if usuarios:
            usuario_encontrado = {
                "Nombres": usuarios.usuario_nombres,
                "Apellidos": usuarios.usuario_apellidos,
                "Fecha de nacimiento": usuarios.usuario_fecha_de_nacimiento,
                "Email": usuarios.usuario_email,
                "Dni": usuarios.usuario_dni,
                "Tipo de usuario": usuarios.tipo_usuario_descripcion
                
            }

            return usuario_encontrado
        else:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado")

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

#Listar usuario por el dni
def get_listar_usuario_dni(usuario_dni, db):
    try:
        query = text(
            """SELECT
                    usuario_nombres,
                    usuario_apellidos,
                    usuario_fecha_de_nacimiento,
                    usuario_email,
                    usuario_dni,
                    tipo_usuario.tipo_usuario_descripcion
                FROM 
                    usuario AS U
                JOIN 
                    tipo_usuario ON U.usuario_tipo_usuario_id = tipo_usuario.tipo_usuario_id 
                WHERE
                    U.status = 1 AND usuario_dni = :usuario_dni""")

        usuarios = db.execute(query, {
            "usuario_dni": usuario_dni
        }).fetchone()

        if usuarios:
            usuarios_resultados = {
                "Nombres": usuarios.usuario_nombres,
                "Apellidos": usuarios.usuario_apellidos,
                "Fecha de nacimiento": usuarios.usuario_fecha_de_nacimiento,
                "Email": usuarios.usuario_email,
                "Dni": usuarios.usuario_dni,
                "Tipo de usuario": usuarios.tipo_usuario_descripcion
            }

        return usuarios_resultados

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

#Registrar Usuario
def get_registrar_usuario(usuario, db):
    password_hash = get_password_hash(usuario.usuario_password)
    try:
        query = text(
            """INSERT INTO usuario (
                usuario_nombres,
                usuario_apellidos,
                usuario_fecha_de_nacimiento,
                usuario_dni,
                usuario_tipo_usuario_id,
                usuario_email,
                usuario_password)
            VALUES (
                :usuario_nombres,
                :usuario_apellidos,
                :usuario_fecha_de_nacimiento,
                :usuario_dni,
                :usuario_tipo_usuario_id,
                :usuario_email,
                :hashed_password)
            """
        )
        db.execute(query, {
            "usuario_nombres": usuario.usuario_nombres,
            "usuario_apellidos": usuario.usuario_apellidos,
            "usuario_fecha_de_nacimiento": usuario.usuario_fecha_de_nacimiento,
            "usuario_dni": usuario.usuario_dni,
            "usuario_tipo_usuario_id": usuario.usuario_tipo_usuario_id,
            "usuario_email": usuario.usuario_email,
            "hashed_password": password_hash
        })
        db.commit()
        return {"mensaje": "Usuario registrado correctamente", "res": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Error al registrar usuario")

#Actualizar usuario
def get_actualizar_usuario(id_usuario,usuario,db):
    #usuario_actualizar=get_listar_usuario_id(usuario.usuario_id,db)
    password_hash = get_password_hash(usuario.usuario_password)
    try:
        query = text(
            """
                UPDATE usuario
                SET
                usuario_nombres=:usuario_nombres,
                usuario_apellidos=:usuario_apellidos,
                usuario_fecha_de_nacimiento=:usuario_fecha_de_nacimiento,
                usuario_dni=:usuario_dni,
                usuario_tipo_usuario_id=:usuario_tipo_usuario_id,
                usuario_email=:usuario_email,
                usuario_password=:hashed_password
                WHERE usuario_id=:usuario_id      
            """)
        db.execute(query, {
            "usuario_nombres": usuario.usuario_nombres,
            "usuario_apellidos": usuario.usuario_apellidos,
            "usuario_fecha_de_nacimiento": usuario.usuario_fecha_de_nacimiento,
            "usuario_dni": usuario.usuario_dni,
            "usuario_tipo_usuario_id": usuario.usuario_tipo_usuario_id,
            "usuario_email": usuario.usuario_email,
            "hashed_password": password_hash,
            "usuario_id":id_usuario
        })
        db.commit()
        return {"mensaje": "Usuario se actualizo correctamente", "res": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail={"mensaje": "Error al actualizar el usuario", "res": False, "error": str(e)})
    
#Eliminar usuario
def get_eliminar_usuario(id_usuario_eli, db):
    try:
        query = text("""
                UPDATE usuario
                SET
                status='1'
                WHERE usuario_id=:id_usuario_eli""")

        result = db.execute(query, {"id_usuario_eli": id_usuario_eli})
        affected_rows = result.rowcount

        if affected_rows > 0:
            return {"mensaje": "El usuario se eliminó correctamente"}
        else:
            raise HTTPException(
                status_code=404, detail=f"No se encontró el usuario con nombres {id_usuario}")

    except (IntegrityError, OperationalError) as e:
        raise HTTPException(
            status_code=500, detail=f"Error en la base de datos: {str(e)}")