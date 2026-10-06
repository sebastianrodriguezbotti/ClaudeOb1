"""Clase Objeto: documento o foto que el visitante entrega y se arrastra."""

import pygame

import ajustes as aj


class Objeto:
    """Documento o foto del visitante, que se puede arrastrar con el mouse.

    Atributos:
        tipo: "documento" o "foto".
        nombre, apartamento: datos del visitante que figuran en el documento.
        imagen_id: personaje cuyo retrato se ve en la foto.
        rect: posición y tamaño en pantalla.
        arrastrando: True mientras el jugador lo tiene agarrado.
    """

    def __init__(self, tipo, visitante):
        """Crea el objeto con los datos del visitante, en su lugar de salida."""
        self.tipo = tipo
        self.nombre = visitante.nombre
        self.apartamento = visitante.apartamento
        self.imagen_id = visitante.imagen_id
        ancho, alto = aj.OBJETO_TAMANOS[tipo]
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect.center = aj.OBJETO_SPAWN[tipo]
        self.arrastrando = False
        self.desfase = (0, 0)   # dónde se agarró, respecto de su esquina

    def manejar_evento(self, evento):
        """Procesa un evento del mouse.

        Devuelve "agarrado", "movido", "soltado" o None si no pasó nada.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.arrastrando = True
                self.desfase = (self.rect.x - evento.pos[0],
                                self.rect.y - evento.pos[1])
                return "agarrado"
        elif evento.type == pygame.MOUSEMOTION and self.arrastrando:
            self.rect.x = evento.pos[0] + self.desfase[0]
            self.rect.y = evento.pos[1] + self.desfase[1]
            self.rect.clamp_ip(pygame.Rect(0, 0, aj.ANCHO, aj.ALTO))
            return "movido"
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.arrastrando:
                self.arrastrando = False
                return "soltado"
        return None

    def dibujar(self, pantalla, fuentes, imagenes):
        """Dibuja el papel con su sombra y el contenido según el tipo."""
        desfase = 6 if self.arrastrando else 3
        pygame.draw.rect(pantalla, aj.COLOR_SOMBRA,
                         self.rect.move(desfase, desfase))
        pygame.draw.rect(pantalla, aj.COLOR_PAPEL, self.rect)
        pygame.draw.rect(pantalla, aj.COLOR_TINTA, self.rect, 2)
        if self.tipo == "documento":
            self._dibujar_documento(pantalla, fuentes)
        else:
            self._dibujar_foto(pantalla, imagenes)

    def _dibujar_documento(self, pantalla, fuentes):
        """Escribe el encabezado, el nombre y el apartamento."""
        x, y = self.rect.x + 10, self.rect.y + 8
        textos = [("DOCUMENTO DE RESIDENTE", 0), (f"Nombre: {self.nombre}", 40),
                  (f"Apto: {self.apartamento}", 66)]
        for texto, desplazamiento in textos:
            pantalla.blit(fuentes["chica"].render(texto, True, aj.COLOR_TINTA),
                          (x, y + desplazamiento))
        pygame.draw.line(pantalla, aj.COLOR_TINTA, (x, y + 24),
                         (self.rect.right - 10, y + 24), 1)

    def _dibujar_foto(self, pantalla, imagenes):
        """Dibuja el retrato del personaje dentro del marco."""
        caja = pygame.Rect(self.rect.x + 10, self.rect.y + 10, *aj.FOTO_CAJA)
        pygame.draw.rect(pantalla, aj.COLOR_FOTO_FONDO, caja)
        retrato = imagenes["fotos"][self.imagen_id]
        pantalla.blit(retrato, retrato.get_rect(center=caja.center))