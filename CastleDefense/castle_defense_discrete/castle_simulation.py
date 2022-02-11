from typing import Callable, List, Optional, Tuple, Dict

from castle import Arma, AtaqueEnemigo, Castillo, Juego, Modelo, Recurso

class Accion:

    def __init__(self, nombre) -> None:
        self.nombre = nombre

    @staticmethod
    def accion_desde_entrada():
        raise NotImplementedError()

class PasarTurno(Accion):
    """
    Acción que se simboliza que el usuario terminó su turno
    """

    def __init__(self) -> None:
        super().__init__("Pasar Turno")

    @staticmethod
    def accion_desde_entrada():
        return PasarTurno()

class AsignarArtesanoArma(Accion):
    """
    Acción que se simboliza que un artesano se va a encargar de construir el arma
    con el nombre dado
    """

    def __init__(self, nombre_arma: str) -> None:
        super().__init__(f"Asignar artesano a arma {nombre_arma}")
        self.nombre_arma = nombre_arma

    @staticmethod
    def accion_desde_entrada():
        nombre = input("Nombre de arma: ")
        return AsignarArtesanoArma(nombre)

class DesasignarArtesanoArma(Accion):
    """
    Acción que se simboliza que un artesano se va a dejar de encargar de construir el arma
    con el nombre dado
    """

    def __init__(self, nombre_arma: str) -> None:
        super().__init__(f"Desasignar artesano a arma {nombre_arma}")
        self.nombre_arma = nombre_arma

    @staticmethod
    def accion_desde_entrada():
        nombre = input("Nombre de arma: ")
        return DesasignarArtesanoArma(nombre)

class AsignarGuerreroArma(Accion):
    """
    Acción que se simboliza que un guerrero se va a encargar de manejar el arma
    con el nombre dado
    """

    def __init__(self, nombre_arma: str) -> None:
        super().__init__(f"Asignar guerrero a arma {nombre_arma}")
        self.nombre_arma = nombre_arma

    @staticmethod
    def accion_desde_entrada():
        nombre = input("Nombre de arma: ")
        return AsignarGuerreroArma(nombre)

class DesasignarGuerreroArma(Accion):
    """
    Acción que se simboliza que un guerrero se va a dejar de encargar de manejar el arma
    con el nombre dado
    """

    def __init__(self, nombre_arma: str) -> None:
        super().__init__(f"Desasignar guerrero a arma {nombre_arma}")
        self.nombre_arma = nombre_arma

    @staticmethod
    def accion_desde_entrada():
        nombre = input("Nombre de arma: ")
        return DesasignarGuerreroArma(nombre)

