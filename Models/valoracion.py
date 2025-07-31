from typing import Optional
from pydantic import BaseModel


class valoracion(BaseModel):
    valoracion_negocio_id: int
    valoracion_usuario_id: int
    valoracion_valoracion_puntaje: Optional[int] = None


class valoracionUpdate(BaseModel):
    valoracion_valoracion_puntaje: Optional[int] = None
