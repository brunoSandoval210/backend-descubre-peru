from pydantic import BaseModel


class NegocioRegistro(BaseModel):
    usuario_id: int
    negocio_ruc: str
    negocio_categoria_id: int
    negocio_razon_social: str
    negocio_numero_telefonico_asociado: str


class edit_empresa(BaseModel):
    usuario_id: int
    negocio_ruc: int
    negocio_categoria_id: int
    negocio_razon_social: str
    negocio_numero_telefonico_asociado: str


class negocioDescripcionRegistro(BaseModel):
    nd_negocios_id: int
    nd_negocio_nombre: str
    nd_negocio_descripcion: str
    nd_negocio_Direccion: str
    nd_negocio_Logo: str
    nd_negocio_ubicacion_latitud: str
    nd_negocio_ubicacion_longitud: str


class negocioDescripcionUpdate(BaseModel):
    nd_negocio_nombre: str
    nd_negocio_descripcion: str
    nd_negocio_Direccion: str
    nd_negocio_Logo: str
    nd_negocio_ubicacion_latitud: int
    nd_negocio_ubicacion_longitud: int

class negocioUbicacion(BaseModel):
    nd_negocio_Direccion: str
    nd_negocio_ubicacion_latitud: float 
    nd_negocio_ubicacion_longitud: float
