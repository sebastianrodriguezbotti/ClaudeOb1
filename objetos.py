"""Objetos arrastrables: documento, autorización y sellos."""

import pygame

import ajustes as aj


class Arrastrable:
    """Base de todo lo que se agarra con el mouse y se mueve por la pantalla.

    Atributos:
        rect: posición y tamaño en pantalla.
        arrastrando: True mientras el jugador lo tiene agarrado.
        desfase: dónde se agarró, respecto de la esquina del rect.
    """

    def __init__(self, rect):
        """Crea el elemento con el rectángulo dado."""
        self.rect = rect
        self.arrastrando = False
        self.desfase = (0, 0)

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


class Objeto(Arrastrable):
    """Papel que entrega el empleado: su documento o la autorización.

    Atributos:
        tipo: "documento" o "autorizacion".
        nombre, rubro, piso, lugar: datos que se leen en el papel.
        sello: None (sin sellar), True (APROBADO) o False (RECHAZADO).
    """

    def __init__(self, tipo, visitante):
        """Crea el papel con los datos del empleado, en su lugar de salida."""
        ancho, alto = aj.OBJETO_TAMANOS[tipo]
        rect = pygame.Rect(0, 0, ancho, alto)
        rect.center = aj.OBJETO_SPAWN[tipo]
        super().__init__(rect)
        self.tipo = tipo
        # el documento puede traer datos distintos a lo que dice el empleado
        self.nombre = (visitante.nombre_documento if tipo == "documento"
                       else visitante.nombre)
        self.rubro = visitante.rubro_documento
        self.imagen_id = visitante.imagen_id      # de quién es la foto
        self.piso = visitante.piso
        self.lugar = visitante.lugar
        self.sello = None

    def dibujar(self, pantalla, fuentes, imagenes):
        """Dibuja el papel con su sombra y el contenido según el tipo."""
        desfase = 6 if self.arrastrando else 3
        pygame.draw.rect(pantalla, aj.COLOR_SOMBRA,
                         self.rect.move(desfase, desfase))
        pygame.draw.rect(pantalla, aj.COLOR_PAPEL, self.rect)
        pygame.draw.rect(pantalla, aj.COLOR_TINTA, self.rect, 2)
        if self.tipo == "documento":
            self._dibujar_foto(pantalla, imagenes)
            self._escribir(pantalla, fuentes, "DOCUMENTO DE EMPLEADO",
                           [f"Nombre: {self.nombre}",
                            f"Rubro: {self.rubro}"],
                           desplazamiento_x=aj.FOTO_CAJA[0] + 12, y_lineas=44)
        else:
            self._escribir(pantalla, fuentes, "AUTORIZACIÓN DE INGRESO",
                           [f"Nombre: {self.nombre}",
                            f"Piso: {self.piso}",
                            f"Área: {self.lugar}"])
            self._dibujar_zona_sello(pantalla, fuentes)

    def _escribir(self, pantalla, fuentes, encabezado, lineas,
                  desplazamiento_x=0, y_lineas=34):
        """Escribe el encabezado, una raya y las líneas de datos."""
        x, y = self.rect.x + 10, self.rect.y + 8
        pantalla.blit(fuentes["chica"].render(encabezado, True,
                                              aj.COLOR_TINTA), (x, y))
        pygame.draw.line(pantalla, aj.COLOR_TINTA, (x, y + 24),
                         (self.rect.right - 10, y + 24), 1)
        for i, linea in enumerate(lineas):
            pantalla.blit(fuentes["chica"].render(linea, True, aj.COLOR_TINTA),
                          (x + desplazamiento_x, y + y_lineas + i * 22))

    def _dibujar_foto(self, pantalla, imagenes):
        """Dibuja la foto (retrato del personaje) a la izquierda del documento."""
        caja = pygame.Rect(self.rect.x + 10, self.rect.y + 38, *aj.FOTO_CAJA)
        pygame.draw.rect(pantalla, aj.COLOR_FOTO_FONDO, caja)
        retrato = imagenes["fotos"][self.imagen_id]
        pantalla.blit(retrato, retrato.get_rect(center=caja.center))
        pygame.draw.rect(pantalla, aj.COLOR_TINTA, caja, 1)

    def _dibujar_zona_sello(self, pantalla, fuentes):
        """Dibuja el recuadro donde va el sello (vacío o ya sellado)."""
        zona = pygame.Rect(self.rect.x + 10, self.rect.bottom - 46,
                           self.rect.width - 20, 36)
        if self.sello is None:
            pygame.draw.rect(pantalla, aj.COLOR_TINTA, zona, 1)
            texto, color, fuente = "SELLO AQUÍ", aj.COLOR_TINTA, "chica"
        else:
            color = aj.COLOR_PERMITIR if self.sello else aj.COLOR_RECHAZAR
            pygame.draw.rect(pantalla, color, zona, 3)
            texto = "APROBADO" if self.sello else "RECHAZADO"
            fuente = "normal"
        imagen = fuentes[fuente].render(texto, True, color)
        pantalla.blit(imagen, imagen.get_rect(center=zona.center))


class Sello(Arrastrable):
    """Sello de la bandeja: APROBADO (True) o RECHAZADO (False).

    Se arrastra hasta la autorización. Si se suelta en otro lado, vuelve
    a la bandeja.
    """

    def __init__(self, valor, centro):
        """Crea el sello en su lugar de la bandeja."""
        rect = pygame.Rect(0, 0, *aj.SELLO_TAMANO)
        rect.center = centro
        super().__init__(rect)
        self.valor = valor
        self.origen = centro

    def volver(self):
        """Lo devuelve a la bandeja."""
        self.arrastrando = False
        self.rect.center = self.origen

    def dibujar(self, pantalla, fuentes):
        """Dibuja el sello: un mango arriba y la base con el texto."""
        color = aj.COLOR_PERMITIR_HOVER if self.valor else aj.COLOR_RECHAZAR_HOVER
        texto = "APROBADO" if self.valor else "RECHAZADO"
        desfase = 6 if self.arrastrando else 2
        base = pygame.Rect(self.rect.x, self.rect.y + 16, self.rect.width,
                           self.rect.height - 16)
        mango = pygame.Rect(self.rect.centerx - 30, self.rect.y, 60, 20)
        pygame.draw.rect(pantalla, aj.COLOR_SOMBRA,
                         base.move(desfase, desfase), border_radius=6)
        pygame.draw.rect(pantalla, aj.COLOR_SELLO_MANGO, mango,
                         border_radius=6)
        pygame.draw.rect(pantalla, color, base, border_radius=6)
        pygame.draw.rect(pantalla, aj.COLOR_BORDE, base, 2, border_radius=6)
        imagen = fuentes["media"].render(texto, True, aj.COLOR_TEXTO)
        pantalla.blit(imagen, imagen.get_rect(center=base.center))