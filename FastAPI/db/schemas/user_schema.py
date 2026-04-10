def user_schema(usuario) -> dict:
    return {"id": str(usuario["_id"]), "username": str(usuario["username"]), "email": str(usuario["email"])}

def users_schema(usuarios) -> list:
    return [user_schema(usuario)for usuario in usuarios]