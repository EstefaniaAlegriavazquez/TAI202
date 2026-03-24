
from fastapi import FastAPI, status,HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuarios import usuario as dbUsuario


router= APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)


@router.get("/")
async def leer_usuarios(db:Session= Depends(get_db)):
   
    queryUsuarios= db.query(dbUsuario).all()
    return {
        "total": len(queryUsuarios),
        "usuarios": queryUsuarios,
        "status": "200"
    }

@router.post("/")
async def crear_usuario(usuarioP: crear_usuario, db:Session= Depends(get_db)):
    
    nuevoU= dbUsuario(nombre= usuarioP.nombre, edad= usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)

    return {
        "mensaje": "Usuario creado",
        "Datos nuevos": usuarioP
    }

# PUT Actualizar usuario completo
@router.put("/")
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
@router.patch("/{id}")
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
@router.delete("/")
async def eliminar_usuario(id: int,usuarioAuth:str= Depends(verificar_peticion)):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )