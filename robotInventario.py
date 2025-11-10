import threading
import time
from colores import Colores

class RobotInventario(threading.Thread):
    def __init__(self, nombre, lock, lista_impresoras, inventario):
        super().__init__()
        self.nombre = nombre
        self.pieza_manos = None
        self.lock = lock
        self.velocidad = 2
        self.activo = True
        self.lista_impresoras = lista_impresoras
        self.inventario = inventario

    def color_pieza(self, pieza):
        if "moto" in pieza:
            return f"{Colores.CIAN}{pieza}{Colores.RESET}"
        elif "auto" in pieza:
            return f"{Colores.MAGENTA}{pieza}{Colores.RESET}"
        return pieza

    def guardar_pieza(self):
        if self.pieza_manos:
            pieza_col = self.color_pieza(self.pieza_manos)
            print(f"{Colores.AMARILLO}{self.nombre} almacenando {pieza_col}...{Colores.RESET}")
            time.sleep(self.velocidad)
            with self.lock:
                if self.pieza_manos in self.inventario:
                    self.inventario[self.pieza_manos] += 1
            print(f"{Colores.AMARILLO}{self.nombre} guardo {pieza_col} en el almacen.{Colores.RESET}")
            self.pieza_manos = None

    def recoger_pieza(self):
        """
        Recorre las impresoras y recoge la primera pieza disponible.
        Retorna True si recogio y guardo una pieza, False en caso contrario.
        """
        for impresora in self.lista_impresoras:
            time.sleep(self.velocidad)
            pieza = None
            # Extraer pieza de la cama bajo lock (minimizar tiempo bajo lock)
            with self.lock:
                if impresora.cama:
                    pieza = impresora.cama.pop(0)
            if pieza:
                pieza_col = self.color_pieza(pieza)
                print(f"{Colores.AMARILLO}{self.nombre} recogio {pieza_col} de {impresora.nombre}.{Colores.RESET}")
                self.pieza_manos = pieza
                # Guardar inmediatamente (no mantener lock durante sleep)
                self.guardar_pieza()
                return True
        return False

    def run(self):
        while self.activo:
            encontrado = self.recoger_pieza()
            if not encontrado:
                time.sleep(1)

    def apagar(self):
        self.activo = False
        print(f"{Colores.AMARILLO}{self.nombre} apagado.{Colores.RESET}")
