"""Constantes del juego: colores, tamaños, velocidades, niveles y textos.

Todo valor "mágico" vive acá para poder ajustarlo sin tocar la lógica.
"""

import os

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))

# --- Ventana ---
ANCHO = 960
ALTO = 540
FPS = 60
TITULO = "Esta noche no"
SUBTITULO = "Portero de edificio. Desconfiá de todos."

# --- Estados del juego ---
ESTADO_MENU = "menu"
ESTADO_INSTRUCCIONES = "instrucciones"
ESTADO_OBJETIVO = "objetivo"
ESTADO_CONFIG = "config"
ESTADO_JUGANDO = "jugando"
ESTADO_NIVEL_COMPLETO = "nivel_completo"
ESTADO_FIN = "fin"
ESTADO_VICTORIA = "victoria"

# --- Colores (R, G, B) ---
COLOR_FONDO = (18, 18, 28)
COLOR_PARED = (40, 40, 58)          # reemplazo de fondo2 si falta la imagen
COLOR_TEXTO = (235, 235, 235)
COLOR_SECUNDARIO = (160, 160, 180)
COLOR_TITULO = (210, 50, 50)
COLOR_ACIERTO = (90, 200, 120)
COLOR_ERROR = (220, 80, 80)
COLOR_PANEL = (28, 28, 42)
COLOR_BOTON = (48, 48, 72)
COLOR_BOTON_HOVER = (76, 76, 110)
COLOR_BORDE = (110, 110, 150)
COLOR_PERMITIR = (40, 110, 70)
COLOR_PERMITIR_HOVER = (60, 150, 95)
COLOR_RECHAZAR = (130, 45, 45)
COLOR_RECHAZAR_HOVER = (180, 65, 65)

# --- Imágenes (carpeta "imagenes" junto a main.py) ---
# Se escriben SIN extensión: se busca .png, .jpg, .jpeg o .webp.
IMAGENES_CARPETA = os.path.join(RUTA_BASE, "imagenes")
EXTENSIONES_IMAGEN = (".png", ".jpg", ".jpeg", ".webp")
FONDO_1 = "fondo1"    # primer plano: va ADELANTE del visitante (PNG con transparencia)
FONDO_2 = "fondo2"    # fondo: va ATRÁS del visitante
# Las 4 imágenes de cada visitante se llaman <prefijo>_<variante>.png
VARIANTES = ["normal", "normal_enojado", "impostor", "impostor_enojado"]
# Colores de reemplazo (R, G, B, A) si falta alguna imagen del visitante
COLORES_REEMPLAZO = {
    "normal": (200, 200, 210, 255),
    "normal_enojado": (230, 160, 90, 255),
    "impostor": (150, 110, 200, 255),
    "impostor_enojado": (220, 70, 70, 255),
}

# --- Visitante ---
VISITANTE_IMG_ALTO = 320       # alto (px) con que se dibuja; el ancho es proporcional
VISITANTE_BASE_Y = 410         # y donde apoya la parte de abajo de la imagen
VISITANTE_VELOCIDAD = 220      # píxeles por segundo al entrar
VISITANTE_X_INICIAL = -250     # centro horizontal al empezar (fuera de pantalla)
VISITANTE_X_DESTINO = ANCHO // 2   # centro horizontal frente a la puerta
SACUDIDA_ENOJADO = 3           # cuánto tiembla cuando está enojado (0 = no tiembla)

# --- Reglas generales ---
VIDAS_INICIALES = 3            # vidas al empezar CADA noche
PUNTOS_ACIERTO = 100
PUNTOS_RACHA = 25              # bonus por cada acierto seguido
PUNTOS_BONUS_VIDA = 50         # bonus por vida que sobra al terminar una noche

# --- Paciencia ---
PACIENCIA_BASE = 12.0          # valor por defecto (cada noche define la suya)
PACIENCIA_MIN = 4.0            # nunca espera menos que esto
PACIENCIA_REDUCCION = 0.5      # segundos que se restan por acierto seguido
PACIENCIA_MEDIA = 0.6          # debajo de esta fracción la barra se pone amarilla
PACIENCIA_ALERTA = 0.3         # debajo de esta fracción: barra roja e imagen enojada
BARRA_ANCHO = 70
BARRA_ALTO = 8
COLOR_BARRA_FONDO = (60, 60, 80)
COLOR_PACIENCIA_ALTA = (90, 200, 120)
COLOR_PACIENCIA_MEDIA = (230, 200, 80)
COLOR_PACIENCIA_BAJA = (220, 80, 80)

