"""Clase Partida: guarda el estado de una partida y aplica sus reglas."""

import ajustes as aj
from objetos import Objeto
from utilidades import (generar_visitante, decision_correcta,
                        calcular_puntaje, calcular_paciencia, armar_mensaje)


class Partida:
    """Estado de una partida completa (las 3 noches).

    Atributos:
        puntaje: puntos acumulados en toda la partida.
        nivel: índice de la noche actual en aj.NIVELES.
        vidas, racha, atendidos: contadores de la noche actual.
        visitante: el Visitante que está en la puerta.
        objetos: documentos y fotos que el jugador tiene en pantalla.
        menu_abierto: True si se ve el menú "pedir documento / foto".
        mensaje, color_mensaje: texto de la última decisión o aviso.
    """

    def __init__(self):
        """Empieza una partida nueva en la primera noche."""
        self.puntaje = 0
        self.iniciar_nivel(0)

    def config_nivel(self):
        """Devuelve el diccionario de configuración de la noche actual."""
        return aj.NIVELES[self.nivel]

    def iniciar_nivel(self, indice):
        """Prepara la noche 'indice': vidas completas y primer visitante."""
        self.nivel = indice
        self.vidas = aj.VIDAS_INICIALES
        self.racha = 0
        self.atendidos = 0
        self.mensaje = ""
        self.color_mensaje = aj.COLOR_TEXTO
        self.siguiente_visitante()

    def siguiente_visitante(self):
        """Genera el próximo visitante y limpia lo que había en pantalla."""
        nivel = self.config_nivel()
        paciencia = calcular_paciencia(self.racha, nivel)
        self.visitante = generar_visitante(paciencia, nivel)
        self.objetos = []
        self.menu_abierto = False

    # --- Documento y foto ---

    def opciones_disponibles(self):
        """Devuelve qué se le puede pedir (lo que todavía no está afuera)."""
        return [t for t in aj.TIPOS_OBJETO
                if not any(o.tipo == t for o in self.objetos)]

    def pedir(self, tipo):
        """El visitante entrega un documento o una foto."""
        self.objetos.append(Objeto(tipo, self.visitante))
        self.menu_abierto = False

    def texto_pendientes(self):
        """Devuelve lo que falta devolver, ej. "mi documento y mi foto"."""
        return " y ".join(aj.TEXTO_OBJETO[t] for t in aj.TIPOS_OBJETO
                          if any(o.tipo == t for o in self.objetos))

    def devolver(self, objeto):
        """El jugador le devuelve el objeto al visitante."""
        self.objetos.remove(objeto)
        if self.visitante.exigiendo:
            if self.objetos:
                self.visitante.exigiendo = self.texto_pendientes()
            else:
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
        self.menu_abierto = False

    def puede_decidir(self):
        """Devuelve False si el visitante exige sus cosas antes de decidir.

        Solo los vecinos de verdad las reclaman (salvo que se active
        IMPOSTOR_EXIGE_DEVOLUCION en ajustes.py).
        """
        if not self.objetos:
            return True
        return self.visitante.es_impostor and not aj.IMPOSTOR_EXIGE_DEVOLUCION

    def exigir_devolucion(self):
        """El visitante reclama lo que todavía no le devolvieron."""
        self.visitante.exigiendo = self.texto_pendientes()
        self.mensaje = "¡Exige que le devuelvas sus cosas!"
        self.color_mensaje = aj.COLOR_ERROR

    # --- Reglas de la noche ---

    def resolver(self, decision, tiempo_agotado=False):
        """Aplica el resultado de atender al visitante actual.

        'decision' es True (permitir) o False (rechazar); si se acabó el
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