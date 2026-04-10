from pydantic import BaseModel

class clase_usuario(BaseModel):
    id: str | None = None
    username: str
    email: str