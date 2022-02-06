
# coding: utf-8

# # Clase Práctica
# 
# ## Juego de Tronos
# 

# ## Problema de ejemplo
# 
# Tyrion Lannister se está quedando sin bebidas alcohólicas, entonces haciendo alusión a su célebre frase, “Eso se lo que hago, bebo y sé cosas” quiere hacer su propia bebida. Para esto cuenta con 30 libras de uvas, 40 libras de cebada y con 30 libras de levadura. Él conoce que para crear un litro de cerveza necesita 1 libra de cebada y 0.5 libras de levadura, mientras que para crear vino los requisitos son 2 libras de uva y 1 libra de levadura. Conociendo que la cerveza tiene un nivel de alcohol de 2% y el vino 4%, ¿cuál es la mejor manera de distribuir los recursos para crear la mayor cantidad de alcohol?
# 
# Resutados:
# - Cerveza: 30
# - Uva: 15
# - Máxima cantidad de alcohol: 1.2

# In[1]:


import numpy as np
import scipy.optimize._linprog as lin

# Función de costo
# Multiplicada por -1 para que scipy maximice
c = np.array([
    0.02, # Alcohol por litro de cerveza
    0.04 # Alcohol por litro de vino
]) * -1

# Restricciones de desigualdad
Ab = np.array([
    [ 0, 2], # Uva
    [ 1, 0], # Cebada
    [ 0.5, 1], # Levadura
    [-1,   0], # Bound inferior de cantidad de cerveza
    [ 0,  -1], # Bound inferior de cantidad de vino
])

b = np.array([
    30, # Cantidad de uva
    40, # Cantidad de cebada
    30, # Cantidad de levadura
    0, # Bound inferior de cantidad de cerveza
    0, # Bound inferior de cantidad de vino
])

print(lin.linprog(c, Ab, b)) # El resultado se multiplica por -1.


# ## Infratructura

# In[11]:


from typing import Callable, List, Optional, Tuple
from gekko import GEKKO
import numpy as np
import gekko


def unfold_list(obj):
    try:
        if isinstance(obj, gekko.gk_variable.GKVariable):
            raise TypeError
        if isinstance(obj, tuple):
            yield from obj
        else:
            for x in obj:
                yield from unfold_list(x)
    except TypeError:
        yield obj

def asignar_puntuacion(opt1, opt2, maxim=False, verbose=True):
    punto_probl_eq1 = 0
    punto_probl_eq2 = 0

    if opt1 is None and opt2 is not None:
        print("La solución dada por el equipo 1 no es factible")
        print(f"La solución dada por el equipo 2 es factible: {opt2}")
        print(f"El equipo 2 gana 1 punto!!")
        punto_probl_eq2 += 1
    elif opt1 is not None and opt2 is None:
        print(f"La solución dada por el equipo 1 es factible: {opt1}")
        print("La solución dada por el equipo 2 no es factible")
        print(f"El equipo 1 gana 1 punto!!")
        punto_probl_eq1 += 1
    elif opt1 is None and opt2 is None:
        print(f"Ambos equipos dieron soluciones no factibles")
        print(f"Los equipos no ganan puntos :(")
    elif opt1 == opt2:
        print(f"Ambos equipos dieron soluciones factibles e iguales: {opt1}")
        print(f"Los equipos 1 y 2 ganan 1 punto cada uno!!")
        punto_probl_eq2 += 1
        punto_probl_eq1 += 1
    elif maxim:
        if opt1 > opt2: # Maximizando
            print(f"El equipo 1 obtuvo mejor resultado maximizando que el equipo 2: {opt1} > {opt2}")
            print(f"El equipo 1 gana 1 punto!!")
            punto_probl_eq1 += 1
        else:
            print(f"El equipo 2 obtuvo mejor resultado maximizando que el equipo 1: {opt1} < {opt2}")
            print(f"El equipo 2 gana 1 punto!!")
            punto_probl_eq2 += 1
    else:
        if opt1 < opt2: # Minimizando
            print(f"El equipo 1 obtuvo mejor resultado minimizando que el equipo 2: {opt1} < {opt2}")
            print(f"El equipo 1 gana 1 punto!!")
            punto_probl_eq1 += 1
        else:
            print(f"El equipo 2 obtuvo mejor resultado minimizando que el equipo 1: {opt1} > {opt2}")
            print(f"El equipo 2 gana 1 punto!!")
            punto_probl_eq2 += 1
            
    return punto_probl_eq1, punto_probl_eq2

