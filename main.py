import tetris
import gamelib
import interfaz

ESPERA_DESCENDER = 16

def main():
    pieza_inicial = tetris.generar_pieza(None)
    juego = tetris.crear_juego(pieza_inicial)
    gamelib.resize(interfaz.PANTALLA, interfaz.PANTALLA)

    timer_bajar = ESPERA_DESCENDER
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        interfaz.mostrar_interfaz(juego)
        gamelib.draw_end()

        for event in gamelib.get_events():
            if not event:
                break
            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key

              # Actualizar el juego, según la tecla presionada
                with open(r'teclas.txt') as teclas:
                    for linea in teclas:
                        linea = linea.strip('\n')
                        linea = linea.split(' ')
                        if linea[0] == tecla and linea[2] == 'IZQUIERDA':
                            juego = tetris.mover(juego, tetris.IZQUIERDA)

                        elif linea[0] == tecla and linea[2] == 'DERECHA':
                            juego = tetris.mover(juego, tetris.DERECHA)

                        elif linea[0] == tecla and linea[2] == 'DESCENDER':
                            juego, cambiar_pieza = tetris.avanzar(juego, siguente)

                        elif linea[0] == tecla and linea[2] == 'ROTAR':
                            juego = tetris.rotar(juego)

                        elif linea[0] == tecla and linea[2] == 'SALIR':
                            exit()


        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            siguente = tetris.generar_pieza(None)
            juego, cambiar_pieza = tetris.avanzar(juego, siguente)

        if tetris.terminado(juego) == True:
            #break
            interfaz.mostar_puntajes(juego)

gamelib.init(main)
