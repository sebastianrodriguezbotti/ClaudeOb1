"""Portero de Medianoche - paso 5: temporizador de paciencia (giro propio).

Cada visitante camina hasta la puerta. El jugador compara su aspecto y lo
que dice con el libro de residentes y decide: A = permitir, R = rechazar.
Si tarda demasiado, el visitante se impacienta y se pierde una vida.
Al perder todas las vidas aparece la pantalla de fin; ENTER reinicia.
"""

import pygame

import ajustes as aj
from utilidades import (generar_visitante, decision_correcta,
                        calcular_puntaje, armar_mensaje, nueva_partida,
                        cargar_sonidos, calcular_paciencia)


def dibujar_libro(pantalla, fuente, fuente_chica):
    """Dibuja el libro de residentes (nombre y rasgos de cada vecino)."""
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, (640, 10, 310, 255))
    pantalla.blit(fuente.render("LIBRO DE RESIDENTES", True, aj.COLOR_TEXTO),
                  (650, 16))
    y = 42
    for apto, d in aj.RESIDENTES.items():
        rasgos = f"pelo {d['pelo']}"
        if d["lentes"]:
            rasgos += ", lentes"
        if d["bigote"]:
            rasgos += ", bigote"
        rasgos += f" · {d['mascota']}"
        pantalla.blit(fuente.render(f"{apto} {d['nombre']}", True,
                                    aj.COLOR_TEXTO), (650, y))
        pantalla.blit(fuente_chica.render(rasgos, True, (160, 160, 180)),
                      (650, y + 20))
        y += 44


def dibujar_ficha(pantalla, fuente, visitante):
    """Dibuja lo que dice el visitante y las teclas de decisión."""
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, (20, 420, 600, 100))
    lineas = [f"«{f}»" for f in visitante.frases()]
    lineas.append("[A] Permitir     [R] Rechazar")
    for i, linea in enumerate(lineas):
        pantalla.blit(fuente.render(linea, True, aj.COLOR_TEXTO),
                      (30, 430 + i * 26))


def main():
    """Inicializa pygame, carga recursos y ejecuta el bucle principal."""
    pygame.init()
    pantalla = pygame.display.set_mode((aj.ANCHO, aj.ALTO))
    pygame.display.set_caption(aj.TITULO)
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 18)
    fuente_chica = pygame.font.SysFont("consolas", 15)
    fuente_grande = pygame.font.SysFont("consolas", 28)

    # --- Recursos: se cargan UNA sola vez, antes del bucle ---
    velo = pygame.Surface((aj.ANCHO, aj.ALTO))   # fondo oscuro del "fin"
    velo.set_alpha(190)
    velo.fill((0, 0, 0))
    sonidos = cargar_sonidos()

    # --- Estado de la partida ---
    puntaje, vidas, racha, visitante = nueva_partida()
    estado = aj.ESTADO_JUGANDO
    mensaje = ""
    color_mensaje = aj.COLOR_TEXTO

    corriendo = True
    while corriendo:
        dt = reloj.tick(aj.FPS) / 1000
        decision = None   # None = nadie decidió; True = permitir; False = rechazar

        # 1) EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
                elif estado == aj.ESTADO_FIN:
                    if evento.key == pygame.K_RETURN:   # volver a jugar
                        puntaje, vidas, racha, visitante = nueva_partida()
                        mensaje = ""
                        estado = aj.ESTADO_JUGANDO
                elif visitante.llego() and evento.key in (pygame.K_a,
                                                          pygame.K_r):
                    decision = evento.key == pygame.K_a

        # 2) ACTUALIZAR
        tiempo_agotado = False
        if estado == aj.ESTADO_JUGANDO:
            if visitante.actualizar(dt):   # True al llegar a la puerta
                sonidos["timbre"].play()
            if decision is None and visitante.esperar(dt):
                tiempo_agotado = True

        # 3) RESOLVER: una decisión del jugador o se acabó la paciencia
        if decision is not None or tiempo_agotado:
            acerto = (not tiempo_agotado) and decision_correcta(visitante,
                                                                decision)
            mensaje = armar_mensaje(visitante, acerto, tiempo_agotado)
            if acerto:
                puntaje = calcular_puntaje(puntaje, True, racha)
                racha += 1
                color_mensaje = aj.COLOR_ACIERTO
                sonidos["acierto"].play()
            else:
                vidas -= 1
                racha = 0
                color_mensaje = aj.COLOR_ERROR
                sonidos["error"].play()
            if vidas <= 0:
                estado = aj.ESTADO_FIN
                sonidos["susto"].play()
            else:
                # el siguiente visitante tiene menos paciencia si hay racha
                visitante = generar_visitante(calcular_paciencia(racha))

        # 4) DIBUJAR
        pantalla.fill(aj.COLOR_FONDO)
        pygame.draw.rect(pantalla, aj.COLOR_PARED, (0, 0, aj.ANCHO, aj.SUELO_Y))
        pygame.draw.rect(pantalla, aj.COLOR_PUERTA, aj.PUERTA_RECT)
        visitante.dibujar(pantalla)
        visitante.dibujar_paciencia(pantalla)
        dibujar_libro(pantalla, fuente, fuente_chica)
        if visitante.llego():
            dibujar_ficha(pantalla, fuente, visitante)

        pantalla.blit(fuente_grande.render(
            f"Puntaje: {puntaje}  Vidas: {vidas}  Racha: {racha}",
            True, aj.COLOR_TEXTO), (20, 15))
        pantalla.blit(fuente.render(mensaje, True, color_mensaje), (20, 55))

        if estado == aj.ESTADO_FIN:
            pantalla.blit(velo, (0, 0))
            textos = [
                ("FIN DE LA PARTIDA", fuente_grande, aj.COLOR_ERROR),
                (f"Puntaje final: {puntaje}", fuente_grande, aj.COLOR_TEXTO),
                (mensaje, fuente, aj.COLOR_TEXTO),
                ("ENTER para volver a jugar", fuente, aj.COLOR_ACIERTO),
            ]
            for i, (texto, fnt, color) in enumerate(textos):
                img = fnt.render(texto, True, color)
                pantalla.blit(img, img.get_rect(
                    center=(aj.ANCHO // 2, 190 + i * 45)))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()