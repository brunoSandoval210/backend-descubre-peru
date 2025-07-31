from fastapi import FastAPI, HTTPException, Depends, Header, APIRouter
from decouple import config
import subprocess
import hmac
import hashlib
from pydantic import BaseModel

webhook = APIRouter()

@webhook.post("/gitlab-webhook",tags=["WebHook"])

async def handle_gitlab_webhook(payload: BaseModel):
    
        subprocess.run(["/home/ubuntu/Desarrollo/ActualizarAutomatico.sh"])
        
        return {"mensaje": "Actualización exitosa"}

@webhook.post("/gitlab-webhook-frontend",tags=["WebHook"])

async def handle_gitlab_webhook_frontend(payload: BaseModel):
    
        subprocess.run(["/home/ubuntu/Desarrollo/ActualizacionFrontend.sh"])
        
        return {"mensaje": "Actualización exitosa"}