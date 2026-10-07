"""Esta noche no - paso 10: entrega de la autorización y personajes al azar.

Estados: menú, instrucciones, objetivo, configuración, jugando, pausa,
nivel completo, fin y victoria. Se maneja con el mouse (botones, clic en el
empleado, arrastrar papeles y sellos) y con el teclado (ENTER = continuar,
ESC = pausa / volver).
"""

import pygame

import ajustes as aj
from interfaz import Deslizador, punto_en_engranaje
from pantallas import (crear_botones, dibujar_menu, dibujar_texto,
                       dibujar_config, dibujar_juego, dibujar_pausa,
                       dibujar_pantalla_final)
from partida import Partida
from utilidades import cargar_sonidos, cargar_imagenes, aplicar_volumen


def manejar_evento_juego(evento, clic, partida, ui, sonidos):
    """Procesa un evento mientras se juega.

    Devuelve (decision, pausa): decision es True (aprobado) o False
    (rechazado) cuando se entrega la autorización sellada, o None;
    pausa es True si se apretó el botón de pausa.
    """
    visitante = partida.visitante

    # 1) Sellos (están arriba de todo). Sellar NO decide.
    if visitante.llego():
        for sello in partida.sellos:
            accion = sello.manejar_evento(evento)
            if accion in ("agarrado", "movido"):
                return None, False
            if accion == "soltado":
                resultado = partida.soltar_sello(sello, evento.pos)
                sello.volver()                 # siempre vuelve a la bandeja
                if resultado == "ok":
                    sonidos["sello"].play()
                elif resultado is not None:
                    sonidos["error"].play()
                return None, False

    # 2) Documento y autorización: el que está arriba tiene prioridad
    for objeto in list(reversed(partida.objetos)):
        accion = objeto.manejar_evento(evento)
        if accion == "agarrado":
            partida.traer_al_frente(objeto)
            return None, False
        if accion == "movido":
            return None, False
        if accion == "soltado":
            if visitante.rect.collidepoint(evento.pos):   # soltado sobre él
                entregado, decision = partida.entregar(objeto)
                sonidos["papel" if entregado else "error"].play()
                return decision, False
            return None, False

    # 3) Clics
    if clic:
        if partida.menu_abierto:
            for tipo in partida.opciones_disponibles():
                if ui[f"pedir_{tipo}"].bajo_mouse(clic):
                    partida.pedir(tipo)
                    sonidos["papel"].play()
                    return None, False
            partida.menu_abierto = False        # clic en otro lado: se cierra
            if visitante.rect.collidepoint(clic):
                return None, False
        if ui["pausa"].bajo_mouse(clic):
            return None, True
        if (visitante.llego() and visitante.rect.collidepoint(clic)
                and partida.opciones_disponibles()):
            partida.menu_abierto = True
    return None, False