def comparar_problemas(problema, arg_eq1, arg_eq2, maxim=False, unfold=False):
    print("Equipo 1:")
    print()
    probl_eq1_opt, _, opt_probl, vector_opt_probl = problema.compare(arg_eq1, unfold=unfold)
    print()

    print("Equipo 2:")
    print()
    probl_eq2_opt, _, _, _ = problema.compare(arg_eq2, unfold=unfold)
    print()

    #Puntuacion de los equipos en el ejercicio 1
    punto_probl_eq1, punto_probl_eq2 = asignar_puntuacion(probl_eq1_opt, probl_eq2_opt, maxim=maxim)
    
    return probl_eq1_opt, probl_eq2_opt, opt_probl, vector_opt_probl, punto_probl_eq1, punto_probl_eq2

class ProblemManager:
    def __init__(self, solver:Callable[[Optional[float],], float], args_fetcher:Callable[[], Tuple[float,]]) -> None:
        self.solver = solver
        self.args_fetcher = args_fetcher

    def solve(self, *args):
        max = self.solver(*args)
        return max

    def compare(self, user_args=None, unfold=False):
        try:
            if unfold:
                opt, vector_variables = self.solve(None, *user_args[1:])
            else:
                opt, vector_variables = self.solve()
        except:
            print("El problema no es factible.")
            return None, None, None, None

        vector_variables = [x for x in unfold_list(vector_variables)]

        print("Asignación óptima:")
        for v in vector_variables:
            print(v.name, ":", v.value)
        
        if user_args is None:
            user_args = self.args_fetcher()

        user_args = [x for x in unfold_list(user_args)]

        try:        
            user_opt, _ = self.solve(*user_args)
            user_args = [x for x in unfold_list(user_args)]
            
            print('El valor alcanzado con su asiganción es de', user_opt)
            if opt > user_opt * 4:
                print('Tu solución es bastante mala con respecto al valor óptimo, es menos que la cuarta parte. El valor óptimo era de', opt)
            elif opt>user_opt * 2:
                print('Tu solución es mala con respecto a valor óptimo, es menos de la mitad. El valor óptimo era de', opt)
            elif opt>user_opt * 1.5:
                print('Tu solución es bastante buena, el valor óptimo era de', opt)
            elif opt < user_opt + 5:
                print('Tu solución es óptima')
            else:
                print('Tu solución es muy buena,casi en lo óptimo, pero el valor óptimo posible alcanzado es', opt)
            return user_opt, user_args, opt, vector_variables 
        except Exception as ex:
            print('Su solución no es factible. El valor óptimo es', opt)
            return None, None, None, None


# # Problemas

# In[3]:


# Puntos ganados por el equipo 1
puntos_equipo_1 = []

# Puntos ganados por el equipo 2
puntos_equipo_2 = []


# ## 1. Casa Mormont
# 
# En la preparación de la batalla se necesitan armas para que los guerreros puedan defenderse del ejército de caminantes blancos. Para esto se tienen escasos recursos, así que hay que usarlos sabiamente. Entre las reservas y el trabajo se logró reunir:
# 
# - 300 unidades de hierro
# - 400 unidades de madera
# - 400 unidades de cuero
# 
# Los herreros y artesanos nos brindan una tabla que muestra la cantidad de materia prima necesaria para construir cada arma y el daño que reporta cada una.
# 
# | Arma      | Hierro | Madera | Cuero | Daño |
# | --------- | ------ | ------ | ----- | ---- |
# | Espada    | 10     | 2      | 4     | 15   |
# | Arco      | 2      | 10     | 5     | 10   |
# | Catapulta | 30     | 100    | 50    | 80   |
# 
# 1. Ayude a darle el mejor uso a estos recursos, diciéndoles a los jefes de la casa la cantidad de espadas, arcos y catapultas que necesitan construir para maximizar el daño que realizan.
# 2. Se quiere tener modelo que generalice el problema anterior en términos de la cantidad de tipos de materiales y cantidad de tipos de armas. Proponga un modelo que haga esta generalización.

# In[4]:


# Ejercicio 1

