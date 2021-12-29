from gekko import GEKKO
import gekko

    
def mormont_house():
    
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

        try:
            modelo.solve(disp=False)
        except Exception:
            return -1
        
        return -modelo.options.OBJFCNVAL
    
    max = mormont_house_solve()
    print('Según tus habilidades como estratega militar que cantidad de cada arma se debería construir')
    swords =int(input('Espadas:'))
    bows =int(input('Arcos:'))
    catapults =int(input('Catapultas:'))
    
    user_max = mormont_house_solve(swords,bows,catapults)
    if user_max>0:
        print('El daño alcanzado con su estrategia es de',user_max)
        # print('El daño  máximo posible a alcanzar con esos recursos es',max)
        if max>user_max*4:
            print('Tu solución es bastante mala con respecto al daño posible, es menos que la cuarta parte.El daño máxima era de',max)
        elif max>user_max*2:
            print('Tu solución es mala con respecto a daño máxima posible,es menos de la mitad.El daño máxima era de',max)
       
        elif max>user_max*1.5:
            print('Tu solución es bastante buena, el daño máxima era de',max)
        elif max<user_max+5:
            print('Tu solución es óptima')
        else:
            print('Tu solución es muy buena,casi en lo óptimo,pero el daño máximo posible alcanzado es, ' ,max)
        
        
    else:
        print('Su solución no es factible.El daño máxima posible es',max )

def greyjoy_house():

    def greyjoy_house_solve(trigo=None, encurtidos=None, ganado=None, agua=None):
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
        
        _trigo = modelo.Var(lb=0, integer=True, name='trigo')
        _encurtidos = modelo.Var(lb=0, integer=True, name='encurtidos')
        _ganado = modelo.Var(lb=0, integer=True, name='ganado')
        _agua = modelo.Var(lb=0, integer=True, name='agua')

        e_vars = [_trigo, _ganado, _encurtidos, _agua]

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

        modelo.Minimize(f(_trigo, _ganado, _encurtidos, _agua))

        try:
            modelo.solve(disp=False)

        except:
            return -1, -1

        return modelo.options.OBJFCNVAL, [_trigo.value, _encurtidos.value, _ganado.value, _agua.value]

    min, _vars = greyjoy_house_solve()
    print('Segun tu habilidad como gastronomo, que cantidad de alimentos se deberia producir')
    trigo = int(input('Trigo:'))
    encurtidos = int(input('Encurtidos:'))
    ganado = int(input('Ganado:'))
    agua = int(input('Agua:'))

    user_min, _ = greyjoy_house_solve(trigo, encurtidos, ganado, agua)
    if user_min > 0:
        print('El costo minimo de su produccion es de ' + str(min) + ' que se obtiene produciendo ' +  str(_vars[0][0]) + ' gramos de trigo, ' + str(_vars[1][0]) + ' unidades de ganado, ' + str(_vars[2][0]) + ' gramos de encurtidos y ' + str(_vars[3][0]) + ' litros de agua potable')
        if min*4<user_min:
            print('Tu solución es bastante mala con respecto al costo mínimo posible, es cuatro veces mayor.El costo mínimo era de',max)
        elif min*2<user_min:
            print('Tu solución es mala con respecto a daño máxima posible,es mas de el doble.El costo mmínimo era de',max)
       
        elif min*1.5<user_min:
            print('Tu solución es bastante buena, el costo mínimo era de',min)
        elif min<user_min+5:
            print('Tu solución es óptima')
        else:
            print('Tu solución es muy buena,casi en lo óptimo,pero el daño máximo posible alcanzado es, ' ,max)
        
        
    else:
        print('Su solución no es factible.El costo minimo posible es',min )
        print('El costo minimo de su produccion es de ' + str(min) + ' que se obtiene produciendo ' +  str(_vars[0][0]) + ' gramos de trigo, ' + str(_vars[1][0]) + ' unidades de ganado, ' + str(_vars[2][0]) + ' gramos de encurtidos y ' + str(_vars[3][0]) + ' litros de agua potable')
        


