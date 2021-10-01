
from typing import List, Optional

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
    def __init__(self, ataque:int, depende: Optional["Arma"], nombre: str, recursos: List[Recurso], artesanos: Artesano, guerreros: Guerrero) -> None:
        self.ataque = ataque
        self.depende = depende
        self.nombre = nombre
        self.recursos = recursos
        self.artesanos = artesanos
        self.guerreros = guerreros
        
    def __str__(self) -> str:
        return f"Arma: {self.nombre}, Ataque: {self.ataque}, Depende: {self.depende.nombre if self.depende else 'NONE'}, Artesanos: {self.artesanos.cantidad}, Guerreros: {self.guerreros.cantidad}, Recursos: {self.recursos}"
    
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
    
    def print_prologo(self):
        recursos = [str(x) for x in self.castillo.recursos]
        artesanos = self.castillo.artesanos.cantidad
        guerreros = self.castillo.guerreros.cantidad
        armas = [str(x) for x in self.castillo.armas]
        dias_de_espera = len(self.estrategia_enemiga.ataques)
        dias_de_llegada = next(i for i,x in enumerate(self.estrategia_enemiga.ataques) if x.poder!=0) if any(x for x in self.estrategia_enemiga.ataques if x.poder!=0) else dias_de_espera

        sep = "\n"
        pr = f"""Estás en un castillo que será asediado por una fuerza que te supera, 
por suerte tu salvación se encuentra a unos {dias_de_espera} días de espera. 
Tu misión es resistir hasta que lleguen los refuerzos. En los almacenes del 
castillo se tienes unos recursos:

{sep.join(recursos)} 

Entre tus filas cuentas con una fuerza de {artesanos} artesanos para 
confeccionar las armas necesarias y {guerreros} guerreros para defenderte. 

Las armas se pueden demorar varios dias en construirse y necesitan 
ser utilizadas por uno o varios guerreros para que sean efectivas.

Las armas que están disponibles son: 

{sep.join(armas)} 

El enemigo tardará unos {dias_de_llegada} días en llegar y luego atacará 
en oleadas cada vez más fuertes, aprovecha el tiempo que tienes para 
irte preparando para la dura batalla, construye armas que puedan 
contener las arremetidas furiosas de los malvados que quieren tomar
las vidas de tus súbditos, en las batallas asígnales estas armas 
a tus guerreros para que puedan luchar. 

Si todo sale bien seguro saldrás victorioso.

Suerte, esperemos que no queden solo ruinas para los aliados."""
        print(pr)

    
    def print_situacion(self):
        print()
        print(f"Se espera un ataque de {self.total_dias} dias")
        print(f"Cuentas inicialmente con:")
        print(f"Recursos")
        for r in self.castillo.recursos:
            print(r)
        print()
        print(f"Armas")
        for a in self.castillo.armas:
            print(a)
        print()
        print(f"Habitantes")
        print(self.castillo.artesanos)
        print(self.castillo.guerreros)
    
    def correr(self):
        self.print_prologo()
        self.print_situacion()
        # TODO Recibir input del usuario y simular el juego
        # Por ahora nos quedamos en generar el modelo
        modelo = self.generar_modelo()
        modelo.solve()
    
    def generar_modelo(self)->Modelo:
        pass
 