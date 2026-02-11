#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#Instancia del servidor
app= FastAPI()

#Endpoints
@app.get("/")
async def holamundo():
    return {"mensaje":"Hola Mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return{
        "mensaje":"Bienvenido a FastAPI",
        "estatus":"200",
    }

#Endpoint con parámetro obligatorio
@app.get("/usuario/{id}")
async def obtener_usuario(id: int):
    return {
        "mensaje": "Usuario encontrado",
        "id_usuario": id
    }

#Endpoint con parámetros opcionales
@app.get("/usuarios")
async def listar_usuarios(edad: Optional[int] = None, ciudad: Optional[str] = None):
    return {
        "edad": edad,
        "ciudad": ciudad
    }