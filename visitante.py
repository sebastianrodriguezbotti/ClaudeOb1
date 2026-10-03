"""Clase Visitante: alguien que toca el timbre del edificio."""

import math

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
        paciencia_max / paciencia: segundos totales y restantes de espera.
    """

    def __init__(self, nombre, apartamento, pelo, lentes, bigote, mascota,
                 es_impostor, motivo=None, paciencia=aj.PACIENCIA_BASE):
        """Crea el visitante con sus datos y lo ubica fuera de pantalla."""
        self.nombre = nombre
        self.apartamento = apartamento
        self.pelo = pelo
        self.lentes = lentes
        self.bigote = bigote
        self.mascota = mascota
        self.es_impostor = es_impostor
        self.motivo = motivo
        self.paciencia_max = paciencia
        self.paciencia = paciencia
        self.x = float(aj.VISITANTE_X_INICIAL)  # float: movimiento suave
        self.rect = pygame.Rect(
            aj.VISITANTE_X_INICIAL,
            aj.SUELO_Y - aj.CUERPO_ALTO,
            aj.CUERPO_ANCHO,
            aj.CUERPO_ALTO,
        )

    def actualizar(self, dt):
        """Hace caminar al visitante hasta la puerta (dt en segundos).

        Devuelve True solo en el cuadro exacto en que llega (para el timbre).
        """
        ya_estaba = self.llego()
        if not ya_estaba:
            self.x = min(self.x + aj.VISITANTE_VELOCIDAD * dt,
                         aj.VISITANTE_X_DESTINO)
        self.rect.x = int(self.x)
        return (not ya_estaba) and self.llego()

    def llego(self):
        """Devuelve True si ya está frente a la puerta."""
        return self.x >= aj.VISITANTE_X_DESTINO

    def esperar(self, dt):
        """Gasta paciencia mientras espera frente a la puerta.

        Devuelve True si la paciencia se agotó.
        """
        if not self.llego():
            return False
        self.paciencia = max(0.0, self.paciencia - dt)
        return self.paciencia <= 0

    def fraccion_paciencia(self):
        """Devuelve la paciencia restante entre 0.0 (nada) y 1.0 (toda)."""
        return self.paciencia / self.paciencia_max

    def impaciente(self):
        """Devuelve True si ya llegó y le queda poca paciencia."""
        return self.llego() and self.fraccion_paciencia() < aj.PACIENCIA_ALERTA

    def frases(self):
        """Devuelve la lista de cosas que dice el visitante."""
        return [
            f"Hola, soy {self.nombre}, del {self.apartamento}.",
            f"Vengo a darle de comer a mi {self.mascota}.",
        ]

    def dibujar(self, pantalla):
        """Dibuja cuerpo, cabeza y rasgos. Si está impaciente, tiembla."""
        radio = aj.CABEZA_RADIO
        impaciente = self.impaciente()
        sacudida = 0
        if impaciente:
            sacudida = int(3 * math.sin(pygame.time.get_ticks() / 30))
        rect = self.rect.move(sacudida, 0)
        cx = rect.centerx
        cy = rect.top - radio + 4

        pygame.draw.rect(pantalla, aj.COLOR_CUERPO, rect)
        pygame.draw.circle(pantalla, aj.COLOR_PIEL, (cx, cy), radio)
        # Pelo: una elipse sobre la parte de arriba de la cabeza
        pygame.draw.ellipse(pantalla, aj.COLORES_PELO[self.pelo],
                            (cx - radio - 1, cy - radio - 4,
                             2 * radio + 2, radio + 2))
        # Ojos: se ponen rojos y más grandes cuando se impacienta
        color_ojos = aj.COLOR_OJOS_ALERTA if impaciente else aj.COLOR_LENTES
        radio_ojo = 3 if impaciente else 2
        for dx in (-8, 8):
            pygame.draw.circle(pantalla, color_ojos, (cx + dx, cy + 2),
                               radio_ojo)
        if self.lentes:
            for dx in (-8, 8):
                pygame.draw.circle(pantalla, aj.COLOR_LENTES,
                                   (cx + dx, cy + 2), 7, 2)
            pygame.draw.line(pantalla, aj.COLOR_LENTES,
                             (cx - 1, cy + 2), (cx + 1, cy + 2), 2)
        if self.bigote:
            pygame.draw.rect(pantalla, aj.COLOR_BIGOTE,
                             (cx - 9, cy + 10, 18, 4))

    def dibujar_paciencia(self, pantalla):
        """Dibuja la barra de paciencia sobre la cabeza (solo si ya llegó)."""
        if not self.llego():
            return
        fraccion = self.fraccion_paciencia()
        if fraccion > aj.PACIENCIA_MEDIA:
            color = aj.COLOR_PACIENCIA_ALTA
        elif fraccion > aj.PACIENCIA_ALERTA:
            color = aj.COLOR_PACIENCIA_MEDIA
        else:
            color = aj.COLOR_PACIENCIA_BAJA
        x = self.rect.centerx - aj.BARRA_ANCHO // 2
        y = self.rect.top - 2 * aj.CABEZA_RADIO - 16
        pygame.draw.rect(pantalla, aj.COLOR_BARRA_FONDO,
                         (x - 1, y - 1, aj.BARRA_ANCHO + 2, aj.BARRA_ALTO + 2))
        pygame.draw.rect(pantalla, color,
                         (x, y, int(aj.BARRA_ANCHO * fraccion), aj.BARRA_ALTO))