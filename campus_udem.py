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
    def aem_visitantes(self) -> tuple:
        if self.tamano == 0:
            return (0, [])

        vertices = list(self.listaAdy.keys())
        visitados = [vertices[0]]
        conexiones_arbol = []
        peso_total = 0

        while len(visitados) < self.tamano:
            peso_minimo = float('inf')
            origen_elegido = None
            destino_elegido = None

            for vertice in visitados:
                for arista in self.listaAdy[vertice]:
                    vecino, distancia, tiempo, congestion, accesible, estado = arista
                    if vecino not in visitados and estado == self.DISPONIBLE:
                        if distancia < peso_minimo:
                            peso_minimo = distancia
                            origen_elegido = vertice
                            destino_elegido = vecino

            if destino_elegido is None:
                break

            visitados.append(destino_elegido)
            conexiones_arbol.append((origen_elegido, destino_elegido, peso_minimo))
            peso_total += peso_minimo

        return (peso_total, conexiones_arbol)
campus = GrafoUDeM()

#                        origen                          destino                         dist  tpo  cong  acc    estado
# Portería principal
campus.agregarCamino("Portería Cra. 87",               "Bloque Administrativo",          90,   2,   7,  True,  "disponible")
campus.agregarCamino("Portería Cra. 87",               "Parqueadero Principal",          60,   1,   8,  True,  "disponible")
campus.agregarCamino("Portería Cra. 87",               "Bloque Audiovisuales",          120,   3,   5,  True,  "disponible")

# Zona administrativa y central
campus.agregarCamino("Bloque Administrativo",          "Biblioteca Eduardo F. Botero",   80,   2,   4,  True,  "disponible")
campus.agregarCamino("Bloque Administrativo",          "Bloque Comunicación e Idiomas",  70,   2,   5,  True,  "disponible")
campus.agregarCamino("Bloque Administrativo",          "Sello Editorial",                50,   1,   3,  True,  "disponible")

# Zona académica (Bloques 5, 6, 7 - Junin)
campus.agregarCamino("Biblioteca Eduardo F. Botero",   "Bloque 5 (Derecho)",             90,   2,   5,  True,  "disponible")
campus.agregarCamino("Biblioteca Eduardo F. Botero",   "CDC (Centro de Cómputo)",        70,   2,   6,  True,  "disponible")
campus.agregarCamino("Bloque 5 (Derecho)",             "Bloque 6 (Ingenierías)",         60,   1,   6,  True,  "disponible")
campus.agregarCamino("Bloque 6 (Ingenierías)",         "Bloque 7 (Ciencias Básicas)",    55,   1,   5,  True,  "mantenimiento")
campus.agregarCamino("Bloque 6 (Ingenierías)",         "CDC (Centro de Cómputo)",        80,   2,   7,  False, "disponible")

# Zona de Comunicacion y Medios
campus.agregarCamino("Bloque Comunicación e Idiomas",  "Bloque Audiovisuales",           65,   2,   4,  True,  "disponible")
campus.agregarCamino("Bloque Audiovisuales",           "Medios Educativos",              55,   1,   3,  True,  "disponible")
campus.agregarCamino("Medios Educativos",              "Bloque Ciencias Sociales",       70,   2,   4,  True,  "disponible")

# Teatro
campus.agregarCamino("Bloque Administrativo",          "Teatro Gabriel Obregón",        130,   3,   4,  True,  "disponible")
campus.agregarCamino("Teatro Gabriel Obregón",         "Bloque Ciencias Sociales",       75,   2,   3,  True,  "disponible")
campus.agregarCamino("Teatro Gabriel Obregón",         "Zona Deportiva / Coliseo",      160,   4,   2,  True,  "disponible")

# CDC y zona tecnológica
campus.agregarCamino("CDC (Centro de Cómputo)",        "Bloque 7 (Ciencias Básicas)",    90,   2,   4,  False, "disponible")
campus.agregarCamino("CDC (Centro de Cómputo)",        "Sello Editorial",               100,   3,   2,  True,  "disponible")

# Zona Deportiva
campus.agregarCamino("Zona Deportiva / Coliseo",       "Parqueadero Principal",         140,   4,   2,  True,  "disponible")
campus.agregarCamino("Zona Deportiva / Coliseo",       "Bloque 7 (Ciencias Básicas)",   120,   3,   3,  True,  "disponible")

