
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

# GET POR ID
@router.get("/{id}")
async def leer_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

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
@router.put("/{id}")
async def actualizar_usuario(
    id: int,
    usuario_actualizado: dict,
    db: Session = Depends(get_db)
):
    usuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = usuario_actualizado.get("nombre")
    usuario.edad = usuario_actualizado.get("edad")

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "Usuario actualizado correctamente",
        "usuario": usuario
    }

#PATCH Actualización parcial
@router.patch("/{id}")
async def actualizar_parcial_usuario(id: int, datos: dict, db: Session = Depends(get_db)):
    usuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if "nombre" in datos:
        usuario.nombre = datos["nombre"]
    if "edad" in datos:
        usuario.edad = datos["edad"]

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "Usuario actualizado parcialmente",
        "usuario": usuario
    }
#DELETE Eliminar usuario
@router.delete("/{id}")
async def eliminar_usuario(
    id: int,
    db: Session = Depends(get_db),
    usuarioAuth: str = Depends(verificar_peticion)
):
    usuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {
        "mensaje": f"Usuario eliminado por {usuarioAuth}"
    }