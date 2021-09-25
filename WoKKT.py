import numpy as np
import scipy.optimize as opt 
import time

## PARAMETROS DEL PROBLEMA ##

cubita_super_cubano_mix = .5
cubita_super_colombiano_mix = .5
cubita_deluxe_cubano_mix = .25
cubita_deluxe_colombiano_mix = .75

total_cafe_colombiano = 200
total_cafe_cubano = 300

tiempo_de_produccion_deluxe = 10/9
tiempo_de_produccion_super = 1

total_de_produccion_super = 500

ganancia_super = 9
ganancia_deluxe = 11

## DESCRIPCION DEL PROBLEMA ##

program_description = \
f"""
Una empacadora de café mezcla café colombiano y café cubano 
para ofertar dos tipos de nuevas marcas: Cubita super y Cubita 
deluxe. Cada Kilogramo de Cubita Super contiene {cubita_super_colombiano_mix} Kg. de café 
colombiano y {cubita_super_cubano_mix} Kg. de café cubano, mientras que cada Kg. de 
Cubita deluxe contiene {cubita_deluxe_cubano_mix} kg. 
de café cubano y {cubita_deluxe_colombiano_mix} de café 
colombiano. Se dispone de {total_cafe_colombiano} Kg. de café colombiano 
y {total_cafe_cubano} Kg. de café cubano. La producción de un Kg. 
del café deluxe requiere {tiempo_de_produccion_deluxe} del tiempo 
que requiere el procesamiento de {tiempo_de_produccion_super} Kg. de café super 
en la mezcladora y se  conoce que si sólo se produjera café super 
podrían mezclarse {total_de_produccion_super}Kg. Si la ganancia por Kg. de Cubita super 
es {ganancia_super} centavos y la de Cubita deluxe es {ganancia_deluxe} centavos. Cuántos Kg
de cada marca deben producirse para maximizar la ganancia? 
"""

## MODELO DEL PROBLEMA ##

cafe_c = np.array([
    ganancia_super, 
    ganancia_deluxe,
])

cafe_A_ub = np.array([
    [cubita_super_colombiano_mix, cubita_deluxe_colombiano_mix],
    [cubita_super_cubano_mix, cubita_deluxe_cubano_mix],
    [tiempo_de_produccion_super, tiempo_de_produccion_deluxe]
])
cafe_b_ub = np.array([
    total_cafe_colombiano,
    total_cafe_cubano,
    total_de_produccion_super,
])

cafe_A_eq = None

cafe_b_eq = None


## UTILES DE OPTIMIZACION ##

solution_meaning = {
    0 : "Optimization proceeding nominally.",
    1 : "Iteration limit reached.",
    2 : "Problem appears to be infeasible.",
    3 : "Problem appears to be unbounded.",
    4 : "Numerical difficulties encountered.",
}

def solve_linear_problem(maximizar, c, A_ub=None, b_ub=None, A_eq=None, b_eq=None):
    if maximizar:
        c = -c.copy()
    sol = opt.linprog(c, A_ub, b_ub, A_eq, b_eq)
    if maximizar:
        sol.fun = -sol.fun
    return sol

def is_feasible_solution(sol, A_ub=None, b_ub=None, A_eq=None, b_eq=None):
    feasible = True
    if A_ub is not None and A_ub.any() and b_ub is not None and b_ub.any():
        feasible = feasible and all(A_ub @ sol <= b_ub)
    if A_eq is not None and A_eq.any() and b_eq is not None and b_eq.any():
        feasible = feasible and all(A_eq @ sol == b_eq)
    return feasible

# Solucion al problema
cafe_solution = solve_linear_problem(True, cafe_c, cafe_A_ub, cafe_b_ub, cafe_A_eq, cafe_b_eq)

## UTILES DE CONSOLA ##

def show_spinner():
    n = 5
    while n>0:
        for i in '|\\-/':
            print('\b' + i, end="")
            time.sleep(.1)
        n -= 1  

def get_number_console(placeholder):
    while True:
        try:
            value = float(input(placeholder))
            return value
        except Exception as e:
            print(e)

def show_cafe_solution_report(cafe_super, cafe_deluxe):
    user_solution = np.array([cafe_super, cafe_deluxe])
    
    true_cafe_super, true_cafe_deluxe = cafe_solution.x
    ganancia_max = cafe_solution.fun
    ganancia_hecha = cafe_c @ user_solution
    feasible_original_problem = cafe_solution.success
    feasible_user_solution = is_feasible_solution(user_solution, cafe_A_ub, cafe_b_ub, cafe_A_eq, cafe_b_eq)
    if feasible_original_problem:
        print("La ganancia máxima es",ganancia_max)
        print("Solución esperada de café super:" ,true_cafe_super)
        print("Solución esperada de café deluxe:",true_cafe_deluxe)
    else:
        print("El problema original no pudo ser resuelto debido a", solution_meaning[cafe_solution.status])    
    print()
    if feasible_user_solution:
        print("La ganancia recibida fue",ganancia_hecha)
        print("Solución dada de café super:" ,cafe_super)
        print("Solución dada de café deluxe:",cafe_deluxe)
    else:
        print("Tu solución no cumple con las restricciones")

def run():
    
    print("Bienvenidos a la Fábrica de Café .")
    name = input("Escriba su nombre: ")
    
    print(f"Hola {name} entonces, como nuevo jefe de operaciones de la")
    print(f"fábrica de café se le asigna la siguiente tarea:")
    print()
    print(program_description)
    print()
    print("Entonces, cuánto, según tu basta experiencia en manejo del café, hace falta")
    print("producir por cada tipo de café para lograr un buen resultado?")
    print()
    
    cafe_super = get_number_console("Cuánto mandarías a hacer de café super: ")
    cafe_deluxe = get_number_console("Cuánto mandarías a hacer de café deluxe: ")
    
    print()
    print("Y sus hombres empezaron el día con las instrucciones de hacer")
    print(f"{cafe_super} Kg de café super y {cafe_deluxe} Kg de café deluxe")
    
    print()
    show_spinner()
    print()
    
    show_cafe_solution_report(cafe_super, cafe_deluxe)
    
if __name__ == "__main__":
    run()