# --- Niveles (noches) ---
# visitantes: cuántos hay que atender | residentes: cuántos vecinos hay en el libro
# prob_impostor: chance de que sea impostor | paciencia: segundos iniciales
# tipos: qué clase de inconsistencia puede tener un impostor
#   ("rasgo" = no dice nada raro, solo se nota en su aspecto)
TIPOS_TODOS = ["nombre", "apartamento", "dicho", "rasgo"]
NIVELES = [
    {"nombre": "Noche 1", "visitantes": 6, "residentes": 3,
     "prob_impostor": 0.35, "paciencia": 14.0,
     "tipos": ["apartamento", "dicho", "rasgo"]},
    {"nombre": "Noche 2", "visitantes": 8, "residentes": 4,
     "prob_impostor": 0.45, "paciencia": 11.0,
     "tipos": TIPOS_TODOS},
    {"nombre": "Noche 3", "visitantes": 10, "residentes": 5,
     "prob_impostor": 0.50, "paciencia": 8.0,
     "tipos": TIPOS_TODOS},
]

# Libro de residentes: apartamento -> datos del inquilino
# (cada noche usa solo los primeros N, según "residentes")
# "imagen" = prefijo de los archivos del visitante (ej. marta_normal.png)
# pelo / lentes / bigote = lo que dice el libro; tienen que coincidir con tus dibujos
RESIDENTES = {
    "1A": {"nombre": "Marta Gómez", "imagen": "marta", "pelo": "rojo",
           "lentes": True, "bigote": False, "mascota": "gato"},
    "1B": {"nombre": "Hugo Pereira", "imagen": "hugo", "pelo": "negro",
           "lentes": False, "bigote": True, "mascota": "perro"},
    "2A": {"nombre": "Lucía Ferrari", "imagen": "lucia", "pelo": "rubio",
           "lentes": True, "bigote": False, "mascota": "canario"},
    "2B": {"nombre": "Tomás Rivero", "imagen": "tomas", "pelo": "gris",
           "lentes": False, "bigote": True, "mascota": "loro"},
    "3A": {"nombre": "Elena Souza", "imagen": "elena", "pelo": "castaño",
           "lentes": False, "bigote": False, "mascota": "conejo"},
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

# --- Sonidos ---
SONIDOS_CARPETA = os.path.join(RUTA_BASE, "sonidos")
NOMBRES_SONIDOS = ["timbre", "acierto", "error", "susto"]
FRECUENCIA_MUESTREO = 44100    # muestras por segundo de los .wav
VOLUMEN = 0.6                  # volumen inicial (0.0 a 1.0)

# --- Interfaz ---
BOTON_ANCHO = 260
BOTON_ALTO = 48
ENGRANAJE_CENTRO = (ANCHO - 45, 45)
ENGRANAJE_RADIO = 22
SLIDER_X = 240
SLIDER_Y = 240
SLIDER_ANCHO = 480

# --- Textos de las pantallas de ayuda (una línea por elemento) ---
TEXTO_INSTRUCCIONES = [
    "Un visitante llega a la puerta y se presenta.",
    "Compará lo que dice y cómo se ve con el libro de residentes.",
    "",
    "Todo coincide:   PERMITIR  (tecla A o clic en el botón verde)",
    "Algo no cuadra:  RECHAZAR  (tecla R o clic en el botón rojo)",
    "",
    "No tardes: la paciencia del visitante se agota.",
    "ESC vuelve al menú.",
]
TEXTO_OBJETIVO = [
    "Sos el portero del edificio y esta noche no podés fallar.",
    "Algunos visitantes no son vecinos: son impostores.",
    "",
    "- Dejá pasar solo a los vecinos reales.",
    "- Rechazá a los impostores (algo no coincide con el libro).",
    "- Cada error o tiempo agotado te cuesta una vida.",
    "- Sobreviví a las 3 noches. Cada una es más difícil.",
]