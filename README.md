# Practica-Estructuras-Campus UdeM
## Descripción del proyecto

El sistema modela el campus como un grafo no dirigido y ponderado donde cada lugar importante es un vértice y los caminos peatonales entre ellos son aristas. Cada camino tiene cinco atributos:

- **Distancia** en metros
- **Tiempo** estimado de recorrido en minutos
- **Nivel de congestión** del 1 (baja) al 10 (muy alta)
- **Accesibilidad** para personas con movilidad reducida
- **Estado** del camino: disponible, bloqueado o en mantenimiento

El sistema implementa el algoritmo de **Dijkstra** con cuatro criterios de búsqueda distintos y el **Árbol de Expansión Mínimo (Prim)** para el recorrido de visitantes.

---

## Lugares del campus modelados

1. Portería Cra. 87 (entrada principal)
2. Bloque Administrativo (Rectoría, Vicerrectorías)
3. Parqueadero Principal
4. Bloque Audiovisuales (CILAE, COP, Auditorios)
5. Biblioteca Eduardo Fernández Botero
6. Bloque Comunicación e Idiomas
7. Sello Editorial / Taller de Publicaciones
8. Bloque 5 - Derecho
9. CDC – Centro Docente de Cómputo
10. Bloque 6 - Ingenierías
11. Bloque 7 - Ciencias Básicas
12. Medios Educativos (Foro Federico Estrada Vélez)
13. Bloque Ciencias Sociales y Humanas
14. Teatro Gabriel Obregón Botero
15. Zona Deportiva / Coliseo
16. Portería Metroplús (entrada secundaria Calle 30)

## Funcionalidades

- **Buscar ruta entre dos lugares** con cuatro criterios de búsqueda:
  1. Ruta más corta por distancia
  2. Ruta más rápida por tiempo
  3. Ruta con menor congestión
  4. Ruta accesible para personas con movilidad reducida
- Los caminos bloqueados o en mantenimiento se ignoran automáticamente.
- Se muestra la ruta completa, el costo total y una explicación de por qué fue seleccionada.
- **Recorrido de visitantes** usando el Árbol de Expansión Mínimo, que conecta todos los lugares del campus con la menor distancia total posible.

## Supuestos asumidos

- Todos los caminos son de doble sentido (el campus es principalmente peatonal).
- Las distancias y tiempos son estimaciones aproximadas basadas en el área del campus (361 248 m²) y una velocidad media de caminata de 4 km/h.
- Los niveles de congestión son valores representativos según la afluencia típica de cada zona del campus en horas pico.
- El Árbol de Expansión Mínimo para visitantes no considera restricciones de accesibilidad, ya que los visitantes se asume que no tienen limitaciones de movilidad, tal como indica el enunciado de la práctica.
- El camino directo entre Portería Metroplús y Teatro Gabriel Obregón está marcado como bloqueado para demostrar que el sistema lo esquiva correctamente.
- El camino entre Bloque 6 (Ingenierías) y Bloque 7 (Ciencias Básicas) está en mantenimiento para ilustrar ese estado.
- El tramo entre Bloque 6 (Ingenierías) y CDC no es accesible para personas con movilidad reducida (escaleras sin rampa).
## Algoritmos implementados

**Dijkstra** — adaptado de la clase `GrafoLista` del archivo `grafos.py` del curso. Se modificó para recibir un criterio de búsqueda y filtrar caminos no disponibles o no accesibles antes de calcular el peso de cada arista.

**Prim (AEM)** — basado en el método `arbolExpansionMinimo()` de la clase `GrafoMatriz` vista en clase, portado a lista de adyacencia. Construye el árbol eligiendo siempre la arista de menor distancia que conecte un nuevo vértice al árbol ya formado.
