from Castle import *
from CastleGEKKO import JuegoGEKKO

def juego1() -> JuegoGEKKO:
    """
    Prueba los fundamentos del juego
    """
    
    recursos = [
        Recurso("Madera", 100),
        Recurso("Hierro", 100),
        Recurso("Cuero", 100),
    ]

    armas = [
        Arma(10, None, "Hacha", [
            Recurso("Madera", 15),
            Recurso("Hierro", 5),
            Recurso("Cuero", 0),
        ], Artesano(1), Guerrero(1)),
        Arma(10, None, "Espada", [
            Recurso("Madera", 5),
            Recurso("Hierro", 15),
            Recurso("Cuero", 0),
        ], Artesano(1), Guerrero(1)),
        Arma(30, None, "Catapulta", [
            Recurso("Madera", 10),
            Recurso("Hierro", 20),
            Recurso("Cuero", 20),
        ], Artesano(2), Guerrero(2)),
    ]

    castillo = Castillo(Artesano(10), Guerrero(10), recursos, armas)

    ataque_enemigo = [
        # Paz
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        # Ataque
        AtaqueEnemigo(10),
        AtaqueEnemigo(10),
        AtaqueEnemigo(10),
        AtaqueEnemigo(150),
    ]

    estrategia = EstrategiaEnemiga(ataque_enemigo)

    return JuegoGEKKO(castillo, estrategia)

def juego2() -> JuegoGEKKO:
    """
    El juego prueba la dependencia de las armas
    """
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
    
    return JuegoGEKKO(castillo, estrategia)

# juego = juego1()
juego = juego2()

juego.correr()