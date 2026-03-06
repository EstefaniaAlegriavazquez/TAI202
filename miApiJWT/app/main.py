#importaciones
from fastapi import FastAPI, status,HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta



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

# Configuración JWT
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Configuraciones OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def crear_token(data: dict):
    datos = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expire})
    token = jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)
    return token

#Enpoint para agregar Token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    if form_data.username != "Estefania" or form_data.password != "1234":
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    access_token = crear_token({"sub": form_data.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

#Función para validar Token
async def validar_token(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")

        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return usuario

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

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
async def actualizar_usuario(id: int, usuario_actualizado: dict, usuario: str = Depends(validar_token)):

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
async def eliminar_usuario(id: int, usuario: str = Depends(validar_token)):

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