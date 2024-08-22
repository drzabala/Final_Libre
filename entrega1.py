from simpleai.search import SearchProblem, breadth_first, depth_first, astar, greedy, uniform_cost, limited_depth_first, iterative_limited_depth_first
from simpleai.search.viewers import ConsoleViewer, WebViewer, BaseViewer

import math

class Problem(SearchProblem):
    def is_goal(self, state):
        cantidad_actual = 0
        cantidad_meta = len(state)
        
        for i in state:
            if len(i) == 4 or len(i) == 0:
                if len(set(i)) == 1 or len(set(i)) == 0:
                    cantidad_actual += 1
        
        return cantidad_meta == cantidad_actual

    def actions(self, state):
        acciones = []
        for pos_i, val_i in enumerate(state):
            pos_i +=1
            #El frasco no este lleno con el mismo color
            if not(len(val_i) == 4 and len(set(val_i)) == 1):
                for pos_j, val_j in enumerate(state):
                    pos_j +=1
                    if pos_i != pos_j and len(val_i) != 0:
                        if len(val_j) == 0:
                            acciones.append((pos_i,pos_j))
                        else:
                            if (len(val_j) < 4 and val_i[-1] == val_j[-1]):
                                 acciones.append((pos_i,pos_j))
            
        return acciones
    
    def result(self, state, action):
        posicion_1 = action[0]-1
        posicion_2 = action[1]-1
        origen = list(state[posicion_1])
        destino = list(state[posicion_2])
        estado = {i:valor for i,valor in enumerate(state)}
        ultimo = origen[-1]
        
        if len(destino) == 0:
            siguiente = ultimo
        else:
            siguiente = destino[-1]

        while siguiente == ultimo and len(destino) < 4:
            destino.append(ultimo)
            del origen[-1]
            if len(origen) == 0:
                siguiente = []
            else:
                siguiente = origen[-1]

        estado[posicion_1] = tuple(origen)
        estado[posicion_2] = tuple(destino)     
        
        state = [j for i,j in estado.items()]
            
        return tuple(state)

    def cost(self, state_ini, action, state_fin):
        return 1

    ##Colores ubicados correctamente
    def heuristic(self, state):
        cantidad = 0
        estado = []
        for i in state:
            estado.extend(set(i))
            if len(set(i)) == 1 and len(i) == 4:
                cantidad += 1
                
        return abs(cantidad - len(set(estado)))

def jugar(frascos,dificil):
    global DIFICIL

    DIFICIL = dificil
    
    # jugador, cajas
    INITIAL = frascos

    problema = Problem(INITIAL)

    # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
    if DIFICIL == True:
        metodo = "greedy"
    else:
        metodo = "astar"
      
    if metodo == "breadth_first":        
        result = breadth_first(problema, graph_search=False, viewer=None)
    if metodo == "depth_first":        
        result = depth_first(problema, graph_search=False, viewer=None)
    if metodo == "astar":        
        result = astar(problema, graph_search=True, viewer=None)
    if metodo == "greedy":        
        result = greedy(problema, graph_search=True, viewer=None)
    if metodo == "limited_depth_first":        
        result = limited_depth_first(problema, graph_search=False, viewer=None)
    if metodo == "iterative_limited_depth_first":
        result = iterative_limited_depth_first(problema, graph_search=False, viewer=None)
    if metodo == "uniform_cost":
        result = uniform_cost(problema, graph_search=False, viewer=None)
    
    pasos = []
    for action,state in result.path():
        if action == None:
            pass
        else:
            pasos.append((action))

    return pasos

if __name__ == '__main__':
    pasos = jugar(
        frascos=(
            ("verde", "azul", "rojo", "naranja"),     # frasco 1, notar el orden de los colores
            ("azul", "rosa", "naranja"),              # frasco 2, notar que es de largo 3, queda un espacio vacío
            ("rosa", "celeste", "verde", "verde"),    # frasco 3, notar cómo "verde" se repite 2 veces por los 2 cuartos iguales
            ("rosa", "rojo", "celeste", "celeste"),   # frasco 4
            ("rojo", "azul", "lila"),                 # frasco 5
            ("verde", "naranja", "celeste", "rojo"),  # frasco 6
            ("azul", "naranja", "rosa"),              # frasco 7
            ("lila", "lila", "lila"),                 # frasco 8, notar la repetición de colores para cada cuarto
            (),                                       # frasco 9, notar que una tupla de largo 0 es un frasco vacío
        ),
        dificil=True,
    )
    
##    pasos = jugar(
##        frascos=(
##            ("beige","celeste","verde_oscuro","rosado"),
##            ("verde_oscuro","lila","verde_oscuro","beige"),
##            ("lila","verde","celeste","rojo"),
##            ("verde","rojo","lila","rosado"),
##            ("rosado","celeste","naranja","lila"),
##            ("celeste","naranja","rosado","naranja"),
##            ("azul","naranja","azul","verde"),
##            ("azul","amarillo","rojo","amarillo"),
##            ("beige","verde","azul","amarillo"),
##            ("amarillo","rojo","verde_oscuro","beige"),
##            (),
##            (),
##        ),
##        dificil=True,
##    ) 
