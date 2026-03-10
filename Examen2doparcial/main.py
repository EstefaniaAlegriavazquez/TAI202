import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, timedelta
import secrets
from fastapi import FastAPI, status,HTTPException, Depends

#Instancia del servidor
app= FastAPI(
    title="Mi Examen",
    description="Estefania Alegria Vazquez",
    version="1.0"
)

# Base de datos ficticia
restaurante = [
    {"id": 1, "nombre": "Restaurante_La luna"},
    {"id": 2, "nombre": "Restaurante_Lupita"},
]


# Seguridad HTTP BASIC#

security= HTTPBasic()
def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuario_correcto= secrets.compare_digest(credenciales.username,"admin")
    contrasena_correcta= secrets.compare_digest(credenciales.password,"rest123")

    if not(usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail=" Credenciales no validas"
        )
    return credenciales.username


#Creamos el modelo validación pydantic
class reserva(BaseModel):
    nombre: str = Field(..., min_length=6, max_length=100)
    numero_personas:int= Field(..., ge=1,le=18,description="Personas aceptadas")
    fecha: int = Field(..., gt=8:00, max_length=10:00 , le=datetime.now().years)
    año: int = Field(..., gt=1450, le=datetime.now().year)

  
#Endpoints
@app.get("/")
async def sistema_reservas():
    return {"mensaje":"Funciona sistema de reservas"}


#Endpoint con parámetro obligatorio
@app.get("/Reservas/{id}")
async def obtener_usuario(nombre: str):
    return {
        "mensaje": "Reserva encontrada",
        "id_usuario": id
    }

#Crear reserva
@app.post("/reservas", status_code=status.HTTP_201_CREATED)
async def crear_reserva(reserva: reserva):

    for reser in reserva:
        if reser["nombre_cliente"].lower() == reserva.nombre.lower():
            raise HTTPException(
                status_code=400,
                detail="La reserva ya existe"
            )

    reserva.append(reserva.dict())

    return {
        "mensaje": "Reserva creada correctamente",
        "status": "201"
    }

#Endpoint para las listas de reservas
@app.get("/reservas", response_model=List[reserva])
async def listar_libros():
    return reserva

#Endpoint con parámetro obligatorio
#Consultar por ID
@app.get("/reservas/{id}")
async def obtener_reserva(id: int, usuarioAuth:str= Depends(verificar_peticion)):
    return {
        "mensaje": "reserva encontrada",
        "id_usuario": id
    }

#DELETE cancelar reserva
@app.delete("/v1/reserva/{id}", tags=["HTTP CRUD"])
async def Cancelar_reserva(id: int, usuarioAuth:str= Depends(verificar_peticion)):

    for reser in reserva:
        if reser["id"] == id:
            reserva.remove(reser)
            return {
                "mensaje": "Reserva eliminada correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Reserva no encontrado"
    )

