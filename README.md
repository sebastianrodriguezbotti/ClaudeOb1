# Esta noche no

Juego de terror y deducción hecho con Python y pygame. Sos el guardia de la puerta de una fábrica durante tres noches: los empleados llegan a entrar a trabajar, pero algunos **no son quienes dicen ser**. Tenés que descubrirlos antes de que sea tarde.

> **Estudiante:** Sebastián Rodríguez Botti · N.º 288211 · 
> **Asignatura:** Programación 2 · Obligatorio 1

---

## Objetivo

Sobrevivir a las **3 noches**. En cada noche llega una cantidad de empleados a la puerta:

- **Aprobá** (sello verde) a los empleados verdaderos.
- **Rechazá** (sello rojo) a los impostores.
- Cada error, o cada empleado que se impacienta porque tardaste demasiado, **cuesta una vida**. Tenés 3 vidas por noche.
- Si te quedás sin vidas, perdés la partida. Si terminás la noche 3, ganás.

## Cómo se juega

1. Un empleado camina hasta la puerta y se presenta: dice su nombre, su rubro y a qué piso y área va.
2. Hacé **clic sobre el empleado** y elegí **Pedir documento** o **Pedir autorización**. Los papeles aparecen en pantalla y se pueden **arrastrar** con el mouse.
3. Compará todo con el panel **EDIFICIO** (arriba a la derecha), que dice qué área hay en cada piso y qué rubro trabaja en cada una:
   - ¿El piso o el rubro que dice coinciden con el edificio?
   - ¿El nombre del documento es el que dijo, y está bien escrito?
   - ¿La cara del empleado coincide con la **foto del documento**?
4. Arrastrá un **sello** (APROBADO o RECHAZADO, abajo a la derecha) sobre la autorización. Una vez sellada, no se puede cambiar.
5. **Entregá** la autorización sellada arrastrándola hasta el empleado: se lleva todo lo que tengas afuera (también su documento) y ahí queda decidido.

Cada empleado tiene una **barra de paciencia**. Cuando se agota, lo ves enojado y, si llega a cero, perdés una vida. A medida que acumulás aciertos seguidos (racha), los siguientes empleados esperan menos.

### Puntaje

- Acierto: **100 puntos** + **25 por cada acierto seguido** anterior (racha).
- Al terminar una noche: **+50 por cada vida que te sobra**.

### Niveles (noches)

| Noche | Empleados | Personajes en el edificio | Impostores | Paciencia inicial |
|---|---|---|---|---|
| 1 | 6 | 3 | 35 % | 30 s |
| 2 | 8 | 5 | 45 % | 25 s |
| 3 | 10 | 8 | 50 % | 20 s |

### Cómo se delata un impostor

Un impostor tiene **una sola** inconsistencia: dice un **piso** que no corresponde a su área, dice un **rubro** que no es de esa área, el **nombre del documento** está mal escrito o es el de otro empleado, o no dice nada raro y solo su **cara no coincide con la foto** del documento. El nombre mal escrito aparece desde la noche 2.

## Controles

| Acción | Cómo |
|---|---|
| Pedir documento o autorización | Clic en el empleado y elegir la opción |
| Mover documento, autorización o sellos | Arrastrar con el mouse |
| Sellar | Soltar un sello sobre la autorización |
| Entregar | Soltar la autorización sellada sobre el empleado |
| Pausa | Botón **II** (arriba) o tecla `ESC` |
| Continuar / jugar de nuevo | `ENTER` o clic en el botón |
| Volver atrás | `ESC` |
| Salir | Cerrar la ventana con la X, o `ESC` en el menú |

El menú inicial tiene **Jugar**, **Instrucciones**, **Objetivo** y un engranaje de **configuración** (volumen y sonido sí/no). La pausa permite continuar, ver las instrucciones, cambiar el volumen o volver al inicio.

## Cómo se ejecuta

Requiere Python 3 y pygame. Se probó con Python 3.14 y `pygame-ce 2.5.8`.

```bash
pip install pygame
python main.py
```

(`pygame-ce`, instalado con `pip install pygame-ce`, también funciona.)

No se usan otras bibliotecas además de pygame y la biblioteca estándar de Python.

Si falta algún archivo `.wav` de `sonidos/`, el juego los genera solo al arrancar (con `generar_sonidos.py`). Si falta alguna imagen, usa un rectángulo de color en su lugar y avisa por consola cuáles faltan.

