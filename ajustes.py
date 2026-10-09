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
ESTADO_APAGON = "apagon"
ESTADO_HISTORIA = "historia"

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
LUGARES = {
    "Recepción": {"piso": 1, "rubro": ("recepcionista", "recepcionista"),
                  "personal": "recepcionistas", "donde": "a Recepción"},
    "Depósito": {"piso": 1, "rubro": ("operario", "operaria"),
                 "personal": "operarios", "donde": "al Depósito"},
    "Comedor": {"piso": 1, "rubro": ("cocinero", "cocinera"),
                "personal": "cocineros", "donde": "al Comedor"},
    "Laboratorio": {"piso": 2, "rubro": ("científico", "científica"),
                    "personal": "científicos", "donde": "al Laboratorio"},
    "Taller": {"piso": 2, "rubro": ("mecánico", "mecánica"),
               "personal": "mecánicos", "donde": "al Taller"},
    "Enfermería": {"piso": 2, "rubro": ("enfermero", "enfermera"),
                   "personal": "enfermeros", "donde": "a Enfermería"},
    "Seguridad": {"piso": 3, "rubro": ("guardia", "guardia"),
                  "personal": "guardias", "donde": "a Seguridad"},
    "Oficinas": {"piso": 3, "rubro": ("administrativo", "administrativa"),
                 "personal": "administrativos", "donde": "a Oficinas"},
}
PISOS = sorted({d["piso"] for d in LUGARES.values()})

# Empleados (cada noche usa solo los primeros N, según "empleados").
# imagen = prefijo de sus 4 archivos (ej. marta_normal.png, marta_impostor.png)
# genero = "m" o "f" (decide la forma de su rubro) | lugar = dónde trabaja
# Cada uno tiene un lugar y un rubro distintos.
EMPLEADOS = [
    {"nombre": "Marta Gómez", "imagen": "marta", "genero": "f",
     "lugar": "Laboratorio"},
    {"nombre": "Hugo Pereira", "imagen": "hugo", "genero": "m",
     "lugar": "Seguridad"},
    {"nombre": "Lucía Ferrari", "imagen": "lucia", "genero": "f",
     "lugar": "Recepción"},
    {"nombre": "Tomás Fernández", "imagen": "tomas", "genero": "m",
     "lugar": "Taller"},
    {"nombre": "Elena Sousa", "imagen": "elena", "genero": "f",
     "lugar": "Depósito"},
    {"nombre": "Gonzalo Silva", "imagen": "gonzalo", "genero": "m",
     "lugar": "Oficinas"},
    {"nombre": "Paula González", "imagen": "paula", "genero": "f",
     "lugar": "Comedor"},
    {"nombre": "Julia Olivera", "imagen": "julia", "genero": "f",
     "lugar": "Enfermería"},
]
# Letras que se confunden fácil: así se escribe mal un nombre en el documento.
CAMBIOS_PARECIDOS = [("z", "s"), ("s", "z"), ("c", "s"), ("s", "c"),
                     ("y", "i"), ("i", "y"), ("b", "v"), ("v", "b"),
                     ("g", "j"), ("j", "g"), ("ll", "y"), ("a", "e"),
                     ("e", "a"), ("o", "u"), ("u", "o")]
