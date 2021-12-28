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


def targaryen_house_solve(aceite=None,dragon=None,caballo=None):
    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP
        
    test = True if  aceite is not None and dragon is not None and caballo is not None else False
     
    #variables
    oil = modelo.Var (lb = 0, integer = True ,name='aceite' )
    dra = modelo.Var (lb = 0, integer = True ,name='dragon')
    horse = modelo.Var (lb = 0, integer = True ,name='caballo')
    
    #restricciones 
    modelo.Equation(0.4*oil + 0.1*dra + 0.15*horse >=85)
    modelo.Equation(0.1*oil + 0.05*dra + 0.35*horse >=70)
    modelo.Equation(0.3*oil + 0.5*dra + 0.05*horse >=90)
        
    #funcion objetivo
    def f(x,y,z):
        return 40*x + 70*y + 30*z
    
    modelo.Minimize(f(oil,dra,horse))
    
    try:
        modelo.solve(disp=False)
    except Exception:
        return -1
    
    return -modelo.options.OBJFCNVAL
def main():
    # mormont_house()
    targaryen_house_solve()

main()