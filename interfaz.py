"""Elementos de interfaz reutilizables: botón, deslizador y engranaje."""

import math

import pygame

import ajustes as aj


class Boton:
    """Botón rectangular con texto que se resalta al pasar el mouse."""

    def __init__(self, texto, centro, ancho=aj.BOTON_ANCHO,
                 alto=aj.BOTON_ALTO, color=aj.COLOR_BOTON,
                 color_hover=aj.COLOR_BOTON_HOVER):
        """Crea el botón centrado en 'centro' (x, y)."""
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect.center = centro

    def bajo_mouse(self, pos):
        """Devuelve True si el punto 'pos' está sobre el botón."""
        return self.rect.collidepoint(pos)

    def dibujar(self, pantalla, fuente, pos_mouse):
        """Dibuja el botón; cambia de color si el mouse está encima."""
        color = self.color_hover if self.bajo_mouse(pos_mouse) else self.color
        pygame.draw.rect(pantalla, color, self.rect, border_radius=8)
        pygame.draw.rect(pantalla, aj.COLOR_BORDE, self.rect, 2,
                         border_radius=8)
        imagen = fuente.render(self.texto, True, aj.COLOR_TEXTO)
        pantalla.blit(imagen, imagen.get_rect(center=self.rect.center))


class Deslizador:
    """Barra que se arrastra con el mouse y guarda un valor entre 0 y 1."""

    def __init__(self, x, y, ancho, valor):
        """Crea la barra en (x, y) con el valor inicial dado."""
        self.rect = pygame.Rect(x, y, ancho, 8)
        self.valor = valor
        self.arrastrando = False

    def _fijar_desde_x(self, x):
        """Convierte una posición x del mouse en un valor entre 0 y 1."""
        self.valor = min(1.0, max(0.0, (x - self.rect.x) / self.rect.width))

    def manejar_evento(self, evento):
        """Procesa un evento del mouse.

        Devuelve "cambio" si el valor cambió, "soltado" si se soltó el
        mouse después de arrastrar, o None si no pasó nada.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.inflate(20, 30).collidepoint(evento.pos):
                self.arrastrando = True
                self._fijar_desde_x(evento.pos[0])
                return "cambio"
        elif evento.type == pygame.MOUSEMOTION and self.arrastrando:
            self._fijar_desde_x(evento.pos[0])
            return "cambio"
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.arrastrando:
                self.arrastrando = False
                return "soltado"
        return None

    def dibujar(self, pantalla):
        """Dibuja la barra, la parte llena y la perilla."""
        pygame.draw.rect(pantalla, aj.COLOR_BARRA_FONDO, self.rect,
                         border_radius=4)
        relleno = self.rect.copy()
        relleno.width = int(self.rect.width * self.valor)
        if relleno.width > 0:
            pygame.draw.rect(pantalla, aj.COLOR_ACIERTO, relleno,
                             border_radius=4)
        perilla = (self.rect.x + relleno.width, self.rect.centery)
        pygame.draw.circle(pantalla, aj.COLOR_TEXTO, perilla, 12)


def dibujar_engranaje(pantalla, centro, radio, color):
    """Dibuja una rueda dentada (el ícono de configuración)."""
    dientes = 8
    puntos = []
    for i in range(dientes * 4):
        angulo = 2 * math.pi * i / (dientes * 4)
        # cada diente: 2 puntos en el radio exterior y 2 en el interior
        r = radio if i % 4 in (0, 1) else radio * 0.75
        puntos.append((centro[0] + r * math.cos(angulo),
                       centro[1] + r * math.sin(angulo)))
    pygame.draw.polygon(pantalla, color, puntos)
    pygame.draw.circle(pantalla, aj.COLOR_FONDO, centro, int(radio * 0.35))


def punto_en_engranaje(pos):
    """Devuelve True si el punto 'pos' cae sobre el engranaje del menú."""
    cx, cy = aj.ENGRANAJE_CENTRO
    return math.hypot(pos[0] - cx, pos[1] - cy) <= aj.ENGRANAJE_RADIO