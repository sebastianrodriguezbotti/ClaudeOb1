"""Clase Partida: guarda el estado de una partida y aplica sus reglas."""

import random

import ajustes as aj
from objetos import Objeto, Sello
from utilidades import (generar_visitante, decision_correcta,
                        calcular_puntaje, calcular_paciencia, armar_mensaje,
                        armar_plan_impostores, elegir_apagones,
                        armar_orden_empleados)


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
        orden: los empleados de la noche en el orden en que llegan (aparecen todos).
        plan: lista de True/False con qué visitantes de la noche son impostores.
        apagones_en: números de los visitantes que apagan la luz en la noche.
        apagones_pendientes: de esos, los que todavía no la apagaron.
        apagon_demora: segundos que espera el empleado actual antes de apagar la luz.
        mensaje, color_mensaje: texto de la última decisión o aviso.
    """

    def __init__(self):
        """Empieza una partida nueva en la primera noche."""
        self.puntaje = 0
        self.visitante = None
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
        self.plan = armar_plan_impostores(self.config_nivel())
        self.orden = armar_orden_empleados(self.config_nivel())   # quién llega en cada turno
        # qué visitantes apagan la luz y cuáles todavía no lo hicieron
        self.apagones_en = elegir_apagones(self.plan, self.config_nivel()["apagones"])
        self.apagones_pendientes = set(self.apagones_en)
        self.siguiente_visitante()

    def siguiente_visitante(self):
        """Genera el próximo empleado (con otra cara) y limpia la pantalla."""
        nivel = self.config_nivel()
        paciencia = calcular_paciencia(self.racha, nivel)
        anterior = self.visitante.imagen_id if self.visitante else None
        # cuánto después de llegar apaga la luz (si le toca): al azar
        self.apagon_demora = random.uniform(*aj.APAGON_DEMORA)
        self.visitante = generar_visitante(paciencia, nivel, anterior,
                                           self.plan[self.atendidos],
                                           self.orden[self.atendidos])
        self.objetos = []
        self.menu_abierto = False
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

    # --- Sellos y entrega ---

    def soltar_sello(self, sello, pos):
        """Procesa un sello soltado en la posición 'pos'.

        Devuelve "ok" (quedó sellada), "sin_autorizacion" (todavía no la
        pidió), "ya_sellada" (no se puede cambiar) o None (se soltó en
        otro lado). Sellar NO decide: hay que entregarla.
        """
        autorizacion = self.autorizacion()
        if autorizacion is None:
            self.mensaje = "Primero pedile la autorización"
            self.color_mensaje = aj.COLOR_ERROR
            return "sin_autorizacion"
        if not autorizacion.rect.collidepoint(pos):
            return None
        if autorizacion.sello is not None:
            self.mensaje = "La autorización ya está sellada"
            self.color_mensaje = aj.COLOR_ERROR
            return "ya_sellada"
        autorizacion.sello = sello.valor
        self.mensaje = "Autorización sellada: entregásela al empleado"
        self.color_mensaje = aj.COLOR_TEXTO
        return "ok"

    def entregar(self, objeto):
        """El jugador suelta un papel sobre el empleado.

        - Documento: se lo lleva (y no pasa nada más).
        - Autorización sin sellar: la rechaza.
        - Autorización sellada: se lleva TODO lo que haya afuera, junto,
          y queda decidido.

        Devuelve (entregado, decision): decision es True (aprobado),
        False (rechazado) o None si todavía no se decide.
        """
        if objeto.tipo == "documento":
            self.objetos.remove(objeto)
            return True, None
        if objeto.sello is None:
            self.mensaje = "Primero sellá la autorización"
            self.color_mensaje = aj.COLOR_ERROR
            return False, None
        self.objetos = []
        return True, objeto.sello

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

    # --- Apagón ---

    def debe_apagar(self):
        """Devuelve True si el impostor de turno tiene que apagar la luz ya."""
        visitante = self.visitante
        espero = visitante.paciencia_max - visitante.paciencia
        return (self.atendidos in self.apagones_pendientes
                and visitante.llego() and espero >= self.apagon_demora)

    def iniciar_apagon(self):
        """Marca este apagón como hecho y suelta todo lo que se arrastraba."""
        self.apagones_pendientes.discard(self.atendidos)
        self.soltar_todo()
        self.mensaje = "¡El impostor apagó la luz!"
        self.color_mensaje = aj.COLOR_ERROR

    def terminar_apagon(self, exito):
        """Aplica el resultado del minijuego de cables.

        Si no se arregló a tiempo se pierde la noche: quedan 0 vidas.
        Devuelve True si eso termina la partida.
        """
        if exito:
            self.mensaje = "Luz restablecida"
            self.color_mensaje = aj.COLOR_ACIERTO
            return False
        self.vidas = 0
        self.racha = 0
        self.mensaje = "No arreglaste la luz a tiempo: perdiste la noche"
        self.color_mensaje = aj.COLOR_ERROR
        return True