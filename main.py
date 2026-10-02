"""Portero de Medianoche - paso 2: visitantes y decisiones.

Cada visitante camina hasta la puerta. El jugador compara sus datos con
el libro de residentes y decide: A = permitir, R = rechazar.
"""

import pygame

import ajustes as aj
from utilidades import generar_visitante, decision_correcta, calcular_puntaje


def dibujar_libro(pantalla, fuente):
    """Dibuja el libro de residentes en la esquina superior derecha."""
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, (680, 10, 270, 150))
    pantalla.blit(fuente.render("LIBRO DE RESIDENTES", True, aj.COLOR_TEXTO),
                  (690, 16))
    y = 42
    for apto, nombre in aj.RESIDENTES.items():
        pantalla.blit(fuente.render(f"{apto}: {nombre}", True, aj.COLOR_TEXTO),
                      (690, y))
        y += 22


def dibujar_ficha(pantalla, fuente, visitante):
    """Dibuja los datos que declara el visitante (si ya llegó)."""
    pygame.draw.rect(pantalla, aj.COLOR_PANEL, (20, 420, 640, 100))
    lineas = [
        f"Nombre: {visitante.nombre}",
        f"Apartamento: {visitante.apartamento}",
        f"Dedos en la mano: {visitante.dedos}",
        "[A] Permitir     [R] Rechazar",
    ]
    for i, linea in enumerate(lineas):
        pantalla.blit(fuente.render(linea, True, aj.COLOR_TEXTO),
                      (30, 426 + i * 22))


def main():
    """Inicializa pygame, carga recursos y ejecuta el bucle principal."""
    pygame.init()
    pantalla = pygame.display.set_mode((aj.ANCHO, aj.ALTO))
    pygame.display.set_caption(aj.TITULO)
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 18)
    fuente_grande = pygame.font.SysFont("consolas", 28)

    # --- Recursos: se cargan UNA sola vez, antes del bucle ---
    # (más adelante: sonidos e imágenes)

    # --- Estado de la partida ---
    puntaje = 0
    vidas = aj.VIDAS_INICIALES
    racha = 0
    visitante = generar_visitante()
    mensaje = ""
    color_mensaje = aj.COLOR_TEXTO

    corriendo = True
    while corriendo:
        dt = reloj.tick(aj.FPS) / 1000

        # 1) EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
                # Solo se decide si el visitante llegó y quedan vidas
                elif visitante.llego() and vidas > 0 and evento.key in (
                        pygame.K_a, pygame.K_r):
                    permitir = evento.key == pygame.K_a
                    acerto = decision_correcta(visitante, permitir)
                    if acerto:
                        puntaje = calcular_puntaje(puntaje, True, racha)
                        racha += 1
                        mensaje, color_mensaje = "¡Bien!", aj.COLOR_ACIERTO
                    else:
                        vidas -= 1
                        racha = 0
                        mensaje, color_mensaje = "¡Error!", aj.COLOR_ERROR
                    visitante = generar_visitante()  # llega el siguiente

        # 2) ACTUALIZAR
        visitante.actualizar(dt)

        # 3) DIBUJAR
        pantalla.fill(aj.COLOR_FONDO)
        pygame.draw.rect(pantalla, aj.COLOR_PARED, (0, 0, aj.ANCHO, aj.SUELO_Y))
        pygame.draw.rect(pantalla, aj.COLOR_PUERTA, (780, 180, 110, 220))
        visitante.dibujar(pantalla)
        dibujar_libro(pantalla, fuente)
        if visitante.llego():
            dibujar_ficha(pantalla, fuente, visitante)

        pantalla.blit(
            fuente_grande.render(
                f"Puntaje: {puntaje}  Vidas: {vidas}  Racha: {racha}",
                True, aj.COLOR_TEXTO),
            (20, 20))
        pantalla.blit(fuente_grande.render(mensaje, True, color_mensaje),
                      (20, 60))
        if vidas <= 0:
            pantalla.blit(fuente_grande.render(
                "FIN DE PARTIDA (reinicio: próximo paso)", True,
                aj.COLOR_ERROR), (200, 250))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()