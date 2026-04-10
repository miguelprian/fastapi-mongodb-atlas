from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router_bau = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class clase_usuario(BaseModel):
    username: str
    nombre: str
    apellidos: str
    edad: int
    disabled: bool

class usuario_password_db(clase_usuario):
    password: str

users_db = {
    "miguelprian":{
        "username":"miguelprian", 
        "nombre":"Miguel", 
        "apellidos":"Prian Perez", 
        "edad":27, 
        "disabled":True,
        "password":"miguelprian123"
        },
    "ernestocp":{
        "username":"ernestocp", 
        "nombre":"Ernesto", 
        "apellidos":"Cuez Perez", 
        "edad":25, 
        "disabled":False,
        "password":"ernesto123"
        },
    "franbelenf":{
        "username":"franbelenf", 
        "nombre":"Francisca", 
        "apellidos":"Flores Olavarria", 
        "edad":32, 
        "disabled":True,
        "password":"franbelen123"
        },
    "javimeji":{
        "username":"javimeji", 
        "nombre":"Javier", 
        "apellidos":"Mejias Gordillo", 
        "edad":30, 
        "disabled":False,
        "password":"javi123"
        },
    "alanisecu":{
        "username":"alanisecu", 
        "nombre":"Alanis", 
        "apellidos":"Ni idea", 
        "edad":22, 
        "disabled":True,
        "password":"alanis123"
        },
    }

async def current_user(token: str = Depends(oauth2)):
    usuario = busca_usuario(token)
    if not usuario:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidas", headers={"WWW-Authenticate": "Bearer"})
    
    if usuario.disabled == True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este usuario esta desabilitado.")
    
    return usuario

def busca_usuario_db(username: str):
    if username in users_db:
        return usuario_password_db(**users_db[username])

def busca_usuario(username: str):
    if username in users_db:
        return clase_usuario(**users_db[username])

@router_bau.post("/loginbau")

async def login(form: OAuth2PasswordRequestForm = Depends()):
    input_username = users_db.get(form.username)
    if not input_username:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail= "Este usuario no se encuentra dentro de la base de datos.")

    usuario = busca_usuario_db(form.username)

    if not form.password == usuario.password:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, detail= "La contraseña que has introducido no es correcta.")
    
    return {"access_token": usuario.username, "token_type":"bearer"}

@router_bau.get("/usersbau/me")

async def me(usuario: clase_usuario = Depends(current_user)):
    return usuario