def mormont_house_solve(swords=None,bows=None,catapults=None):
    #1 Mormont House
    #resourses
    iron = 300
    wood = 400
    leather = 400
    
    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP
    
    test = True if  swords is not None and bows is not None and catapults is not None else False
    
    #variables
    sword = modelo.Var (lb = 0, integer = True ,name='sword' )
    bow = modelo.Var (lb = 0, integer = True ,name='bow')
    catapult = modelo.Var (lb = 0, integer = True ,name='catapult')

    #restricciones 
    modelo.Equation(10*sword + 2*bow + 80*catapult <= iron)
    modelo.Equation(2*sword + 10*bow + 100*catapult <= wood)
    modelo.Equation(15*sword + 10*bow + 50*catapult <= leather)
    
    #test
    if test:
        modelo.Equation(sword==swords)
        modelo.Equation(bow==bows)
        modelo.Equation(catapult==catapults)
    

    #funcion objetivo
    def f(x,y,z):
        return 15*x + 10*y + 80*z

    modelo.Maximize(f(sword,bow,catapult))

    modelo.solve(disp=False)
    
    return -modelo.options.OBJFCNVAL, [sword, bow, catapult]

def mormont_house_input():
    print('Según tus habilidades como estratega militar que cantidad de cada arma se debería construir')
    swords =int(input('Espadas:'))
    bows =int(input('Arcos:'))
    catapults =int(input('Catapultas:'))
    return [swords, bows, catapults]

# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_1_equipo_1 = [
    0, # Espadas
    0, # Arcos
    0, # Catapultas
]

argumentos_problema_1_equipo_2 = [
    0, # Espadas
    0, # Arcos
    0, # Catapultas
]

problema_1 = ProblemManager(mormont_house_solve, mormont_house_input)

probl1_eq1_opt, probl1_eq2_opt, opt_probl1, vector_opt_probl1, punto_probl1_eq1, punto_probl1_eq2 =     comparar_problemas(problema_1, argumentos_problema_1_equipo_1, argumentos_problema_1_equipo_2, maxim=True)

# Agregar puntuación
puntos_equipo_1.append(punto_probl1_eq1)
puntos_equipo_2.append(punto_probl1_eq2)


# ## 2. Casa Greyjoy
# 
# Un importante recurso para la contienda es la comida. Los soldados y la mano de obra son muchos y cada uno necesita ser alimentado para poder trabajar y luchar contra los temibles caminantes blancos. Esta responsabilidad cae sobre Casa Greyjoy. Los cálculos estiman que para hacer una comida para una persona se necesitan:
# 
# - 60 gramos de proteína
# - 120 gramos de carbohidratos
# - 20 gramos de aceite
# - 1.5 litros de agua
# 
# Para satisfacer esta demanda se tienen un conjunto de alimentos y ganado a disposición, cada uno aportando diferentes cantidades de nutrientes.
# 
# | Recurso       | Proteína | Carbohidratos | Aceite | Costo |
# | ------------- | -------- | ------------- | ------ | ----- |
# | Trigo         | 10       | 40            | 20     | 10    |
# | Ganado vacuno | 100      | 10            | 50     | 60    |
# | Encurtidos    | 20       | 30            | 10     | 30    |
# | Agua          | -        | -             | -      | 5     |
# 
# 1. Sabiendo que se espera un ejército de alrededor 10 000 personas, proponga a los jefes de la casa una manera de cumplir con los requerimientos con el menor costo posible.
# 2. Se quiere tener modelo que generalice el problema anterior en términos de la cantidad de tipos de nutrientes y cantidad de tipos de recursos. Proponga un modelo que haga esta generalización.

# In[5]:


# Ejercicio 2
def greyjoy_house_solve(trigo=None, ganado=None, encurtidos=None, agua=None):
    
    # Datos
    total_ppl = 1000
    proteinas = 60 * total_ppl
    carbohidratos = 120 * total_ppl
    aceite = 20 * total_ppl
    agua = 1.5 * total_ppl

    totals = [proteinas, carbohidratos, aceite]

    nutrientes_costo = [
        [10, 40, 20, 10],
        [100, 10, 50, 60],
        [20, 30, 10, 30],
        [0, 0, 0, 5]
    ]

    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1
    modelo.options.LINEAR = 1

    test = True if not trigo is None and not encurtidos is None and not ganado is None and not agua is None else False
    
    # Variables de decisión
    _trigo = modelo.Var(lb=0, integer=True, name='trigo')
    _ganado = modelo.Var(lb=0, integer=True, name='ganado')
    _encurtidos = modelo.Var(lb=0, integer=True, name='encurtidos')
    _agua = modelo.Var(lb=0, integer=True, name='agua')

    e_vars = [_trigo, _ganado, _encurtidos, _agua]

    # Restricciones de demanda
    eq = 0
    for i in range(3):
        for j in range(3):
            eq += e_vars[j] * nutrientes_costo[j][i]

        modelo.Equation(eq >= totals[i])
        eq = 0

    modelo.Equation(_agua >= agua)

    if test:
        modelo.Equation(_trigo==trigo)
        modelo.Equation(_encurtidos==encurtidos)
        modelo.Equation(_ganado==ganado)
        modelo.Equation(_agua==agua)

    def f(x, y, z, w):
        return x * nutrientes_costo[0][3] + y * nutrientes_costo[1][3] + z * nutrientes_costo[2][3] + w * nutrientes_costo[3][3]

    # Función objetivo
    modelo.Minimize(f(_trigo, _ganado, _encurtidos, _agua))

    modelo.solve(disp=False)

    return modelo.options.OBJFCNVAL, e_vars

