"""Dibujo de cada pantalla: menú, ayudas, configuración, partida y pausa."""

import textwrap

import pygame

import ajustes as aj
from interfaz import Boton, dibujar_engranaje, punto_en_engranaje


def crear_botones():
    """Devuelve un diccionario con todos los botones (datos en ajustes.py)."""
    return {nombre: Boton(*datos) for nombre, datos in aj.BOTONES.items()}


def dibujar_escenario(pantalla, imagenes, visitante=None):
    """Dibuja las capas de atrás hacia adelante.

    Orden: fondo2 (atrás), empleado (en el medio, si hay) y fondo1 (adelante).
    """
    pantalla.blit(imagenes["fondo2"], (0, 0))
    if visitante is not None:
        visitante.dibujar(pantalla, imagenes)
    pantalla.blit(imagenes["fondo1"], (0, 0))


def _texto_centrado(pantalla, fuente, texto, color, y):
    """Dibuja 'texto' centrado horizontalmente a la altura y."""
    imagen = fuente.render(texto, True, color)
    pantalla.blit(imagen, imagen.get_rect(center=(aj.ANCHO // 2, y)))


def _boton_menu(pantalla, boton, fuente, pos_mouse):
    """Dibuja un botón del menú: oscuro, con borde rojo que se enciende."""
    encima = boton.bajo_mouse(pos_mouse)
    pygame.draw.rect(pantalla, aj.COLOR_MENU_BOTON_HOVER if encima
                     else aj.COLOR_MENU_BOTON, boton.rect, border_radius=4)
    pygame.draw.rect(pantalla, aj.COLOR_MENU_BORDE_HOVER if encima
                     else aj.COLOR_MENU_BORDE, boton.rect, 2, border_radius=4)
    imagen = fuente.render(boton.texto.upper(), True, aj.COLOR_MENU_TEXTO)
    pantalla.blit(imagen, imagen.get_rect(center=boton.rect.center))


def dibujar_menu(pantalla, fuentes, ui, pos_mouse, imagenes):
    """Dibuja la pantalla inicial: título, botones y engranaje.

    Usa la tipografía y los colores del afiche (título con resplandor rojo,
    letra de máquina de escribir).
    """
    dibujar_escenario(pantalla, imagenes)
    # el título parpadea de vez en cuando, como una luz fallando
    apagado = (pygame.time.get_ticks() // aj.PARPADEO_MS) % aj.PARPADEO_CADA == 0
    versiones = imagenes.get("titulo")
    if versiones:
        imagen = versiones["apagado" if apagado else "encendido"]
        pantalla.blit(imagen, imagen.get_rect(center=(aj.ANCHO // 2,
                                                      aj.MENU_TITULO_Y)))
    else:       # si no se pudo armar el efecto: texto simple
        color = aj.COLOR_TITULO_APAGADO if apagado else aj.COLOR_TITULO
        _texto_centrado(pantalla, fuentes["titulo"], aj.TITULO.upper(), color,
                        aj.MENU_TITULO_Y)
    _texto_centrado(pantalla, fuentes["menu_texto"], aj.SUBTITULO,
                    aj.COLOR_MENU_SECUNDARIO, aj.MENU_SUBTITULO_Y)
    for nombre in ("jugar", "instrucciones", "objetivo"):
        _boton_menu(pantalla, ui[nombre], fuentes["menu_texto"], pos_mouse)
    encima = punto_en_engranaje(pos_mouse)
    dibujar_engranaje(pantalla, aj.ENGRANAJE_CENTRO, aj.ENGRANAJE_RADIO,
                      aj.COLOR_MENU_BORDE_HOVER if encima
                      else aj.COLOR_MENU_BORDE)
    _texto_centrado(pantalla, fuentes["menu_chica"], aj.MENU_LEMA,
                    aj.COLOR_MENU_SECUNDARIO, aj.MENU_LEMA_Y)
    _texto_centrado(pantalla, fuentes["menu_chica"], "ESC para salir",
                    aj.COLOR_SECUNDARIO, aj.MENU_LEMA_Y + 24)


def dibujar_texto(pantalla, fuentes, titulo, lineas, imagenes):
    """Dibuja una pantalla de ayuda con un título y varias líneas."""
    dibujar_escenario(pantalla, imagenes)
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, aj.PANEL_AYUDA,
                     border_radius=10)
    _texto_centrado(pantalla, fuentes["grande"], titulo, aj.COLOR_TITULO, 95)
    y = aj.AYUDA_Y
    for linea in lineas:
        imagen = fuentes["media"].render(linea, True, aj.COLOR_TEXTO)
        pantalla.blit(imagen, (120, y))
        y += aj.AYUDA_PASO
    _texto_centrado(pantalla, fuentes["chica"],
                    "Hacé clic o apretá cualquier tecla para volver",
                    aj.COLOR_SECUNDARIO, 465)


def dibujar_config(pantalla, fuentes, ui, deslizadores, pos_mouse, imagenes):
    """Dibuja la pantalla de configuración: volúmenes y sonido sí/no."""
    dibujar_escenario(pantalla, imagenes)
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, aj.PANEL_CONFIG,
                     border_radius=10)
    _texto_centrado(pantalla, fuentes["grande"], "CONFIGURACIÓN",
                    aj.COLOR_TITULO, 115)
    for nombre, texto in (("efectos", "Efectos"), ("musica", "Música")):
        deslizador = deslizadores[nombre]
        etiqueta = fuentes["media"].render(
            f"{texto}: {int(deslizador.valor * 100)}%", True, aj.COLOR_TEXTO)
        pantalla.blit(etiqueta, (aj.SLIDER_X, deslizador.rect.y - 35))
        deslizador.dibujar(pantalla)
    ui["sonido"].dibujar(pantalla, fuentes["media"], pos_mouse)
    ui["volver"].dibujar(pantalla, fuentes["media"], pos_mouse)


def dibujar_historia(pantalla, velo, fuentes, imagenes, titulo, paginas,
                     pagina, letras):
    """Dibuja una pantalla de la historia; el texto aparece letra por letra.

    'titulo' es el nombre de la noche, 'paginas' la lista de textos de esa
    historia y 'letras' cuántas letras de la página se ven hasta ahora.
    """
    dibujar_escenario(pantalla, imagenes)
    pantalla.blit(velo, (0, 0))
    _texto_centrado(pantalla, fuentes["grande"], titulo, aj.COLOR_TITULO, 120)
    texto = paginas[pagina]
    restantes = letras
    for i, linea in enumerate(textwrap.wrap(texto, aj.HISTORIA_ANCHO_LINEA)):
        parte = linea[:max(0, restantes)]
        restantes -= len(linea) + 1            # +1 por el espacio cortado
        if parte:
            _texto_centrado(pantalla, fuentes["grande"], parte, aj.COLOR_TEXTO,
                            aj.HISTORIA_Y + i * aj.HISTORIA_PASO)
    _texto_centrado(pantalla, fuentes["chica"],
                    f"{pagina + 1}/{len(paginas)}   "
                    "Clic o ENTER: seguir · ESC: saltar la historia",
                    aj.COLOR_SECUNDARIO, 495)


def dibujar_edificio(pantalla, fuentes, nivel):
    """Dibuja el directorio de la fábrica: qué hay en cada piso."""
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, aj.PANEL_EDIFICIO)
    pantalla.blit(fuentes["normal"].render("EDIFICIO", True, aj.COLOR_TEXTO),
                  (650, 16))
    pisos = {}
    for datos in aj.EMPLEADOS[:nivel["empleados"]]:
        lugar = datos["lugar"]
        pisos.setdefault(aj.LUGARES[lugar]["piso"], []).append(lugar)
    y = 42
    for piso in sorted(pisos):
        pantalla.blit(fuentes["normal"].render(f"PISO {piso}", True,
                                               aj.COLOR_TEXTO), (650, y))
        y += 20
        for lugar in pisos[piso]:
            personal = aj.LUGARES[lugar]["personal"]
            pantalla.blit(fuentes["chica"].render(
                f"{lugar} ({personal})", True, aj.COLOR_SECUNDARIO),
                (665, y))
            y += 17


def dibujar_ficha(pantalla, fuentes, visitante):
    """Dibuja lo que dice el empleado."""
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, aj.PANEL_FICHA)
    lineas = [(f"«{f}»", aj.COLOR_TEXTO) for f in visitante.frases()]
    for i, (linea, color) in enumerate(lineas):
        pantalla.blit(fuentes["normal"].render(linea, True, color),
                      (30, 455 + i * 26))


