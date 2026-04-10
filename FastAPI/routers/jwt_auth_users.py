from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

algoritmo = "HS256"
duracion_token = 1
secret = "07fae26d8a738c3b4a0a723997f12f7e8192a6ff5ca034ec021af0439674b76e"

router_jau = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class clase_usuario(BaseModel):
    username: str
    nombre: str
    apellidos: str
    edad: int
    disabled: bool

class clase_usuario_password(clase_usuario):
    password: str

users_db = {
    "miguelprian":{
        "username":"miguelprian", 
        "nombre":"Miguel", 
        "apellidos":"Prian Perez", 
        "edad":27, 
        "disabled":True,
        "password":"$2a$12$sife8scx1.zD2h0Fhtmda.q5lAYC/I9GcXOmkVy/QXAeKmVqfxzC6"
        },
    "ernestocp":{
        "username":"ernestocp", 
        "nombre":"Ernesto", 
        "apellidos":"Cuez Perez", 
        "edad":25, 
        "disabled":False,
        "password":"$2a$12$RS7UK7zYHnCWQ1uUY4vRa.GEiaN3r/Fq7BhWQvnUPrS3P1TZGZsXy"
        },
    "franbelenf":{
        "username":"franbelenf", 
        "nombre":"Francisca", 
        "apellidos":"Flores Olavarria", 
        "edad":32, 
        "disabled":True,
        "password":"$2a$12$6zaK2.2HU2xp6yACc.RoBeql0Dy.DTZ2KvlBFSG3CgJTqvXv.N1sS"
        },
    "javimeji":{
        "username":"javimeji", 
        "nombre":"Javier", 
        "apellidos":"Mejias Gordillo", 
        "edad":30, 
        "disabled":False,
        "password":"$2a$12$QucoOnFpIVnARyC8yhaDTOBN8WDJvwt/UDzzJJQttC5l087ptdOMG"
        },
    "alanisecu":{
        "username":"alanisecu", 
        "nombre":"Alanis", 
        "apellidos":"Ni idea", 
        "edad":22, 
        "disabled":True,
        "password":"$2a$12$jkTqsw/BgMHkUkVJ/Te2G.X/UNEk6s4z8RMuzJDiJH.oDb7A5HOMm"
        },
    }

def busca_usuario_db(username: str):
    if username in users_db:
        return clase_usuario_password(**users_db[username])
    
def busca_usuario(username: str):
    if username in users_db:
        return clase_usuario(**users_db[username])

async def auth_user(token: str = Depends(oauth2)): 
    try:
        username = jwt.decode(token, secret, algorithms=[algoritmo]).get("sub")
        if username == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario esta vacio.")
    except JWTError:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidas", headers={"WWW-Authenticate": "Bearer"})
    return busca_usuario(username)

async def current_user(usuario: clase_usuario = Depends(auth_user)):
    if usuario.disabled == True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este usuario esta desabilitado.")
    
    return usuario

@router_jau.post("/loginjau")

async def login(form: OAuth2PasswordRequestForm = Depends()):
    input_username = users_db.get(form.username)
    if not input_username:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail= "Este usuario no se encuentra dentro de la base de datos.")

    usuario = busca_usuario_db(form.username)

    if not crypt.verify(str(form.password), str(usuario.password)):
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, detail= "La contraseña que has introducido no es correcta.")
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=duracion_token)

    access_token = {"sub": usuario.username, "exp": expire, }

    return {"access_token": jwt.encode(access_token, secret, algorithm=algoritmo), "token_type":"bearer"}

@router_jau.get("/usersjau/me")

async def me(usuario: clase_usuario = Depends(current_user)):
    return usuario
