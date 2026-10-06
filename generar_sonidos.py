"""Genera los efectos de sonido del juego como archivos .wav.

Se hace con matemática (ondas seno, cuadradas y ruido), usando solo la
librería estándar de Python. Se ejecuta solo si faltan los sonidos:
    python generar_sonidos.py
"""

import math
import os
import random
import struct
import wave

import ajustes as aj


def _onda(frecuencia, duracion, tipo="seno", volumen=0.5):
    """Devuelve la lista de muestras de un tono con volumen decreciente."""
    total = int(aj.FRECUENCIA_MUESTREO * duracion)
    muestras = []
    for i in range(total):
        t = i / aj.FRECUENCIA_MUESTREO
        valor = math.sin(2 * math.pi * frecuencia * t)
        if tipo == "cuadrada":
            valor = 1.0 if valor >= 0 else -1.0
        caida = 1 - i / total              # baja de 1 a 0 (fade out)
        muestras.append(valor * volumen * caida)
    return muestras


def _barrido(f_inicio, f_fin, duracion, ruido=0.3, volumen=0.6):
    """Devuelve un tono que cambia de frecuencia, mezclado con ruido."""
    total = int(aj.FRECUENCIA_MUESTREO * duracion)
    muestras = []
    fase = 0.0
    for i in range(total):
        avance = i / total
        frecuencia = f_inicio + (f_fin - f_inicio) * avance
        fase += 2 * math.pi * frecuencia / aj.FRECUENCIA_MUESTREO
        valor = (1 - ruido) * math.sin(fase) + ruido * random.uniform(-1, 1)
        muestras.append(valor * volumen * (1 - avance))
    return muestras


def _ruido(duracion, volumen=0.5):
    """Devuelve un ruido suave que se apaga rápido (como un papel)."""
    total = int(aj.FRECUENCIA_MUESTREO * duracion)
    muestras = []
    anterior = 0.0
    for i in range(total):
        anterior = 0.6 * anterior + 0.4 * random.uniform(-1, 1)  # suaviza
        muestras.append(anterior * volumen * (1 - i / total) ** 2)
    return muestras


def _guardar(nombre, muestras):
    """Escribe las muestras (entre -1 y 1) en sonidos/<nombre>.wav."""
    os.makedirs(aj.SONIDOS_CARPETA, exist_ok=True)
    ruta = os.path.join(aj.SONIDOS_CARPETA, f"{nombre}.wav")
    with wave.open(ruta, "wb") as archivo:
        archivo.setnchannels(1)                    # mono
        archivo.setsampwidth(2)                    # 16 bits
        archivo.setframerate(aj.FRECUENCIA_MUESTREO)
        datos = b"".join(
            struct.pack("<h", int(max(-1, min(1, m)) * 32767))
            for m in muestras)
        archivo.writeframes(datos)


def generar_todos():
    """Crea todos los sonidos del juego."""
    random.seed(7)  # el ruido sale igual cada vez
    _guardar("timbre", _onda(660, 0.35) + _onda(520, 0.6))
    _guardar("acierto", _onda(523, 0.1) + _onda(659, 0.1) + _onda(784, 0.25))
    _guardar("error", _onda(110, 0.5, tipo="cuadrada", volumen=0.4))
    _guardar("susto", _barrido(900, 70, 1.1))
    _guardar("papel", _ruido(0.18))


if __name__ == "__main__":
    generar_todos()
    print("Sonidos generados en", aj.SONIDOS_CARPETA)