## Qué hay en cada archivo

| Archivo | Qué contiene |
|---|---|
| `main.py` | Punto de entrada: crea la ventana, carga los recursos una sola vez y ejecuta el bucle principal (eventos, actualizar, resolver, dibujar). Maneja los estados del juego. |
| `ajustes.py` | Todas las constantes: colores, tamaños, velocidades, fuentes, botones, niveles, empleados, lugares, textos de ayuda. |
| `partida.py` | Clase `Partida`: puntaje, vidas, racha, noche actual, papeles en pantalla y reglas para resolver cada empleado. |
| `visitante.py` | Clase `Visitante`: el empleado que llega a la puerta (movimiento, paciencia, imagen según su estado). |
| `objetos.py` | Clases `Arrastrable`, `Objeto` (documento y autorización) y `Sello`. Todo lo que se arrastra con el mouse. |
| `interfaz.py` | Clases `Boton` y `Deslizador`, y el dibujo del engranaje. |
| `pantallas.py` | Funciones que dibujan cada pantalla: menú, ayudas, configuración, escena de juego, pausa y carteles finales. |
| `utilidades.py` | Funciones con lógica y carga de recursos: generar empleados al azar, decidir si el sello fue correcto, puntaje, paciencia, mensajes, carga de sonidos e imágenes. |
| `generar_sonidos.py` | Genera los efectos de sonido (`.wav`) con ondas y ruido, sin bibliotecas externas. |
| `sonidos/` | Los efectos: `timbre`, `acierto`, `error`, `susto`, `papel` y `sello`. |
| `imagenes/` | Fondos y personajes (ver abajo). |

### Imágenes

La carpeta `imagenes/` tiene dos fondos y cuatro versiones de cada uno de los 8 personajes:

- `fondo2` va atrás, el empleado en el medio y `fondo1` adelante (con transparencia).
- `<personaje>_normal`, `<personaje>_normal_enojado`, `<personaje>_impostor` y `<personaje>_impostor_enojado`, con los personajes `marta`, `hugo`, `lucia`, `tomas`, `elena`, `gonzalo`, `paula` y `julia`.

## Origen y licencia de los recursos

- **Sonidos:** generados por código en este mismo proyecto (`generar_sonidos.py`) con ondas seno, cuadradas y ruido. No se usaron sonidos de terceros.
- **Imágenes:** generadas con Midjourney y ChatGPT; los retoques finales se hicieron en Photoshop.
- **Fuente:** `consolas`, que es una fuente del sistema, no se incluye en el proyecto.

## Uso de inteligencia artificial

Se usó **Claude** (Anthropic) como apoyo principal durante el desarrollo. Al inicio se probó Copilot, pero se siguió con Claude por los resultados. Las imágenes se hicieron con Midjourney y ChatGPT y se retocaron en Photoshop. Claude además ayudó con el informe (diagramas de flujo, diagramación y corrección ortográfica).

- **Qué hizo:** a partir de las decisiones de diseño del estudiante (mecánica de inspección y sellos, temática de fábrica, niveles, paciencia, pausa, arrastrar documentos) escribió y modificó el código en varias iteraciones, generó el script de sonidos, armó pruebas automáticas del flujo del juego y ayudó a redactar la documentación.
- **Qué hizo el estudiante:** definió la idea y todas las reglas, creó las imágenes y los 8 personajes, probó el juego, pidió cada cambio y revisó el resultado. Cuando un cambio no gustó, se volvió a la versión anterior desde GitHub.
- **Revisión:** todo el contenido generado fue revisado por el estudiante, que es responsable de cualquier error.

Referencia (APA 7):

> Anthropic. (2026). *Claude* (Sonnet 5.5) [Modelo de lenguaje de gran tamaño]. https://claude.ai
>
> Midjourney, Inc. (2026). *Midjourney* [Modelo de generación de imágenes]. https://www.midjourney.com
>
> OpenAI. (2026). *ChatGPT* [Modelo de lenguaje de gran tamaño]. https://chatgpt.com
>
> Microsoft. (2026). *Copilot* [Asistente de IA]. https://copilot.microsoft.com

## Repositorio

⚠ COMPLETAR: enlace al repositorio de GitHub: `https://github.com/<usuario>/<repositorio>`