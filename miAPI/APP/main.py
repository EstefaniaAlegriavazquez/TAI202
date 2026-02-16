#importaciones
from fastapi import FastAPI, status,HTTPException
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

#tabla ficticia
usuarios=[
    {"id":1,"nombre":"Fanny","edad":21},
    {"id":2,"nombre":"Aly","edad":21},
    {"id":3,"nombre":"Dulce","edad":21},

]

@app.get("/v1/usuarios/",tags=['HTTP CRUD'])
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "ususrios": usuarios,
        "status":"200"
    }

@app.get("/v1/usuarios/",tags=['HTTP CRUD'])
async def agregar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id")
            raise HTTPException(
                status_code=400,
                detail="El id ya exixte"
            )

    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Creado",
        "Datos nuevos": usuario
    }