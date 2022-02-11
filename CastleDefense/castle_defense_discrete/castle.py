"""
API para crear niveles del juego
"""

from typing import Dict, List, Optional, Union
    
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
    def __init__(self, ataque:int, depende: Optional["Arma"], nombre: str, recursos: Union[List[Recurso], Dict[str, int]], artesanos: Union[int,Artesano], guerreros: Union[int,Guerrero]) -> None:
        self.ataque = ataque
        self.depende = depende
        self.nombre = nombre
        self.recursos = _convertir_a_lista_recurso(recursos)
        self.artesanos = _convertir_en_artesano_guerrero(artesanos, Artesano)
        self.guerreros = _convertir_en_artesano_guerrero(guerreros, Guerrero)
        
    def __str__(self) -> str:
        return f"Arma: {self.nombre}, Ataque: {self.ataque}, Depende: {self.depende.nombre if self.depende else 'NONE'}, Artesanos: {self.artesanos.cantidad}, Guerreros: {self.guerreros.cantidad}, Recursos: {self.recursos}"
    
    def __repr__(self) -> str:
        return str(self)
    
class Castillo:
    def __init__(self, artesanos: Union[int,Artesano], guerreros: Union[int,Guerrero], recursos: Union[List[Recurso], Dict[str, int]], armas: List[Arma]) -> None:
        self.recursos = _convertir_a_lista_recurso(recursos)
        self.artesanos = _convertir_en_artesano_guerrero(artesanos, Artesano)
        self.guerreros = _convertir_en_artesano_guerrero(guerreros, Guerrero)
        self.armas = armas

class AtaqueEnemigo:
    def __init__(self, poder: int) -> None:
        self.poder = poder

    def __str__(self) -> str:
        return f"Ataque: {self.poder}"

class EstrategiaEnemiga:
    def __init__(self, ataques: List[Union[AtaqueEnemigo,int]]) -> None:
        self.ataques = [AtaqueEnemigo(x) if isinstance(x, int) else x for x in ataques]

class Tarea:
    def __init__(self, nombre: str, recursos: List[Recurso]) -> None:
        self.nombre = nombre
        self.recursos = recursos

class Modelo:
    def solve(self):
        pass

class Juego:
    def __init__(self, nivel: 'Nivel') -> None:
        self.nivel = nivel
        self._acomodar_datos_castillo()

    @property
    def castillo(self):
        return self.nivel.castillo

    @property
    def estrategia_enemiga(self):
        return self.nivel.estrategia_enemiga

    def _acomodar_datos_castillo(self):
        """
        Realiza una modificación al `castillo` añadiendo supuestos básicos del modelo
        y realiza comprobaciones básicas
        """

        # Ordenar los recursos del castillo por nombre para que coincidan en índice 
        # con los recursos de las armas
        self.castillo.recursos.sort(key=lambda x: x.nombre) 

        cant_tipos_recursos = len(self.castillo.recursos)
        
        for arma in self.castillo.armas:
            faltantes = set([s.nombre for s in self.castillo.recursos]).difference([x.nombre for x in arma.recursos])
            for f in faltantes: # Añadir con costo 0 los recursos que no se definieron en las armas
                arma.recursos.append(Recurso(f, 0))
            # Ordenar los recursos del castillo por nombre para que coincidan en índice con los recursos del castillo
            arma.recursos.sort(key=lambda x: x.nombre)
            if cant_tipos_recursos != len(arma.recursos):
                raise Exception(f"La cantidad de tipos de recursos en el arma {arma.nombre} es diferente a la cantidad de tipos de recursos definida. Esto puede significar algún error en los nombres de los recursos al crear el arma o la omisión de alguno en la definición de estos")
        
                
                
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

Las armas se pueden demorar varios días en construirse y necesitan 
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
        print(f"Se espera un ataque de {len(self.estrategia_enemiga.ataques)} dias")
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
        modelo = self.generar_modelo()
        modelo.solve()
    
    def generar_modelo(self)->Modelo:
        raise NotImplementedError


def _convertir_a_lista_recurso(dict_recurso: Union[List[Recurso], Dict[str, int]]) -> List[Recurso]:
    if isinstance(dict_recurso, dict):
        return [Recurso(x, dict_recurso[x]) for x in dict_recurso]
    return dict_recurso

def _convertir_en_artesano_guerrero(numero: Union[int, Artesano, Guerrero], tipo_esperado) -> Union[Artesano, Guerrero]:
    if isinstance(numero, int):
        return tipo_esperado(numero)    
    return numero

class Nivel:

    FACIL = 1
    MEDIO = 2
    DIFICIL = 3

    def __init__(self, nombre: str, dificultad:int, estrategia_enemiga: EstrategiaEnemiga, castillo: Castillo) -> None:
        self.nombre = nombre
        self.dificultad = dificultad
        self.estrategia_enemiga = estrategia_enemiga
        self.castillo = castillo