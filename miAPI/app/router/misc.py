import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

misc= APIRouter(tags=["Varios"])

#Endpoints
@misc.get("/")
async def holamundo():
    return {"mensaje":"Hola Mundo FastAPI"}

@misc.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return{
        "mensaje":"Bienvenido a FastAPI",
        "estatus":"200",
    }

#Endpoint con parámetro obligatorio
@misc.get("/usuario/{id}")
async def obtener_usuario(id: int):
    return {
        "mensaje": "Usuario encontrado",
        "id_usuario": id
    }

#Endpoint con parámetros opcionales
@misc.get("/usuarios")
async def listar_usuarios(edad: Optional[int] = None, ciudad: Optional[str] = None):
    return {
        "edad": edad,
        "ciudad": ciudad
    }




# Parámetro obligatorio
@misc.get("/v1/parametroOb/{id}", tags=["Parametro Obligatorio"])
async def consultaid(id: int):
    return {
        "mensaje": "Usuario encontrado",
        "usuario": id,
        "status": "200"
    }

# Parámetro opcional
@misc.get("/v1/parametroOp/", tags=["Parametro Opcional"])
async def consultatodos(id: Optional[int] = None):

    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {
                    "mensaje": "Usuario encontrado",
                    "usuario": usuario,
                    "status": "200"
                }

        return {
            "mensaje": "Usuario no encontrado",
            "status": "404"
        }

    return {
        "mensaje": "No se proporciono id",
        "status": "200"
    }