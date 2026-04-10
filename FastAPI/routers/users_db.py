from fastapi import APIRouter, HTTPException, status
from db.models.user_model import clase_usuario
from db.client import db_client
from db.schemas.user_schema import user_schema, users_schema
from bson import ObjectId

router_users_db = APIRouter(prefix="/usersdb", tags= ["users_db"], responses={status.HTTP_404_NOT_FOUND: {"error 404": "No encontrado"}})

def busca_usuario(field:str, key):
    try:
        usuario_busqueda = db_client.users.find_one({field:key})
        if not usuario_busqueda:
            return None
        return clase_usuario(**user_schema(usuario_busqueda))
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor.")

@router_users_db.get("/", response_model=list[clase_usuario] | clase_usuario)

async def usuarios(id:str | None = None):
    if id:
        return busca_usuario("_id", ObjectId(id))
    return users_schema(db_client.users.find())

@router_users_db.get("/{id}")

async def usuario(id:str):
    return busca_usuario("_id", ObjectId(id))

@router_users_db.post("/", response_model=clase_usuario, status_code=status.HTTP_201_CREATED)

async def crear_usuario(usuario:clase_usuario):
    if type(busca_usuario("username", usuario.username)) == clase_usuario and type(busca_usuario("email", usuario.email)) == clase_usuario:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail="Este usuario ya existe dentro de la base de datos.")
    elif type(busca_usuario("username", usuario.username)) == clase_usuario:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail="Este username ya existe dentro de la base de datos.")
    elif type(busca_usuario("email", usuario.email)) == clase_usuario:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail="Este email ya existe dentro de la base de datos.")
    usuario_dict = dict(usuario)
    del usuario_dict["id"]
    id = db_client.users.insert_one(usuario_dict).inserted_id
    nuevo_usuario = user_schema(db_client.users.find_one({"_id":id}))
    return clase_usuario(**nuevo_usuario)

@router_users_db.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

async def eliminar_usuario(id:str):
    encontrado = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    if encontrado == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Este usuario no existe.")

@router_users_db.put("/", response_model=clase_usuario)

async def actualizar_usuario(usuario:clase_usuario):
    try:
        diccionario_usuario = dict(usuario)
        del diccionario_usuario["id"]
        db_client.users.find_one_and_replace({"_id":ObjectId(usuario.id)}, diccionario_usuario)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se ha podido actualizar el usuario.")
    return busca_usuario("_id", ObjectId(usuario.id))