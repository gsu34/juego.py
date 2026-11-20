"""


Controles:
    Flechas / WASD ... mover
    ESPACIO .......... poner bomba
    R ................ reiniciar nivel actual (o partida si ya terminó)
    1 / 2 / 3 ........ ir a un nivel
    ESC .............. salir
"""

import copy
import importlib
import math
import random
import subprocess
import sys



def instalar_pygame():
    """Instala pygame con pip si no esta disponible."""
    # En un .exe (PyInstaller) pygame ya viene incluido: no hay nada que instalar.
    if getattr(sys, "frozen", False):
        return

    try:
        import pygame  # noqa: F401
        return
    except ImportError:
        pass

    print("pygame no esta instalado. Instalando...")
    comando = [sys.executable, "-m", "pip", "install", "pygame"]

    for extra in ([], ["--user"]):
        try:
            subprocess.check_call(comando + extra)
            importlib.invalidate_caches()
            print("pygame instalado correctamente.\n")
            return
        except (subprocess.CalledProcessError, OSError):
            continue

    print("\nNo se pudo instalar pygame automaticamente.")
    print("Instalalo manualmente con:  pip install pygame")
    try:
        input("Presiona ENTER para salir...")
    except EOFError:
        pass
    sys.exit(1)


instalar_pygame()

import pygame  # noqa: E402



TAM = 50
FILAS = 11
COLUMNAS = 15
HUD_ALTO = 60

ANCHO = COLUMNAS * TAM
ALTO = FILAS * TAM + HUD_ALTO
FPS = 60

# Tipos de celda
VACIO, PARED, BLOQUE = 0, 1, 2

# Jugador
RADIO_JUGADOR = 17
VELOCIDAD_JUGADOR = 4
VIDAS_INICIALES = 3
INVULNERABLE_MS = 2000

# Bombas
TIEMPO_BOMBA_MS = 1800
DURACION_EXPLOSION_MS = 500
ALCANCE_BOMBA = 2
MAX_BOMBAS = 2

# Enemigos
RADIO_ENEMIGO = 16
VELOCIDAD_ENEMIGO = 2
ENEMIGOS_POR_NIVEL = {1: 3, 2: 4, 3: 5}

# Puntos
PUNTOS_BLOQUE = 10
PUNTOS_ENEMIGO = 100

# Colores
FONDO = (25, 25, 25)
PISO = (45, 120, 55)
PISO_CLARO = (60, 145, 65)
PARED_COLOR = (80, 80, 80)
PARED_CLARA = (120, 120, 120)
BLOQUE_COLOR = (170, 80, 40)
AMARILLO = (240, 210, 40)
NEGRO = (20, 20, 20)
BLANCO = (255, 255, 255)
ROJO = (220, 40, 40)
NARANJA = (255, 130, 20)
MORADO = (150, 60, 190)

TECLAS_NIVEL = {
    pygame.K_1: 1, pygame.K_KP1: 1,
    pygame.K_2: 2, pygame.K_KP2: 2,
    pygame.K_3: 3, pygame.K_KP3: 3,
}

DIRECCIONES = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# ==========================================
# MAPAS (0 = vacio, 1 = pared, 2 = bloque)
# ==========================================

