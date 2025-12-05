from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from utils.positions import Position
from utils.states import States


class Estadistica(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jugador_id: int = Field(foreign_key="jugador.id")
    partido_id: int = Field(foreign_key="partido.id")

    goles: int = 0
    asistencias: int = 0
    minutos: int = 0
    amarillas: int = 0
    rojas: int = 0

    jugador: "Jugador" = Relationship(back_populates="estadisticas_partido")
    partido: "Partido" = Relationship(back_populates="estadisticas_jugadores")


class Jugador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    fecha_nacimiento: str
    numero_camiseta: int
    nacionalidad: str
    altura: int
    peso: int
    pie_dominante: str
    posicion: Position
    estado: States = States.ACTIVO

    estadisticas_partido: List[Estadistica] = Relationship(back_populates="jugador")


class Partido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rival: str
    fecha: str
    resultado_local: int
    resultado_visitante: int
    estado_partido: str = ""   

    estadisticas_jugadores: List[Estadistica] = Relationship(back_populates="partido")