def greyjoy_house_input():
    print('Segun tu habilidad como gastronomo, que cantidad de alimentos se deberia producir')
    trigo = int(input('Trigo:'))
    ganado = int(input('Ganado:'))
    encurtidos = int(input('Encurtidos:'))
    agua = int(input('Agua:'))
    return [trigo, ganado, encurtidos, agua]

# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_2_equipo_1 = [
    0, # Trigo
    0, # Ganado
    0, # Encurtido
    0, # Agua
]

argumentos_problema_2_equipo_2 = [
    0, # Trigo
    0, # Ganado
    0, # Encurtido
    0, # Agua
]

problema_2 = ProblemManager(greyjoy_house_solve, greyjoy_house_input)

probl2_eq1_opt, probl2_eq2_opt, opt_probl2, vector_opt_probl2, punto_probl2_eq1, punto_probl2_eq2 =     comparar_problemas(problema_2, argumentos_problema_2_equipo_1, argumentos_problema_2_equipo_2)

# Agregar puntuación
puntos_equipo_1.append(punto_probl2_eq1)
puntos_equipo_2.append(punto_probl2_eq2)


# ## 3. Casa Targaryen
# 
# El fuego valiryo posee un gran poder ofensivo, este fuego verde arde incluso en el agua y es incapaz de extinguirlo una vez se prende, solo terminando de arder cuando se consume completamente. Las armas imbuidas en este elemento presentan un poder ofensivo superior y además pueden ser usado como bombas incendiarias, así que la producción de este es indispensable. Para fabricar el fuego valiryo se necesita mezclar ciertos ingredientes cuyos nombres no fueron revelados, pero, se conoce la proporción de estos en diferentes recursos naturales:
# 
# | Recurso           | Ingrediente 1 | Ingrediente 2 | Ingrediente 3 | Costo |
# | ----------------- | ------------- | ------------- | ------------- | ----- |
# | Aceite de ballena | 40%           | 10%           | 30%           | 40    |
# | Polvo de dragón   | 10%           | 5%            | 50%           | 70    |
# | Pelo de caballo   | 15%           | 35%           | 5%            | 30    |
# 
# Los alquimistas tienen destilados ya:
# 
# - Ingrediente 1: 15 litros
# - Ingrediente 2: 30 litros
# - Ingrediente 3: 10 litros
# 
# El porcentaje del fuego valiryo se revela que es:
# 
# - Ingrediente 1: 20%
# - Ingrediente 2: 35%
# - Ingrediente 3: 45%
# 
# El fuego valiryo está conformado por un 30% de Ingrediente 1, 20% de Ingrediente 2 y 50% de Ingrediente 3. Como dato adicional los alquimistas necesitan procesar el residuo de los recursos para conservar la pureza del fuego, para esto se tiene un costo extra de 5 por cada unidad de material de desecho. Se cuenta como residuo las cantidades que no son ingredientes del fuego que sale del procesamiento de los recursos, por ejemplo el uno de una unidad de aceite de ballena produce 0.2 unidades de residuo.
# 
# 1. Ayude a los alquimistas a crear 100 unidades de fuego valiryo con el menor costo posible para enfrentar al enemigo.

# In[6]:


