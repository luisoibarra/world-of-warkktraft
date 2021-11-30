from castle import Castillo, Juego, Modelo


class ModeloSimulacion(Modelo):
    
    def __init__(self, juego: 'JuegoSimulacion') -> None:
        super().__init__()
        self.juego = juego # Desde aqui es accesible el castillo y la estrategia del enemigo
    
    def solve(self):
        """
        Recrea el juego en interacción con el usuario
        """
        raise NotImplementedError

class JuegoSimulacion(Juego):
    
    def generar_modelo(self) -> Modelo:
        return ModeloSimulacion(self)