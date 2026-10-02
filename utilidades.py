"""Funciones auxiliares de la lógica del juego."""

import random

import ajustes as aj
from visitante import Visitante


def generar_visitante():
    """Crea un visitante al azar, humano o impostor.

    Un humano tiene datos coherentes con el libro de residentes.
    Un impostor tiene UNA inconsistencia (nombre, apartamento o dedos).
    """
    apartamento = random.choice(list(aj.RESIDENTES))
    nombre = aj.RESIDENTES[apartamento]
    dedos = aj.DEDOS_NORMALES

    if random.random() >= aj.PROB_IMPOSTOR:
        return Visitante(nombre, apartamento, dedos, es_impostor=False)

    motivo = random.choice(["nombre", "apartamento", "dedos"])
    if motivo == "nombre":
        nombre = random.choice(aj.NOMBRES_FALSOS)
    elif motivo == "apartamento":
        otros = [a for a in aj.RESIDENTES if a != apartamento]
        apartamento = random.choice(otros)  # nombre de otro inquilino
    else:
        dedos = random.choice([4, 6, 7])
    return Visitante(nombre, apartamento, dedos, True, motivo)


def decision_correcta(visitante, permitir):
    """Devuelve True si la decisión fue la acertada.

    Lo correcto es dejar pasar a los humanos y rechazar a los impostores.
    """
    return permitir == (not visitante.es_impostor)


def calcular_puntaje(puntaje, acerto, racha):
    """Devuelve el nuevo puntaje según el resultado y la racha actual.

    Cada acierto suma puntos base más un bonus por racha.
    Un error no resta puntos (resta una vida en main.py).
    """
    if acerto:
        return puntaje + aj.PUNTOS_ACIERTO + aj.PUNTOS_RACHA * racha
    return puntaje