# Ejercicio 3
def targaryen_house_solve(aceite=None,dragon=None,caballo=None):
    total = 100
    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP

    test = True if  aceite is not None and dragon is not None and caballo is not None else False

    #variables
    oil = modelo.Var (lb = 0 ,name='aceite' )
    dra = modelo.Var (lb = 0 ,name='dragon')
    horse = modelo.Var (lb = 0,name='caballo')
    ing1 = modelo.Var (lb = 0 ,name='1')#ing1 30%
    ing2 = modelo.Var (lb = 0 ,name='2')#ing2 20%
    ing3 = modelo.Var (lb = 0 ,name='3')#50%
    #restricciones 
    modelo.Equation(0.4*oil + 0.1*dra + 0.15*horse +ing1 ==0.3*total)
    modelo.Equation(0.1*oil + 0.05*dra + 0.35*horse + ing2 ==0.2*total)
    modelo.Equation(0.3*oil + 0.5*dra + 0.05*horse + ing3 ==0.5*total)
    modelo.Equation(oil*0.8 + dra*0.65 + horse*0.55 + ing1 + ing2+ ing3==total)

    if test:
        modelo.Equation(oil==aceite)
        modelo.Equation(dra==dragon)
        modelo.Equation(horse==caballo)
    #funcion objetivo
    def f(oil,dra,horse):
        return 40*oil + 70*dra + 30*horse + 0.2*oil*5 + 0.35*dra*5 + 0.45*horse*5

    modelo.Minimize(f(oil,dra,horse))

    modelo.solve(disp=False)

    return modelo.options.OBJFCNVAL, [oil, dra, horse]

def targaryen_house_input():
    print('Según tus habilidades como alquimista,como se debería hacer la compra de los ingrediente')
    oil =int(input('Aceite de ballena: '))
    dra =int(input('Polvo de Dragon: '))
    horse =int(input('Piel de caballo:'))
    return [oil, dra, horse]

# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_3_equipo_1 = [
    0, # Aceite de ballena
    0, # Polvo de Dragón
    0, # Piel de caballo
]

argumentos_problema_3_equipo_2 = [
    0, # Aceite de ballena
    0, # Polvo de Dragón
    0, # Piel de caballo
]

problema_3 = ProblemManager(targaryen_house_solve, targaryen_house_input)

probl3_eq1_opt, probl3_eq2_opt, opt_probl3, vector_opt_probl3, punto_probl3_eq1, punto_probl3_eq2 =     comparar_problemas(problema_3, argumentos_problema_3_equipo_1, argumentos_problema_3_equipo_2)

# Agregar puntuación
puntos_equipo_1.append(punto_probl3_eq1)
puntos_equipo_2.append(punto_probl3_eq2)


# ## 4. Casa Baratheon
# 
# Es hora de reunir todos los recursos y tropas. Para esto se conoce que hacen falta trasladar las armas, comida, soldados y fuego valiryo hacia diferentes puntos intermedios para finalmente llegar a Winterfell. El traslado está condicionado por diferentes situaciones, clima, calidad del camino, tipo de recurso, que hacen que se tenga un desgaste de los recursos en el traslado en dependencia del destino. Este desgaste se observa:
# 
# Armas:
# 
# | Lugares | 2.1  | 2.2  | 2.3  |
# | ------- | ---- | ---- | ---- |
# | 1.1     | 5    | 10   | 7    |
# | 1.2     | 10   | 20   | 10   |
# | 1.3     | 7    | 10   | 7    |
# 
# Comida:
# 
# | Lugares | 2.1  | 2.2  | 2.3  |
# | ------- | ---- | ---- | ---- |
# | 1.1     | 25   | 20   | 15   |
# | 1.2     | 20   | 17   | 10   |
# | 1.3     | 15   | 10   | 5    |
# 
# Soldados:
# 
# | Lugares | 2.1  | 2.2  | 2.3  |
# | ------- | ---- | ---- | ---- |
# | 1.1     | 10   | 7    | 7    |
# | 1.2     | 7    | 10   | 9   |
# | 1.3     | 7    | 9    | 8    |
# 
# Fuego valiryo:
# 
# | Lugares | 2.1  | 2.2  | 2.3  |
# | ------- | ---- | ---- | ---- |
# | 1.1     | 30   | 25   | 25   |
# | 1.2     | 25   | 5    | 5    |
# | 1.3     | 25   | 5    | 5    |
# 
# En total se quieren trasladar 8 000 armas, 30 000 unidades de comida, 10 000 soldados, 100 unidades de fuego valiryo.
# 
# 1. Diga dónde se tienen que asignar los recursos y tropas para que el desgaste del transporte sea lo menor posible.
# 2. Para mitigar el desgaste de los caminos, estos tienen algunas restricciones sobre la cantidad de recursos que pueden ser transportados por ellos. Se tienen que transportar como mínimo en cada camino unas 3500 unidades de cualquier tipo de recusros o tropas. ¿Cuál sería la nueva asignación?

# In[7]:


