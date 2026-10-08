"""Funciones auxiliares de la lógica del juego."""

import os
import random
import re

import pygame

import ajustes as aj
import generar_sonidos
from visitante import Visitante


def alterar_nombre(nombre):
    """Devuelve el nombre con UNA letra cambiada por otra parecida.

    Ej.: "Marta Gómez" -> "Marta Gomez" o "Marta Gómes". Si no hay ninguna
    letra confundible, intercambia dos letras vecinas del final.
    """
    opciones = []
    for viejo, nuevo in aj.CAMBIOS_PARECIDOS:
        for hallazgo in re.finditer(viejo, nombre):
            opciones.append((hallazgo.start(), len(viejo), nuevo))
    if opciones:
        inicio, largo, nuevo = random.choice(opciones)
        return nombre[:inicio] + nuevo + nombre[inicio + largo:]
    letras = list(nombre)
    for i in range(len(letras) - 2, 0, -1):
        if letras[i] != letras[i + 1]:
            letras[i], letras[i + 1] = letras[i + 1], letras[i]
            break
    return "".join(letras)


def armar_plan_impostores(nivel):
    """Devuelve una lista de True/False (uno por visitante de la noche).

    True = ese visitante es impostor. Hay exactamente nivel["impostores"]
    impostores, en un orden al azar.
    """
    plan = ([True] * nivel["impostores"]
            + [False] * (nivel["visitantes"] - nivel["impostores"]))
    random.shuffle(plan)
    return plan


def elegir_apagon(plan):
    """Devuelve el número de visitante (empezando en 0) que apaga la luz.

    Siempre es un impostor; si se puede, uno que no sea de los primeros.
    """
    impostores = [i for i, es in enumerate(plan) if es]
    tarde = [i for i in impostores if i >= aj.APAGON_MIN_ATENDIDOS]
    return random.choice(tarde or impostores)


def generar_visitante(paciencia=aj.PACIENCIA_BASE, nivel=aj.NIVELES[0],
                      evitar_imagen=None, es_impostor=False):
    """Crea un empleado al azar; 'es_impostor' dice si es verdadero o impostor.

    Elige uno de los primeros N empleados de ajustes.EMPLEADOS
    ('evitar_imagen' evita repetir al anterior). Un impostor usa las
    imágenes de "impostor" (su cara no coincide con la foto del documento)
    y además tiene UNA inconsistencia: dice un piso que no corresponde,
    dice un rubro que no es de ese lugar, el nombre de su documento está
    mal (mal escrito o de otro empleado), o ninguna ("aspecto": solo se
    nota la cara).
    """
    empleados = aj.EMPLEADOS[:nivel["empleados"]]
    candidatos = [e for e in empleados if e["imagen"] != evitar_imagen]
    datos = random.choice(candidatos or empleados)
    indice = 0 if datos["genero"] == "m" else 1   # posición en la tupla del rubro
    nombre, lugar = datos["nombre"], datos["lugar"]
    info = aj.LUGARES[lugar]
    rubro, piso = info["rubro"][indice], info["piso"]

    if not es_impostor:
        return Visitante(nombre, rubro, lugar, piso, datos["imagen"], False,
                         paciencia=paciencia)

    tipo = random.choice(nivel["tipos"])
    nombre_documento = rubro_documento = None
    if tipo == "nombre":
        if random.random() < 0.5:
            nombre_documento = alterar_nombre(nombre)      # mal escrito
        else:                                              # el de otro empleado
            nombre_documento = random.choice(
                [e["nombre"] for e in empleados if e["nombre"] != nombre])
        motivo = f"El documento decía {nombre_documento}, no {nombre}"
    elif tipo == "piso":
        falso = random.choice([p for p in aj.PISOS if p != piso])
        motivo = f"{lugar} está en el piso {piso}, no en el {falso}"
        piso = falso
    elif tipo == "aspecto":
        motivo = "Su cara no coincidía con la foto del documento"
    else:
        otro = random.choice([e for e in empleados if e["lugar"] != lugar])
        falso = aj.LUGARES[otro["lugar"]]["rubro"][indice]
        motivo = (f"Dijo ser {falso}, pero va {info['donde']} "
                  f"({info['personal']})")
        rubro_documento = rubro      # su documento dice el rubro verdadero
        rubro = falso
    return Visitante(nombre, rubro, lugar, piso, datos["imagen"], True,
                     motivo, paciencia, nombre_documento, rubro_documento)


def decision_correcta(visitante, permitir):
    """Devuelve True si la decisión fue la acertada.

    Lo correcto es aprobar a los verdaderos y rechazar a los impostores.
    """
    return permitir == (not visitante.es_impostor)


def calcular_puntaje(puntaje, acerto, racha):
    """Devuelve el nuevo puntaje según el resultado y la racha actual.

    Cada acierto suma puntos base más un bonus por racha.
    Un error no resta puntos (resta una vida).
    """
    if acerto:
        return puntaje + aj.PUNTOS_ACIERTO + aj.PUNTOS_RACHA * racha
    return puntaje


def calcular_paciencia(racha, nivel):
    """Devuelve los segundos de paciencia del próximo empleado.

    Parte de la paciencia del nivel y baja con cada acierto seguido,
    pero nunca por debajo del mínimo.
    """
    return max(aj.PACIENCIA_MIN,
               nivel["paciencia"] - aj.PACIENCIA_REDUCCION * racha)


