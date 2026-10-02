"""Funciones auxiliares de la lógica del juego."""

import os
import random

import pygame

import ajustes as aj
import generar_sonidos
from visitante import Visitante


def _texto_rasgo(nombre_rasgo, valor):
    """Devuelve el rasgo en palabras (uso interno), ej. 'con lentes'."""
    if nombre_rasgo == "lentes":
        return "con lentes" if valor else "sin lentes"
    return "con bigote" if valor else "sin bigote"


def generar_visitante():
    """Crea un visitante al azar, humano o impostor.

    Un humano coincide en todo con el libro de residentes.
    Un impostor tiene UNA inconsistencia: nombre, apartamento,
    un rasgo físico o algo que dice (la mascota).
    """
    apto = random.choice(list(aj.RESIDENTES))
    datos = aj.RESIDENTES[apto]
    nombre = datos["nombre"]
    pelo, lentes = datos["pelo"], datos["lentes"]
    bigote, mascota = datos["bigote"], datos["mascota"]

    if random.random() >= aj.PROB_IMPOSTOR:
        return Visitante(nombre, apto, pelo, lentes, bigote, mascota, False)

    tipo = random.choice(["nombre", "apartamento", "rasgo", "dicho"])
    motivo = ""
    if tipo == "nombre":
        nombre = aj.NOMBRES_PARECIDOS[apto]
        motivo = f"Su nombre estaba mal: es {datos['nombre']}"
    elif tipo == "apartamento":
        real = apto
        apto = random.choice([a for a in aj.RESIDENTES if a != real])
        motivo = f"{nombre} vive en el {real}, no en el {apto}"
    elif tipo == "rasgo":
        rasgo = random.choice(["pelo", "lentes", "bigote"])
        if rasgo == "pelo":
            pelo = random.choice([p for p in aj.COLORES_PELO if p != pelo])
            motivo = f"Tenía pelo {pelo}; el libro dice {datos['pelo']}"
        elif rasgo == "lentes":
            lentes = not lentes
            motivo = f"Estaba {_texto_rasgo('lentes', lentes)}; el libro no"
        else:
            bigote = not bigote
            motivo = f"Estaba {_texto_rasgo('bigote', bigote)}; el libro no"
    else:
        mascota = random.choice([m for m in aj.MASCOTAS if m != mascota])
        motivo = f"Dijo tener un {mascota}; el libro dice {datos['mascota']}"
    return Visitante(nombre, apto, pelo, lentes, bigote, mascota, True, motivo)


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


def armar_mensaje(visitante, acerto):
    """Devuelve el texto de resultado que se muestra tras decidir."""
    if acerto and not visitante.es_impostor:
        return "¡Bien!"
    prefijo = "¡Bien!" if acerto else "¡Error!"
    detalle = visitante.motivo if visitante.es_impostor else (
        "Era un vecino de verdad")
    return f"{prefijo} {detalle}"


def nueva_partida():
    """Devuelve los valores iniciales: (puntaje, vidas, racha, visitante)."""
    return 0, aj.VIDAS_INICIALES, 0, generar_visitante()


def cargar_sonidos():
    """Devuelve un diccionario {nombre: pygame.mixer.Sound}.

    Si faltan los archivos .wav, los genera primero.
    """
    faltan = any(
        not os.path.exists(os.path.join(aj.SONIDOS_CARPETA, f"{n}.wav"))
        for n in aj.NOMBRES_SONIDOS)
    if faltan:
        generar_sonidos.generar_todos()
    sonidos = {}
    for nombre in aj.NOMBRES_SONIDOS:
        sonido = pygame.mixer.Sound(
            os.path.join(aj.SONIDOS_CARPETA, f"{nombre}.wav"))
        sonido.set_volume(aj.VOLUMEN)
        sonidos[nombre] = sonido
    return sonidos