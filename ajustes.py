"""Constantes del juego: colores, tamaños y velocidades.

Todo valor "mágico" vive acá para poder ajustarlo sin tocar la lógica.
"""

# --- Ventana ---
ANCHO = 960
ALTO = 540
FPS = 60
TITULO = "Portero de Medianoche"

# --- Estados del juego ---
ESTADO_JUGANDO = "jugando"
ESTADO_FIN = "fin"

# --- Colores (R, G, B) ---
COLOR_FONDO = (18, 18, 28)
COLOR_PARED = (40, 40, 58)
COLOR_PUERTA = (90, 60, 40)
COLOR_CUERPO = (200, 200, 210)
COLOR_PIEL = (230, 190, 160)
COLOR_TEXTO = (235, 235, 235)
COLOR_ACIERTO = (90, 200, 120)
COLOR_ERROR = (220, 80, 80)
COLOR_PANEL = (28, 28, 42)
COLOR_LENTES = (30, 30, 30)
COLOR_BIGOTE = (50, 30, 20)

# Colores de pelo disponibles (nombre -> color)
COLORES_PELO = {
    "negro": (20, 20, 20),
    "rubio": (230, 200, 100),
    "rojo": (190, 60, 40),
    "gris": (170, 170, 170),
    "castaño": (110, 70, 40),
}

# --- Escenario ---
SUELO_Y = 400                          # donde apoyan los pies
PUERTA_RECT = (790, 270, 100, 130)     # x, y, ancho, alto

# --- Visitante ---
CUERPO_ANCHO = 50
CUERPO_ALTO = 80
CABEZA_RADIO = 22
VISITANTE_VELOCIDAD = 140      # píxeles por segundo
VISITANTE_X_INICIAL = -80      # arranca fuera de la pantalla
VISITANTE_X_DESTINO = 450      # se detiene frente a la puerta

# --- Reglas del juego ---
VIDAS_INICIALES = 3
PROB_IMPOSTOR = 0.4            # probabilidad de que un visitante sea impostor
PUNTOS_ACIERTO = 100
PUNTOS_RACHA = 25              # bonus por cada acierto seguido

# Libro de residentes: apartamento -> datos del inquilino
RESIDENTES = {
    "1A": {"nombre": "Marta Gómez", "pelo": "rojo", "lentes": True,
           "bigote": False, "mascota": "gato"},
    "1B": {"nombre": "Hugo Pereira", "pelo": "negro", "lentes": False,
           "bigote": True, "mascota": "perro"},
    "2A": {"nombre": "Lucía Ferrari", "pelo": "rubio", "lentes": True,
           "bigote": False, "mascota": "canario"},
    "2B": {"nombre": "Tomás Rivero", "pelo": "gris", "lentes": False,
           "bigote": True, "mascota": "loro"},
    "3A": {"nombre": "Elena Souza", "pelo": "castaño", "lentes": False,
           "bigote": False, "mascota": "conejo"},
}

# Nombres casi iguales a los reales (para el impostor que "falla" el nombre)
NOMBRES_PARECIDOS = {
    "1A": "Marta Gomes",
    "1B": "Hugo Pereyra",
    "2A": "Lucia Ferrary",
    "2B": "Tomás Rivera",
    "3A": "Elena Sousa",
}

# Mascotas posibles (para que el impostor invente una distinta)
MASCOTAS = ["gato", "perro", "canario", "loro", "conejo", "pez"]