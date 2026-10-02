"""Clase Visitante: alguien que toca el timbre del edificio."""

import pygame

import ajustes as aj


class Visitante:
    """Persona (o impostor) que camina hasta la puerta y pide entrar.

    Atributos:
        nombre: nombre que dice tener.
        apartamento: apartamento al que dice ir.
        dedos: cantidad de dedos en la mano (los impostores fallan a veces).
        es_impostor: True si es un monstruo disfrazado.
        motivo: qué dato lo delata (None si es humano).
    """

    def __init__(self, nombre, apartamento, dedos, es_impostor, motivo=None):
        """Crea el visitante con sus datos y lo ubica fuera de pantalla."""
        self.nombre = nombre
        self.apartamento = apartamento
        self.dedos = dedos
        self.es_impostor = es_impostor
        self.motivo = motivo
        self.x = float(aj.VISITANTE_X_INICIAL)  # float: movimiento suave
        self.rect = pygame.Rect(
            aj.VISITANTE_X_INICIAL,
            aj.SUELO_Y - aj.VISITANTE_ALTO,
            aj.VISITANTE_ANCHO,
            aj.VISITANTE_ALTO,
        )

    def actualizar(self, dt):
        """Hace caminar al visitante hasta la puerta (dt en segundos)."""
        if not self.llego():
            self.x = min(self.x + aj.VISITANTE_VELOCIDAD * dt,
                         aj.VISITANTE_X_DESTINO)
        self.rect.x = int(self.x)

    def llego(self):
        """Devuelve True si ya está frente a la puerta."""
        return self.x >= aj.VISITANTE_X_DESTINO

    def dibujar(self, pantalla):
        """Dibuja al visitante en la pantalla."""
        pygame.draw.rect(pantalla, aj.COLOR_VISITANTE, self.rect)