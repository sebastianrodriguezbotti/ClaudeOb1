"""Funciones auxiliares de la lógica del juego."""

import os
import random

import pygame

import ajustes as aj
import generar_sonidos
from visitante import Visitante


def generar_visitante(paciencia=aj.PACIENCIA_BASE, nivel=aj.NIVELES[0]):
    """Crea un visitante al azar, humano o impostor, según el nivel.

    'nivel' define cuántos vecinos hay, qué tan seguido aparecen impostores
    y qué tipos de inconsistencia pueden tener. 'paciencia' son los
    segundos que espera frente a la puerta.
    """
    apartamentos = list(aj.RESIDENTES)[:nivel["residentes"]]
    apto = random.choice(apartamentos)
    datos = aj.RESIDENTES[apto]
    nombre = datos["nombre"]
    pelo, lentes = datos["pelo"], datos["lentes"]
    bigote, mascota = datos["bigote"], datos["mascota"]

    if random.random() >= nivel["prob_impostor"]:
        return Visitante(nombre, apto, pelo, lentes, bigote, mascota, False,
                         paciencia=paciencia)

    tipo = random.choice(nivel["tipos"])
    motivo = ""
    if tipo == "nombre":
        nombre = aj.NOMBRES_PARECIDOS[apto]
        motivo = f"Su nombre estaba mal: es {datos['nombre']}"
    elif tipo == "apartamento":
        real = apto
        apto = random.choice([a for a in apartamentos if a != real])
        motivo = f"{nombre} vive en el {real}, no en el {apto}"
    elif tipo == "rasgo":
        rasgo = random.choice(["pelo", "lentes", "bigote"])
        if rasgo == "pelo":
            pelo = random.choice([p for p in aj.COLORES_PELO if p != pelo])
            motivo = f"Tenía pelo {pelo}; el libro dice {datos['pelo']}"
        elif rasgo == "lentes":
            lentes = not lentes
            motivo = ("Tenía lentes y el libro no los menciona" if lentes
                      else "No tenía lentes y el libro dice que sí")
        else:
            bigote = not bigote
            motivo = ("Tenía bigote y el libro no lo menciona" if bigote
                      else "No tenía bigote y el libro dice que sí")
    else:
        mascota = random.choice([m for m in aj.MASCOTAS if m != mascota])
        motivo = f"Dijo tener un {mascota}; el libro dice {datos['mascota']}"
    return Visitante(nombre, apto, pelo, lentes, bigote, mascota, True,
                     motivo, paciencia)


def decision_correcta(visitante, permitir):
    """Devuelve True si la decisión fue la acertada.

    Lo correcto es dejar pasar a los humanos y rechazar a los impostores.
    """
    return permitir == (not visitante.es_impostor)


def calcular_puntaje(puntaje, acerto, racha):
    """Devuelve el nuevo puntaje según el resultado y la racha actual.

    Cada acierto suma puntos base más un bonus por racha.
    Un error no resta puntos (resta una vida).
    """
    if acerto:
        return puntaje + aj.PUNTOS_ACIERTO + aj.PUNTOS_RACHA * racha
    return puntaje


def calcular_paciencia(racha, nivel):
    """Devuelve los segundos de paciencia del próximo visitante.

    Parte de la paciencia del nivel y baja con cada acierto seguido,
    pero nunca por debajo del mínimo.
    """
    return max(aj.PACIENCIA_MIN,
               nivel["paciencia"] - aj.PACIENCIA_REDUCCION * racha)


def armar_mensaje(visitante, acerto, tiempo_agotado=False):
    """Devuelve el texto de resultado que se muestra tras decidir."""
    if tiempo_agotado:
        return "¡Tiempo! El visitante se impacientó"
    if acerto and not visitante.es_impostor:
        return "¡Bien!"
    prefijo = "¡Bien!" if acerto else "¡Error!"
    detalle = visitante.motivo if visitante.es_impostor else (
        "Era un vecino de verdad")
    return f"{prefijo} {detalle}"


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


def aplicar_volumen(sonidos, volumen, activo):
    """Ajusta el volumen de todos los sonidos y devuelve el volumen aplicado.

    Si el sonido está desactivado, el volumen efectivo es 0.
    """
    efectivo = volumen if activo else 0.0
    for sonido in sonidos.values():
        sonido.set_volume(efectivo)
    return efectivo