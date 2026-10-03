"""Esta noche no - paso 7: imágenes (fondos y visitantes).

Estados: menú, instrucciones, objetivo, configuración, jugando,
nivel completo, fin y victoria. Se maneja con el mouse (botones) y con
el teclado (A = permitir, R = rechazar, ENTER = continuar, ESC = volver).
"""

import pygame

import ajustes as aj
from interfaz import Deslizador, punto_en_engranaje
from pantallas import (crear_botones, dibujar_menu, dibujar_texto,
                       dibujar_config, dibujar_juego, dibujar_pantalla_final)
from partida import Partida
from utilidades import cargar_sonidos, cargar_imagenes, aplicar_volumen


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
    partida = Partida()

    corriendo = True
    while corriendo:
        dt = reloj.tick(aj.FPS) / 1000
        pos_mouse = pygame.mouse.get_pos()
        decision = None   # None = nadie decidió; True = permitir; False = rechazar

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
                else:
                    estado = aj.ESTADO_MENU

            elif estado == aj.ESTADO_MENU:
                if (clic and ui["jugar"].bajo_mouse(clic)) or \
                        tecla == pygame.K_RETURN:
                    partida = Partida()
                    estado = aj.ESTADO_JUGANDO
                elif clic and ui["instrucciones"].bajo_mouse(clic):
                    estado = aj.ESTADO_INSTRUCCIONES
                elif clic and ui["objetivo"].bajo_mouse(clic):
                    estado = aj.ESTADO_OBJETIVO
                elif clic and punto_en_engranaje(clic):
                    deslizador.arrastrando = False
                    estado = aj.ESTADO_CONFIG

            elif estado in (aj.ESTADO_INSTRUCCIONES, aj.ESTADO_OBJETIVO):
                if clic or tecla:            # clic o cualquier tecla: volver
                    estado = aj.ESTADO_MENU

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
                    estado = aj.ESTADO_MENU

            elif estado == aj.ESTADO_JUGANDO:
                if partida.visitante.llego():
                    if tecla == pygame.K_a or (
                            clic and ui["permitir"].bajo_mouse(clic)):
                        decision = True
                    elif tecla == pygame.K_r or (
                            clic and ui["rechazar"].bajo_mouse(clic)):
                        decision = False

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

        # 2) ACTUALIZAR (solo mientras se juega)
        if estado == aj.ESTADO_JUGANDO:
            visitante = partida.visitante
            if visitante.actualizar(dt):   # True al llegar a la puerta
                sonidos["timbre"].play()
            tiempo_agotado = decision is None and visitante.esperar(dt)

            # 3) RESOLVER: una decisión del jugador o se acabó la paciencia
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
            if not jugando:
                dibujar_pantalla_final(pantalla, velo, estado, partida,
                                       fuentes, ui, pos_mouse)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()