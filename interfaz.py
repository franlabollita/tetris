import tetris
import gamelib
#import main

#Tamaños constantes
PANTALLA = 800
BORDE_Y = 40
BORDE_X = 220
CUADRADO = 40


def dibujar_pieza(pieza):

    pieza_nueva = []
    for x,y in pieza:
        x_nueva = (x * 40) + 240
        y_nueva = (y * 40) + 60
        pieza_nueva.append((x_nueva,y_nueva))

    return pieza_nueva

def dibujar_superficie(superficie):

    superficie_nueva = []
    for x,y in superficie:
        x_nueva = (x * 40) + 240
        y_nueva = (y * 40) + 60
        superficie_nueva.append((x_nueva,y_nueva))

    return superficie_nueva


def mostrar_interfaz(juego):

    _, pieza, superficie = juego

    for extremo_variable in range(BORDE_X, PANTALLA+1 - BORDE_X, CUADRADO):
        gamelib.draw_line(extremo_variable, BORDE_Y, extremo_variable, PANTALLA - BORDE_Y, fill = 'white', width = 2)
    for extremo_variable in range(BORDE_Y, PANTALLA+1 - BORDE_Y, CUADRADO):
        gamelib.draw_line(BORDE_X, extremo_variable, PANTALLA - BORDE_X, extremo_variable, fill = "white", width = 2)


    pieza_interfaz = dibujar_pieza(pieza)
    for x,y in pieza_interfaz:
        gamelib.draw_text('X', x, y, fill='red', size = 15)

    superficie_interfaz = dibujar_superficie(superficie)
    for x, y in superficie_interfaz:
        gamelib.draw_text('O', x, y, fill='red', size = 15)

    if tetris.terminado(juego) == True:
        gamelib.draw_end()

def mostar_puntajes(juego):
    #while gamelib.loop(fps=1):
    gamelib.draw_text('GAME OVER', PANTALLA / 2, BORDE_Y * 1.5, fill = 'Red', size = 30)
        #gamelib.draw_text('GAME OVER', PANTALLA / 2, BORDE_Y * 1.5, fill = 'White', size = 30)
