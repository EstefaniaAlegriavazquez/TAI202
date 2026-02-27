from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital",
    description="Estefania Alegria Vazquez - Practica 5",
    version="1.0"
)

#Base de datos ficticia
libros = []
prestamos = []

#Creamos el modelo validación pydantic
class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr

class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str = Field(..., min_length=2, max_length=100)
    año: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: str = Field(..., pattern="^(disponible|prestado)$")

class Prestamo(BaseModel):
    nombre_libro: str
    usuario: Usuario

#Endpoints

# Endpoint inicial
@app.get("/")
async def inicio():
    return {"mensaje": "API Biblioteca funcionando correctamente"}

#Endpoint para registrar libro
@app.post("/libros", status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro: Libro):

    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=400,
                detail="El libro ya existe"
            )

    libros.append(libro.dict())

    return {
        "mensaje": "Libro registrado correctamente",
        "status": "201"
    }

#Endpoint para las listas de libros
@app.get("/libros", response_model=List[Libro])
async def listar_libros():
    return libros

#Endpoint para buscar un libro por su nombre 
@app.get("/libros/{nombre}")
async def buscar_libro(nombre: str):

    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            return libro

    raise HTTPException(
        status_code=400,
        detail="Libro no encontrado"
    )

#Endpoint para registrar libro
@app.post("/prestamos")
async def registrar_prestamo(prestamo: Prestamo):

    for libro in libros:
        if libro["nombre"].lower() == prestamo.nombre_libro.lower():

            if libro["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )

            libro["estado"] = "prestado"
            prestamos.append(prestamo.dict())

            return {
                "mensaje": "Préstamo registrado correctamente",
                "status": "200"
            }

    raise HTTPException(
        status_code=400,
        detail="Libro no encontrado"
    )

#Endpoint para devolver un libro
@app.put("/prestamos/devolver/{nombre_libro}")
async def devolver_libro(nombre_libro: str):

    for libro in libros:
        if libro["nombre"].lower() == nombre_libro.lower():

            if libro["estado"] == "disponible":
                raise HTTPException(
                    status_code=409,
                    detail="El libro no está prestado"
                )

            libro["estado"] = "disponible"

            return {
                "mensaje": "Libro devuelto correctamente",
                "status": "200"
            }

    raise HTTPException(
        status_code=400,
        detail="Libro no encontrado"
    )

#Endpoint para eliminar registro de prestamo
@app.delete("/prestamos/{nombre_libro}")
async def eliminar_prestamo(nombre_libro: str):

    for prestamo in prestamos:
        if prestamo["nombre_libro"].lower() == nombre_libro.lower():
            prestamos.remove(prestamo)

            return {
                "mensaje": "Registro de préstamo eliminado",
                "status": "200"
            }

    raise HTTPException(
        status_code=409,
        detail="El registro de préstamo no existe"
    )