def main():
    """Inicializa pygame, carga recursos y ejecuta el bucle principal."""
    pygame.init()
    pantalla = pygame.display.set_mode((aj.ANCHO, aj.ALTO))
    pygame.display.set_caption(aj.TITULO)
    reloj = pygame.time.Clock()

    # --- Recursos: se cargan UNA sola vez, antes del bucle ---
    fuentes = {
        "titulo": pygame.font.SysFont("consolas", 64, bold=True),
        "grande": pygame.font.SysFont("consolas", 28),
        "media": pygame.font.SysFont("consolas", 20),
        "normal": pygame.font.SysFont("consolas", 18),
        "chica": pygame.font.SysFont("consolas", 15),
    }
    velo = pygame.Surface((aj.ANCHO, aj.ALTO))   # fondo oscuro de los carteles
    velo.set_alpha(190)
    velo.fill((0, 0, 0))
    imagenes = cargar_imagenes()
    sonidos = cargar_sonidos()
    ui = crear_botones()
    deslizador = Deslizador(aj.SLIDER_X, aj.SLIDER_Y, aj.SLIDER_ANCHO,
                            aj.VOLUMEN)
    sonido_activo = True
    aplicar_volumen(sonidos, deslizador.valor, sonido_activo)

    # --- Estado ---
    estado = aj.ESTADO_MENU
    origen = aj.ESTADO_MENU   # a dónde vuelven instrucciones y configuración
    partida = Partida()

    corriendo = True
    while corriendo:
        dt = reloj.tick(aj.FPS) / 1000
        pos_mouse = pygame.mouse.get_pos()
        decision = None   # True = aprobado; False = rechazado; None = nadie decidió

        # 1) EVENTOS
        for evento in pygame.event.get():
            # clic = posición si hubo clic izquierdo; tecla = código si hubo tecla
            clic = None
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                clic = evento.pos
            tecla = evento.key if evento.type == pygame.KEYDOWN else None

            if evento.type == pygame.QUIT:
                corriendo = False
            elif tecla == pygame.K_ESCAPE:
                if estado == aj.ESTADO_MENU:
                    corriendo = False
                elif estado == aj.ESTADO_JUGANDO:
                    partida.soltar_todo()
                    estado = aj.ESTADO_PAUSA
                elif estado == aj.ESTADO_PAUSA:
                    estado = aj.ESTADO_JUGANDO
                elif estado in (aj.ESTADO_INSTRUCCIONES, aj.ESTADO_OBJETIVO,
                                aj.ESTADO_CONFIG):
                    estado = origen
                else:
                    estado = aj.ESTADO_MENU

            elif estado == aj.ESTADO_MENU:
                if (clic and ui["jugar"].bajo_mouse(clic)) or \
                        tecla == pygame.K_RETURN:
                    partida = Partida()
                    estado = aj.ESTADO_JUGANDO
                elif clic and ui["instrucciones"].bajo_mouse(clic):
                    origen, estado = aj.ESTADO_MENU, aj.ESTADO_INSTRUCCIONES
                elif clic and ui["objetivo"].bajo_mouse(clic):
                    origen, estado = aj.ESTADO_MENU, aj.ESTADO_OBJETIVO
                elif clic and punto_en_engranaje(clic):
                    deslizador.arrastrando = False
                    origen, estado = aj.ESTADO_MENU, aj.ESTADO_CONFIG

            elif estado in (aj.ESTADO_INSTRUCCIONES, aj.ESTADO_OBJETIVO):
                if clic or tecla:            # clic o cualquier tecla: volver
                    estado = origen

            elif estado == aj.ESTADO_CONFIG:
                accion = deslizador.manejar_evento(evento)
                if accion:
                    aplicar_volumen(sonidos, deslizador.valor, sonido_activo)
                    if accion == "soltado":
                        sonidos["acierto"].play()   # prueba del volumen
                if clic and ui["sonido"].bajo_mouse(clic):
                    sonido_activo = not sonido_activo
                    ui["sonido"].texto = ("Sonido: SÍ" if sonido_activo
                                          else "Sonido: NO")
                    aplicar_volumen(sonidos, deslizador.valor, sonido_activo)
                elif (clic and ui["volver"].bajo_mouse(clic)) or \
                        tecla == pygame.K_RETURN:
                    estado = origen

            elif estado == aj.ESTADO_JUGANDO:
                quedo, pausa = manejar_evento_juego(evento, clic, partida,
                                                    ui, sonidos)
                if quedo is not None:
                    decision = quedo
                if pausa:
                    partida.soltar_todo()
                    estado = aj.ESTADO_PAUSA

            elif estado == aj.ESTADO_PAUSA:
                if clic and ui["p_continuar"].bajo_mouse(clic):
                    estado = aj.ESTADO_JUGANDO
                elif clic and ui["p_instrucciones"].bajo_mouse(clic):
                    origen, estado = aj.ESTADO_PAUSA, aj.ESTADO_INSTRUCCIONES
                elif clic and ui["p_volumen"].bajo_mouse(clic):
                    deslizador.arrastrando = False
                    origen, estado = aj.ESTADO_PAUSA, aj.ESTADO_CONFIG
                elif clic and ui["p_inicio"].bajo_mouse(clic):
                    estado = aj.ESTADO_MENU

            elif estado == aj.ESTADO_NIVEL_COMPLETO:
                if tecla == pygame.K_RETURN or (
                        clic and ui["siguiente"].bajo_mouse(clic)):
                    partida.iniciar_nivel(partida.nivel + 1)
                    estado = aj.ESTADO_JUGANDO

            elif estado in (aj.ESTADO_FIN, aj.ESTADO_VICTORIA):
                otra_vez = (ui["reintentar"] if estado == aj.ESTADO_FIN
                            else ui["de_nuevo"])
                if tecla == pygame.K_RETURN or (
                        clic and otra_vez.bajo_mouse(clic)):
                    partida = Partida()
                    estado = aj.ESTADO_JUGANDO
                elif clic and ui["menu"].bajo_mouse(clic):
                    estado = aj.ESTADO_MENU

        # 2) ACTUALIZAR (solo mientras se juega: en pausa todo queda quieto)
        if estado == aj.ESTADO_JUGANDO:
            visitante = partida.visitante
            if visitante.actualizar(dt):   # True al llegar a la puerta
                sonidos["timbre"].play()
            tiempo_agotado = decision is None and visitante.esperar(dt)

            # 3) RESOLVER: se entregó la autorización sellada o se acabó el tiempo
            if decision is not None or tiempo_agotado:
                acerto, evento_fin = partida.resolver(decision, tiempo_agotado)
                sonidos["acierto" if acerto else "error"].play()
                if evento_fin == "fin":
                    estado = aj.ESTADO_FIN
                    sonidos["susto"].play()
                elif evento_fin == "nivel_completo":
                    estado = aj.ESTADO_NIVEL_COMPLETO
                elif evento_fin == "victoria":
                    estado = aj.ESTADO_VICTORIA

        # 4) DIBUJAR
        pantalla.fill(aj.COLOR_FONDO)
        if estado == aj.ESTADO_MENU:
            dibujar_menu(pantalla, fuentes, ui, pos_mouse, imagenes)
        elif estado == aj.ESTADO_INSTRUCCIONES:
            dibujar_texto(pantalla, fuentes, "INSTRUCCIONES",
                          aj.TEXTO_INSTRUCCIONES, imagenes)
        elif estado == aj.ESTADO_OBJETIVO:
            dibujar_texto(pantalla, fuentes, "OBJETIVO", aj.TEXTO_OBJETIVO,
                          imagenes)
        elif estado == aj.ESTADO_CONFIG:
            dibujar_config(pantalla, fuentes, ui, deslizador, pos_mouse,
                           imagenes)
        else:
            jugando = estado == aj.ESTADO_JUGANDO
            dibujar_juego(pantalla, partida, fuentes, ui, pos_mouse, jugando,
                          imagenes)
            if estado == aj.ESTADO_PAUSA:
                dibujar_pausa(pantalla, velo, fuentes, ui, pos_mouse)
            elif not jugando:
                dibujar_pantalla_final(pantalla, velo, estado, partida,
                                       fuentes, ui, pos_mouse)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()