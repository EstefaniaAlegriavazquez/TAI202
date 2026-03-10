import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

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

#Creamos el modelo validación pydantic
class reserva(BaseModel):
    nombre: str = Field(..., min_length=6, max_length=100)
    numero_personas:int= Field(..., ge=1,le=18,description="Personas aceptadas")
    fecha: str = Field(..., min_length=8:00, max_length=10:00)
    año: int = Field(..., gt=1450, le=datetime.now().year)
    
#Enpoints
@app.get("/v1/restaurante/",tags=['HTTP CRUD'])
# Parámetro obligatorio
@app.get("/v1/parametroOb/{nombre}", tags=["Parametro Obligatorio"])
async def consultaid(id: int):
    return {
        "mensaje": "Usuario encontrado",
        "usuario": id,
        "status": "200"
    }

#Endpoint para crear reserva
@app.post("/reservas", status_code=status.HTTP_201_CREATED)
async def registrar_reserva(libro: Libro):

    for r in reservas:
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