# Un impostor con pista de "nombre": qué tan seguido la tiene y cómo es
PROB_NOMBRE_MAL = 0.65         # chance de que un impostor tenga el nombre mal
PROB_ESCRITO_MAL = 0.85        # si es así: nombre con una letra mal (si no, el de otro)

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
# visitantes: cuántos hay que atender | empleados: cuántos personajes (y lugares) hay
# impostores: cuántos de los visitantes SON impostores (cantidad exacta, mezclada al azar)
# paciencia: segundos iniciales | tipos: cómo puede delatarse un impostor:
#   "piso"   = dice un piso que no corresponde a su lugar de trabajo
#   "rubro"  = dice un rubro que no es de ese lugar
#   "nombre" = el documento tiene su nombre mal escrito (una letra mal), o el de otro empleado
#   "aspecto" = su cara no coincide con la foto del documento
# Un impostor tiene una o varias de estas pistas a la vez. Si "aspecto" no está,
# su cara SÍ coincide con la foto (solo se delata por lo que dice o por el papel).
# pistas: cuántas inconsistencias puede tener un impostor (se elige una al azar)
# apagones: cuántas veces apagan la luz en la noche | cables: cuántos cables hay que
# reconectar en cada apagón | tiempo_cables: segundos para hacerlo (si se acaba,
# se pierde la noche)
TIPOS_TODOS = ["nombre", "piso", "rubro", "aspecto"]
NIVELES = [
    {"nombre": "Noche 1", "visitantes": 6, "empleados": 3,
     "impostores": 3, "paciencia": 30.0,
     "tipos": ["piso", "rubro", "aspecto", "nombre"], "pistas": [1, 1, 2],
     "apagones": 1, "cables": 3, "tiempo_cables": 15.0},
    {"nombre": "Noche 2", "visitantes": 8, "empleados": 5,
     "impostores": 4, "paciencia": 25.0, "tipos": TIPOS_TODOS,
     "pistas": [1, 2, 2],
     "apagones": 1, "cables": 4, "tiempo_cables": 13.0},
    {"nombre": "Noche 3", "visitantes": 10, "empleados": 8,
     "impostores": 6, "paciencia": 20.0, "tipos": TIPOS_TODOS,
     "pistas": [1, 2, 2, 3],
     "apagones": 2, "cables": 5, "tiempo_cables": 11.0},
]

# --- Apagón (minijuego de cables) ---
# Un impostor apaga la luz (1 o 2 veces por noche): hay que reconectar los cables.
APAGON_MIN_ATENDIDOS = 1       # un apagón ocurre después de atender al menos a 1
APAGON_ALPHA = 225             # oscuridad del apagón (0 = nada, 255 = negro total)
APAGON_DEMORA = (0.5, 2.5)      # segundos (mín., máx.) desde que el impostor llega
APAGON_TITILEO = 2.0           # segundos que titila la luz antes de quedar a oscuras
APAGON_PARPADEO = 0.12         # duración de cada parpadeo (segundos)
APAGON_PAUSA_FINAL = 0.9       # segundos que se muestra el resultado
COLOR_NEGRO = (0, 0, 0)       # color de la oscuridad del apagón
COLORES_CABLES = [(220, 50, 50), (50, 100, 235), (240, 205, 50),
                  (225, 70, 225), (60, 200, 100)]
CABLES_X_IZQ = 210             # x de los enchufes de la izquierda
CABLES_X_DER = 750             # x de los enchufes de la derecha
CABLES_Y_CENTRO = 300          # y del centro de la columna de enchufes
CABLES_PASO = 62               # separación vertical entre enchufes
CABLES_RADIO = 20              # radio del enchufe (zona donde se agarra y se suelta)
CABLES_GROSOR = 12             # grosor del cable
CABLES_BARRA = (260, 100, 440, 12)   # barra del tiempo: x, y, ancho, alto
COLOR_ENCHUFE = (70, 70, 80)

# --- Sonidos ---
SONIDOS_CARPETA = os.path.join(RUTA_BASE, "sonidos")
NOMBRES_SONIDOS = ["timbre", "acierto", "error", "susto", "papel", "sello",
                   "apagon", "cable", "pasos"]
FRECUENCIA_MUESTREO = 44100    # muestras por segundo de los .wav
VOLUMEN_EFECTOS = 0.35         # volumen inicial de los efectos (0.0 a 1.0)
VOLUMEN_MUSICA = 0.8           # volumen inicial de la música (0.0 a 1.0)
MUSICA_PICO = 0.9              # la música se normaliza para llegar a este nivel
MUSICA_RUTA = os.path.join(SONIDOS_CARPETA, "musica.wav")   # música de tensión
MUSICA_DURACION = 16           # segundos que dura antes de repetirse

# --- Interfaz ---
# Fuentes: nombre y tamaño de cada una (se cargan una vez en main.py)
FUENTE_NOMBRE = "consolas"
FUENTES_TAMANOS = {"titulo": 64, "grande": 28, "media": 20, "normal": 18,
                   "chica": 15}
