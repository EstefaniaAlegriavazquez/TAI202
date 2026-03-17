
from fastapi import FastAPI, status,HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion


router= APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)


@router.get("/")
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

@router.post("/")
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