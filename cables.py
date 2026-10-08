"""Minijuego del apagón: reconectar los cables del mismo color."""

import math
import random

import pygame

import ajustes as aj


class Apagon:
    """El impostor apaga la luz: titila, queda todo a oscuras y hay que
    arrastrar cada cable de la izquierda hasta el enchufe del mismo color
    de la derecha antes de que se acabe el tiempo.

    Atributos:
        cantidad: cuántos cables hay.
        restante: segundos que quedan para arreglarlo.
        fase: "titilar", "cables", "listo" (se muestra el resultado) o "fin".
        exito: True si se conectaron todos a tiempo.
        orden_der: orden_der[j] es el color del enchufe derecho número j
            (mezclado, para que los cables se crucen).
        conectados: colores que ya están conectados.
        arrastrando: color del cable que se está arrastrando (o None).
    """

    def __init__(self, cantidad, tiempo):
        """Prepara el apagón con 'cantidad' cables y 'tiempo' segundos."""
        self.cantidad = cantidad
        self.tiempo = tiempo
        self.restante = tiempo
        self.reloj = 0.0              # segundos de la fase actual
        self.fase = "titilar"
        self.exito = False
        self.orden_der = list(range(cantidad))
        while cantidad > 1 and self.orden_der == sorted(self.orden_der):
            random.shuffle(self.orden_der)
        self.conectados = set()
        self.arrastrando = None
        self.pos = (0, 0)             # posición del mouse

    def _y(self, indice):
        """Devuelve la altura del enchufe número 'indice'."""
        return aj.CABLES_Y_CENTRO + round(
            (indice - (self.cantidad - 1) / 2) * aj.CABLES_PASO)

    def _pos_izq(self, color):
        """Devuelve la posición del enchufe izquierdo de ese color."""
        return (aj.CABLES_X_IZQ, self._y(color))

    def _pos_der(self, indice):
        """Devuelve la posición del enchufe derecho número 'indice'."""
        return (aj.CABLES_X_DER, self._y(indice))

    @staticmethod
    def _cerca(a, b):
        """Devuelve True si los puntos a y b están dentro del radio de un enchufe."""
        return math.hypot(a[0] - b[0], a[1] - b[1]) <= aj.CABLES_RADIO

    def terminado(self):
        """Devuelve True cuando ya se puede volver al juego."""
        return self.fase == "fin"

    def manejar_evento(self, evento):
        """Procesa el mouse. Devuelve "agarrado", "conectado", "error" o None."""
        if self.fase != "cables":
            return None
        if evento.type == pygame.MOUSEMOTION:
            self.pos = evento.pos
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for color in range(self.cantidad):
                if (color not in self.conectados
                        and self._cerca(evento.pos, self._pos_izq(color))):
                    self.arrastrando = color
                    self.pos = evento.pos
                    return "agarrado"
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            color, self.arrastrando = self.arrastrando, None
            if color is None:
                return None
            for j in range(self.cantidad):
                if self._cerca(evento.pos, self._pos_der(j)):
                    if self.orden_der[j] == color:
                        self.conectados.add(color)
                        return "conectado"
                    return "error"      # enchufe de otro color
        return None

    def actualizar(self, dt):
        """Avanza el tiempo (dt en segundos) y cambia de fase si corresponde."""
        self.reloj += dt
        if self.fase == "titilar" and self.reloj >= aj.APAGON_TITILEO:
            self.fase, self.reloj = "cables", 0.0
        elif self.fase == "cables":
            self.restante = max(0.0, self.restante - dt)
            if len(self.conectados) == self.cantidad:
                self.exito = True
                self.fase, self.reloj = "listo", 0.0
            elif self.restante <= 0:
                self.fase, self.reloj = "listo", 0.0
        elif self.fase == "listo" and self.reloj >= aj.APAGON_PAUSA_FINAL:
            self.fase = "fin"

    def luz_encendida(self):
        """Devuelve True si en este momento hay luz (se ve la escena normal).

        Pasa en los instantes en que la luz titila encendida y cuando ya
        se arregló.
        """
        if self.fase == "titilar":
            return not self._oscuro()
        return self.fase == "listo" and self.exito

    def _oscuro(self):
        """Devuelve True si, durante el titileo, la luz está apagada."""
        return (self.reloj >= aj.APAGON_TITILEO - 0.5
                or int(self.reloj / aj.APAGON_PARPADEO) % 2 == 1)

    def dibujar(self, pantalla, fuentes):
        """Dibuja los carteles y los cables (main.py ya dibujó la escena y,
        si no hay luz, el velo oscuro encima)."""
        if self.fase == "titilar":
            return
        if self.fase == "listo":
            if self.exito:
                texto, color = "¡LUZ RESTABLECIDA!", aj.COLOR_ACIERTO
            else:
                texto, color = "¡SE ACABÓ EL TIEMPO!", aj.COLOR_ERROR
            imagen = fuentes["grande"].render(texto, True, color)
            pantalla.blit(imagen, imagen.get_rect(center=(aj.ANCHO // 2, 270)))
            return
        titulo = fuentes["grande"].render("¡UN IMPOSTOR APAGÓ LA LUZ!", True,
                                          aj.COLOR_ERROR)
        pantalla.blit(titulo, titulo.get_rect(center=(aj.ANCHO // 2, 45)))
        ayuda = fuentes["normal"].render(
            "Arrastrá cada cable hasta el enchufe de su color", True,
            aj.COLOR_TEXTO)
        pantalla.blit(ayuda, ayuda.get_rect(center=(aj.ANCHO // 2, 75)))
        x, y, ancho, alto = aj.CABLES_BARRA
        pygame.draw.rect(pantalla, aj.COLOR_BARRA_FONDO, (x, y, ancho, alto))
        pygame.draw.rect(pantalla, aj.COLOR_ERROR,
                         (x, y, int(ancho * self.restante / self.tiempo), alto))
        # enchufes (el derecho está mezclado)
        for color in range(self.cantidad):
            pygame.draw.circle(pantalla, aj.COLOR_ENCHUFE,
                               self._pos_izq(color), aj.CABLES_RADIO + 5)
            pygame.draw.circle(pantalla, aj.COLORES_CABLES[color],
                               self._pos_izq(color), aj.CABLES_RADIO)
        for j, color in enumerate(self.orden_der):
            pygame.draw.circle(pantalla, aj.COLOR_ENCHUFE,
                               self._pos_der(j), aj.CABLES_RADIO + 5)
            pygame.draw.circle(pantalla, aj.COLORES_CABLES[color],
                               self._pos_der(j), aj.CABLES_RADIO)
        # cables ya conectados y el que se está arrastrando
        for j, color in enumerate(self.orden_der):
            if color in self.conectados:
                pygame.draw.line(pantalla, aj.COLORES_CABLES[color],
                                 self._pos_izq(color), self._pos_der(j),
                                 aj.CABLES_GROSOR)
        if self.arrastrando is not None:
            pygame.draw.line(pantalla, aj.COLORES_CABLES[self.arrastrando],
                             self._pos_izq(self.arrastrando), self.pos,
                             aj.CABLES_GROSOR)