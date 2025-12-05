from fastapi import APIRouter, HTTPException
from typing import List
from models import Jugador

router = APIRouter()

@router.post("/jugadores", response_model=Jugador)
async def crear_jugador(jugador: Jugador):
    jugadores_db.append(jugador)
    return jugador

@router.get("/jugadores", response_model=List[Jugador])
async def listar_jugadores():
    return jugadores_db

@router.get("/jugadores/{nombre}", response_model=Jugador)
async def obtener_jugador(nombre: str):
    for j in jugadores_db:
        if j.nombre == nombre:
            return j
    raise HTTPException(status_code=404, detail="Jugador no encontrado")

@router.put("/jugadores/{nombre}", response_model=Jugador)
async def actualizar_jugador(nombre: str, jugador_actualizado: Jugador):
    for i, j in enumerate(jugadores_db):
        if j.nombre == nombre:
            jugadores_db[i] = jugador_actualizado
            return jugador_actualizado
    raise HTTPException(status_code=404, detail="Jugador no encontrado")

@router.delete("/jugadores/{nombre}")
async def eliminar_jugador(nombre: str):
    for i, j in enumerate(jugadores_db):
        if j.nombre == nombre:
            jugadores_db.pop(i)
            return {"message": "Jugador eliminado"}
    raise HTTPException(status_code=404, detail="Jugador no encontrado")