MAPAS_ORIGINALES = {
    1: [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,2,0,0,1,0,1,0,0,2,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,2,0,0,0,2,0,0,0,2,0,0,0,2,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,0,2,0,0,0,0,0,0,0,2,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,2,0,0,0,2,0,0,0,2,0,0,0,2,1],
        [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,0,2,0,0,1,0,1,0,0,2,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
    2: [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,2,0,0,0,2,0,0,0,2,0,1],
        [1,0,1,1,1,0,1,0,1,0,1,1,1,0,1],
        [1,0,1,2,0,0,1,0,1,0,0,2,1,0,1],
        [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
        [1,2,1,0,1,2,0,0,0,2,1,0,1,2,1],
        [1,0,0,0,0,0,1,0,1,0,0,0,0,0,1],
        [1,0,1,2,1,0,1,0,1,0,1,2,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,0,2,0,0,1,0,1,0,0,2,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
    3: [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,2,0,0,1,0,2,0,0,0,2,0,1],
        [1,0,1,1,0,0,1,0,1,1,1,0,1,0,1],
        [1,0,0,0,0,1,0,0,0,2,0,0,0,0,1],
        [1,1,1,0,0,1,0,1,1,1,0,1,1,0,1],
        [1,0,0,0,2,0,0,0,0,0,0,0,2,0,1],
        [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,2,0,0,1],
        [1,2,1,1,1,0,1,0,1,1,1,0,1,1,1],
        [1,0,0,2,0,0,0,0,0,2,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
}

INICIO_JUGADOR = (TAM + TAM // 2, TAM + TAM // 2)


# ==========================================
# UTILIDADES
# ==========================================

def celda_de(x, y):
    """Devuelve (fila, columna) para una posicion en pixeles."""
    return int(y // TAM), int(x // TAM)


def centro_de(fila, columna):
    """Devuelve el centro en pixeles de una celda."""
    return columna * TAM + TAM // 2, fila * TAM + TAM // 2


def rect_circular(x, y, radio):
    return pygame.Rect(int(x - radio), int(y - radio), radio * 2, radio * 2)


# ==========================================
# ENTIDADES
# ==========================================

class Bomba:
    def __init__(self, fila, columna, ahora):
        self.fila = fila
        self.columna = columna
        self.detona_en = ahora + TIEMPO_BOMBA_MS
        # Mientras el jugador siga encima, puede salir de la casilla.
        self.atravesable = True

    @property
    def rect(self):
        return pygame.Rect(
            self.columna * TAM + 5, self.fila * TAM + 5, TAM - 10, TAM - 10
        )


class Enemigo:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.direccion = random.choice(DIRECCIONES)
        self.vivo = True

    @property
    def rect(self):
        return rect_circular(self.x, self.y, RADIO_ENEMIGO)


# ==========================================
# JUEGO
# ==========================================

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Bomberman - 3 Niveles")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Arial", 18, True)
        self.fuente_grande = pygame.font.SysFont("Arial", 40, True)
        self.fuente_chica = pygame.font.SysFont("Arial", 14)
        self.nueva_partida()

    # ---------- Estado ----------

    def nueva_partida(self):
        self.vidas = VIDAS_INICIALES
        self.puntaje = 0
        self.cargar_nivel(1)

    def cargar_nivel(self, numero):
        self.nivel = numero
        # Copia profunda: los mapas originales nunca se modifican.
        self.mapa = copy.deepcopy(MAPAS_ORIGINALES[numero])
        self.jugador_x, self.jugador_y = INICIO_JUGADOR
        self.bombas = []
        self.explosiones = []  # lista de (fila, columna, fin_ms)
        self.invulnerable_hasta = pygame.time.get_ticks() + 1000
        self.estado = "jugando"  # jugando | nivel_completo | game_over | victoria
        self.estado_desde = 0
        self.enemigos = self.crear_enemigos(ENEMIGOS_POR_NIVEL[numero])

    def crear_enemigos(self, cantidad):
        """Coloca enemigos en celdas vacias alcanzables y lejos del jugador."""
        inicio = celda_de(*INICIO_JUGADOR)
        alcanzables = self.celdas_alcanzables(inicio)
        candidatas = [
            c for c in alcanzables
            if self.mapa[c[0]][c[1]] == VACIO
            and abs(c[0] - inicio[0]) + abs(c[1] - inicio[1]) >= 6
        ]
        random.shuffle(candidatas)
        enemigos = []
        for fila, columna in candidatas[:cantidad]:
            enemigos.append(Enemigo(*centro_de(fila, columna)))
        return enemigos

    def celdas_alcanzables(self, inicio):
        """BFS desde 'inicio' considerando que los bloques se pueden destruir."""
        visitadas = {inicio}
        pendientes = [inicio]
        while pendientes:
            fila, col = pendientes.pop()
            for df, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nf, nc = fila + df, col + dc
                if (0 <= nf < FILAS and 0 <= nc < COLUMNAS
                        and (nf, nc) not in visitadas
                        and self.mapa[nf][nc] != PARED):
                    visitadas.add((nf, nc))
                    pendientes.append((nf, nc))
        return visitadas

    # ---------- Colisiones ----------

    def choca_con_mapa(self, rect):
        """Revisa solo las celdas que toca el rectangulo."""
        for fila in range(rect.top // TAM, rect.bottom // TAM + 1):
            for col in range(rect.left // TAM, rect.right // TAM + 1):
                if not (0 <= fila < FILAS and 0 <= col < COLUMNAS):
                    return True
                if self.mapa[fila][col] in (PARED, BLOQUE):
                    if rect.colliderect(
                        pygame.Rect(col * TAM, fila * TAM, TAM, TAM)
                    ):
                        return True
        return False

    def choca_con_bombas(self, rect):
        for bomba in self.bombas:
            if not bomba.atravesable and rect.colliderect(bomba.rect):
                return True
        return False

    def es_libre(self, x, y, radio):
        rect = rect_circular(x, y, radio)
        return not self.choca_con_mapa(rect) and not self.choca_con_bombas(rect)

    # ---------- Jugador ----------

    def mover_jugador(self):
        teclas = pygame.key.get_pressed()
        dx = dy = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += 1

        if dx == 0 and dy == 0:
            return

        factor = VELOCIDAD_JUGADOR / (math.sqrt(2) if dx and dy else 1)
        self.intentar_mover_jugador(dx * factor, dy * factor)

    def intentar_mover_jugador(self, dx, dy):
        r = RADIO_JUGADOR
        movio_x = movio_y = True

        if dx:
            if self.es_libre(self.jugador_x + dx, self.jugador_y, r):
                self.jugador_x += dx
            else:
                movio_x = False
        if dy:
            if self.es_libre(self.jugador_x, self.jugador_y + dy, r):
                self.jugador_y += dy
            else:
                movio_y = False

        # Ayuda en esquinas: si solo se mueve en un eje y choca,
        # empuja suavemente hacia el centro del pasillo.
        if dx and not dy and not movio_x:
            self.alinear_hacia_centro(eje="y")
        elif dy and not dx and not movio_y:
            self.alinear_hacia_centro(eje="x")

    def alinear_hacia_centro(self, eje):
        tolerancia = 16
        if eje == "y":
            centro = (self.jugador_y // TAM) * TAM + TAM // 2
            diff = centro - self.jugador_y
            paso = max(-VELOCIDAD_JUGADOR, min(VELOCIDAD_JUGADOR, diff))
            if 0 < abs(diff) <= tolerancia and self.es_libre(
                self.jugador_x, self.jugador_y + paso, RADIO_JUGADOR
            ):
                self.jugador_y += paso
        else:
            centro = (self.jugador_x // TAM) * TAM + TAM // 2
            diff = centro - self.jugador_x
            paso = max(-VELOCIDAD_JUGADOR, min(VELOCIDAD_JUGADOR, diff))
            if 0 < abs(diff) <= tolerancia and self.es_libre(
                self.jugador_x + paso, self.jugador_y, RADIO_JUGADOR
            ):
                self.jugador_x += paso

    def rect_jugador(self):
        return rect_circular(self.jugador_x, self.jugador_y, RADIO_JUGADOR)

    def recibir_dano(self):
        ahora = pygame.time.get_ticks()
        if ahora < self.invulnerable_hasta or self.estado != "jugando":
            return
        self.vidas -= 1
        if self.vidas <= 0:
            self.estado = "game_over"
            self.estado_desde = ahora
        else:
            self.jugador_x, self.jugador_y = INICIO_JUGADOR
            self.invulnerable_hasta = ahora + INVULNERABLE_MS
            # Si reaparece sobre una bomba, que pueda salir de ella.
            rect_j = self.rect_jugador()
            for bomba in self.bombas:
                if rect_j.colliderect(bomba.rect):
                    bomba.atravesable = True

    # ---------- Bombas y explosiones ----------

    def colocar_bomba(self):
        if self.estado != "jugando" or len(self.bombas) >= MAX_BOMBAS:
            return
        fila, col = celda_de(self.jugador_x, self.jugador_y)
        if any(b.fila == fila and b.columna == col for b in self.bombas):
            return
        self.bombas.append(Bomba(fila, col, pygame.time.get_ticks()))

    def actualizar_bombas(self):
        ahora = pygame.time.get_ticks()
        rect_j = self.rect_jugador()

        # La bomba se vuelve solida cuando ni el jugador ni un enemigo
        # siguen encima (evita que alguien quede atrapado dentro).
        for bomba in self.bombas:
            if (bomba.atravesable
                    and not rect_j.colliderect(bomba.rect)
                    and not any(e.rect.colliderect(bomba.rect) for e in self.enemigos)):
                bomba.atravesable = False

        # Detonaciones (incluye reacciones en cadena).
        detonando = True
        while detonando:
            detonando = False
            for bomba in self.bombas[:]:
                if ahora >= bomba.detona_en:
                    self.bombas.remove(bomba)
                    self.explotar(bomba, ahora)
                    detonando = True

        self.explosiones = [e for e in self.explosiones if ahora < e[2]]

    def explotar(self, bomba, ahora):
        celdas = [(bomba.fila, bomba.columna)]

        for df, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            for distancia in range(1, ALCANCE_BOMBA + 1):
                nf = bomba.fila + df * distancia
                nc = bomba.columna + dc * distancia

                if not (0 <= nf < FILAS and 0 <= nc < COLUMNAS):
                    break
                tipo = self.mapa[nf][nc]
                if tipo == PARED:
                    break

                celdas.append((nf, nc))

                if tipo == BLOQUE:
                    self.mapa[nf][nc] = VACIO
                    self.puntaje += PUNTOS_BLOQUE
                    break

        fin = ahora + DURACION_EXPLOSION_MS
        for fila, col in celdas:
            self.explosiones.append((fila, col, fin))

        # Reaccion en cadena: las bombas alcanzadas detonan de inmediato.
        for otra in self.bombas:
            if (otra.fila, otra.columna) in celdas:
                otra.detona_en = ahora

    def celdas_en_llamas(self):
        return {(f, c) for f, c, _ in self.explosiones}

    # ---------- Enemigos ----------

    def actualizar_enemigos(self):
        for enemigo in self.enemigos:
            self.mover_enemigo(enemigo)

    def mover_enemigo(self, e):
        dx, dy = e.direccion
        nx = e.x + dx * VELOCIDAD_ENEMIGO
        ny = e.y + dy * VELOCIDAD_ENEMIGO

        # En el centro de una celda, a veces cambia de direccion.
        cerca_centro = (
            abs(e.x % TAM - TAM / 2) < VELOCIDAD_ENEMIGO
            and abs(e.y % TAM - TAM / 2) < VELOCIDAD_ENEMIGO
        )
        if cerca_centro and random.random() < 0.25:
            self.elegir_direccion(e)
            return

        if self.es_libre(nx, ny, RADIO_ENEMIGO):
            e.x, e.y = nx, ny
        else:
            self.elegir_direccion(e)

    def elegir_direccion(self, e):
        opciones = [
            d for d in DIRECCIONES
            if self.es_libre(
                e.x + d[0] * VELOCIDAD_ENEMIGO * 2,
                e.y + d[1] * VELOCIDAD_ENEMIGO * 2,
                RADIO_ENEMIGO,
            )
        ]
        if opciones:
            e.direccion = random.choice(opciones)

    # ---------- Reglas ----------

    def revisar_colisiones(self):
        if self.estado != "jugando":
            return

        llamas = self.celdas_en_llamas()

        # Enemigos alcanzados por el fuego
        for enemigo in self.enemigos:
            if celda_de(enemigo.x, enemigo.y) in llamas:
                enemigo.vivo = False
                self.puntaje += PUNTOS_ENEMIGO
        self.enemigos = [e for e in self.enemigos if e.vivo]

        # Jugador alcanzado por el fuego
        if celda_de(self.jugador_x, self.jugador_y) in llamas:
            self.recibir_dano()

        # Jugador tocado por un enemigo
        rect_j = self.rect_jugador()
        for enemigo in self.enemigos:
            if rect_j.colliderect(enemigo.rect):
                self.recibir_dano()
                break

        # Nivel completado
        if self.estado == "jugando" and not self.enemigos:
            self.estado = "nivel_completo"
            self.estado_desde = pygame.time.get_ticks()

    def actualizar_estado(self):
        ahora = pygame.time.get_ticks()
        if self.estado == "nivel_completo" and ahora - self.estado_desde > 2000:
            if self.nivel < 3:
                self.cargar_nivel(self.nivel + 1)
            else:
                self.estado = "victoria"

    # ---------- Dibujo ----------

    def dibujar_mapa(self):
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x, y = col * TAM, fila * TAM
                pygame.draw.rect(self.pantalla, PISO, (x, y, TAM, TAM))
                pygame.draw.rect(self.pantalla, PISO_CLARO, (x, y, TAM, TAM), 1)

                tipo = self.mapa[fila][col]
                if tipo == PARED:
                    pygame.draw.rect(
                        self.pantalla, PARED_COLOR, (x + 2, y + 2, TAM - 4, TAM - 4)
                    )
                    pygame.draw.rect(
                        self.pantalla, PARED_CLARA, (x + 7, y + 7, TAM - 14, TAM - 14)
                    )
                elif tipo == BLOQUE:
                    pygame.draw.rect(
                        self.pantalla, BLOQUE_COLOR, (x + 5, y + 5, TAM - 10, TAM - 10)
                    )

    def dibujar_bombas(self):
        ahora = pygame.time.get_ticks()
        for bomba in self.bombas:
            x, y = centro_de(bomba.fila, bomba.columna)
            # Late mas rapido cuando esta por explotar
            restante = bomba.detona_en - ahora
            pulso = 1 + 0.12 * math.sin(ahora / (60 if restante < 600 else 150))
            pygame.draw.circle(self.pantalla, NEGRO, (x, y), int(17 * pulso))
            pygame.draw.circle(self.pantalla, ROJO, (x - 5, y - 5), 5)

    def dibujar_explosiones(self):
        for fila, col, _ in self.explosiones:
            x, y = col * TAM, fila * TAM
            pygame.draw.rect(self.pantalla, NARANJA, (x + 3, y + 3, TAM - 6, TAM - 6))
            pygame.draw.rect(self.pantalla, ROJO, (x + 13, y + 13, TAM - 26, TAM - 26))

    def dibujar_enemigos(self):
        for e in self.enemigos:
            x, y = int(e.x), int(e.y)
            pygame.draw.circle(self.pantalla, MORADO, (x, y), RADIO_ENEMIGO)
            pygame.draw.circle(self.pantalla, BLANCO, (x - 5, y - 4), 4)
            pygame.draw.circle(self.pantalla, BLANCO, (x + 5, y - 4), 4)
            pygame.draw.circle(self.pantalla, NEGRO, (x - 5, y - 4), 2)
            pygame.draw.circle(self.pantalla, NEGRO, (x + 5, y - 4), 2)

    def dibujar_jugador(self):
        ahora = pygame.time.get_ticks()
        # Parpadeo mientras es invulnerable
        if ahora < self.invulnerable_hasta and (ahora // 100) % 2 == 0:
            return
        x, y = int(self.jugador_x), int(self.jugador_y)
        pygame.draw.circle(self.pantalla, AMARILLO, (x, y), RADIO_JUGADOR)
        pygame.draw.circle(self.pantalla, NEGRO, (x - 6, y - 5), 3)
        pygame.draw.circle(self.pantalla, NEGRO, (x + 6, y - 5), 3)

    def dibujar_hud(self):
        pygame.draw.rect(self.pantalla, NEGRO, (0, FILAS * TAM, ANCHO, HUD_ALTO))
        linea1 = (
            f"Nivel {self.nivel}   Vidas: {self.vidas}   "
            f"Puntos: {self.puntaje}   Enemigos: {len(self.enemigos)}"
        )
        linea2 = "Flechas/WASD: mover | ESPACIO: bomba | R: reiniciar | 1/2/3: nivel | ESC: salir"
        self.pantalla.blit(self.fuente.render(linea1, True, BLANCO), (10, FILAS * TAM + 6))
        self.pantalla.blit(
            self.fuente_chica.render(linea2, True, (170, 170, 170)),
            (10, FILAS * TAM + 36),
        )

    def dibujar_mensaje(self, texto, subtexto=""):
        velo = pygame.Surface((ANCHO, FILAS * TAM), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 170))
        self.pantalla.blit(velo, (0, 0))
        t = self.fuente_grande.render(texto, True, BLANCO)
        self.pantalla.blit(t, t.get_rect(center=(ANCHO // 2, FILAS * TAM // 2 - 20)))
        if subtexto:
            s = self.fuente.render(subtexto, True, AMARILLO)
            self.pantalla.blit(s, s.get_rect(center=(ANCHO // 2, FILAS * TAM // 2 + 25)))

    def dibujar(self):
        self.pantalla.fill(FONDO)
        self.dibujar_mapa()
        self.dibujar_explosiones()
        self.dibujar_bombas()
        self.dibujar_enemigos()
        self.dibujar_jugador()
        self.dibujar_hud()

        if self.estado == "nivel_completo":
            self.dibujar_mensaje(f"¡Nivel {self.nivel} completado!")
        elif self.estado == "game_over":
            self.dibujar_mensaje("GAME OVER", "Presiona R para jugar de nuevo")
        elif self.estado == "victoria":
            self.dibujar_mensaje(
                "¡GANASTE!", f"Puntaje final: {self.puntaje} - R para jugar de nuevo"
            )

        pygame.display.flip()

    # ---------- Bucle principal ----------

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type != pygame.KEYDOWN:
                continue

            if evento.key == pygame.K_ESCAPE:
                return False
            elif evento.key == pygame.K_SPACE:
                self.colocar_bomba()
            elif evento.key == pygame.K_r:
                if self.estado in ("game_over", "victoria"):
                    self.nueva_partida()
                else:
                    self.cargar_nivel(self.nivel)
            elif evento.key in TECLAS_NIVEL:
                self.cargar_nivel(TECLAS_NIVEL[evento.key])
        return True

    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()

            if self.estado == "jugando":
                self.mover_jugador()
                self.actualizar_enemigos()
            self.actualizar_bombas()
            self.revisar_colisiones()
            self.actualizar_estado()

            self.dibujar()
            self.reloj.tick(FPS)


def main():
    pygame.init()
    Juego().ejecutar()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
