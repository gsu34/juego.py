import pygame
import sys

pygame.init()

# ==========================================
# CONFIGURACIÓN
# ==========================================

TAM = 50
FILAS = 11
COLUMNAS = 15

ANCHO = COLUMNAS * TAM
ALTO = FILAS * TAM + 50

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego estilo Bomberman - 2 Mapas")

reloj = pygame.time.Clock()

# ==========================================
# COLORES
# ==========================================

FONDO = (25, 25, 25)
PISO = (45, 120, 55)
PISO_CLARO = (60, 145, 65)
PARED = (80, 80, 80)
PARED_CLARA = (120, 120, 120)
BLOQUE = (170, 80, 40)
AMARILLO = (240, 210, 40)
NEGRO = (20, 20, 20)
BLANCO = (255, 255, 255)

fuente = pygame.font.SysFont("Arial", 20, True)


# ==========================================
# MAPA 1
# ==========================================

mapa1 = [
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
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]


# ==========================================
# MAPA 2
# ==========================================

mapa2 = [
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
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]


# ==========================================
# VARIABLES DEL JUGADOR
# ==========================================

# Posición en PIXELES
jugador_x = TAM + TAM // 2
jugador_y = TAM + TAM // 2

radio_jugador = 17
velocidad = 4

mapa_actual = 1


# ==========================================
# DIBUJAR MAPA
# ==========================================

def dibujar_mapa(mapa):

    for fila in range(FILAS):

        for columna in range(COLUMNAS):

            x = columna * TAM
            y = fila * TAM

            # Piso
            pygame.draw.rect(
                pantalla,
                PISO,
                (x, y, TAM, TAM)
            )

            # Cuadrícula
            pygame.draw.rect(
                pantalla,
                PISO_CLARO,
                (x, y, TAM, TAM),
                1
            )

            # Pared
            if mapa[fila][columna] == 1:

                pygame.draw.rect(
                    pantalla,
                    PARED,
                    (x + 2, y + 2, TAM - 4, TAM - 4)
                )

                pygame.draw.rect(
                    pantalla,
                    PARED_CLARA,
                    (x + 7, y + 7, TAM - 14, TAM - 14)
                )

            # Bloque destruible
            elif mapa[fila][columna] == 2:

                pygame.draw.rect(
                    pantalla,
                    BLOQUE,
                    (x + 5, y + 5, TAM - 10, TAM - 10)
                )


# ==========================================
# DIBUJAR JUGADOR
# ==========================================

def dibujar_jugador():

    x = int(jugador_x)
    y = int(jugador_y)

    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (x, y),
        radio_jugador
    )

    # Ojos
    pygame.draw.circle(
        pantalla,
        NEGRO,
        (x - 6, y - 5),
        3
    )

    pygame.draw.circle(
        pantalla,
        NEGRO,
        (x + 6, y - 5),
        3
    )


# ==========================================
# COMPROBAR COLISIÓN
# ==========================================

def puede_moverse(x, y):

    mapa = mapa1 if mapa_actual == 1 else mapa2

    # Rectángulo del jugador
    jugador_rect = pygame.Rect(
        int(x - radio_jugador),
        int(y - radio_jugador),
        radio_jugador * 2,
        radio_jugador * 2
    )

    # Revisar todas las paredes y bloques
    for fila in range(FILAS):

        for columna in range(COLUMNAS):

            if mapa[fila][columna] == 1 or mapa[fila][columna] == 2:

                bloque_rect = pygame.Rect(
                    columna * TAM,
                    fila * TAM,
                    TAM,
                    TAM
                )

                if jugador_rect.colliderect(bloque_rect):
                    return False

    return True


# ==========================================
# MOVIMIENTO LIBRE
# ==========================================

def mover_jugador():

    global jugador_x
    global jugador_y

    teclas = pygame.key.get_pressed()

    movimiento_x = 0
    movimiento_y = 0

    # Flechas
    if teclas[pygame.K_LEFT]:
        movimiento_x -= velocidad

    if teclas[pygame.K_RIGHT]:
        movimiento_x += velocidad

    if teclas[pygame.K_UP]:
        movimiento_y -= velocidad

    if teclas[pygame.K_DOWN]:
        movimiento_y += velocidad

    # Movimiento horizontal
    nuevo_x = jugador_x + movimiento_x

    if puede_moverse(nuevo_x, jugador_y):
        jugador_x = nuevo_x

    # Movimiento vertical
    nuevo_y = jugador_y + movimiento_y

    if puede_moverse(jugador_x, nuevo_y):
        jugador_y = nuevo_y


# ==========================================
# CAMBIAR DE MAPA
# ==========================================

def cambiar_mapa(numero):

    global mapa_actual
    global jugador_x
    global jugador_y

    mapa_actual = numero

    # Posición inicial
    jugador_x = TAM + TAM // 2
    jugador_y = TAM + TAM // 2


# ==========================================
# BUCLE PRINCIPAL
# ==========================================

ejecutando = True

while ejecutando:

    # ======================================
    # EVENTOS
    # ======================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:

            # Cambiar mapa
            if evento.key == pygame.K_1:
                cambiar_mapa(1)

            elif evento.key == pygame.K_2:
                cambiar_mapa(2)

            # Salir
            elif evento.key == pygame.K_ESCAPE:
                ejecutando = False

    # ======================================
    # MOVER JUGADOR
    # ======================================

    mover_jugador()

    # ======================================
    # DIBUJAR
    # ======================================

    pantalla.fill(FONDO)

    if mapa_actual == 1:
        dibujar_mapa(mapa1)
    else:
        dibujar_mapa(mapa2)

    dibujar_jugador()

    # Barra inferior
    pygame.draw.rect(
        pantalla,
        NEGRO,
        (0, FILAS * TAM, ANCHO, 50)
    )

    texto = fuente.render(
        f"Mapa {mapa_actual} | Flechas: mover | 1/2: cambiar mapa | ESC: salir",
        True,
        BLANCO
    )

    pantalla.blit(
        texto,
        (15, FILAS * TAM + 14)
    )

    pygame.display.flip()

    reloj.tick(60)


pygame.quit()
sys.exit()
