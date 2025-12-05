from fastapi import FastAPI
from database import init_db
from routers.jugadores import router as jugadores_router
from routers.partidos import router as partidos_router

app = FastAPI(title="SIGMOTOA FC")

@app.get("/")
async def root():
    return {"message": "sigmotoa FC data"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Bienvenido a sigmotoa FC {name}"}


init_db()

app.include_router(jugadores_router)
app.include_router(partidos_router)

