"""Dibujo de cada pantalla: menú, ayudas, configuración y partida."""

import pygame

import ajustes as aj
from interfaz import Boton, dibujar_engranaje, punto_en_engranaje


def crear_botones():
    """Devuelve un diccionario con todos los botones del juego."""
    cx = aj.ANCHO // 2
    return {
        "jugar": Boton("Jugar", (cx, 240)),
        "instrucciones": Boton("Instrucciones", (cx, 305)),
        "objetivo": Boton("Objetivo", (cx, 370)),
        "sonido": Boton("Sonido: SÍ", (cx, 320)),
        "volver": Boton("Volver", (cx, 400)),
        "permitir": Boton("PERMITIR [A]", (715, 470), 150, 50,
                          aj.COLOR_PERMITIR, aj.COLOR_PERMITIR_HOVER),
        "rechazar": Boton("RECHAZAR [R]", (875, 470), 150, 50,
                          aj.COLOR_RECHAZAR, aj.COLOR_RECHAZAR_HOVER),
        "siguiente": Boton("Siguiente noche", (cx, 340)),
        "reintentar": Boton("Reintentar", (cx, 340)),
        "de_nuevo": Boton("Jugar de nuevo", (cx, 340)),
        "menu": Boton("Menú", (cx, 400)),
    }


def dibujar_escenario(pantalla):
    """Dibuja la pared y la puerta del edificio."""
    pygame.draw.rect(pantalla, aj.COLOR_PARED, (0, 0, aj.ANCHO, aj.SUELO_Y))
    pygame.draw.rect(pantalla, aj.COLOR_PUERTA, aj.PUERTA_RECT)


def _texto_centrado(pantalla, fuente, texto, color, y):
    """Dibuja 'texto' centrado horizontalmente a la altura y."""
    imagen = fuente.render(texto, True, color)
    pantalla.blit(imagen, imagen.get_rect(center=(aj.ANCHO // 2, y)))


def dibujar_menu(pantalla, fuentes, ui, pos_mouse):
    """Dibuja la pantalla inicial: título, botones y engranaje."""
    dibujar_escenario(pantalla)
    # el título parpadea de vez en cuando, como una luz fallando
    apagado = (pygame.time.get_ticks() // 90) % 31 == 0
    color = (110, 30, 30) if apagado else aj.COLOR_TITULO
    _texto_centrado(pantalla, fuentes["titulo"], aj.TITULO.upper(), color, 110)
    _texto_centrado(pantalla, fuentes["media"], aj.SUBTITULO,
                    aj.COLOR_SECUNDARIO, 170)
    for nombre in ("jugar", "instrucciones", "objetivo"):
        ui[nombre].dibujar(pantalla, fuentes["media"], pos_mouse)
    encima = punto_en_engranaje(pos_mouse)
    dibujar_engranaje(pantalla, aj.ENGRANAJE_CENTRO, aj.ENGRANAJE_RADIO,
                      aj.COLOR_TEXTO if encima else aj.COLOR_SECUNDARIO)
    _texto_centrado(pantalla, fuentes["chica"], "ESC para salir",
                    aj.COLOR_SECUNDARIO, 515)


def dibujar_texto(pantalla, fuentes, titulo, lineas):
    """Dibuja una pantalla de ayuda con un título y varias líneas."""
    dibujar_escenario(pantalla)
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, (80, 50, 800, 440),
                     border_radius=10)
    _texto_centrado(pantalla, fuentes["grande"], titulo, aj.COLOR_TITULO, 95)
    y = 150
    for linea in lineas:
        imagen = fuentes["media"].render(linea, True, aj.COLOR_TEXTO)
        pantalla.blit(imagen, (120, y))
        y += 30
    _texto_centrado(pantalla, fuentes["chica"],
                    "Hacé clic o apretá cualquier tecla para volver",
                    aj.COLOR_SECUNDARIO, 465)


def dibujar_config(pantalla, fuentes, ui, deslizador, pos_mouse):
    """Dibuja la pantalla de configuración: volumen y sonido."""
    dibujar_escenario(pantalla)
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, (200, 70, 560, 400),
                     border_radius=10)
    _texto_centrado(pantalla, fuentes["grande"], "CONFIGURACIÓN",
                    aj.COLOR_TITULO, 115)
    etiqueta = fuentes["media"].render(
        f"Volumen: {int(deslizador.valor * 100)}%", True, aj.COLOR_TEXTO)
    pantalla.blit(etiqueta, (aj.SLIDER_X, 190))
    deslizador.dibujar(pantalla)
    ui["sonido"].dibujar(pantalla, fuentes["media"], pos_mouse)
    ui["volver"].dibujar(pantalla, fuentes["media"], pos_mouse)


def dibujar_libro(pantalla, fuentes, nivel):
    """Dibuja el libro con los vecinos de la noche actual."""
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, (640, 10, 310, 255))
    pantalla.blit(fuentes["normal"].render("LIBRO DE RESIDENTES", True,
                                           aj.COLOR_TEXTO), (650, 16))
    y = 42
    for apto, d in list(aj.RESIDENTES.items())[:nivel["residentes"]]:
        rasgos = f"pelo {d['pelo']}"
        if d["lentes"]:
            rasgos += ", lentes"
        if d["bigote"]:
            rasgos += ", bigote"
        rasgos += f" · {d['mascota']}"
        pantalla.blit(fuentes["normal"].render(f"{apto} {d['nombre']}", True,
                                               aj.COLOR_TEXTO), (650, y))
        pantalla.blit(fuentes["chica"].render(rasgos, True,
                                              aj.COLOR_SECUNDARIO),
                      (650, y + 20))
        y += 44


def dibujar_ficha(pantalla, fuentes, visitante):
    """Dibuja lo que dice el visitante y las teclas de decisión."""
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, (20, 420, 600, 100))
    lineas = [f"«{f}»" for f in visitante.frases()]
    lineas.append("[A] Permitir     [R] Rechazar")
    for i, linea in enumerate(lineas):
        pantalla.blit(fuentes["normal"].render(linea, True, aj.COLOR_TEXTO),
                      (30, 430 + i * 26))


def dibujar_juego(pantalla, partida, fuentes, ui, pos_mouse, activo):
    """Dibuja la escena de juego completa.

    'activo' indica si se puede decidir (muestra los botones de decisión).
    """
    dibujar_escenario(pantalla)
    visitante = partida.visitante
    visitante.dibujar(pantalla)
    visitante.dibujar_paciencia(pantalla)
    nivel = partida.config_nivel()
    dibujar_libro(pantalla, fuentes, nivel)
    if visitante.llego():
        dibujar_ficha(pantalla, fuentes, visitante)
        if activo:
            ui["permitir"].dibujar(pantalla, fuentes["media"], pos_mouse)
            ui["rechazar"].dibujar(pantalla, fuentes["media"], pos_mouse)

    actual = min(partida.atendidos + 1, nivel["visitantes"])
    pantalla.blit(fuentes["grande"].render(
        f"Puntaje: {partida.puntaje}  Vidas: {partida.vidas}  "
        f"Racha: {partida.racha}", True, aj.COLOR_TEXTO), (20, 12))
    pantalla.blit(fuentes["media"].render(
        f"{nivel['nombre']} de {len(aj.NIVELES)} · "
        f"Visitante {actual}/{nivel['visitantes']}", True,
        aj.COLOR_SECUNDARIO), (20, 50))
    pantalla.blit(fuentes["normal"].render(partida.mensaje, True,
                                           partida.color_mensaje), (20, 80))


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
                  "más vecinos y menos paciencia."]
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