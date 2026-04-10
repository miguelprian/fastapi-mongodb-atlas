#uvicorn main:app --reload

from fastapi import FastAPI
from routers import products
from routers import users
from routers import basic_auth_users
from routers import jwt_auth_users
from routers import users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(products.router_products)
app.include_router(users.router_users)
app.include_router(basic_auth_users.router_bau)
app.include_router(jwt_auth_users.router_jau)
app.include_router(users_db.router_users_db)
app.mount("/statics", StaticFiles(directory="statics"), name="statics")

@app.get("/")

async def hola_fastapi():
    return {"mensaje":"Hola FASTAPI"}

@app.get("/nombre")

async def nombre():
    return {"nombre":"Miguel Alejandro"}