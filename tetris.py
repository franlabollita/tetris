import random

ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

PIEZAS = (
    ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo
    ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag)
    ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z)
    ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea)
    ((0, 0), (0, 1), (0, 2), (1, 2)), # L
    ((0, 0), (1, 0), (2, 0), (2, 1)), # -L
    ((0, 0), (1, 0), (2, 0), (1, 1)), # T
)

class Nodo:
    def __init__(self, dato):
        self.prox = None
        self.dato = dato


class ListaEnlazadaCircular:
    def __init__(self):
        self.prim = None
        self.length = 0

    def append(self, elemento):
        nuevo = Nodo(elemento)

        if not self.prim:
            self.prim = nuevo
            nuevo.prox = self.prim
            return

        actual = self.prim
        while actual.prox != self.prim:
            actual = actual.prox

        actual.prox = nuevo
        nuevo.prox = self.prim
        self.length += 1

    def __len__(self):
        return self.length


class ListaIterador:
    def __init__(self, list):
        self.list = list
        self.anterior = None
        self.actual = list.prim

    def avanzar(self):
        self.actual = self.actual.prox

    def dato_actual(self):
        return self.actual.dato



def generar_grilla():
    """
    Genera una grilla de juego de tamaño 9 x 18.
    [(0,0), (1,0), (2,0), ... , (8, 17)]
    """

    grilla_de_juego = []

    for y in range(ALTO_JUEGO):
        for x in range(ANCHO_JUEGO):
            grilla_de_juego.append((x,y))

    return grilla_de_juego

def es_moviemiento_valido(juego):
    """
    Verifica que se puede bajar la pieza una fila.
    """
    _, pieza, superficie = juego

    for fragmento_x, fragmento_y in pieza:
        if hay_superficie(juego, fragmento_x, fragmento_y + 1) or fragmento_y == 17:
            return False

    return True

def fila_esta_completa(juego, fila):
    """
    Se fija se la fila esta completa.
    """

    contador = 0

    for x in range(ANCHO_JUEGO):
        if hay_superficie(juego, x, fila) == True:
            contador += 1

        if contador == 9:
            return True

    return False

def remover_fila(superficie, fila_y):
    """
    Elimina la fila de la superficie si fila_esta_completa == True.
    """

    superficie_nueva = []

    for posicion in superficie:
        if posicion[1] != fila_y:
            superficie_nueva.append(posicion)

    superficie_nueva = tuple(superficie_nueva)

    return superficie_nueva

def bajar_superficie(superficie, fila_y):
    """
    Baja las superficie que esta arriba de la fila recien eliminada.
    """
    superficie_nueva = []

    for posicion_x, posicion_y in superficie:
        if posicion_y < fila_y:
            superficie_nueva.append((posicion_x, posicion_y + 1))
        else:
            superficie_nueva.append((posicion_x, posicion_y))

    return superficie_nueva

def convertir_a_lecirc(linea):

    counter_1 = 0
    counter_2 = 0
    lista_enlazada = ListaEnlazadaCircular() #linea de pieza.txt en un nuevo formato
    lista_menor = [] #(0,1)
    lista_mayor = [] #((0,1), (0,2), (1,1), (2,1))
    linea = linea.split(' ')

    for pos in linea:
        lista_menor.append(int(pos))
        counter_1 += 1

        if (counter_1 % 2) == 0:
            lista_menor = tuple(lista_menor)
            lista_mayor.append(lista_menor)
            lista_menor = []
            counter_1 = 0
            counter_2 +=1

            if counter_2 % 4 == 0:
                lista_mayor = sorted(lista_mayor)
                lista_enlazada.append(lista_mayor)
                lista_mayor = []
                counter_2 = 0

    return lista_enlazada

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """

    if pieza != None:
        return PIEZAS[pieza]

    return random.choice(PIEZAS)

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y).
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """

    pieza_nueva = []

    for fragmento_x, fragmento_y in pieza:
        pieza_nueva.append((fragmento_x + dx, fragmento_y + dy))

    return tuple(pieza_nueva)

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de
    sus posiciones superiores es 0 (cero).
    """

    grilla = generar_grilla()

    pieza = trasladar_pieza(pieza_inicial, ANCHO_JUEGO // 2, 0)

    superficie = []

    return grilla, pieza, superficie

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """

    grilla, _, _ = juego

    return int(len(grilla) / ALTO_JUEGO), int(len(grilla) / ANCHO_JUEGO)

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina
    superior izquierda de la grilla.
    """

    _, pieza, _ = juego

    return pieza

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.

    La coordenada (0, 0) se refiere a la posición que está en la esquina
    superior izquierda de la grilla.
    """

    _, _, superficie = juego

    if any((x,y) == posicion for posicion in superficie):
        return True

    return False

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """

    grilla, pieza, superficie = juego

    for fragmento_x, fragmento_y in pieza:
        if fragmento_x == 0 and direccion == IZQUIERDA or fragmento_x == ANCHO_JUEGO - 1 and direccion == DERECHA:
            return juego

    pieza = trasladar_pieza(pieza, direccion, 0)

    return grilla, pieza, superficie

def rotar(juego):

    grilla, pieza, superficie = juego
    primer_posicion, _, _, _ = pieza

    pieza_en_origen = trasladar_pieza(pieza, int(- primer_posicion[0]), int(- primer_posicion[1]))
    pieza_en_origen = tuple(sorted(pieza_en_origen))

    with open('piezas.txt') as rotaciones:
        for linea in rotaciones:
            linea = linea.strip('\n#CuboZLS-LIT ,')
            linea = linea.replace(';', ' ').replace(',', ' ')
            lista_enlazada = convertir_a_lecirc(linea)
            it = ListaIterador(lista_enlazada)

            for i in range(len(lista_enlazada) + 1):
                if pieza_en_origen == tuple(it.actual.dato):
                    it.avanzar()
                    dato = it.dato_actual()
                    pieza_en_origen = tuple(it.actual.dato)
                    break

                it.avanzar()

            if pieza_en_origen == tuple(it.actual.dato):
                break

    pieza_en_origen = trasladar_pieza(pieza_en_origen, int(primer_posicion[0]), int(primer_posicion[1]))

    return grilla, pieza_en_origen, superficie

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.

    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).

    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar
    completamente en la grilla para poder seguir jugando, si al intentar
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada,
    se debe devolver el mismo juego que se recibió.
    """
    if terminado(juego):
        return juego, False

    grilla, pieza, superficie = juego

    pieza_nueva = trasladar_pieza(pieza, 0, 1)

    if es_moviemiento_valido(juego):
        juego_nuevo = grilla, pieza_nueva, superficie
        return juego_nuevo, False

    else:
        for fragmento in pieza:
            superficie.append(fragmento)

    for fila_y in range(ALTO_JUEGO):
        if fila_esta_completa(juego, fila_y):
            superficie = remover_fila(superficie, fila_y)
            superficie = bajar_superficie(superficie, fila_y)

    pieza_nueva = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)

    juego_nuevo = grilla, pieza_nueva, superficie
    return juego_nuevo, True

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """

    _, pieza, superficie = juego

    if any(hay_superficie(juego, x, y) for x, y in pieza):
        return True

    return False