class EstadoDeJuego:

    # Campos que se copian del estado
    __DATA_FIELDS = [
        'recursos',
        'armas',
        'artesanos',
        'guerreros',
        'ataques_por_turno',
        'turno',
        'estado',
        'asignacion_armas_guerreros',
        'asignacion_armas_artesanos',
        'armas_construidas'
    ]

    CORRIENDO = "CORRIENDO"
    GANADO = "GANADO"
    PERDIDO = "PERDIDO"

    def __init__(self,  recursos: Dict[str,Recurso] = [], 
                        armas: Dict[str,Arma] = [], 
                        artesanos: int = 0, 
                        guerreros: int = 0, 
                        ataques_por_turno: List[AtaqueEnemigo] = [],
                        turno: int = 0,
                        estado: str = "CORRIENDO",
                        asignacion_armas_guerreros: Dict[str, int] = {},
                        asignacion_armas_artesanos: Dict[str, int] = {},
                        armas_construidas: Dict[str, int] = {},
                        juego: Juego = None) -> None:
        
        if juego is not None:
            self.__asignar_campos_iniciales(
                {x.nombre:x for x in juego.castillo.recursos.copy()},
                {x.nombre:x for x in juego.castillo.armas.copy()},
                juego.castillo.artesanos.cantidad,
                juego.castillo.guerreros.cantidad,
                juego.estrategia_enemiga.ataques.copy(),
                0,
                EstadoDeJuego.CORRIENDO,
                { x.nombre:0 for x in juego.castillo.armas },
                { x.nombre:0 for x in juego.castillo.armas },
                { x.nombre:0 for x in juego.castillo.armas },
            )
        else:
            self.__asignar_campos_iniciales(
                recursos,
                armas,
                artesanos,
                guerreros,
                ataques_por_turno,
                turno,
                estado,
                asignacion_armas_guerreros,
                asignacion_armas_artesanos,
                armas_construidas
            )

    def __asignar_campos_iniciales(self, recursos: Dict[str,Recurso], 
                                         armas: Dict[str,Arma], 
                                         artesanos: int, 
                                         guerreros: int, 
                                         ataques_por_turno: List[AtaqueEnemigo],
                                         turno: int,
                                         estado: str,
                                         asignacion_armas_guerreros: Dict[str, int],
                                         asignacion_armas_artesanos: Dict[str, int],
                                         armas_construidas: Dict[str, int]):
        self.recursos = recursos
        self.armas = armas
        self.artesanos = artesanos
        self.guerreros = guerreros
        self.ataques_por_turno = ataques_por_turno
        self.turno = turno
        self.estado = estado,
        # Diccionario nombre de arma -> cantidad de artesanos asignados a esta
        self.asignacion_armas_artesanos = asignacion_armas_artesanos
        # Diccionario nombre de arma -> cantidad de guerreros asignados a esta
        self.asignacion_armas_guerreros = asignacion_armas_guerreros
        self.armas_construidas = armas_construidas

    @property
    def dano_actual(self):
        dano = 0
        for (nombre_arma, guerreros_asignados) in self.asignacion_armas_guerreros.items():
            arma = self.armas[nombre_arma]
            dano += (min(guerreros_asignados // arma.guerreros.cantidad, self.armas_construidas[nombre_arma])) * arma.ataque
        return dano

    @property
    def artesanos_usados(self):
        return sum(self.asignacion_armas_artesanos.values())

    @property
    def guerreros_usados(self):
        return sum(self.asignacion_armas_guerreros.values())

    def reaccionar_a(self, accion: Accion) -> Tuple[str, 'EstadoDeJuego']:
        """
        Devuelve un string con una descripcion del error si hubo alguno y el proximo
        estado del juego. En caso de haber un error el estado no cambiará
        """
        if isinstance(accion, AsignarArtesanoArma):
            return self._reaccionar_a_asignar_artesano_arma(accion)
        if isinstance(accion, AsignarGuerreroArma):
            return self._reaccionar_a_asignar_guerrero_arma(accion)
        if isinstance(accion, DesasignarGuerreroArma):
            return self._reaccionar_a_desasignar_guerrero_arma(accion)
        if isinstance(accion, DesasignarArtesanoArma):
            return self._reaccionar_a_desasignar_artesano_arma(accion)
        if isinstance(accion, PasarTurno):
            return self._reaccionar_a_pasar_turno(accion)
            
        return f"El tipo de la acción {accion} no está manejado", self.copy()


    def _reaccionar_a_asignar_artesano_arma(self, accion: AsignarArtesanoArma) ->  Tuple[str, 'EstadoDeJuego']:
        """
        Reacciona ante la asignación de un artesano a un arma
        """
        if accion.nombre_arma not in self.asignacion_armas_artesanos:
            return f"El arma con nombre {accion.nombre_arma} no existe", self.copy_with()
        if self.artesanos_usados < self.artesanos:
            arma = self.armas[accion.nombre_arma]
            arma_que_depende = arma.depende
            artesanos_arma = self.asignacion_armas_artesanos.copy()
            artesanos_arma[accion.nombre_arma] += 1

            if arma_que_depende is not None:
                cant_dep_arma = self._armas_dependientes_de(arma_que_depende.nombre, artesanos_arma)
                if self.armas_construidas[arma_que_depende.nombre] <= cant_dep_arma:
                    return "No tiene la cantidad de armas suficiente para construir una nueva arma de este tipo", self.copy_with()

            feedback, recursos = self._comprobar_recursos_asignar_artesanos(accion.nombre_arma, self.recursos, artesanos_arma)
            if recursos is None:
                return feedback, self.copy_with()
            return "OK", self.copy_with(asignacion_armas_artesanos=artesanos_arma, recursos=recursos)
        else:
            return "La asignación de artesanos está al máximo", self.copy_with()

    def _reaccionar_a_desasignar_artesano_arma(self, accion: DesasignarArtesanoArma) ->  Tuple[str, 'EstadoDeJuego']:
        """
        Reacciona ante el pedido de desasignar un artesano de un arma
        """
        if accion.nombre_arma not in self.asignacion_armas_artesanos:
            return f"El arma con nombre {accion.nombre_arma} no existe", self.copy_with()
        artesanos_arma = self.asignacion_armas_artesanos.copy()
        if artesanos_arma[accion.nombre_arma] > 0:
            artesanos_arma[accion.nombre_arma] -= 1
            feedback, recursos = self._comprobar_recursos_desasignar_artesanos(accion.nombre_arma, self.recursos, artesanos_arma)
            if recursos is None:
                return feedback, self.copy_with()
            return "OK", self.copy_with(asignacion_armas_artesanos=artesanos_arma, recursos=recursos)
        else:
            return "La asignación de artesanos está en 0", self.copy_with()


    def _reaccionar_a_asignar_guerrero_arma(self, accion: AsignarGuerreroArma) ->  Tuple[str, 'EstadoDeJuego']:
        """
        Reacciona ante la asignación de un guerrero a un arma
        """
        if accion.nombre_arma not in self.asignacion_armas_guerreros:
            return f"El arma con nombre {accion.nombre_arma} no existe", self.copy_with()
        if self.guerreros_usados < self.guerreros:
            if self.armas_construidas[accion.nombre_arma] == 0:
                return f"No tiene construída ninguna arma de este tipo", self.copy_with()
            guerreros_arma = self.asignacion_armas_guerreros.copy()
            guerreros_arma[accion.nombre_arma] += 1
            return "OK", self.copy_with(asignacion_armas_guerreros=guerreros_arma)
        else:
            return "La asignación de guerreros está al máximo", self.copy_with()

    def _reaccionar_a_desasignar_guerrero_arma(self, accion: DesasignarGuerreroArma) ->  Tuple[str, 'EstadoDeJuego']:
        """
        Reacciona ante el pedido de desasignar un guerrero del manejo de un arma
        """
        if accion.nombre_arma not in self.asignacion_armas_guerreros:
            return f"El arma con nombre {accion.nombre_arma} no existe", self.copy_with()
        guerreros_arma = self.asignacion_armas_guerreros.copy()
        if guerreros_arma[accion.nombre_arma] > 0:
            guerreros_arma[accion.nombre_arma] -= 1
            return "OK", self.copy_with(asignacion_armas_guerreros=guerreros_arma)
        else:
            return "La asignación de guerreros es actualmente 0", self.copy_with()


    def _reaccionar_a_pasar_turno(self, accion: PasarTurno) ->  Tuple[str, 'EstadoDeJuego']:
        """
        Reacciona ante el pedido de pasar turno
        """
        siguiente_turno = self.turno + 1
        armas_dicc_vacio = { x:0 for x in self.armas }
        nuevas_armas_construidas = self._armas_a_construir_en_turno(self.asignacion_armas_artesanos)
        nuevas_armas = { x:self.armas_construidas[x] + nuevas_armas_construidas[x] for x in self.armas_construidas}
        if self.turno == len(self.ataques_por_turno):
            return "GANÓ", self.copy_with(turno=siguiente_turno, 
                                          armas_construidas=nuevas_armas,
                                          asignacion_armas_artesanos=armas_dicc_vacio.copy(), 
                                          asignacion_armas_guerreros=armas_dicc_vacio.copy(),
                                          estado=self.GANADO)
        if self.dano_actual >= self.ataques_por_turno[self.turno].poder:
            return "OK", self.copy_with(turno=siguiente_turno,
                                        armas_construidas=nuevas_armas,
                                        asignacion_armas_artesanos=armas_dicc_vacio.copy(), 
                                        asignacion_armas_guerreros=armas_dicc_vacio.copy())
        else:
            self.dano_actual < self.ataques_por_turno[self.turno].poder
            return "PERDIÓ el daño del enemigo supera al que puede causar", self.copy_with(turno=siguiente_turno,estado=self.PERDIDO) 


    def _comprobar_recursos_desasignar_artesanos(self, nombre_arma:str, 
                                                    recursos_actuales: Dict[str, Recurso], 
                                                    asignacion_armas_artesanos: Dict[str,int]) -> Tuple[str, Dict[str,Recurso]]:
        if nombre_arma not in asignacion_armas_artesanos:
            return f"El arma con nombre {nombre_arma} no existe", None


        arma = self.armas[nombre_arma]
        # La cantidad de artesanos no supera la necesaria para hacer el pedido
        if asignacion_armas_artesanos[nombre_arma] % arma.artesanos.cantidad != 0:
            return "Ok", recursos_actuales.copy()

        recursos = recursos_actuales.keys()

        recursos_totales_a_apagar = [(recurso, total, precio) for (recurso, total, precio) in 
                zip(recursos,
                    [recursos_actuales[x].cantidad for x in recursos],
                    [next(x.cantidad for x in arma.recursos if x.nombre == nombre) for nombre in recursos])]

        nuevos_recursos = {recurso:Recurso(recurso, total + precio) for (recurso, total, precio) in recursos_totales_a_apagar}
        return "OK", nuevos_recursos

    def _comprobar_recursos_asignar_artesanos(self, nombre_arma:str, 
                                                    recursos_actuales: Dict[str, Recurso], 
                                                    asignacion_armas_artesanos: Dict[str,int]) -> Tuple[str, Dict[str,Recurso]]:
        if nombre_arma not in asignacion_armas_artesanos:
            return f"El arma con nombre {nombre_arma} no existe", None


        arma = self.armas[nombre_arma]
        # La cantidad de artesanos no supera la necesaria para hacer el pedido
        if asignacion_armas_artesanos[nombre_arma] % arma.artesanos.cantidad != 0:
            return "Ok", recursos_actuales.copy()

        recursos = recursos_actuales.keys()

        recursos_totales_a_apagar = [(recurso, total, precio) for (recurso, total, precio) in 
                zip(recursos,
                    [recursos_actuales[x].cantidad for x in recursos],
                    [next(x.cantidad for x in arma.recursos if x.nombre == nombre) for nombre in recursos])]

        # Todos los precios se cumplen
        if all(total >= precio for _,total,precio in recursos_totales_a_apagar):
            nuevos_recursos = {recurso:Recurso(recurso, total - precio) for (recurso, total, precio) in recursos_totales_a_apagar}
            return "OK", nuevos_recursos
        return f"No se satisfacen las necesidades de los recursos {' '.join([x for x,t,p in recursos_totales_a_apagar if t < p])}", None

    def _armas_a_construir_en_turno(self, asignacion_armas_artesanos: Dict[str,int]) -> Dict[str,int]:
        """
        Devuelve la cantidad de armas que se construiran en el turno en caso de acabar este
        """
        armas = {}
        for x in asignacion_armas_artesanos:
            asignados = asignacion_armas_artesanos[x]
            arma = self.armas[x]
            armas[x] = asignados // arma.artesanos.cantidad
        return armas
    
    def _armas_dependientes_de(self, nombre_arma: str, asignacion_armas_artesanos: Dict[str,int]) -> int:
        """
        Devuelve la cantidad de armas que dependen y depenedran en el proximo turno del arma 
        """
        dep = [x for x in self.armas.values() if x.depende is not None and x.depende.nombre == nombre_arma]
        construidas = sum(self.armas_construidas[x.nombre] for x in dep)
        por_construir = sum(constr for x,constr in self._armas_a_construir_en_turno(asignacion_armas_artesanos).items() if x == nombre_arma)
        return construidas + por_construir

    def __str__(self) -> str:
        nl = "\n"
        string = \
f"""
Turno {self.turno}
Artesanos disponibles: {self.artesanos - self.artesanos_usados}
Guerreros disponibles: {self.guerreros - self.guerreros_usados}
Recursos disponibles: 
{nl.join([f"{x}: {y}" for x,y in self.recursos.items()])}
Daño a realizar: {self.dano_actual}
Daño a repeler: {self.ataques_por_turno[self.turno] if self.turno < len(self.ataques_por_turno) else 'No Ataque'}
Asiganciones Artesanos:
{nl.join([f"{x}: {y}" for x,y in self.asignacion_armas_artesanos.items()])}
Asiganciones Guerreros:
{nl.join([f"{x}: {y}" for x,y in self.asignacion_armas_guerreros.items()])}
Armas Construidas:
{nl.join([f"{x}: {y}" for x,y in self.armas_construidas.items()])}

"""
        return string

    def copy_with(self, **kwargs) -> 'EstadoDeJuego':
        parametros_completos = kwargs.copy()
        for x in set(self.__DATA_FIELDS).difference(parametros_completos.keys()):
            try:
                parametros_completos[x] = self.__getattribute__(x).copy()
            except:
                parametros_completos[x] = self.__getattribute__(x)
        return EstadoDeJuego(**parametros_completos)


def devolver_accion(estado: EstadoDeJuego) -> Accion:
    """
    Devuelve la accion que desea realizar el usuario
    """

    acciones_posibles = {
        "1": ("Asignar artesano a arma",AsignarArtesanoArma),
        "2": ("Asignar guerrero a arma",AsignarGuerreroArma),
        "3": ("Desasignar artesano a arma",DesasignarArtesanoArma),
        "4": ("Desasignar guerrero a arma",DesasignarGuerreroArma),
        "5": ("Pasar turno",PasarTurno),
    }

    print("Seleccione la accion a realizar:")
    for opt, (msg, tipo_accion) in acciones_posibles.items():
        print(f"{opt}: {msg}")
    accion = None
    while accion not in acciones_posibles:
        accion = input(">>")
        if accion in acciones_posibles:
            _,tipo_accion = acciones_posibles[accion]
            return tipo_accion.accion_desde_entrada()
        else:
            print("Elección inválida")


class ModeloSimulacion(Modelo):
    
    def __init__(self, juego: 'JuegoSimulacion', pedir_accion: Callable[[EstadoDeJuego], Accion], retroalimentacion_accion: Callable[[str], None]) -> None:
        super().__init__()
        self.juego = juego # Desde aqui es accesible el castillo y la estrategia del enemigo
        self.pedir_accion = pedir_accion
        self.retroalimentacion_accion = retroalimentacion_accion
        
    def solve(self):
        """
        Recrea el juego en interacción con el usuario
        """
        
        estado = EstadoDeJuego(juego=self.juego)
        while estado.estado != estado.CORRIENDO:
            print(estado)
            accion = self.pedir_accion(estado)
            msg, estado = estado.reaccionar_a(accion)
            self.retroalimentacion_accion(msg)
            print(msg)

        print("Has", estado.estado)
            
            
class JuegoSimulacion(Juego):
    
    def generar_modelo(self) -> Modelo:
        return ModeloSimulacion(self, devolver_accion, lambda x: None)