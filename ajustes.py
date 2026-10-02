"""Constantes del juego: colores, tamaños y velocidades.

Todo valor "mágico" vive acá para poder ajustarlo sin tocar la lógica.
"""

# --- Ventana ---
ANCHO = 960
ALTO = 540
FPS = 60
TITULO = "Portero de Medianoche"

# --- Colores (R, G, B) ---
COLOR_FONDO = (18, 18, 28)
COLOR_PARED = (40, 40, 58)
COLOR_PUERTA = (90, 60, 40)
COLOR_VISITANTE = (200, 200, 210)
COLOR_TEXTO = (235, 235, 235)

# --- Visitante ---
VISITANTE_ANCHO = 60
VISITANTE_ALTO = 120
VISITANTE_VELOCIDAD = 140      # píxeles por segundo
VISITANTE_X_INICIAL = -80      # arranca fuera de la pantalla
VISITANTE_X_DESTINO = 450      # se detiene frente a la puerta
SUELO_Y = 400                  # donde apoyan los pies

# --- Partida ---
VIDAS_INICIALES = 3

# --- Reglas del juego ---
PROB_IMPOSTOR = 0.4            # probabilidad de que un visitante sea impostor
PUNTOS_ACIERTO = 100
PUNTOS_RACHA = 25              # bonus por cada acierto seguido extra
DEDOS_NORMALES = 5

# Libro de residentes: apartamento -> nombre del inquilino
RESIDENTES = {
    "1A": "Marta Gómez",
    "1B": "Hugo Pereira",
    "2A": "Lucía Ferrari",
    "2B": "Tomás Rivero",
    "3A": "Elena Souza",
}
NOMBRES_FALSOS = ["Marta Gomes", "Hugo Pereyra", "Lucia Ferrary", "Tomás Rivera"]

# Colores de la interfaz
COLOR_ACIERTO = (90, 200, 120)
COLOR_ERROR = (220, 80, 80)
COLOR_PANEL = (28, 28, 42)