def dibujar_juego(pantalla, partida, fuentes, ui, pos_mouse, activo,
                  imagenes):
    """Dibuja la escena de juego completa.

    'activo' indica si se puede jugar (muestra el botón de pausa, el menú
    de pedidos y la pista).
    """
    visitante = partida.visitante
    dibujar_escenario(pantalla, imagenes, visitante)   # fondo2, empleado, fondo1
    visitante.dibujar_paciencia(pantalla)
    nivel = partida.config_nivel()
    dibujar_edificio(pantalla, fuentes, nivel)
    if visitante.llego():
        dibujar_ficha(pantalla, fuentes, visitante)
        pygame.draw.rect(pantalla, aj.COLOR_PANEL, aj.PANEL_BANDEJA,
                         border_radius=8)             # bandeja de sellos

    actual = min(partida.atendidos + 1, nivel["visitantes"])
    pantalla.blit(fuentes["grande"].render(
        f"Puntaje: {partida.puntaje}  Vidas: {partida.vidas}  "
        f"Racha: {partida.racha}", True, aj.COLOR_TEXTO), (20, 12))
    pantalla.blit(fuentes["media"].render(
        f"{nivel['nombre']} de {len(aj.NIVELES)} · "
        f"Empleado {actual}/{nivel['visitantes']}", True,
        aj.COLOR_SECUNDARIO), (20, 50))
    if len(partida.mensaje) <= aj.MENSAJE_LARGO:
        lineas, fuente, paso = [partida.mensaje], fuentes["normal"], 22
    else:        # mensaje largo (varias pistas): letra chica y varias líneas
        lineas = textwrap.wrap(partida.mensaje, aj.MENSAJE_ANCHO_LINEA)
        fuente, paso = fuentes["chica"], 18
    for i, linea in enumerate(lineas):
        pantalla.blit(fuente.render(linea, True, partida.color_mensaje),
                      (20, 80 + i * paso))

    if activo:
        ui["pausa"].dibujar(pantalla, fuentes["normal"], pos_mouse)
    for objeto in partida.objetos:            # papeles arriba de la escena
        objeto.dibujar(pantalla, fuentes, imagenes)
    if visitante.llego():
        for sello in partida.sellos:          # los sellos, arriba de todo
            sello.dibujar(pantalla, fuentes)
    if activo and visitante.llego():
        arrastrando = (any(o.arrastrando for o in partida.objetos)
                       or any(s.arrastrando for s in partida.sellos))
        if partida.menu_abierto:
            for tipo in partida.opciones_disponibles():
                ui[f"pedir_{tipo}"].dibujar(pantalla, fuentes["media"],
                                            pos_mouse)
        elif (visitante.rect.collidepoint(pos_mouse)
              and partida.opciones_disponibles() and not arrastrando):
            # pista junto al mouse
            pygame.draw.rect(pantalla, aj.COLOR_PANEL,
                             (pos_mouse[0] + 14, pos_mouse[1] + 14, *aj.PISTA_TAMANO))
            pantalla.blit(fuentes["chica"].render(
                "Clic: pedir documento o autorización", True,
                aj.COLOR_TEXTO), (pos_mouse[0] + 20, pos_mouse[1] + 18))


