#importaciones
from fastapi import FastAPI, status,HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel,Field

#Instancia del servidor
app= FastAPI(
    title="Mi primer API",
    description="Estefania Alegria Vazquez",
    version="1.0"
)

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

# Base de datos ficticia
usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]



#Creamos el modelo validación pydantic
class crear_usuario(BaseModel):
    id:int = Field(...,gt=0, description="Identificador de usurio")
    nombre:str= Field(..., min_length=3,max_length=50,example="Estefania")
    edad:int= Field(..., ge=1,le=123,description="Edad valida entre 1 y 123")


# Parámetro obligatorio
@app.get("/v1/parametroOb/{id}", tags=["Parametro Obligatorio"])
async def consultaid(id: int):
    return {
        "mensaje": "Usuario encontrado",
        "usuario": id,
        "status": "200"
    }

# Parámetro opcional
@app.get("/v1/parametroOp/", tags=["Parametro Opcional"])
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

@app.get("/v1/usuarios/", tags=["HTTP CRUD"])
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

@app.post("/v1/usuarios/", tags=["HTTP CRUD"])
async def crear_usuario(usuario: crear_usuario):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario)

    return {
        "mensaje": "Usuario creado",
        "Datos nuevos": usuario
    }

# PUT Actualizar usuario completo
@app.put("/v1/usuarios/{id}", tags=["HTTP CRUD"])
async def actualizar_usuario(id: int, usuario_actualizado: dict):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": "Usuario actualizado correctamente",
                "usuario": usuario_actualizado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

#PATCH Actualización parcial
@app.patch("/v1/usuarios/{id}", tags=["HTTP CRUD"])
async def actualizar_parcial_usuario(id: int, datos_actualizar: dict):

    for usr in usuarios:
        if usr["id"] == id:
            usr.update(datos_actualizar)
            return {
                "mensaje": "Usuario actualizado parcialmente",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

#DELETE Eliminar usuario
@app.delete("/v1/usuarios/{id}", tags=["HTTP CRUD"])
async def eliminar_usuario(id: int):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )