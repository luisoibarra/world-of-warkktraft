# Castle Defense

Se presenta un juego sencillo en el cual se necesita defender un castillo de oleadas de ataques. Para la defensa el castillo posee unos recursos iniciales y una fuerza de trabajo constituída por Artesanos y Guerreros. Los Artesanos pueden construir Armas que sirven para defender el castillo, estas Armas solo cuentan en la defensa mientras los Guerreros las utilicen.

## Modelo

Se modeló el problema anterior como un problema de optimización lineal discreto usando el GEKKO como solucionador de problemas. Para más información ver `castle_defense_discrete/CastleDefense.ipynb`

## API

Se implementó una API capaz de representar fácilmente este tipo de problemas con el objetivo de poder usar la misma representación para diferentes objetivos, como por ejemplo usar otro solucionador o hacer un simulador del juego en el que el usuario interactúe y sea el que tome la decisiones.

## Correr el programa

1. Correr setup.sh. Esto instalará los paquetes necesarios de Python, por lo que solo es necesario correrlo la primera vez.

2. Asegurarse de tener la terminal en la misma carpeta que el archivo `main.py`.

3. En la terminal correr `python3 main.py` o `python main.py`.

## TODO

- Hacer más niveles.
- README-Informe