# Ejercicio 4
def baratheon_house_solve(recursos_caminos=None, preservar_caminos=False):
    
    # Datos
    names = ['armas', 'comida', 'soldados', 'fuego_valiryo']
    
    necesario_recursos = [8000, 30000, 10000, 100]
    costo_caminos = [
        [
            [5, 10, 7],
            [10, 20, 10],
            [7, 10, 7]
        ],
        [
            [25, 20, 15],
            [20, 17, 10],
            [15, 10, 5]
        ],
        [
            [10, 7, 7],
            [7, 10, 9],
            [7, 9, 8]
        ],
        [
            [30, 25, 25],
            [25, 5, 5],
            [25, 5, 5]
        ]
    ]
    min_por_camino = 3500

    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP

    test = True if not recursos_caminos is None else False

    # Variables de decisión
    _vars = [[[None for _ in range(3)] for _ in range(3)] for _ in range(4)]

    for i in range(len(_vars)):
        for j in range(len(_vars[i])):
            for l in range(len(_vars[i][j])):
                _vars[i][j][l] = modelo.Var(lb=0, integer=True, name=(names[i] + '_' + str(j) + '_' + str(l)))

    # Restricciones de demanda
    eq = 0
    for i in range(len(_vars)):
        for j in range(len(_vars[i])):
            for l in range(len(_vars[i][j])):
                eq += _vars[i][j][l]

        modelo.Equation(eq >= necesario_recursos[i])
        eq = 0

    # Restricciones de balanceo de demanda entre caminos
    if preservar_caminos:
        i = j = l = 0
        for j in range(len(_vars[0])):
            for l in range(len(_vars[0][j])):
                for i in range(len(_vars)):
                    eq += _vars[i][j][l]

                modelo.Equation(eq >= min_por_camino)
                eq = 0

    if test:
        for i in range(len(_vars)):
            for j in range(len(_vars[i])):
                for l in range(len(_vars[i][j])):
                    modelo.Equation(recursos_caminos[i][j][l]==_vars[i][j][l])

    def f(matrix):
        ret = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for l in range(len(matrix[i][j])):
                    ret += matrix[i][j][l] * costo_caminos[i][j][l]

        return ret

    # Función objetivo
    modelo.Minimize(f(_vars))

    modelo.solve(disp=False)

    return modelo.options.OBJFCNVAL, _vars

def baratheon_house_input():
    names = ['armas', 'comida', 'soldados', 'fuego_valiryo']
    print('Se intentara preservar los caminos?')
    print('1 - Si')
    print('2 - No')
    while True:
        raw = input()
        try:
            ans = int(raw)
        
        except:
            print('Escriba una entrada correcta')

        if ans == 1:
            preservar = True
            break

        elif ans == 2:
            preservar = False
            break

        else:
            print('Escriba una entrada correcta')


    min = baratheon_house_solve(preservar_caminos=preservar)
    print('Segun el analisis que haz realizado sobre los caminos, cual seria la distribucion de recursos a enviar por cada ruta?')
    print()
    user_ans = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(4)]
    for i in range(len(user_ans)):
        for j in range(len(user_ans[i])):
            for l in range(len(user_ans[i][j])):
                user_ans[i][j][l] = int(input('Escriba la cantidad de ' + names[i] + ' a enviar por la ruta comenzando en el lugar 1.' + str(j + 1) + ' y terminando en el lugar 2.' + str(l + 1) + ': '))

    return user_ans


# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_4_equipo_1 = [
    [ # Transporte de Armas
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Comida
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Soldados
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Fuego Valiryo
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    
], False