# Porteria Metroplús
campus.agregarCamino("Portería Metroplús",             "Bloque Comunicación e Idiomas",  80,   2,   6,  True,  "disponible")
campus.agregarCamino("Portería Metroplús",             "Bloque Audiovisuales",           95,   3,   5,  True,  "disponible")
campus.agregarCamino("Portería Metroplús",             "Teatro Gabriel Obregón",        110,   3,   4,  True,  "bloqueado")

# MENÚ PRINCIPAL


def mostrar_lugares():
    print("\n  Lugares del campus Universidad de Medellín:")
    for i, lugar in enumerate(campus.listaAdy.keys(), 1):
        print(f"    {i:2}. {lugar}")

def seleccionar_lugar(mensaje: str) -> str:
    lugares = list(campus.listaAdy.keys())
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit():
            idx = int(entrada) - 1
            if 0 <= idx < len(lugares):
                return lugares[idx]
        elif entrada in lugares:
            return entrada
        print("  Opción inválida, intenta de nuevo.")

def menu_ruta():

    print("          BUSCAR RUTA EN EL CAMPUS")

    mostrar_lugares()

    origen  = seleccionar_lugar("\n  Número del lugar de ORIGEN  : ")
    destino = seleccionar_lugar("  Número del lugar de DESTINO : ")

    print("\n  Criterio de búsqueda:")
    print("    1. Ruta más corta por distancia")
    print("    2. Ruta más rápida por tiempo")
    print("    3. Ruta con menor congestión")
    print("    4. Ruta accesible para personas con movilidad reducida")

    opciones = {
        "1": GrafoUDeM.CRITERIO_DISTANCIA,
        "2": GrafoUDeM.CRITERIO_TIEMPO,
        "3": GrafoUDeM.CRITERIO_CONGESTION,
        "4": GrafoUDeM.CRITERIO_ACCESIBLE,
    }

    criterio_input = input("\n  Selecciona criterio (1-4): ").strip()
    criterio = opciones.get(criterio_input)

    if criterio is None:
        print("   Opción inválida.")
        return

    costo, camino, explicacion = campus.dijkstra(origen, destino, criterio)

    print("\n" + "─" * 50)
    if not camino:
        print(f"   {explicacion}")
    else:
        unidades = {
            GrafoUDeM.CRITERIO_DISTANCIA:  "metros",
            GrafoUDeM.CRITERIO_TIEMPO:     "minutos",
            GrafoUDeM.CRITERIO_CONGESTION: "unidades de congestión",
            GrafoUDeM.CRITERIO_ACCESIBLE:  "metros (ruta accesible)",
        }
        print(f"   Costo total : {costo:.1f} {unidades[criterio]}")
        print(f"\n  {explicacion}")
    print("─" * 50)

def menu_visitantes():
    print("  RECORRIDO DE VISITANTES — Árbol de Expansión Mínimo")


    peso_total, conexiones = campus.aem_visitantes()

    if not conexiones:
        print("   No se pudo calcular el AEM.")
        return

    print(f"\n  Recorrido sugerido para visitar todos los lugares del campus UdeM.")
    print(f"  Distancia total del recorrido: {peso_total:.0f} metros\n")
    print("  Conexiones del recorrido:")
    for i, (origen, destino, dist) in enumerate(conexiones, 1):
        print(f"    {i:2}. {origen}")
        print(f"         └─► {destino}  ({dist:.0f} m)")

def main():
    print("\n" + "═" * 55)
    print("   Sistema de Rutas — Universidad de Medellín")
    print("   Carrera 87 N° 30-65, Belén Los Alpes, Medellín")
    print("═" * 55)

    while True:
        print("\n  Menú principal:")
        print("    1. Buscar ruta entre dos lugares")
        print("    2. Ver recorrido para visitantes (AEM)")
        print("    3. Salir")

        opcion = input("\n  Selecciona una opción: ").strip()

        if opcion == "1":
            menu_ruta()
        elif opcion == "2":
            menu_visitantes()
        elif opcion == "3":
            print("\n  ¡Hasta luego!\n")
            break
        else:
            print("   Opción inválida.")


if __name__ == "__main__":
    main()


    
