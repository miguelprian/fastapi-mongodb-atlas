from fastapi import APIRouter

router_products = APIRouter(prefix="/products", tags= ["products"], responses={404: {"error":"No encontrado"}})

lista_productos = [
    {"id":1, "nombre":"Manzana", "color":"Rojo"}, 
    {"id":2, "nombre":"Pera", "color":"Verde"}, 
    {"id":3, "nombre":"Platano", "color":"Amarillo"}, 
    {"id":4, "nombre":"Ciruela", "color":"Morado"}
    ]

@router_products.get("/")

async def productos():
    return lista_productos

@router_products.get("/{id}")

async def productos(id:int):
    return lista_productos[id-1]