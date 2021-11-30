from typing import Tuple
from castle_defense_discrete.castle_simulation import JuegoSimulacion
from castle_defense_discrete.castle import *
from castle_defense_discrete.castle_gekko import JuegoGEKKO

def configuracion_juego1() -> Tuple[Castillo,EstrategiaEnemiga]:
    recursos = [
        Recurso("Madera", 100),
        Recurso("Hierro", 100),
        Recurso("Cuero", 100),
    ]
    # recursos = { # Se puede usar un diccionario para los recursos
    #     "Madera": 100,
    #     "Hierro": 100,
    #     "Cuero": 100,
    # }

    armas = [
        Arma(10, None, "Hacha", [
            Recurso("Madera", 15),
            Recurso("Hierro", 5),
            Recurso("Cuero", 0), # Se puede omitir si no se pone
        ], Artesano(1), Guerrero(1)),
        Arma(10, None, "Espada", [
            Recurso("Hierro", 15), # El orden no tiene que ser el mismo
            Recurso("Madera", 5),
        ], Artesano(1), 1), # Se puede simplemente poner el número 
        Arma(30, None, "Catapulta", { # Como diccionario también funciona
            "Madera": 10,
            "Hierro": 20,
            "Cuero": 20,
        }, 2, Guerrero(2)), # También en el artesano
    ]

    castillo = Castillo(Artesano(10), Guerrero(10), recursos, armas)

    ataque_enemigo = [
        # Paz
        0, # Se puede poner un número normal
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        # Ataque
        AtaqueEnemigo(10),
        AtaqueEnemigo(10),
        AtaqueEnemigo(10),
        AtaqueEnemigo(150),
    ]

    estrategia = EstrategiaEnemiga(ataque_enemigo)
    
    return castillo, estrategia

def juego1() -> JuegoGEKKO:
    """
    Prueba los fundamentos del juego
    """
    
    castillo, estrategia = configuracion_juego1()

    return JuegoGEKKO(castillo, estrategia)

def configuracion_juego2() -> Tuple[Castillo,EstrategiaEnemiga]:
    recursos = [
        Recurso("Oro", 1000)
    ]
    
    arma1 = Arma(0, None, "Parte1", [Recurso("Oro", 100)], Artesano(2), Guerrero(10000))
    arma2 = Arma(0, arma1, "Parte2", [Recurso("Oro", 200)], Artesano(3), Guerrero(10000))
    arma3 = Arma(100, arma2, "ArmaFinal", [Recurso("Oro", 200)], Artesano(4), Guerrero(2))
    
    castillo = Castillo(Artesano(8), Guerrero(5), recursos, [arma1,arma2,arma3])
    
    estrategia = EstrategiaEnemiga([
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(200),
    ])
    return castillo, estrategia

def juego2() -> JuegoGEKKO:
    """
    El juego prueba la dependencia de las armas
    """
    
    castillo, estrategia = configuracion_juego2()
    
    return JuegoGEKKO(castillo, estrategia)

def juego3() -> JuegoSimulacion:
    """
    Simula el juego 1, ya con el usuario jugando
    """
    
    castillo, estrategia = configuracion_juego1()
    
    return JuegoSimulacion(castillo, estrategia)

def juego4() -> JuegoSimulacion:
    """
    Simula el juego 2, ya con el usuario jugando
    """
    
    castillo, estrategia = configuracion_juego2()
    
    return JuegoSimulacion(castillo, estrategia)


# juego = juego1()
juego = juego2()
# juego = juego3()
# juego = juego4()

juego.correr()