def targaryen_house():
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

        try:
            modelo.solve(disp=False)
        except Exception:
            return -1

        return modelo.options.OBJFCNVAL

    max =targaryen_house_solve()
    print('Según tus habilidades como alquimista,como se debería hacer la compra de los ingrediente')
    oil =int(input('Aceite de ballena: '))
    dra =int(input('Polvo de Dragon: '))
    horse =int(input('Piel de caballo:'))
    
    user_max = targaryen_house_solve(oil,dra,horse)
    if user_max>0:
        print('El costo mínimo de su compra es ',user_max)
        # print('El daño  máximo posible a alcanzar con esos recursos es',max)
        if max*4<user_max:
            print('Tu solución es bastante mala con respecto al costo mínimo posible, es cuatro veces mayor.El costo mínimo era de',max)
        elif max*2<user_max:
            print('Tu solución es mala con respecto a daño máxima posible,es mas de el doble.El costo mmínimo era de',max)
       
        elif max*1.5<user_max:
            print('Tu solución es bastante buena, el costo mínimo era de',max)
        elif max<user_max+5:
            print('Tu solución es óptima')
        else:
            print('Tu solución es muy buena,casi en lo óptimo,pero el daño máximo posible alcanzado es, ' ,max)
        
        
    else:
        print('Su solución no es factible.El costo minimo posible es',max )


def baratheon_house():
    names = ['armas', 'comida', 'soldados', 'fuego_valiryo']

    def baratheon_house_solve(recursos_caminos=None, preservar_caminos=False):
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


        _vars = [[[None for _ in range(3)] for _ in range(3)] for _ in range(4)]

        for i in range(len(_vars)):
            for j in range(len(_vars[i])):
                for l in range(len(_vars[i][j])):
                    _vars[i][j][l] = modelo.Var(lb=0, integer=True, name=(names[i] + '_' + str(j) + '_' + str(l)))

        eq = 0
        for i in range(len(_vars)):
            for j in range(len(_vars[i])):
                for l in range(len(_vars[i][j])):
                    eq += _vars[i][j][l]

            modelo.Equation(eq >= necesario_recursos[i])
            eq = 0

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

        modelo.Minimize(f(_vars))

        try:
            modelo.solve(disp=False)
        
        except Exception:
            return -1, -1

        ret_vars = [[[_vars[i][j][l].value for l in range(len(_vars[i][j]))] for j in range(len(_vars[i]))] for i in range(len(_vars))]
        return modelo.options.OBJFCNVAL, ret_vars

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


    min, _vars = baratheon_house_solve(preservar_caminos=preservar)
    print('Segun el analisis que haz realizado sobre los caminos, cual seria la distribucion de recursos a enviar por cada ruta?')
    print()
    user_ans = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(4)]
    for i in range(len(user_ans)):
        for j in range(len(user_ans[i])):
            for l in range(len(user_ans[i][j])):
                user_ans[i][j][l] = int(input('Escriba la cantidad de ' + names[i] + ' a enviar por la ruta comenzando en el lugar 1.' + str(j + 1) + ' y terminando en el lugar 2.' + str(l + 1) + ': '))

    user_min, _ = baratheon_house_solve(user_ans, preservar)
    if user_min > 0:
        print('El costo minimo de su produccion es de ', user_min)
        print('La distribucion de los caminos es de:\n')
        print('Para las armas:\n', _vars[0])
        print('Para la comida:\n', _vars[1])
        print('Para los soldados:\n', _vars[2])
        print('Para el fuego valiryo:\n', _vars[3])
        if min*4<user_min:
            print('Tu solución es bastante mala con respecto al costo mínimo posible, es cuatro veces mayor.El costo mínimo era de',max)
        elif min*2<user_min:
            print('Tu solución es mala con respecto a daño máxima posible,es mas de el doble.El costo mmínimo era de',max)
       
        elif min*1.5<user_min:
            print('Tu solución es bastante buena, el costo mínimo era de',min)
        elif min<user_min+5:
            print('Tu solución es óptima')
        else:
            print('Tu solución es muy buena,casi en lo óptimo,pero el daño máximo posible alcanzado es, ' ,max)
        
        
    else:
        print('Su solución no es factible.El costo minimo posible es',min )
        print('La distribucion de los caminos es de:\n')
        print('Para las armas:\n', _vars[0])
        print('Para la comida:\n', _vars[1])
        print('Para los soldados:\n', _vars[2])
        print('Para el fuego valiryo:\n', _vars[3])




def main():
    # mormont_house()
    # targaryen_house()
    # greyjoy_house()
    baratheon_house()


main()