def dibujar_pausa(pantalla, velo, fuentes, ui, pos_mouse):
    """Dibuja el velo oscuro y el menú de pausa."""
    pantalla.blit(velo, (0, 0))
    _texto_centrado(pantalla, fuentes["grande"], "PAUSA", aj.COLOR_TITULO, 130)
    for nombre in ("p_continuar", "p_instrucciones", "p_volumen", "p_inicio"):
        ui[nombre].dibujar(pantalla, fuentes["media"], pos_mouse)


def dibujar_pantalla_final(pantalla, velo, estado, partida, fuentes, ui,
                           pos_mouse):
    """Dibuja el velo oscuro y el cartel de nivel completo, fin o victoria."""
    pantalla.blit(velo, (0, 0))
    nivel = partida.config_nivel()
    if estado == aj.ESTADO_NIVEL_COMPLETO:
        titulo = f"¡{nivel['nombre'].upper()} COMPLETADA!"
        color = aj.COLOR_ACIERTO
        lineas = [f"Puntaje: {partida.puntaje}",
                  "La próxima noche será más difícil:",
                  "más puestos en el edificio y menos tiempo."]
        botones = ["siguiente"]
    elif estado == aj.ESTADO_FIN:
        titulo, color = "FIN DE LA PARTIDA", aj.COLOR_ERROR
        lineas = [f"Puntaje final: {partida.puntaje}", partida.mensaje]
        botones = ["reintentar", "menu"]
    else:
        titulo = f"¡SOBREVIVISTE LAS {len(aj.NIVELES)} NOCHES!"
        color = aj.COLOR_ACIERTO
        lineas = [f"Puntaje final: {partida.puntaje}"]
        botones = ["de_nuevo", "menu"]
    _texto_centrado(pantalla, fuentes["grande"], titulo, color, 140)
    for i, linea in enumerate(lineas):
        _texto_centrado(pantalla, fuentes["media"], linea, aj.COLOR_TEXTO,
                        200 + i * 35)
    for nombre in botones:
        ui[nombre].dibujar(pantalla, fuentes["media"], pos_mouse)