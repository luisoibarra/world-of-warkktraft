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
    def total_artesanos(self):
        return self.castillo.artesanos.cantidad
    
    @property
    def total_guerreros(self):
        return self.castillo.guerreros.cantidad
    
    @property
    def artesanos_necesarios_por_arma_i(self):
        return np.array([x.artesanos.cantidad for x in self.castillo.armas])

    @property
    def recurso_i_necesario_para_arma_j(self):
        return np.array([
            [
                next(x for x in a.recursos if x.nombre == r.nombre).cantidad for a in self.castillo.armas
            ] for r in self.castillo.recursos
        ])
        
    @property
    def guerreros_necesarios_por_arma_i(self):
        return np.array([x.guerreros.cantidad for x in self.castillo.armas])

    @property
    def danno_arma_i(self):
        return np.array([x.ataque for x in self.castillo.armas])

    @property
    def ataque_enemigo_por_dia_i(self):
        return np.array([x.poder for x in self.estrategia_enemiga.ataques])
 
    def generar_modelo(self):
        
        # Generando modelo
        
        modelo = GEKKO(remote=False)
        modelo.options.SOLVER = 1  # APOPT is an MINLP solver
        modelo.options.LINEAR = 1 # Is a MILP
        
        # Calculando constantes
        
        artesanos_necesarios_por_arma_i = self.artesanos_necesarios_por_arma_i
        recurso_i_necesario_para_arma_j = self.recurso_i_necesario_para_arma_j
        guerreros_necesarios_por_arma_i = self.guerreros_necesarios_por_arma_i
        danno_arma_i = self.danno_arma_i
        ataque_enemigo_por_dia_i = self.ataque_enemigo_por_dia_i
        armas_dependientes = [(i,x) for i,x in enumerate(self.castillo.armas) if x.depende is not None]
        dependencia_arma_i = {i:next(j for j,y in enumerate(self.castillo.armas) if y.nombre==x.depende.nombre) for i,x in armas_dependientes}

        # Definiendo variables
        
        artesanos_dia_i_para_arma_j  = np.array([[modelo.Var(lb=0, integer=True, name=f"ArtesanosPara{x.nombre}Dia{i}") for x in self.castillo.armas] for i in range(self.total_dias)])
        dia_i_recurso_disponible_j  = np.array([[modelo.Var(lb=0, name=f"Recurso{x.nombre}Dia{i}") for x in self.castillo.recursos] for i in range(self.total_dias)])
        dia_i_arma_j_contruida = np.array([[modelo.Var(lb=0, integer=True, name=f"Arma{x.nombre}ConstruidaDia{i}") for x in self.castillo.armas] for i in range(self.total_dias)])
        dia_i_asignacion_guerreros_arma_j = np.array([[modelo.Var(lb=0, integer=True, name=f"GuerreroConArma{x.nombre}Dia{i}") for x in self.castillo.armas] for i in range(self.total_dias)])
        dia_i_armas_j_en_uso = np.array([[modelo.Var(lb=0, integer=True, name=f"Arma{x.nombre}EnUsoDia{i}") for x in self.castillo.armas] for i in range(self.total_dias)])
        
        # Añadiendo restricciones
        
        for i in range(self.total_dias):
            # La asignacion de artesanos no puede superar la cantidad de ellos
            modelo.Equation(modelo.sum(artesanos_dia_i_para_arma_j[i]) <= self.total_artesanos)
            
            for j in range(artesanos_dia_i_para_arma_j.shape[1]):
                # La asigancion de artesanos a construir 
                # el arma j tiene que satisfacer la cantidad
                # necesaria para realizar la tarea
                if i < self.total_dias - 1:
                    modelo.Equation(artesanos_dia_i_para_arma_j[i][j] == artesanos_necesarios_por_arma_i[j] * dia_i_arma_j_contruida[i+1][j])
                else:
                    # Los artesanos no construyen nada para el proximo dia pq ya es el final
                    modelo.Equation(artesanos_dia_i_para_arma_j[i][j] == 0)
                    
            if i < self.total_dias - 1:
                for j in range(recurso_i_necesario_para_arma_j.shape[0]):
                    # Tienen que existir los recursos para 
                    # construir las armas asociadas al dia
                    CT_ij = modelo.sum(recurso_i_necesario_para_arma_j[j] * dia_i_arma_j_contruida[i+1])
                    modelo.Equation(CT_ij <= dia_i_recurso_disponible_j[i][j])
                
                    # Actualizacion de los recursos por dia
                    modelo.Equation(dia_i_recurso_disponible_j[i+1][j] == dia_i_recurso_disponible_j[i][j] - CT_ij)
            
            # Los guerreros asociados a 
            # las armas no pueden superar el maximo
            modelo.Equation(modelo.sum(dia_i_asignacion_guerreros_arma_j[i]) <= self.total_guerreros)
            
            # Las armas tienen la cantidad de 
            # guerreros suficiente para operar
            for j in range(dia_i_armas_j_en_uso.shape[1]):
                modelo.Equation(guerreros_necesarios_por_arma_i[j]*dia_i_armas_j_en_uso[i][j] == dia_i_asignacion_guerreros_arma_j[i][j])
            
            # El poder de ataque tiene que ser 
            # superior al ataque del enemigo
            modelo.Equation(modelo.sum(dia_i_armas_j_en_uso[i] * danno_arma_i) >= ataque_enemigo_por_dia_i[i])
            
            # Las armas tienen que existir para poder usarse
            for j in range(dia_i_armas_j_en_uso.shape[1]):
                modelo.Equation(dia_i_armas_j_en_uso[i][j] <= modelo.sum(dia_i_arma_j_contruida[:i,j]))
                
            # La cantidad de armas de las que depende es mayor a la cantidad de las armas que existe.
            for j in dependencia_arma_i:
                modelo.Equation(modelo.sum(dia_i_arma_j_contruida[:i,dependencia_arma_i[j]]) >= modelo.sum(dia_i_arma_j_contruida[:i+1,j]))

                        
        # Condiciones iniciales
        
        for j in range(dia_i_recurso_disponible_j.shape[1]):
            # Restriccion que pone los recursos iniciales
            modelo.Equation(dia_i_recurso_disponible_j[0][j] == self.castillo.recursos[j].cantidad)
        
        for j in range(dia_i_arma_j_contruida.shape[1]):
            # Restriccion de armas iniciales
            modelo.Equation(dia_i_arma_j_contruida[0][j] == 0) 
        
        # Funcion objetivo
         
        modelo.Maximize(np.sum(dia_i_armas_j_en_uso))
        
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
                print("Recursos disponible", [f"{self.castillo.recursos[i].nombre}: {x.value}" for i,x in enumerate(dia_i_recurso_disponible_j[i])])
                print("Artesanos para armas", [f"{self.castillo.armas[i].nombre}: {x.value}" for i,x in enumerate(artesanos_dia_i_para_arma_j[i])])
                print("Armas terminadas en el turno", [f"{self.castillo.armas[i].nombre}: {x.value}" for i,x in enumerate(dia_i_arma_j_contruida[i])])
                print("Total de armas", [f"{x.nombre} {sum(c[0] for c in dia_i_arma_j_contruida[:i+1,j])}" for j,x in enumerate(self.castillo.armas)])
                print("Guerreros armados", [f"{self.castillo.armas[i].nombre}: {x.value}" for i,x in enumerate(dia_i_asignacion_guerreros_arma_j[i])])
                print("Armas en combate", [f"{self.castillo.armas[i].nombre}: {x.value}" for i,x in enumerate(dia_i_armas_j_en_uso[i])])
                print("Poder de fuego", sum(x.value[0]*y for x,y in zip(dia_i_armas_j_en_uso[i],danno_arma_i)))
                print("Ataque enemigo", ataque_enemigo_por_dia_i[i])

        return ModeloGEKKO(solver)
                        