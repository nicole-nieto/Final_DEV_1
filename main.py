from fastapi import FastAPI, HTTPException
from models import Jugador, Partido, Estadistica
from typing import List

app = FastAPI(title="sigmotoa FC")


@app.get("/")
async def root():
    return {"message": "sigmotoa FC data"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Bienvenido a sigmotoa FC {name}"}

jugadores_db: List[Jugador] = []
partidos_db: List[Partido] = []


@app.post("/jugadores", response_model=Jugador)
async def crear_jugador(jugador: Jugador):
    jugadores_db.append(jugador)
    return jugador


@app.get("/jugadores", response_model=List[Jugador])
async def listar_jugadores():
    return jugadores_db


@app.get("/jugadores/{nombre}", response_model=Jugador)
async def obtener_jugador(nombre: str):
    for j in jugadores_db:
        if j.nombre == nombre:
            return j
    raise HTTPException(status_code=404, detail="Jugador no encontrado")


@app.put("/jugadores/{nombre}", response_model=Jugador)
async def actualizar_jugador(nombre: str, jugador_actualizado: Jugador):
    for i, j in enumerate(jugadores_db):
        if j.nombre == nombre:
            jugadores_db[i] = jugador_actualizado
            return jugador_actualizado
    raise HTTPException(status_code=404, detail="Jugador no encontrado")


@app.delete("/jugadores/{nombre}")
async def eliminar_jugador(nombre: str):
    for i, j in enumerate(jugadores_db):
        if j.nombre == nombre:
            jugadores_db.pop(i)
            return {"message": "Jugador eliminado"}
    raise HTTPException(status_code=404, detail="Jugador no encontrado")



@app.post("/partidos", response_model=Partido)
async def crear_partido(partido: Partido):
    partidos_db.append(partido)
    return partido


@app.get("/partidos", response_model=List[Partido])
async def listar_partidos():
    return partidos_db


@app.get("/partidos/{rival}", response_model=Partido)
async def obtener_partido(rival: str):
    for p in partidos_db:
        if p.rival == rival:
            return p
    raise HTTPException(status_code=404, detail="Partido no encontrado")
