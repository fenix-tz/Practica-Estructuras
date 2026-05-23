from typing import Any, List, Dict
from collections import deque


class GrafoUDeM:

    CRITERIO_DISTANCIA  = "distancia"
    CRITERIO_TIEMPO     = "tiempo"
    CRITERIO_CONGESTION = "congestion"
    CRITERIO_ACCESIBLE  = "accesible"

    DISPONIBLE    = "disponible"
    BLOQUEADO     = "bloqueado"
    MANTENIMIENTO = "mantenimiento"

    def __init__(self):
        self.listaAdy: Dict[Any, List[tuple]] = {}
        self.tamano: int = 0

    def agregarVertice(self, valor: Any):
        if valor in self.listaAdy:
            return
        self.listaAdy[valor] = []
        self.tamano += 1

    def agregarCamino(self, origen, destino,
                      distancia: float, tiempo: float,
                      congestion: int, accesible: bool,
                      estado: str, dirigido: bool = False):
        
        if origen not in self.listaAdy:
            self.agregarVertice(origen)
        if destino not in self.listaAdy:
            self.agregarVertice(destino)

        destinos_actuales = [v[0] for v in self.listaAdy[origen]]
        if destino not in destinos_actuales:
            self.listaAdy[origen].append(
                (destino, distancia, tiempo, congestion, accesible, estado)
            )

        if not dirigido:
            destinos_actuales2 = [v[0] for v in self.listaAdy[destino]]
            if origen not in destinos_actuales2:
                self.listaAdy[destino].append(
                    (origen, distancia, tiempo, congestion, accesible, estado)
                )

    def _peso_por_criterio(self, arista: tuple, criterio: str,
                           solo_accesibles: bool = False) -> float:
        _, distancia, tiempo, congestion, accesible, estado = arista

        if estado in (self.BLOQUEADO, self.MANTENIMIENTO):
            return float('inf')

        if solo_accesibles and not accesible:
            return float('inf')

        if criterio == self.CRITERIO_DISTANCIA:
            return distancia
        elif criterio == self.CRITERIO_TIEMPO:
            return tiempo
        elif criterio == self.CRITERIO_CONGESTION:
            return congestion
        else:  # ACCESIBLE: optimiza distancia entre caminos accesibles
            return distancia

    def dijkstra(self, inicio: Any, fin: Any, criterio: str) -> tuple:
        if inicio not in self.listaAdy or fin not in self.listaAdy:
            return (float('inf'), [], "Uno o ambos lugares no existen en el campus.")

        solo_accesibles = (criterio == self.CRITERIO_ACCESIBLE)

        distancias = {v: float('inf') for v in self.listaAdy}
        distancias[inicio] = 0
        predecesores = {v: None for v in self.listaAdy}
        visitados = []
        verticeActual = inicio

        while verticeActual is not None and verticeActual != fin:
            for arista in self.listaAdy[verticeActual]:
                vecino = arista[0]
                if vecino not in visitados:
                    peso = self._peso_por_criterio(arista, criterio, solo_accesibles)
                    if peso == float('inf'):
                        continue
                    nueva_dist = distancias[verticeActual] + peso
                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        predecesores[vecino] = verticeActual

            visitados.append(verticeActual)

            distanciaMenor = float('inf')
            verticeMenor = None
            for v in distancias:
                if distancias[v] < distanciaMenor and v not in visitados:
                    distanciaMenor = distancias[v]
                    verticeMenor = v
            verticeActual = verticeMenor

        if distancias[fin] == float('inf'):
            return (float('inf'), [], "No existe ruta disponible con el criterio seleccionado.")

        camino = []
        paso = fin
        while paso is not None:
            camino.insert(0, paso)
            paso = predecesores[paso]

        explicacion = self._generar_explicacion(camino, distancias[fin], criterio)
        return (distancias[fin], camino, explicacion)

    def _generar_explicacion(self, camino: list, costo: float, criterio: str) -> str:
        nombres = {
            self.CRITERIO_DISTANCIA:  ("distancia",                  "metros"),
            self.CRITERIO_TIEMPO:     ("tiempo",                     "minutos"),
            self.CRITERIO_CONGESTION: ("congestión",                 "unidades de congestión"),
            self.CRITERIO_ACCESIBLE:  ("distancia (ruta accesible)", "metros"),
        }
        etiqueta, unidad = nombres.get(criterio, ("costo", ""))
        ruta_str = " → ".join(camino)

        extra = ""
        if criterio == self.CRITERIO_ACCESIBLE:
            extra = " Solo se usaron caminos habilitados para personas con movilidad reducida."

        return (
            f"Se eligió esta ruta porque tiene el menor {etiqueta} total "
            f"({costo:.1f} {unidad}) entre todos los caminos disponibles.{extra}\n"
            f"Recorrido: {ruta_str}"
        )