# Tipografía del menú inicial (la del afiche). Se usa el primer archivo que exista
# en la carpeta "fuentes"; si ninguno existe se usa la fuente del sistema.
FUENTES_CARPETA = os.path.join(RUTA_BASE, "fuentes")
FUENTES_TITULO = ["titulo.ttf", "DejaVuSansCondensed-Bold.ttf"]
FUENTES_MENU = ["CourierPrime-Bold.ttf", "LiberationMono-Bold.ttf"]
TAMANO_MENU_TITULO = 104
TAMANO_MENU_TEXTO = 22
TAMANO_MENU_CHICA = 16
# Título con resplandor rojo, como en el afiche
COLOR_TITULO_TEXTO = (8, 4, 4)         # letras casi negras
COLOR_TITULO_BRILLO = (235, 25, 25)    # resplandor rojo
COLOR_TITULO_DESGASTE = (95, 18, 18)   # manchas que "gastan" las letras
TITULO_MARGEN = 56                     # espacio alrededor para el resplandor
TITULO_DESENFOQUE = 12                 # más grande = resplandor más difuso
TITULO_BRILLO_FUERTE = 7               # cuántas veces se suma el resplandor (luz prendida)
TITULO_BRILLO_DEBIL = 2                # ídem con el parpadeo (luz fallando)
TITULO_MANCHAS = 260                   # cantidad de manchas de desgaste
TITULO_ANCHO_MAX = ANCHO - 60          # el título no puede ser más ancho que esto
MENU_TITULO_Y = 110
MENU_SUBTITULO_Y = 190
MENU_LEMA_Y = 495
MENU_LEMA = "Compará documentos  -  Sellá  -  Desconfiá de todos"
# Botones del menú (oscuros con borde rojo)
COLOR_MENU_BOTON = (24, 10, 10)
COLOR_MENU_BOTON_HOVER = (76, 16, 16)
COLOR_MENU_BORDE = (150, 30, 30)
COLOR_MENU_BORDE_HOVER = (240, 70, 70)
COLOR_MENU_TEXTO = (240, 240, 240)
COLOR_MENU_SECUNDARIO = (185, 185, 185)
# Velo oscuro que se pone detrás de los carteles (pausa, fin, victoria)
COLOR_VELO = (0, 0, 0)
VELO_ALPHA = 190
# El título del menú parpadea como una luz fallando
COLOR_TITULO_APAGADO = (110, 30, 30)
PARPADEO_MS = 90               # duración de cada tic del parpadeo
PARPADEO_CADA = 31             # cada cuántos tics se apaga el título
# Paneles (x, y, ancho, alto)
PANEL_AYUDA = (80, 50, 800, 440)
PANEL_CONFIG = (200, 70, 560, 400)
PANEL_EDIFICIO = (640, 10, 310, 255)
PANEL_FICHA = (20, 445, 600, 70)
PANEL_BANDEJA = (632, 435, 326, 70)
MENSAJE_LARGO = 56             # más de estos caracteres: se achica y se parte en líneas
MENSAJE_ANCHO_LINEA = 66       # caracteres por línea en un mensaje largo
PISTA_TAMANO = (320, 22)       # cartelito junto al mouse
# Botones: nombre -> (texto, centro) o (texto, centro, ancho, alto)
_CX = ANCHO // 2
_CX_PEDIR = VISITANTE_X_DESTINO + 190    # menú que sale al clickear al empleado
BOTONES = {
    "jugar": ("Jugar", (_CX, 240)),
    "instrucciones": ("Instrucciones", (_CX, 305)),
    "objetivo": ("Objetivo", (_CX, 370)),
    "sonido": ("Sonido: SÍ", (_CX, 345)),
    "volver": ("Volver", (_CX, 410)),
    "pausa": ("II", (618, 30), 36, 36),
    "pedir_documento": ("Pedir documento", (_CX_PEDIR, 290), 230, 38),
    "pedir_autorizacion": ("Pedir autorización", (_CX_PEDIR, 336), 230, 38),
    "p_continuar": ("Continuar", (_CX, 200)),
    "p_instrucciones": ("Instrucciones", (_CX, 262)),
    "p_volumen": ("Volumen", (_CX, 324)),
    "p_inicio": ("Volver al inicio", (_CX, 386)),
    "siguiente": ("Siguiente noche", (_CX, 340)),
    "reintentar": ("Reintentar", (_CX, 340)),
    "de_nuevo": ("Jugar de nuevo", (_CX, 340)),
    "menu": ("Menú", (_CX, 400)),
}
BOTON_ANCHO = 260
BOTON_ALTO = 48
ENGRANAJE_CENTRO = (ANCHO - 45, 45)
ENGRANAJE_RADIO = 22
SLIDER_X = 240
SLIDER_ANCHO = 480
SLIDER_EFECTOS_Y = 200         # barra del volumen de los efectos
SLIDER_MUSICA_Y = 275          # barra del volumen de la música

