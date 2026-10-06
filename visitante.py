"""Clase Visitante: un empleado (o impostor) que llega a la puerta."""

import math

import pygame

import ajustes as aj


class Visitante:
    """Empleado que camina hasta la puerta de la fábrica y pide entrar.

    Atributos:
        nombre, rubro: lo que dice ser.
        lugar, piso: adónde dice ir (área de la fábrica y piso).
        imagen_id: prefijo de sus imágenes (qué personaje es).
        nombre_documento, rubro_documento: lo que figura en su documento.
        es_impostor: True si es un monstruo disfrazado.
        motivo: qué lo delata (None si es verdadero).
        paciencia_max / paciencia: segundos totales y restantes de espera.
        exigiendo: lo que reclama que le devuelvan ("" si nada).
        x: centro horizontal de la imagen (float para moverse suave).
        rect: rectángulo donde se dibujó la imagen por última vez.
    """

    def __init__(self, nombre, rubro, lugar, piso, imagen_id, es_impostor,
                 motivo=None, paciencia=aj.PACIENCIA_BASE,
                 nombre_documento=None, rubro_documento=None):
        """Crea al empleado con sus datos y lo ubica fuera de pantalla."""
        self.nombre = nombre
        self.rubro = rubro
        self.lugar = lugar
        self.piso = piso
        self.imagen_id = imagen_id
        self.es_impostor = es_impostor
        self.motivo = motivo
        self.nombre_documento = nombre_documento or nombre
        self.rubro_documento = rubro_documento or rubro
        self.paciencia_max = paciencia
        self.paciencia = paciencia
        self.exigiendo = ""
        self.x = float(aj.VISITANTE_X_INICIAL)
        self.rect = pygame.Rect(int(self.x),
                                aj.VISITANTE_BASE_Y - aj.VISITANTE_IMG_ALTO,
                                1, aj.VISITANTE_IMG_ALTO)

    def actualizar(self, dt):
        """Hace caminar al empleado hasta la puerta (dt en segundos).

        Devuelve True solo en el cuadro exacto en que llega (para el timbre).
        """
        ya_estaba = self.llego()
        if not ya_estaba:
            self.x = min(self.x + aj.VISITANTE_VELOCIDAD * dt,
                         aj.VISITANTE_X_DESTINO)
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

    def variante(self):
        """Devuelve cuál de las 4 imágenes corresponde ahora.

        "normal", "normal_enojado", "impostor" o "impostor_enojado".
        """
        base = "impostor" if self.es_impostor else "normal"
        return base + "_enojado" if self.impaciente() else base

    def frases(self):
        """Devuelve la lista de cosas que dice el empleado."""
        donde = aj.LUGARES[self.lugar]["donde"]
        return [
            f"Hola, soy {self.nombre}. Trabajo de {self.rubro}.",
            f"Voy {donde}, en el piso {self.piso}.",
        ]

    def dibujar(self, pantalla, imagenes):
        """Dibuja la imagen del empleado apoyada en VISITANTE_BASE_Y.

        Si está enojado, además tiembla un poco.
        """
        imagen = imagenes["visitantes"][self.imagen_id][self.variante()]
        sacudida = 0
        if self.impaciente():
            sacudida = int(aj.SACUDIDA_ENOJADO
                           * math.sin(pygame.time.get_ticks() / 30))
        self.rect = imagen.get_rect(
            midbottom=(int(self.x) + sacudida, aj.VISITANTE_BASE_Y))
        pantalla.blit(imagen, self.rect)

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
        x = int(self.x) - aj.BARRA_ANCHO // 2
        y = self.rect.top - 16
        pygame.draw.rect(pantalla, aj.COLOR_BARRA_FONDO,
                         (x - 1, y - 1, aj.BARRA_ANCHO + 2, aj.BARRA_ALTO + 2))
        pygame.draw.rect(pantalla, color,
                         (x, y, int(aj.BARRA_ANCHO * fraccion), aj.BARRA_ALTO))