from Data.CloudinaryConfig import *
from cloudinary import uploader

#Guardar Imagen
def post_guardar_imagen(file_path, carpeta=""):
    try:
        configuracion_carpeta = {"folder": carpeta} if carpeta else {}

        resultado = uploader.upload(file_path, **configuracion_carpeta)
        data_resultado = {
            "public_id": resultado.get('public_id'),
            "url": resultado.get('secure_url'),
            "type": resultado.get('format')
        }
        return data_resultado
    except Exception as e:
        return {"error": str(e)}
    
#Actualizar imagen
def put_actualizar_imagen(public_id, file_path):
    try:
        resultado = uploader.explicit(
            public_id,
            type="upload",
            invalidate=True,  
        )

        resultado_nueva = uploader.upload(file_path, public_id=public_id)

        data_resultado = {
            "public_id": resultado_nueva.get('public_id'),
            "url": resultado_nueva.get('secure_url'),
            "type": resultado_nueva.get('format')
        }
        return data_resultado
    except Exception as e:
        return {"error": str(e)}
    
#Eliminar imagen    
def delete_eliminar_imagen(public_id):
    try:
        resultado = uploader.destroy(public_id)

        if resultado.get('result') == 'ok':
            return {"mensaje": f"Imagen con public_id {public_id} eliminada correctamente"}
        else:
            return {"error": f"No se pudo eliminar la imagen con public_id {public_id}"}
    except Exception as e:
        return {"error": str(e)}