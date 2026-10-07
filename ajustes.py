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
SUBTITULO = "Guardia de la fábrica. Desconfiá de todos."

# --- Estados del juego ---
ESTADO_MENU = "menu"
ESTADO_INSTRUCCIONES = "instrucciones"
ESTADO_OBJETIVO = "objetivo"
ESTADO_CONFIG = "config"
ESTADO_JUGANDO = "jugando"
ESTADO_PAUSA = "pausa"
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
COLOR_PERMITIR = (40, 110, 70)          # sello APROBADO
COLOR_PERMITIR_HOVER = (60, 150, 95)
COLOR_RECHAZAR = (130, 45, 45)          # sello RECHAZADO
COLOR_RECHAZAR_HOVER = (180, 65, 65)
COLOR_SELLO_MANGO = (70, 55, 45)
COLOR_PAPEL = (228, 218, 184)           # documento y autorización
COLOR_TINTA = (35, 30, 25)
COLOR_FOTO_FONDO = (50, 50, 60)         # fondo detrás del retrato
COLOR_SOMBRA = (12, 12, 18)

# --- Imágenes (carpeta "imagenes" junto a main.py) ---
# Se escriben SIN extensión: se busca .png, .jpg, .jpeg o .webp.
IMAGENES_CARPETA = os.path.join(RUTA_BASE, "imagenes")
EXTENSIONES_IMAGEN = (".png", ".jpg", ".jpeg", ".webp")
FONDO_1 = "fondo1"    # primer plano: va ADELANTE del empleado (PNG con transparencia)
FONDO_2 = "fondo2"    # fondo: va ATRÁS del empleado
# Las 4 imágenes de cada empleado se llaman <prefijo>_<variante>.png
VARIANTES = ["normal", "normal_enojado", "impostor", "impostor_enojado"]
# Colores de reemplazo (R, G, B, A) si falta alguna imagen del empleado
COLORES_REEMPLAZO = {
    "normal": (200, 200, 210, 255),
    "normal_enojado": (230, 160, 90, 255),
    "impostor": (150, 110, 200, 255),
    "impostor_enojado": (220, 70, 70, 255),
}

# --- Empleado en la puerta ---
VISITANTE_IMG_ALTO = 320       # alto (px) con que se dibuja; el ancho es proporcional
VISITANTE_BASE_Y = 410         # y donde apoya la parte de abajo de la imagen
VISITANTE_VELOCIDAD = 220      # píxeles por segundo al entrar
VISITANTE_X_INICIAL = -250     # centro horizontal al empezar (fuera de pantalla)
VISITANTE_X_DESTINO = ANCHO // 2   # centro horizontal frente a la puerta
SACUDIDA_ENOJADO = 3           # cuánto tiembla cuando está enojado (0 = no tiembla)

# --- La fábrica ---
# piso: en qué piso queda | rubro: (masculino, femenino) de quien trabaja ahí
# personal: lo mismo en plural | donde: cómo se dice "voy ..." (con su artículo)
# El orden importa: cada noche usa solo los primeros N lugares ("lugares").
LUGARES = {
    "Recepción": {"piso": 1, "rubro": ("recepcionista", "recepcionista"),
                  "personal": "recepcionistas", "donde": "a Recepción"},
    "Laboratorio": {"piso": 2, "rubro": ("científico", "científica"),
                    "personal": "científicos", "donde": "al Laboratorio"},
    "Seguridad": {"piso": 3, "rubro": ("guardia", "guardia"),
                  "personal": "guardias", "donde": "a Seguridad"},
    "Depósito": {"piso": 1, "rubro": ("operario", "operaria"),
                 "personal": "operarios", "donde": "al Depósito"},
    "Taller": {"piso": 2, "rubro": ("mecánico", "mecánica"),
               "personal": "mecánicos", "donde": "al Taller"},
    "Oficinas": {"piso": 3, "rubro": ("administrativo", "administrativa"),
                 "personal": "administrativos", "donde": "a Oficinas"},
}
PISOS = sorted({d["piso"] for d in LUGARES.values()})

# Personajes: cada uno es un juego de 4 imágenes (<imagen>_normal.png, etc.).
# genero: "m" o "f" (decide qué nombres y qué forma del rubro le tocan).
# Para sumar un personaje: agregá sus 4 imágenes y una línea acá.
CARAS = [
    {"imagen": "marta", "genero": "f"},
    {"imagen": "hugo", "genero": "m"},
    {"imagen": "lucia", "genero": "f"},
    {"imagen": "tomas", "genero": "m"},
    {"imagen": "elena", "genero": "f"},
]
# Cada empleado sale de combinar al azar: una cara + nombre + apellido + lugar.
NOMBRES = {
    "f": ["Marta", "Lucía", "Elena", "Julia", "Sofía", "Carla", "Paula",
          "Valentina", "Camila", "Renata"],
    "m": ["Hugo", "Tomás", "Diego", "Martín", "Andrés", "Bruno", "Mateo",
          "Sergio", "Gonzalo", "Ignacio"],
}
APELLIDOS = ["Gómez", "Pereira", "Ferrari", "Rivero", "Souza", "Suárez",
             "Méndez", "Olivera", "Núñez", "Silva", "Cabrera", "Benítez",
             "Fernández", "Rodríguez", "Techera", "Barrios"]
