from pydantic import BaseModel
from typing import Optional


class ImagenRegistro(BaseModel):
    nombre: str
    public_id: str
    url: str
    type: str
    negocio_id: Optional[int] = 0
    usuario_id: Optional[int] = 0


class ImagenActualizar(BaseModel):
    nombre: str
    public_id: str
    url: str
    type: str
