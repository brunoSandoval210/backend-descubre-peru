from fastapi import HTTPException
from sqlalchemy import text

# Registro - Logica de la valoración del negocio


def post_registrar_valoracion(valoracion, db):
    try:
        query = text(
            """
            INSERT INTO valoracion(
                valoracion_negocio_id,
                valoracion_usuario_id,
                valoracion_valoracion_puntaje
                )
            VALUES(
                :valoracion_negocio_id,
                :valoracion_usuario_id,
                :valoracion_valoracion_puntaje
                )
            """
        )

        db.execute(query, {
            "valoracion_negocio_id": valoracion.valoracion_negocio_id,
            "valoracion_usuario_id": valoracion.valoracion_usuario_id,
            "valoracion_valoracion_puntaje": valoracion.valoracion_valoracion_puntaje,
        })

        db.commit()
        return {"mensaje": "La valoración ha sido registrada correctamente", "res": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail={
                            "mensaje": "Error al registrar la valoración", "res": False, "error": str(e)})

# Update - Logica de la actualizacion de la valoracion del negocio


def update_valoracion(valoracion_id, update, db):
    try:
        query = text("""
                UPDATE valoracion
                SET
                valoracion_valoracion_puntaje = :valoracion_valoracion_puntaje
                WHERE valoracion_id = :valoracion_id;  
                """)

        db.execute(query, {
            "valoracion_valoracion_puntaje": update.valoracion_valoracion_puntaje,
            "valoracion_id": valoracion_id
        })

        db.commit()
        return {"mensaje": "La valoracion se modificó correctamente", "res": True}

    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error en la base de datos: {str(e)}")