# Letras que se confunden fácil: así se escribe mal un nombre en el documento.
CAMBIOS_PARECIDOS = [("ó", "o"), ("í", "i"), ("á", "a"), ("é", "e"),
                     ("ú", "u"), ("z", "s"), ("s", "z"), ("y", "i"),
                     ("i", "y"), ("b", "v"), ("v", "b"), ("ll", "y")]

# --- Documento, autorización y sellos ---
TIPOS_OBJETO = ("documento", "autorizacion")     # lo que se le puede pedir
OBJETO_TAMANOS = {"documento": (320, 160), "autorizacion": (230, 160)}
OBJETO_SPAWN = {"documento": (180, 340), "autorizacion": (170, 170)}   # centro
# Foto del documento: el retrato sale de la imagen "normal" del empleado.
FOTO_CAJA = (100, 112)                   # tamaño de la foto en el documento
FOTO_RECORTE = (0.15, 0.0, 0.70, 0.62)   # zona de la imagen: x, y, ancho, alto (fracciones)
SELLO_TAMANO = (150, 50)
SELLO_CENTROS = {True: (715, 470), False: (875, 470)}   # True = APROBADO

# --- Reglas generales ---
VIDAS_INICIALES = 3            # vidas al empezar CADA noche
PUNTOS_ACIERTO = 100
PUNTOS_RACHA = 25              # bonus por cada acierto seguido
PUNTOS_BONUS_VIDA = 50         # bonus por vida que sobra al terminar una noche

# --- Paciencia (segundos) ---
PACIENCIA_BASE = 30.0          # valor por defecto (cada noche define la suya)
PACIENCIA_MIN = 10.0           # nunca espera menos que esto
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
# visitantes: cuántos empleados hay que atender | lugares: cuántos hay en el edificio
# prob_impostor: chance de que sea impostor | paciencia: segundos iniciales
# tipos: cómo puede delatarse un impostor:
#   "piso"   = dice un piso que no corresponde a su lugar de trabajo
#   "rubro"  = dice un rubro que no es de ese lugar
#   "nombre" = el nombre de su documento está mal escrito
#   "aspecto" = no dice nada raro: solo su cara no coincide con la foto del documento
TIPOS_TODOS = ["nombre", "piso", "rubro", "aspecto"]
NIVELES = [
    {"nombre": "Noche 1", "visitantes": 6, "lugares": 3,
     "prob_impostor": 0.35, "paciencia": 30.0,
     "tipos": ["piso", "rubro", "aspecto"]},
    {"nombre": "Noche 2", "visitantes": 8, "lugares": 4,
     "prob_impostor": 0.45, "paciencia": 25.0, "tipos": TIPOS_TODOS},
    {"nombre": "Noche 3", "visitantes": 10, "lugares": 6,
     "prob_impostor": 0.50, "paciencia": 20.0, "tipos": TIPOS_TODOS},
]

# --- Sonidos ---
SONIDOS_CARPETA = os.path.join(RUTA_BASE, "sonidos")
NOMBRES_SONIDOS = ["timbre", "acierto", "error", "susto", "papel", "sello"]
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
    "Un empleado llega a la puerta de la fábrica y se presenta.",
    "Compará lo que dice con el EDIFICIO: pisos, áreas y rubros.",
    "Clic en el empleado: pedile su documento (trae foto) y la",
    "autorización de ingreso. Arrastralos para leerlos.",
    "Compará su cara con la foto del documento.",
    "",
    "Arrastrá un SELLO sobre la autorización: APROBADO si todo",
    "coincide, RECHAZADO si algo no cuadra (no se puede cambiar).",
    "Después arrastrá la autorización sellada hasta el empleado:",
    "se lleva todo junto, con su documento. Ahí se decide.",
    "",
    "No tardes: su paciencia se agota. ESC o II pausan el juego.",
]
TEXTO_OBJETIVO = [
    "Sos el guardia de la fábrica y esta noche no podés fallar.",
    "Algunos empleados no son quienes dicen ser: son impostores.",
    "",
    "- Dejá entrar solo a los empleados verdaderos (sello APROBADO).",
    "- Rechazá a los impostores (sello RECHAZADO).",
    "- Cada error o tiempo agotado te cuesta una vida.",
    "- Sobreviví a las 3 noches. Cada una es más difícil.",
]