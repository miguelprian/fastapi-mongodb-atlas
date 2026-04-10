from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router_users = APIRouter(prefix="/users", tags= ["users"], responses={404: {"error":"No encontrado"}})

class clase_usuario(BaseModel):
    id: int
    nombre: str
    apellidos: str
    ubicacion: str
    edad: int

lista_usuarios = [clase_usuario(id=1, nombre="Miguel Alejandro", apellidos="Prian Perez", ubicacion="Alemania", edad=27),
                  clase_usuario(id=2, nombre="Francisca Belen", apellidos="Flores-Olavarria", ubicacion="Alemania", edad=32),
                  clase_usuario(id=3, nombre="Ernesto", apellidos="Cuez Perez", ubicacion="Alemania", edad=25)
                  ]

def busca_usuario(id:int):
    variable_usuario = filter(lambda clase_usuario: clase_usuario.id==id, lista_usuarios)
    try:
        return list(variable_usuario)[0]
    except:
        return {"error":"No existe este usuario dentro de la base de datos"}

@router_users.get("/")

async def usersclass():
    return lista_usuarios

@router_users.get("/{id}")

async def user(id:int):
    return busca_usuario(id)

#@router_users.get("/userquery/")

#async def user(id:int):
#    return busca_usuario(id)

#@router_users.get("/usersjson")

#async def usersjson():
#    return [{"id":1, "nombre":"Miguel", "apellidos":"Prian Perez", "ubicacion":"Alemania", "edad":27},
#            {"id":2, "nombre":"Francisca", "apellidos":"Contreras Flores", "ubicacion":"Alemania", "edad":32},
#            {"id":3, "nombre":"Ernesto", "apellidos":"Cuez Perez", "ubicacion":"Alemania", "edad":25}]

@router_users.post("/", response_model=clase_usuario, status_code=201)

async def crear_usuario(usuario:clase_usuario):
    if type(busca_usuario(usuario.id)) == clase_usuario:
        raise HTTPException(status_code=404, detail="Este usuario ya existe.")
    else:
        lista_usuarios.append(usuario)
        return {"ok":"Se ha añadido el usuario correctamente."}

@router_users.put("/")

async def actualizar_usuario(usuario:clase_usuario):
    encontrado = False
    for i, usuario_guardado in enumerate(lista_usuarios):
        if usuario_guardado.id == usuario.id:
            lista_usuarios[i] = usuario
            encontrado = True
            return {"ok":"Se ha actualizado correctamente."}
    if encontrado == False:
        raise HTTPException(status_code=404, detail="Este usuario no existe.")

@router_users.delete("/{id}")

async def eliminar_usuario(id:int):
    encontrado = False
    for i, usuario_guardado in enumerate(lista_usuarios):
        if usuario_guardado.id == id:
            del lista_usuarios[i]
            encontrado = True
            return {"ok":"Se ha eliminado el usuario correctamente."}
    if encontrado == False:
        raise HTTPException(status_code=404, detail="Este usuario no existe.")
