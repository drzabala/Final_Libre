from simpleai.search import SearchProblem, breadth_first, depth_first, astar, greedy, uniform_cost, limited_depth_first, iterative_limited_depth_first
from simpleai.search.viewers import ConsoleViewer, WebViewer, BaseViewer

import math

CONECTADAS = {'sunchales':[('lehmann',32)],'lehmann':[('rafaela',8),('sunchales',32)],'rafaela':[('lehmann',8),('susana',10),('esperanza',70)], 
              'susana':[('rafaela',10),('angelica',25)],'angelica':[('san_vicente',18),('susana',25),('sc_de_saguier',60),('santo_tome',85)],
              'san_vicente':[('angelica',18)],'sc_de_saguier':[('angelica',60)],'santo_tome':[('santa_fe',5),('sauce_viejo',15),('angelica',85)],
              'sauce_viejo':[('santo_tome',15)],'santa_fe':[('santo_tome',5),('recreo',10)],'recreo':[('santa_fe',10),('esperanza',20)],
              'esperanza':[('recreo',20),('rafaela',70)]} 

CONSUMO = 0.01 #consumo de combustible es de 1 litro cada 100km recorridos

#sedes de la empresa    
SEDES = {'santa_fe','rafaela'}

CAMIONES = {}

ENVIOS = {}

class Problem(SearchProblem):
    def is_goal(self, state):
        camiones,pendientes = state
        if len(pendientes) != 0:
            return False
        else:
            for camion in camiones:
                idcamion, ciudad, consumo, paquete = camion
                if (len(paquete) > 0):
                    for idpaquete in paquete:
                        if ENVIOS[idpaquete][1] != ciudad:
                            return False
                            
                if ciudad not in SEDES:
                    return False
            
        return True

    def actions(self, state):
        acciones = []
        camiones,pendientes = state
        for camion in camiones:
            idcamion, ciudad, consumo, paquete = camion
            for destino in CONECTADAS[ciudad]:
                nuevo_consumo = round((destino[1]*CONSUMO),2)
                if consumo >= nuevo_consumo:
                    acciones.append((idcamion,destino[0],nuevo_consumo))
                    
        return acciones
    
    def result(self, state, action):
        camiones,pendientes = state
        camiones = list(camiones)
        pendientes = list(pendientes)

        sitio =  {i[0]:[i[1],i[2],i[3]] for i in camiones}

        ciudad, consumo, paquete = sitio[action[0]]
        paquete = list(paquete)
      
        for idpaquete in pendientes:
            if ciudad == ENVIOS[idpaquete][0]:                    
                paquete.append(idpaquete) 

        pendientes = [idpaquete for idpaquete in pendientes if not idpaquete in paquete]

        if len(paquete) != 0:
            paquete = [idpaquete for idpaquete in paquete if not ciudad == ENVIOS[idpaquete][1]]

        ciudad = action[1]  
        
        if ciudad in SEDES:
            consumo = CAMIONES[action[0]][1]
        else:
            consumo = round((consumo - action[2]),2)   

        sitio[action[0]] = tuple((ciudad, consumo, tuple(paquete)))
        camiones = [(i,j[0],j[1],j[2]) for i,j in sitio.items()] 
        return tuple(camiones), tuple(pendientes)

    def cost(self, state1, action, state2):
        return action[2]
    
    def heuristic(self, state):
        camiones,pendientes = state
        distancia = []
        if pendientes:
            for idpaquete in pendientes:
                ciudades = []
                for ciudad in CONECTADAS[ENVIOS[idpaquete][0]]:
                    ciudades.append(ciudad[1])
                distancia.append(min(ciudades))
            return round((max(distancia) * CONSUMO),2)
        return 0

def planear_camiones(metodo, camiones, paquetes):
    transporte = []
    for camion in camiones:
        transporte.append((camion[0],camion[1], camion[2],()))
        CAMIONES[camion[0]] = (camion[1],camion[2])
    
    pendientes = []
    for paquete in paquetes:
        pendientes.append(paquete[0])
        ENVIOS[paquete[0]] = (paquete[1],paquete[2])

    # id, ciudad, consumo, paquete entregado
    INITIAL = (tuple(transporte), tuple(pendientes))

    problema = Problem(INITIAL)

    if metodo == 'breadth_first':        
        result = breadth_first(problema, graph_search=False, viewer=None)
    if metodo == 'depth_first':        
        result = depth_first(problema, graph_search=False, viewer=None)
    if metodo == 'astar':        
        result = astar(problema, graph_search=False, viewer=None)
    if metodo == 'greedy':        
        result = greedy(problema, graph_search=False, viewer=None)
    if metodo == 'limited_depth_first':        
        result = limited_depth_first(problema, graph_search=False, viewer=None)
    if metodo == 'iterative_limited_depth_first':
        result = iterative_limited_depth_first(problema, graph_search=False, viewer=None)
    if metodo == 'uniform_cost':
        result = uniform_cost(problema, graph_search=False, viewer=None)
    
    itinerario = []
    for action,state in result.path():
        if action == None:
            pass
        else:            
            camion = action[0]
            camiones,pendientes = state
            sitio =  {i[0]:[i[1],i[2],i[3]] for i in camiones}
            ciudad = sitio[camion][0]
            consumo = action[2]
            paquete = sitio[camion][2]
            itinerario.append((camion,ciudad,consumo,list(paquete)))

    return itinerario

if __name__ == '__main__':   
    itinerario = planear_camiones(
      # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
      metodo="breadth_first",
      camiones=[
        # id, ciudad de origen, y capacidad de combustible máxima (litros)
        ('c1', 'rafaela', 1.5),
##        ('c2', 'rafaela', 2),
##        ('c3', 'santa_fe', 2),
      ],
      paquetes=[
        # id, ciudad de origen, y ciudad de destino
        ('p1', 'rafaela', 'angelica'),
##        ('p2', 'rafaela', 'santa_fe'),
##        ('p3', 'esperanza', 'susana'),
##        ('p4', 'recreo', 'san_vicente'),
      ],
    ) 