# --- Textos de las pantallas de ayuda (una línea por elemento) ---
TEXTO_INSTRUCCIONES = [
    "Un empleado llega a la puerta de la fábrica y se presenta.",
    "Compará lo que dice con el EDIFICIO: pisos, áreas y rubros.",
    "Clic en el empleado: pedile su documento (trae foto) y la",
    "autorización. Arrastralos para leerlos. Compará su cara.",
    "Un impostor puede fallar en una o en varias cosas a la vez.",
    "Arrastrá un SELLO sobre la autorización: APROBADO o",
    "RECHAZADO. Después arrastrá la autorización sellada al",
    "empleado: se lleva todo junto y ahí se decide.",
    "",
    "APAGÓN: si un impostor apaga la luz, arrastrá cada cable",
    "hasta el enchufe de su mismo color antes de que se acabe",
    "el tiempo. Si no lo lográs, perdés la noche.",
    "No tardes: su paciencia se agota. ESC o II pausan.",
]
AYUDA_Y = 140                  # y de la primera línea de las ayudas
AYUDA_PASO = 24                # separación entre líneas de las ayudas
TEXTO_OBJETIVO = [
    "Sos el guardia de la fábrica y esta noche no podés fallar.",
    "Algunos empleados no son quienes dicen ser: son impostores.",
    "",
    "- Dejá entrar solo a los empleados verdaderos (sello APROBADO).",
    "- Rechazá a los impostores (sello RECHAZADO).",
    "- Cada error o tiempo agotado te cuesta una vida.",
    "- Si no arreglás el apagón a tiempo, perdés la noche.",
    "- Si un impostor apaga la luz, reconectá los cables a tiempo.",
    "- Sobreviví a las 3 noches. Cada una es más difícil.",
]

# --- Historia (antes de cada noche) ---
# HISTORIAS[n] son las pantallas que se ven antes de la noche n + 1; el texto
# aparece letra por letra.
HISTORIAS = [
    [   # antes de la noche 1
        "Hace tres meses perdí mi trabajo. El alquiler vencía, la heladera "
        "estaba vacía y nadie me llamaba.",
        "Un día vi un aviso pegado en un poste, escrito a mano: «Se necesita "
        "guardia de seguridad. Sueldo triple. Solo de noche. Sin preguntas.»",
        "La fábrica no figura en ningún mapa y nadie sabe qué produce. "
        "Solo abre de noche, y todos los empleados entran por la misma puerta.",
        "El primer día el jefe me dio un sello verde, uno rojo y una sola "
        "regla: «Dejá entrar solo a los nuestros. Los otros no son personas.»",
        "Hoy es mi primera noche en la puerta. Voy a revisar sus papeles, "
        "mirarles la cara y desconfiar de todos. Esta noche no.",
    ],
    [   # antes de la noche 2
        "Sobreviví a la primera noche. Cobré el triple, como decía el aviso, "
        "pero no pude dormir en todo el día.",
        "En mi casillero encontré una nota sin firma: «Revisá también los "
        "nombres. A veces copian la cara. A veces copian la letra.»",
        "El jefe ni me miró: «Esta noche vienen más. Y cada vez tienen menos "
        "paciencia.» Detrás suyo, una luz parpadeó.",
    ],
    [   # antes de la noche 3
        "Ya lo entendí: cada vez que llega uno de ellos, la luz se apaga. "
        "Dicen que no soportan que los miren de frente.",
        "Anoche, cuando volvió la luz, había huellas mojadas en el pasillo. "
        "Terminaban justo detrás de mi silla.",
        "Es la última noche del turno. Si me equivoco una vez más, no vuelvo "
        "a ver el amanecer. Si acierto, cobro y me voy. Esta noche no.",
    ],
]
HISTORIA_LETRAS_POR_SEG = 45   # velocidad con que aparece el texto
HISTORIA_ANCHO_LINEA = 52      # caracteres por línea
HISTORIA_Y = 190               # y de la primera línea
HISTORIA_PASO = 34             # separación entre líneas