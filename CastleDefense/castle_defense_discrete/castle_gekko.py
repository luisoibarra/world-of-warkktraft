"""
Solución del modelo del juego usando GEKKO 
"""

from typing import Callable
from gekko import GEKKO
import gekko
from castle import Castillo, Juego, Modelo
import numpy as np

class ModeloGEKKO(Modelo):
    
    def __init__(self, solve: Callable) -> None:
        self.solver = solve
        
    def solve(self):
        self.solver()
        

class JuegoGEKKO(Juego):
    
    @property
    def total_dias(self):
        return len(self.estrategia_enemiga.ataques)
    
    @property
    def a_t(self):
        return self.castillo.artesanos.cantidad
    
    @property
    def g_t(self):
        return self.castillo.guerreros.cantidad
    
    @property
    def aw_j(self):
        return np.array([x.artesanos.cantidad for x in self.castillo.armas])

    @property
    def cw_ij(self):
        return np.array([
            [
                next(x for x in a.recursos if x.nombre == r.nombre).cantidad for a in self.castillo.armas
            ] for r in self.castillo.recursos
        ])
        
    @property
    def ww_j(self):
        return np.array([x.guerreros.cantidad for x in self.castillo.armas])

    @property
    def d_j(self):
        return np.array([x.ataque for x in self.castillo.armas])

    @property
    def E_i(self):
        return np.array([x.poder for x in self.estrategia_enemiga.ataques])
 
    def generar_modelo(self):
        
        # Generando modelo
        
        modelo = GEKKO(remote=False)
        modelo.options.SOLVER = 1  # APOPT is an MINLP solver
        modelo.options.LINEAR = 1 # Is a MILP
        
        # Calculando constantes
        
        aw_j = self.aw_j
        cw_ij = self.cw_ij
        ww_j = self.ww_j
        d_j = self.d_j
        E_i = self.E_i
        armas_dependientes = [(i,x) for i,x in enumerate(self.castillo.armas) if x.depende is not None]
        wd_i = {i:next(j for j,y in enumerate(self.castillo.armas) if y.nombre==x.depende.nombre) for i,x in armas_dependientes}

        # Definiendo variables
        
        a_ij  = np.array([[modelo.Var(lb=0, integer=True, name=f"ArtesanosPara{x.nombre}Dia{i}") for x in self.castillo.armas] for i in range(self.total_dias)])
        r_ij  = np.array([[modelo.Var(lb=0, name=f"Recurso{x.nombre}Dia{i}") for x in self.castillo.recursos] for i in range(self.total_dias)])
        bw_ij = np.array([[modelo.Var(lb=0, integer=True, name=f"Arma{x.nombre}ConstruidaDia{i}") for x in self.castillo.armas] for i in range(self.total_dias)])
        Aw_ij = np.array([[modelo.Var(lb=0, integer=True, name=f"GuerreroConArma{x.nombre}Dia{i}") for x in self.castillo.armas] for i in range(self.total_dias)])
        AU_ij = np.array([[modelo.Var(lb=0, integer=True, name=f"Arma{x.nombre}EnUsoDia{i}") for x in self.castillo.armas] for i in range(self.total_dias)])
        
        # Añadiendo restricciones
        
        for i in range(self.total_dias):
            # La asignacion de artesanos no puede superar la cantidad de ellos
            modelo.Equation(modelo.sum(a_ij[i]) <= self.a_t)
            
            for j in range(a_ij.shape[1]):
                # La asigancion de artesanos a construir 
                # el arma j tiene que satisfacer la cantidad
                # necesaria para realizar la tarea
                if i < self.total_dias - 1:
                    modelo.Equation(a_ij[i][j] == aw_j[j] * bw_ij[i+1][j])
                else:
                    # Los artesanos no construyen nada para el proximo dia pq ya es el final
                    modelo.Equation(a_ij[i][j] == 0)
                    
            if i < self.total_dias - 1:
                for j in range(cw_ij.shape[0]):
                    # Tienen que existir los recursos para 
                    # construir las armas asociadas al dia
                    CT_ij = modelo.sum(cw_ij[j] * bw_ij[i+1])
                    modelo.Equation(CT_ij <= r_ij[i][j])
                
                    # Actualizacion de los recursos por dia
                    modelo.Equation(r_ij[i+1][j] == r_ij[i][j] - CT_ij)
            
            # Los guerreros asociados a 
            # las armas no pueden superar el maximo
            modelo.Equation(modelo.sum(Aw_ij[i]) <= self.g_t)
            
            # Las armas tienen la cantidad de 
            # guerreros suficiente para operar
            for j in range(AU_ij.shape[1]):
                modelo.Equation(ww_j[j]*AU_ij[i][j] == Aw_ij[i][j])
            
            # El poder de ataque tiene que ser 
            # superior al ataque del enemigo
            modelo.Equation(modelo.sum(AU_ij[i] * d_j) >= E_i[i])
            
            # Las armas tienen que existir para poder usarse
            for j in range(AU_ij.shape[1]):
                modelo.Equation(AU_ij[i][j] <= modelo.sum(bw_ij[:i,j]))
                
            # La cantidad de armas de las que depende es mayor a la cantidad de las armas que existe.
            for j in wd_i:
                modelo.Equation(modelo.sum(bw_ij[:i,wd_i[j]]) >= modelo.sum(bw_ij[:i+1,j]))

                        
        # Condiciones iniciales
        
        for j in range(r_ij.shape[1]):
            # Restriccion que pone los recursos iniciales
            modelo.Equation(r_ij[0][j] == self.castillo.recursos[j].cantidad)
        
        for j in range(bw_ij.shape[1]):
            # Restriccion de armas iniciales
            modelo.Equation(bw_ij[0][j] == 0) 
        
        # Funcion objetivo
         
        modelo.Maximize(np.sum(AU_ij))
        
        def solver():
            try:
                modelo.solve(disp=False)
            except Exception:
                print("No puedes ganar :_(")
                return
            
            self.print_situacion()
            
            print("Evolucion")
            for i in range(self.total_dias):
                print()
                print("Dia",i+1)
                print()
                print("Recursos disponible", [f"{self.castillo.recursos[i].nombre}: {x.value}" for i,x in enumerate(r_ij[i])])
                print("Artesanos para armas", [f"{self.castillo.armas[i].nombre}: {x.value}" for i,x in enumerate(a_ij[i])])
                print("Armas terminadas en el turno", [f"{self.castillo.armas[i].nombre}: {x.value}" for i,x in enumerate(bw_ij[i])])
                print("Total de armas", [f"{x.nombre} {sum(c[0] for c in bw_ij[:i+1,j])}" for j,x in enumerate(self.castillo.armas)])
                print("Guerreros armados", [f"{self.castillo.armas[i].nombre}: {x.value}" for i,x in enumerate(Aw_ij[i])])
                print("Armas en combate", [f"{self.castillo.armas[i].nombre}: {x.value}" for i,x in enumerate(AU_ij[i])])
                print("Poder de fuego", sum(x.value[0]*y for x,y in zip(AU_ij[i],d_j)))
                print("Ataque enemigo", E_i[i])

        return ModeloGEKKO(solver)
                        