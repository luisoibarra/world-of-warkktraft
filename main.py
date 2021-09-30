from Castle import *
from CastleGEKKO import JuegoGEKKO

recursos = [
    Recurso("Madera", 100),
    Recurso("Hierro", 100),
    Recurso("Cuero", 100),
]

habitantes = [
    Artesano(10),
    Guerrero(10),
]

armas = [
    Arma(10, 1, "Hacha", [
        Recurso("Madera", 10),
        Recurso("Hierro", 10),
        Recurso("Cuero", 10),
    ], Artesano(1), Guerrero(1)),
    Arma(10, 1, "Espada", [
        Recurso("Madera", 10),
        Recurso("Hierro", 10),
        Recurso("Cuero", 10),
    ], Artesano(1), Guerrero(1)),
    Arma(30, 2, "Catapulta", [
        Recurso("Madera", 10),
        Recurso("Hierro", 10),
        Recurso("Cuero", 10),
    ], Artesano(2), Guerrero(2)),
]

castillo = Castillo(habitantes[0], habitantes[1], recursos, armas)

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

juego = JuegoGEKKO(castillo, estrategia)

modelo = juego.generar_modelo()