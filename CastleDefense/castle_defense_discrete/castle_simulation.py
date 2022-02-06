from castle import Castillo, Juego, Modelo


class ModeloSimulacion(Modelo):
    
    def __init__(self, juego: 'JuegoSimulacion') -> None:
        super().__init__()
        self.juego = juego # Desde aqui es accesible el castillo y la estrategia del enemigo
    
    def solve(self):
        """
        Recrea el juego en interacción con el usuario
        """
        dia_actual = 0
        total_de_dias = self.juego.estrategia_enemiga
        
        recursos_actuales = {x.nombre:x.cantidad for x in self.juego.castillo.recursos}
        
        while dia_actual < len(total_de_dias):
            # TODO
            # Imprimir el estado del dia actal
            # - Poder de oleada
            # - Recuros
            # - Uso de los habitantes hasta ahora
            # - etc
            poder_enemigo_ronda_actual = self.juego.estrategia_enemiga[dia_actual]
            print("Poder del enemigo en la oleada:", poder_enemigo_ronda_actual)
            for rec_name in recursos_actuales:
                print(rec_name, "->", recursos_actuales[rec_name])
            
            # TODO
            # Recibir la entrada de las variables por parte del usuario y verificar
            # que cumplan los requerimientos del problema
            # - artesanos para contruir armas
            # - armas construidas (tiene que estar previamente mandadas a constuir)
            # - guerreros asignados a las armas (tienen que estar constuidas)
            # - las armas con guerreros asignados son las que generan ataque
            # - no exceder el numero máximo de guerreros y artesanos en las asignaciones por día
            # - Actualizar el estado actual de los recursos etc
            
            # TODO
            # Verificar si cumple que el ataque generado por las armas puede repeler la oleada enemiga
            
            
            
class JuegoSimulacion(Juego):
    
    def generar_modelo(self) -> Modelo:
        return ModeloSimulacion(self)