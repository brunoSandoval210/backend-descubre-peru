from fastapi import FastAPI
from dotenv import load_dotenv
from Routes.usuario_routes import usuario_routes
from Routes.negocio_routes import negocio_routes
from Routes.imagene_routes import imagenes_routes
from Routes.comentario_routes import comentario_routes
from Routes.valoracion_routes import valoracion_routes
from Routes.categoria_routes import categoria_routes
from fastapi.middleware.cors import CORSMiddleware
from Routes.webhook import webhook

app=FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(usuario_routes,prefix="/usuario")
app.include_router(negocio_routes,prefix="/negocio")
app.include_router(imagenes_routes,prefix="/imagen")
app.include_router(comentario_routes,prefix="/comentario")
app.include_router(valoracion_routes,prefix="/valoracion")
app.include_router(categoria_routes,prefix="/categoria")
app.include_router(webhook,prefix="/webhook")
load_dotenv()