def armar_mensaje(visitante, acerto, tiempo_agotado=False):
    """Devuelve el texto de resultado que se muestra tras decidir."""
    if tiempo_agotado:
        return "¡Tiempo! El empleado se impacientó"
    if acerto and not visitante.es_impostor:
        return "¡Bien!"
    prefijo = "¡Bien!" if acerto else "¡Error!"
    detalle = visitante.motivo if visitante.es_impostor else (
        "Era un empleado de verdad")
    return f"{prefijo} {detalle}"


def cargar_sonidos():
    """Devuelve un diccionario {nombre: pygame.mixer.Sound}.

    Si faltan los archivos .wav, los genera primero.
    """
    faltan = any(
        not os.path.exists(os.path.join(aj.SONIDOS_CARPETA, f"{n}.wav"))
        for n in aj.NOMBRES_SONIDOS)
    if faltan:
        generar_sonidos.generar_todos()
    sonidos = {}
    for nombre in aj.NOMBRES_SONIDOS:
        sonido = pygame.mixer.Sound(
            os.path.join(aj.SONIDOS_CARPETA, f"{nombre}.wav"))
        sonido.set_volume(aj.VOLUMEN)
        sonidos[nombre] = sonido
    return sonidos


def aplicar_volumen(sonidos, volumen, activo):
    """Ajusta el volumen de todos los sonidos y devuelve el volumen aplicado.

    Si el sonido está desactivado, el volumen efectivo es 0.
    """
    efectivo = volumen if activo else 0.0
    for sonido in sonidos.values():
        sonido.set_volume(efectivo)
    return efectivo


def _ruta_imagen(base):
    """Busca imagenes/<base> con alguna extensión. Devuelve la ruta o None."""
    for extension in aj.EXTENSIONES_IMAGEN:
        ruta = os.path.join(aj.IMAGENES_CARPETA, base + extension)
        if os.path.exists(ruta):
            return ruta
    return None


def _cargar_imagen(base, color_reemplazo, tamano_reemplazo, faltan):
    """Carga una imagen; si no existe, devuelve un rectángulo de color.

    Los nombres de las imágenes que faltan se agregan a la lista 'faltan'.
    """
    ruta = _ruta_imagen(base)
    if ruta is None:
        faltan.append(base)
        reemplazo = pygame.Surface(tamano_reemplazo, pygame.SRCALPHA)
        reemplazo.fill(color_reemplazo)
        return reemplazo
    return pygame.image.load(ruta).convert_alpha()


def _escalar_a_alto(imagen, alto):
    """Devuelve la imagen escalada a 'alto' píxeles, manteniendo proporción."""
    ancho = max(1, round(imagen.get_width() * alto / imagen.get_height()))
    return pygame.transform.smoothscale(imagen, (ancho, alto))


def _recortar(imagen, fracciones):
    """Devuelve el pedazo de la imagen indicado como fracciones (x, y, ancho, alto)."""
    fx, fy, fancho, falto = fracciones
    ancho, alto = imagen.get_width(), imagen.get_height()
    zona = pygame.Rect(int(ancho * fx), int(alto * fy),
                       max(1, int(ancho * fancho)), max(1, int(alto * falto)))
    return imagen.subsurface(zona).copy()


def _ajustar_en_caja(imagen, caja):
    """Devuelve la imagen escalada para entrar en 'caja' (ancho, alto)."""
    factor = min(caja[0] / imagen.get_width(), caja[1] / imagen.get_height())
    tamano = (max(1, round(imagen.get_width() * factor)),
              max(1, round(imagen.get_height() * factor)))
    return pygame.transform.smoothscale(imagen, tamano)


def cargar_imagenes():
    """Carga todas las imágenes UNA vez y las devuelve en un diccionario.

    Estructura: {"fondo1": Surface, "fondo2": Surface,
                 "visitantes": {imagen_id: {variante: Surface}},
                 "fotos": {imagen_id: Surface}}   # retrato para el documento
    Si falta un archivo usa un reemplazo de color (para que el juego no se
    rompa) y avisa por consola cuáles faltan.
    """
    faltan = []
    tamano = (aj.ANCHO, aj.ALTO)
    fondo1 = _cargar_imagen(aj.FONDO_1, (0, 0, 0, 0), tamano, faltan)
    fondo2 = _cargar_imagen(aj.FONDO_2, aj.COLOR_PARED, tamano, faltan)
    imagenes = {
        "fondo1": pygame.transform.smoothscale(fondo1, tamano),
        "fondo2": pygame.transform.smoothscale(fondo2, tamano),
        "visitantes": {},
        "fotos": {},
    }
    for datos in aj.EMPLEADOS:
        prefijo = datos["imagen"]
        if prefijo in imagenes["visitantes"]:
            continue
        variantes = {}
        for variante in aj.VARIANTES:
            imagen = _cargar_imagen(
                f"{prefijo}_{variante}", aj.COLORES_REEMPLAZO[variante],
                (aj.VISITANTE_IMG_ALTO // 2, aj.VISITANTE_IMG_ALTO), faltan)
            variantes[variante] = _escalar_a_alto(imagen,
                                                  aj.VISITANTE_IMG_ALTO)
        imagenes["visitantes"][prefijo] = variantes
        retrato = _recortar(variantes["normal"], aj.FOTO_RECORTE)
        imagenes["fotos"][prefijo] = _ajustar_en_caja(retrato, aj.FOTO_CAJA)
    if faltan:
        print(f"[aviso] Faltan {len(faltan)} imágenes en "
              f"{aj.IMAGENES_CARPETA}: " + ", ".join(faltan))
    return imagenes