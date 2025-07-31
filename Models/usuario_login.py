from pydantic import BaseModel, EmailStr

class UsuarioLogin(BaseModel):
    email: str
    contrasena: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None
    
class User(BaseModel):
    nombres: str
    apellidos: str
    email: str
    status: int | None = None
