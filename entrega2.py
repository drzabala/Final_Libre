import itertools
import collections
from collections import Counter
from itertools import islice
from simpleai.search import CspProblem, backtrack, min_conflicts, MOST_CONSTRAINED_VARIABLE,LEAST_CONSTRAINING_VALUE,HIGHEST_DEGREE_VARIABLE


##Todos los frascos deben llenarse hasta el tope.
def C1(var,val):
    return len(var) == len(val)

##Debe haber exáctamente 4 segmentos de cada color, ni más ni menos, de lo contrario no se podría resolver el juego.
def C2(var,val):
    cant_color = Counter(val)  
    return all(count == 4 for count in cant_color.values())

##Ningún frasco debe comenzar resuelto. Es decir, ningún frasco debe tener 4 segmentos del mismo color.
def C3 (var,val):          
    return all(len(set(val[i:i+4])) != 1 for i in range(0, len(val), 4))
## Mejora la performance

##    iterador = iter(val)
##    while batch := tuple(islice(iterador, 4)):
##        if len(set(batch)) == 1:
##            return False
##    
##    return True

##Ningún color puede comenzar con todos sus segmentos en el fondo de 4 frascos, porque se trataría de una situación excesivamente difícil de resolver. 
def C4 (var,val):
    return max(Counter(val).values()) < 4

##Si dos frascos son adyacentes, deben compartir al menos un color.
def C5(var,val):
    val_1 = set(val[0:4])
    val_2 = set(val[4:8])
    return bool(val_1 & val_2)

##    return val[0] == val[4] or val[1] == val[5] or val[2] == val[6] or val[3] == val[7]
## Error de interpretación entre los frascos adyacentes y sus posiciones.

## Si dos frascos son adyacentes, no pueden tener más de 6 colores diferentes entre ambos,para evitar situaciones demasiado complejas.
def C6(var,val):
    return len(set(val)) <= 6

##No puede haber dos frascos exáctamente iguales.
def C7(var,val):
    return not(val[0] == val[4] and val[1] == val[5] and val[2] == val[6] and val[3] == val[7])


def armar_nivel(colores, contenidos_parciales):
    
    global variables
    global restricciones
    global contenidos
    global cant_colores
    global dic_colores
    
    restricciones = []
    valores = colores
    cant_colores = colores
    
    #Cantidad de frascos de acuerdo a la cantidad de colores diferenctes con capacidad de 4 segmentos
    variables = list((i,j) for i,valor in enumerate(colores)for j in range(4))
    
    contenidos = {key:list(value) for key,value in enumerate(contenidos_parciales)}

    dic_colores = {valor: 4 for valor in colores}
    
    ##Colores en cada segmento del frasco
    dominios = {a: valores for a in variables}

    ##Segmentos completos
    for keys,value in contenidos.items():
        valor = list(value)
        for j,color in enumerate(valor):
            dominios[keys,j] = [color]

    ##Todos los frascos tienen capacidad de 4 segmentos.
    frasco = {i: [(i, j) for j in range(4)] for i in range(len(colores))}

    restricciones.append((variables,C1))
    restricciones.append((variables,C2))
    restricciones.append((variables,C3))
    
    var = [(i,0) for i in frasco]
    restricciones.append((var,C4))
    
    for var_pair in itertools.combinations(frasco.values(),2):
        adyacentes = []
        adyacentes = var_pair[0] + var_pair[1]
        restricciones.append((adyacentes,C7))
        i,j = var_pair[0][0]
        x,y = var_pair[1][0] 
        if abs(i-x) == 1:
            restricciones.append((adyacentes,C5))
            restricciones.append((adyacentes,C6))

    problema = CspProblem(variables, dominios, restricciones)

    result = []
    metodo_busqueda = "min_conflicts"
    iteraciones = None
    
    if metodo_busqueda == "backtrack":
        result = backtrack(problema,
                              variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                              value_heuristic=LEAST_CONSTRAINING_VALUE,
                              inference=True)
    
    if metodo_busqueda == "min_conflicts":
       	result = min_conflicts(problema, iterations_limit=iteraciones)

    frascos = [tuple(result[i, j] for j in range(4)) for i in range(len(cant_colores))]

    return frascos
        

if __name__ == '__main__':
    frascos = armar_nivel(
        colores=["rojo", "verde", "azul", "amarillo"],  # 4 colores, por lo que deberemos armar 4 frascos
        contenidos_parciales=[
            ("verde", "azul", "rojo", "rojo"),          # el frasco 1 ya está completo
            ("verde", "rojo"),                          # el frasco 2 ya tiene dos segmentos completos, hay que rellenar el resto
                                                        # los frascos 3 y 4 no vinieron definidos, por lo que tenemos más libertad en ellos
        ],
    )

##    frascos = armar_nivel(
##        
##        colores=["rojo","verde","azul","celeste","lila","naranja","amarillo","verde_oscuro"],  
##        contenidos_parciales=[
##            ("rojo","verde_oscuro","verde_oscuro","verde_oscuro",),          
##            ("celeste","azul","azul",),                          
##            ("naranja","verde_oscuro","verde","azul",),
##            ("amarillo","amarillo",),
##            ("celeste",),  
##        ],
##    )
    

