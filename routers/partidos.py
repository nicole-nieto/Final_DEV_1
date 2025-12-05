from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from database import get_session
from models import Partido, Jugador, Estadistica

router = APIRouter(prefix="/partidos", tags=["Partidos"])


def calcular_estado(resultado_local: int, resultado_visitante: int) -> str:
    if resultado_local > resultado_visitante:
        return "VICTORIA"
    if resultado_local < resultado_visitante:
        return "DERROTA"
    return "EMPATE"


@router.post("/", status_code=201)
def crear_partido(partido: Partido, session: Session = Depends(get_session)):

    existe = session.exec(select(Partido).where(Partido.rival == partido.rival, Partido.fecha == partido.fecha)).first()
    if existe:
        raise HTTPException(status_code=409, detail="Partido ya existe (mismo rival y fecha)")

    partido.estado_partido = calcular_estado(partido.resultado_local, partido.resultado_visitante)
    session.add(partido)
    session.commit()
    session.refresh(partido)
    return partido


@router.get("/", response_model=List[Partido])
def listar_partidos(session: Session = Depends(get_session)):
    partidos = session.exec(select(Partido)).all()
    salida = []
    for p in partidos:
        
        estad = session.exec(select(Estadistica).where(Estadistica.partido_id == p.id)).all()
        salida.append({
            "partido": p,
            "estado_partido": p.estado_partido or calcular_estado(p.resultado_local, p.resultado_visitante),
            "participantes": estad
        })
    return salida


@router.get("/{partido_id}")
def obtener_partido(partido_id: int, session: Session = Depends(get_session)):
    p = session.get(Partido, partido_id)
    if not p:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    estad = session.exec(select(Estadistica).where(Estadistica.partido_id == p.id)).all()
    return {
        "partido": p,
        "estado_partido": p.estado_partido or calcular_estado(p.resultado_local, p.resultado_visitante),
        "participantes": estad
    }


@router.post("/{partido_id}/estadistica", status_code=201)
def agregar_o_actualizar_estadistica(partido_id: int, jugador_id: int, minutos: int = 0,
                                     goles: int = 0, asistencias: int = 0,
                                     amarillas: int = 0, rojas: int = 0,
                                     session: Session = Depends(get_session)):
    partido = session.get(Partido, partido_id)
    jugador = session.get(Jugador, jugador_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    existente = session.exec(
        select(Estadistica).where(Estadistica.partido_id == partido_id, Estadistica.jugador_id == jugador_id)
    ).first()

    if existente:
        
        existente.minutos = minutos
        existente.goles = goles
        existente.asistencias = asistencias
        existente.amarillas = amarillas
        existente.rojas = rojas
        session.add(existente)
        session.commit()
        session.refresh(existente)
        return existente
    else:
        nuevo = Estadistica(
            partido_id=partido_id,
            jugador_id=jugador_id,
            minutos=minutos,
            goles=goles,
            asistencias=asistencias,
            amarillas=amarillas,
            rojas=rojas
        )
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        return nuevo
