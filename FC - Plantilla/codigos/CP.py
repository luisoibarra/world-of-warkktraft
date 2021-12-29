from typing import Callable, List, Optional, Tuple
from gekko import GEKKO
import gekko
import numpy as np

def unfold(obj):
    try:
        if isinstance(obj, gekko.gk_variable.GKVariable):
            raise TypeError
        if isinstance(obj, tuple):
            yield from obj
        else:
            for x in obj:
                yield from unfold(x)
    except TypeError:
        yield obj
    
class ProblemManager:
    def __init__(self, solver:Callable[[Optional[float],], float], args_fetcher:Callable[[], Tuple[float,]]) -> None:
        self.solver = solver
        self.args_fetcher = args_fetcher

    def solve(self, *args):
        max = self.solver(*args)
        return max

    def compare(self, user_args=None):
        try:
            opt, vector_variables = self.solve()
        except:
            print("El problema no es factible.")
            return None, None, None, None

        vector_variables = [x for x in unfold(vector_variables)]

        print("Asignación óptima:")
        for v in vector_variables:
            print(v.name, ":", v.value)
        
        if user_args is None:
            user_args = self.args_fetcher()

        user_args = [x for x in unfold(user_args)]

        try:        
            user_opt, user_args = self.solve(*user_args)
            user_args = [x for x in unfold(user_args)]
            
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

# Ejercicio 2
def greyjoy_house_solve(trigo=None, encurtidos=None, ganado=None, agua=None):
    
    # Datos
    total_ppl = 1000
    proteinas = 60 * total_ppl
    carbohidratos = 120 * total_ppl
    aceite = 20 * total_ppl
    agua = 1.5 * total_ppl

    totals = [proteinas, carbohidratos, aceite]

    nutrientes_costo = [[10, 40, 20, 10],
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
    _encurtidos = modelo.Var(lb=0, integer=True, name='encurtidos')
    _ganado = modelo.Var(lb=0, integer=True, name='ganado')
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
    encurtidos = int(input('Encurtidos:'))
    ganado = int(input('Ganado:'))
    agua = int(input('Agua:'))
    return [trigo, encurtidos, ganado, agua]

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
    min_por_camino = 5500

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

# Ejercicio 5
def stark_house_solve(*waves_values):

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

def main():
    solver = stark_house_solve
    inputer = stark_house_input
    solver = baratheon_house_solve
    inputer = baratheon_house_input
    # solver = mormont_house_solve
    # inputer = mormont_house_input
    problem = ProblemManager(solver, inputer)
    problem.compare()


main()