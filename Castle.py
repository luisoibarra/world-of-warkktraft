
from typing import List

class Habitante:
    def __init__(self, nombre: str, cantidad: int) -> None:
        self.nombre = nombre
        self.cantidad = cantidad
      
    def __repr__(self) -> str:
        return str(self)
          
    def __str__(self) -> str:
        return f"{self.nombre}, Cantidad: {self.cantidad}"

class Artesano(Habitante):
    def __init__(self, cantidad: int) -> None:
        super().__init__("Artesano", cantidad)

class Guerrero(Habitante):
    def __init__(self, cantidad: int) -> None:
        super().__init__("Guerrero", cantidad)

class Recurso:
    def __init__(self, nombre: str, cantidad: int) -> None:
        self.nombre = nombre
        self.cantidad = cantidad

    def __str__(self) -> str:
        return f"Recurso: {self.nombre}, Cantidad: {self.cantidad}"
    
    def __repr__(self) -> str:
        return str(self)

class Arma:
    def __init__(self, ataque:int, demora: int, nombre: str, recursos: List[Recurso], artesanos: Artesano, guerreros: Guerrero) -> None:
        self.ataque = ataque
        self.demora = demora
        self.nombre = nombre
        self.recursos = recursos
        self.artesanos = artesanos
        self.guerreros = guerreros
        
    def __str__(self) -> str:
        return f"Arma: {self.nombre}, Ataque: {self.ataque}, Demora: {self.demora}, Artesanos: {self.artesanos.cantidad}, Guerreros: {self.guerreros.cantidad}, Recursos: {self.recursos}"
    
    def __repr__(self) -> str:
        return str(self)
    
class Castillo:
    def __init__(self, artesanos: Artesano, guerreros: Guerrero, recursos: List[Recurso], armas: List[Arma]) -> None:
        self.recursos = recursos
        self.artesanos = artesanos
        self.guerreros = guerreros
        self.armas = armas

class AtaqueEnemigo:
    def __init__(self, poder: int) -> None:
        self.poder = poder

class EstrategiaEnemiga:
    def __init__(self, ataques = List[AtaqueEnemigo]) -> None:
        self.ataques = ataques

class Modelo:
    def solve(self):
        pass

class Juego:
    def __init__(self, castillo: Castillo, estrategia_enemiga: EstrategiaEnemiga) -> None:
        self.castillo = castillo    
        self.estrategia_enemiga = estrategia_enemiga
        
    def generar_modelo(self)->Modelo:
        pass
 