"""Clase Partida: guarda el estado de una partida y aplica sus reglas."""

import ajustes as aj
from utilidades import (generar_visitante, decision_correcta,
                        calcular_puntaje, calcular_paciencia, armar_mensaje)


class Partida:
    """Estado de una partida completa (las 3 noches).

    Atributos:
        puntaje: puntos acumulados en toda la partida.
        nivel: índice de la noche actual en aj.NIVELES.
        vidas, racha, atendidos: contadores de la noche actual.
        visitante: el Visitante que está en la puerta.
        mensaje, color_mensaje: resultado de la última decisión.
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
        """Genera el próximo visitante con la paciencia que corresponde."""
        nivel = self.config_nivel()
        paciencia = calcular_paciencia(self.racha, nivel)
        self.visitante = generar_visitante(paciencia, nivel)

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