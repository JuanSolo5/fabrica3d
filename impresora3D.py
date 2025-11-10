import threading
import time
from queue import Empty
from colores import Colores

class Impresora3D(threading.Thread):
    def __init__(self, nombre, lock, tiempos_piezas, cola_impresion):
        super().__init__()
        self.nombre = nombre
        self.lock = lock
        self.tiempos_piezas = tiempos_piezas
        self.cola_impresion = cola_impresion
        self.cama = []
        self.activa = True

    def color_pieza(self, pieza):
        if "moto" in pieza:
            return f"{Colores.CIAN}{pieza}{Colores.RESET}"
        elif "auto" in pieza:
            return f"{Colores.MAGENTA}{pieza}{Colores.RESET}"
        return pieza

    def calibrar(self):
        print(f"{Colores.AZUL}{self.nombre} calibrando...{Colores.RESET}")
        time.sleep(2)
        print(f"{Colores.AZUL}{self.nombre} calibrada correctamente.{Colores.RESET}")

    def imprimir_pieza(self, pieza):
        pieza_col = self.color_pieza(pieza)
        tiempo_impresion = self.tiempos_piezas.get(pieza, 5)
        print(f"{Colores.AZUL}{self.nombre} imprimiendo {pieza_col}... ({tiempo_impresion}s){Colores.RESET}")
        time.sleep(tiempo_impresion)
        print(f"{Colores.AZUL}{self.nombre} termino de imprimir {pieza_col}.{Colores.RESET}")
        with self.lock:
            self.cama.append(pieza)

    def run(self):
        while self.activa:
            try:
                pieza = self.cola_impresion.get(timeout=2)
                self.calibrar()
                self.imprimir_pieza(pieza)
                self.cola_impresion.task_done()
            except Empty:
                time.sleep(1)

    def apagar(self):
        self.activa = False
        print(f"{Colores.AZUL}{self.nombre} apagada.{Colores.RESET}")