argumentos_problema_4_equipo_2 = [
    [ # Transporte de Armas
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Comida
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Soldados
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Fuego Valiryo
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
], False

problema_4 = ProblemManager(baratheon_house_solve, baratheon_house_input)

print("Inciso a)")
print()
probl4_eq1_opt, probl4_eq2_opt, opt_probl4, vector_opt_probl4, punto_probl4_eq1, punto_probl4_eq2 =     comparar_problemas(problema_4, argumentos_problema_4_equipo_1, argumentos_problema_4_equipo_2, unfold=True)

# Agregar puntuación
puntos_equipo_1.append(punto_probl4_eq1)
puntos_equipo_2.append(punto_probl4_eq2)


# In[8]:



argumentos_problema_4_2_equipo_1 = [
    [ # Transporte de Armas
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Comida
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Soldados
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Fuego Valiryo
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    
], True

argumentos_problema_4_2_equipo_2 = [
    [ # Transporte de Armas
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Comida
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Soldados
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Fuego Valiryo
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
], True

print("Inciso b)")
print()
probl4_2_eq1_opt, probl4_2_eq2_opt, opt_probl4_2, vector_opt_probl4_2, punto_probl4_2_eq1, punto_probl4_2_eq2 =     comparar_problemas(problema_4, argumentos_problema_4_2_equipo_1, argumentos_problema_4_2_equipo_2, unfold=True)

# Agregar puntuación
puntos_equipo_1.append(punto_probl4_2_eq1)
puntos_equipo_2.append(punto_probl4_2_eq2)


# ## 5. Casa Stark
# 
# Ya se encuentran todos los recursos en Winterfell, listos para la batalla, el frío y la oscuridad cubren todo. Los exploradores regresan de su misión informando que los caminantes blancos atacarán en 12 oleadas y calculan el estimado de fuerza de cada una de ellas:
# 
# | Oleada | 1    | 2    | 3    | 4    | 5    | 6     | 7     | 8    | 9    | 10   | 11   | 12   |
# | ------ | ---- | ---- | ---- | ---- | ---- | ----- | ----- | ---- | ---- | ---- | ---- | ---- |
# | Fuerza | 2000 | 3000 | 4000 | 6000 | 8000 | 10000 | 10000 | 6000 | 4000 | 3000 | 2000 | 2000 |
# 
# Se sabe que cada soldado puede derrotar a un caminante blanco antes de perecer, además se tiene un lugar inicialmente vacío en las cercanías del campo de batalla, ahí las tropas pueden actuar como una fuerza de acción rápida además den descansar y reparar sus armas para continuar luchando, aunque por desgracia este lugar tiene un máximo de 5000 hombres. Las tropas se van enviando constantemente en cada oleada para reforzar la ofensiva. Debido al proceso de movilización, aumentar la cantidad de hombres que se envían a la batalla en cada oleada tiene un costo de 1 por hombre y disminuirlo de 0.5. 
# 
# 1. Realice un plan de lucha que permita ganar la batalla con el mínimo de costo posible.
# 2. Para que Arya pueda dar el golpe final se tiene que tener en la última oleada una diferencia de poder ganadora para los caminantes blancos de 1000, para que el jefe se confíe y salga al campo de batalla. Teniendo esto en cuenta, ¿qué cambios le harías a la estrategia?

# In[9]:


def stark_house_solve(waves_values=None, arya=False):
    if waves_values is None:
        waves_values = []

    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP

    # Constantes
    wave_strength_i = np.array([2000, 3000, 4000, 6000, 8000, 10000, 10000, 6000, 4000, 3000, 2000, 2000])
    waves_amount = len(wave_strength_i)
    max_refuge_capacity = 5000
    arya_threshold = 1000

    # Variables
    men_sent_wave_i = np.array([modelo.Var(lb=0, integer=True, name=f"Hombres enviados oleada {i}") for i in range(waves_amount)])
    # Aux variables para eliminar módulo
    positive_z_i = np.array([modelo.Var(lb=0, name=f"Diferencia positiva oleada {i+1}-{i}") for i in range(waves_amount-1)])
    negative_z_i = np.array([modelo.Var(ub=0, name=f"Diferencia negativa oleada {i+1}-{i}") for i in range(waves_amount-1)])

    # Restricciones
    def z_i(i):
        return men_sent_wave_i[i+1] - men_sent_wave_i[i]

    def all_men_k(k):
        """
        Devuelve la expresión de todos los hombres enviados hasta la oleada k
        """
        return (k+1)*men_sent_wave_i[0] + modelo.sum([(k - i)*(z_i(i)) for i in range(k)])

    def all_wave_strength_k(k):
        """
        Devuelve la expresión de toda la fuerza de las oleadas hasta la oleada k
        """
        return modelo.sum(wave_strength_i[:k+1])
    
    for i in range(waves_amount-1):
        modelo.Equation(z_i(i) == positive_z_i[i] + negative_z_i[i])

    for i in range(waves_amount):
        modelo.Equation(all_men_k(i) - all_wave_strength_k(i) <= max_refuge_capacity)
        modelo.Equation(all_men_k(i) - all_wave_strength_k(i) >= 0)

    # Restriccion de Arya
    if arya:
        modelo.Equation(all_wave_strength_k(waves_amount-1) - all_men_k(waves_amount-2) >= arya_threshold) 

    # Restricciones de usuario
    for i,restr in enumerate(waves_values):
        modelo.Equation(men_sent_wave_i[i] == restr)

    # Función objetivo
    modelo.Minimize(modelo.sum([0.75 * (positive_z_i[i] - negative_z_i[i]) + 0.25 * z_i(i) for i in range(waves_amount-1)]))

    modelo.solve(disp=False)

    return modelo.options.OBJFCNVAL, men_sent_wave_i

def stark_house_input():
    print("Introduce la cantidad de guerreros a enviar en cada oleada:")
    guerreros = []
    for i in range(12):
        guerreros.append(int(input(f"Oleada {i+1}: ")))
    return guerreros

# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_5_equipo_1 = [
    0, # Hombres enviados oleada 1
    0, # Hombres enviados oleada 2
    0, # Hombres enviados oleada 3
    0, # Hombres enviados oleada 4
    0, # Hombres enviados oleada 5
    0, # Hombres enviados oleada 6
    0, # Hombres enviados oleada 7
    0, # Hombres enviados oleada 8
    0, # Hombres enviados oleada 9
    0, # Hombres enviados oleada 10
    0, # Hombres enviados oleada 11
    0, # Hombres enviados oleada 12
], False

argumentos_problema_5_equipo_2 = [
    0, # Hombres enviados oleada 1
    0, # Hombres enviados oleada 2
    0, # Hombres enviados oleada 3
    0, # Hombres enviados oleada 4
    0, # Hombres enviados oleada 5
    0, # Hombres enviados oleada 6
    0, # Hombres enviados oleada 7
    0, # Hombres enviados oleada 8
    0, # Hombres enviados oleada 9
    0, # Hombres enviados oleada 10
    0, # Hombres enviados oleada 11
    0, # Hombres enviados oleada 12
], False

print("Inciso a)")
print()
problema_5 = ProblemManager(stark_house_solve, stark_house_input)

probl5_eq1_opt, probl5_eq2_opt, opt_probl5, vector_opt_probl5, punto_probl5_eq1, punto_probl5_eq2 =     comparar_problemas(problema_5, argumentos_problema_5_equipo_1, argumentos_problema_5_equipo_2, unfold=True)

# Agregar puntuación
puntos_equipo_1.append(punto_probl5_eq1)
puntos_equipo_2.append(punto_probl5_eq2)


# In[12]:


argumentos_problema_5_2_equipo_1 = [
    0, # Hombres enviados oleada 1
    0, # Hombres enviados oleada 2
    0, # Hombres enviados oleada 3
    0, # Hombres enviados oleada 4
    0, # Hombres enviados oleada 5
    0, # Hombres enviados oleada 6
    0, # Hombres enviados oleada 7
    0, # Hombres enviados oleada 8
    0, # Hombres enviados oleada 9
    0, # Hombres enviados oleada 10
    0, # Hombres enviados oleada 11
    0, # Hombres enviados oleada 12
], True

argumentos_problema_5_2_equipo_2 = [
    0, # Hombres enviados oleada 1
    0, # Hombres enviados oleada 2
    0, # Hombres enviados oleada 3
    0, # Hombres enviados oleada 4
    0, # Hombres enviados oleada 5
    0, # Hombres enviados oleada 6
    0, # Hombres enviados oleada 7
    0, # Hombres enviados oleada 8
    0, # Hombres enviados oleada 9
    0, # Hombres enviados oleada 10
    0, # Hombres enviados oleada 11
    0, # Hombres enviados oleada 12
], True

print("Inciso b)")
print()
probl5_2_eq1_opt, probl5_2_eq2_opt, opt_probl5_2, vector_opt_probl5_2, punto_probl5_2_eq1, punto_probl5_2_eq2 =     comparar_problemas(problema_5, argumentos_problema_5_2_equipo_1, argumentos_problema_5_2_equipo_2, unfold=True)

# Agregar puntuación
puntos_equipo_1.append(punto_probl5_2_eq1)
puntos_equipo_2.append(punto_probl5_2_eq2)


# # Conlcusión
# 
# Conteo de puntos y dar resultados

# In[16]:


equipo1 = sum(puntos_equipo_1)
equipo2 = sum(puntos_equipo_2)

print("Puntos equipo 1:", equipo1)

print("Puntos equipo 2:", equipo2)

ganador = "1" if equipo1 > equipo2 else "2" if equipo1 < equipo2 else "1 y 2"

print("Felicidades equipo", ganador, "por participar y ganar en la lucha contra los caminantes blancos")

