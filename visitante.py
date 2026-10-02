"""Clase Visitante: alguien que toca el timbre del edificio."""

import pygame

import ajustes as aj


class Visitante:
    """Persona (o impostor) que camina hasta la puerta y pide entrar.

    Atributos:
        nombre, apartamento: lo que dice ser y adónde dice ir.
        pelo, lentes, bigote: rasgos físicos que se ven en el dibujo.
        mascota: lo que cuenta sobre su mascota.
        es_impostor: True si es un monstruo disfrazado.
        motivo: qué lo delata (None si es humano).
    """

    def __init__(self, nombre, apartamento, pelo, lentes, bigote, mascota,
                 es_impostor, motivo=None):
        """Crea el visitante con sus datos y lo ubica fuera de pantalla."""
        self.nombre = nombre
        self.apartamento = apartamento
        self.pelo = pelo
        self.lentes = lentes
        self.bigote = bigote
        self.mascota = mascota
        self.es_impostor = es_impostor
        self.motivo = motivo
        self.x = float(aj.VISITANTE_X_INICIAL)  # float: movimiento suave
        self.rect = pygame.Rect(
            aj.VISITANTE_X_INICIAL,
            aj.SUELO_Y - aj.CUERPO_ALTO,
            aj.CUERPO_ANCHO,
            aj.CUERPO_ALTO,
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

    def frases(self):
        """Devuelve la lista de cosas que dice el visitante."""
        return [
            f"Hola, soy {self.nombre}, del {self.apartamento}.",
            f"Vengo a darle de comer a mi {self.mascota}.",
        ]

    def dibujar(self, pantalla):
        """Dibuja cuerpo, cabeza y rasgos (pelo, lentes, bigote)."""
        radio = aj.CABEZA_RADIO
        cx = self.rect.centerx
        cy = self.rect.top - radio + 4

        pygame.draw.rect(pantalla, aj.COLOR_CUERPO, self.rect)
        pygame.draw.circle(pantalla, aj.COLOR_PIEL, (cx, cy), radio)
        # Pelo: una elipse sobre la parte de arriba de la cabeza
        pygame.draw.ellipse(pantalla, aj.COLORES_PELO[self.pelo],
                            (cx - radio - 1, cy - radio - 4,
                             2 * radio + 2, radio + 2))
        # Ojos
        for dx in (-8, 8):
            pygame.draw.circle(pantalla, aj.COLOR_LENTES, (cx + dx, cy + 2), 2)
        if self.lentes:
            for dx in (-8, 8):
                pygame.draw.circle(pantalla, aj.COLOR_LENTES,
                                   (cx + dx, cy + 2), 7, 2)
            pygame.draw.line(pantalla, aj.COLOR_LENTES,
                             (cx - 1, cy + 2), (cx + 1, cy + 2), 2)
        if self.bigote:
            pygame.draw.rect(pantalla, aj.COLOR_BIGOTE,
                             (cx - 9, cy + 10, 18, 4))