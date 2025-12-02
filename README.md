# fabrica3d

Este proyecto implementa una fabrica automatizada que construye vehiculos (motos y autos) utilizando programacion concurrente en Python. 
Se simula el flujo completo de produccion mediante multiples hilos que trabajan en paralelo y comparten recursos.
La fábrica cuenta con tres tipos de procesos concurrentes instanciados como objetos:

1. Impresoras: Cada impresora funciona como un hilo independiente. Toman piezas desde una cola de impresion, hacen un proceso de calibracipn, impresion y luego dejan la pieza terminada en su cama de impresion.

2. Robots de inventario: Recorre todas las impresoras y recoge las piezas terminadas. Luego las guarda en un inventario global.

3. Ensambladores: Toma ordenes desde una cola y verifica si el inventario tiene las piezas necesarias. Cuando estan disponibles, consume el inventario y ensambla un vehiculo. Si faltan piezas, espera activamente hasta que las impresoras produzcan mas.
