

class Jugador():
    pass


class Estadistica(BaseModel):
    goles_marcados: int = 0
    asistencias: int = 0
    minutos_jugados: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0


class Partido(BaseModel):
    rival: str
    fecha: str 
    resultado_local: int
    resultado_visitante: int
    goles_local: List[str] = [] 
    goles_visitante: List[str] = [] 

