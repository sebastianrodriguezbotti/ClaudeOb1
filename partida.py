"""Clase Partida: guarda el estado de una partida y aplica sus reglas."""

import ajustes as aj
from objetos import Objeto, Sello
from utilidades import (generar_visitante, decision_correcta,
                        calcular_puntaje, calcular_paciencia, armar_mensaje)


class Partida:
    """Estado de una partida completa (las 3 noches).

    Atributos:
        puntaje: puntos acumulados en toda la partida.
        nivel: índice de la noche actual en aj.NIVELES.
        vidas, racha, atendidos: contadores de la noche actual.
        visitante: el empleado que está en la puerta.
        objetos: documento y autorización que el jugador tiene en pantalla.
        sellos: los dos sellos de la bandeja (APROBADO y RECHAZADO).
        menu_abierto: True si se ve el menú "pedir documento / autorización".
        sello_pendiente: None, o la decisión ya sellada que falta resolver.
        mensaje, color_mensaje: texto de la última decisión o aviso.
    """

    def __init__(self):
        """Empieza una partida nueva en la primera noche."""
        self.puntaje = 0
        self.sellos = [Sello(True, aj.SELLO_CENTROS[True]),
                       Sello(False, aj.SELLO_CENTROS[False])]
        self.iniciar_nivel(0)

    def config_nivel(self):
        """Devuelve el diccionario de configuración de la noche actual."""
        return aj.NIVELES[self.nivel]

    def iniciar_nivel(self, indice):
        """Prepara la noche 'indice': vidas completas y primer empleado."""
        self.nivel = indice
        self.vidas = aj.VIDAS_INICIALES
        self.racha = 0
        self.atendidos = 0
        self.mensaje = ""
        self.color_mensaje = aj.COLOR_TEXTO
        self.siguiente_visitante()

    def siguiente_visitante(self):
        """Genera el próximo empleado y limpia lo que había en pantalla."""
        nivel = self.config_nivel()
        paciencia = calcular_paciencia(self.racha, nivel)
        self.visitante = generar_visitante(paciencia, nivel)
        self.objetos = []
        self.menu_abierto = False
        self.sello_pendiente = None
        self.espera_sello = 0.0
        for sello in self.sellos:
            sello.volver()

    # --- Documento y autorización ---

    def opciones_disponibles(self):
        """Devuelve qué se le puede pedir (lo que todavía no está afuera)."""
        return [t for t in aj.TIPOS_OBJETO
                if not any(o.tipo == t for o in self.objetos)]

    def pedir(self, tipo):
        """El empleado entrega un documento o la autorización."""
        self.objetos.append(Objeto(tipo, self.visitante))
        self.menu_abierto = False

    def autorizacion(self):
        """Devuelve el papel de autorización si está afuera, o None."""
        for objeto in self.objetos:
            if objeto.tipo == "autorizacion":
                return objeto
        return None

    def documento_afuera(self):
        """Devuelve True si el documento del empleado está en pantalla."""
        return any(o.tipo == "documento" for o in self.objetos)

    def devolver(self, objeto):
        """El jugador le devuelve el documento al empleado."""
        self.objetos.remove(objeto)
        if self.visitante.exigiendo:
            self.visitante.exigiendo = ""
            self.mensaje = ""

    def traer_al_frente(self, objeto):
        """Pone el objeto arriba de los demás (se dibuja último)."""
        self.objetos.remove(objeto)
        self.objetos.append(objeto)

    def soltar_todo(self):
        """Cancela arrastres y cierra el menú (al pausar)."""
        for objeto in self.objetos:
            objeto.arrastrando = False
        for sello in self.sellos:
            sello.volver()
        self.menu_abierto = False

    # --- Sellos ---

    def puede_decidir(self):
        """Devuelve False si el empleado exige su documento antes de sellar.

        Solo los empleados verdaderos lo reclaman (salvo que se active
        IMPOSTOR_EXIGE_DEVOLUCION en ajustes.py).
        """
        if not self.documento_afuera():
            return True
        return self.visitante.es_impostor and not aj.IMPOSTOR_EXIGE_DEVOLUCION

    def exigir_devolucion(self):
        """El empleado reclama el documento que todavía no le devolvieron."""
        self.visitante.exigiendo = "mi documento"
        self.mensaje = "¡Exige que le devuelvas su documento!"
        self.color_mensaje = aj.COLOR_ERROR

    def soltar_sello(self, sello, pos):
        """Procesa un sello soltado en la posición 'pos'.

        Devuelve "ok" (quedó sellada), "exige" (el empleado reclama su
        documento), "sin_autorizacion" (todavía no la pidió) o None
        (se soltó en otro lado).
        """
        autorizacion = self.autorizacion()
        if autorizacion is None:
            self.mensaje = "Primero pedile la autorización"
            self.color_mensaje = aj.COLOR_ERROR
            return "sin_autorizacion"
        if not autorizacion.rect.collidepoint(pos):
            return None
        if not self.puede_decidir():
            self.exigir_devolucion()
            return "exige"
        autorizacion.sello = sello.valor
        self.sello_pendiente = sello.valor
        self.espera_sello = aj.RETARDO_SELLO
        self.mensaje = ""
        return "ok"

    def avanzar_sello(self, dt):
        """Espera un instante con el sello a la vista (dt en segundos).

        Devuelve la decisión (True/False) cuando termina la espera, o
        None si no hay sello o todavía falta.
        """
        if self.sello_pendiente is None:
            return None
        self.espera_sello -= dt
        if self.espera_sello > 0:
            return None
        decision = self.sello_pendiente
        self.sello_pendiente = None
        return decision

    # --- Reglas de la noche ---

    def resolver(self, decision, tiempo_agotado=False):
        """Aplica el resultado de atender al empleado actual.

        'decision' es True (aprobado) o False (rechazado); si se acabó el
        tiempo no importa. Devuelve (acerto, evento), donde evento es None,
        "nivel_completo", "victoria" o "fin".
        """
        acerto = (not tiempo_agotado) and decision_correcta(self.visitante,
                                                            decision)
        self.mensaje = armar_mensaje(self.visitante, acerto, tiempo_agotado)
        self.atendidos += 1
        if acerto:
            self.puntaje = calcular_puntaje(self.puntaje, True, self.racha)
            self.racha += 1
            self.color_mensaje = aj.COLOR_ACIERTO
        else:
            self.vidas -= 1
            self.racha = 0
            self.color_mensaje = aj.COLOR_ERROR

        if self.vidas <= 0:
            return acerto, "fin"
        if self.atendidos >= self.config_nivel()["visitantes"]:
            self.puntaje += self.vidas * aj.PUNTOS_BONUS_VIDA
            if self.nivel == len(aj.NIVELES) - 1:
                return acerto, "victoria"
            return acerto, "nivel_completo"
        self.siguiente_visitante()
        return acerto, None