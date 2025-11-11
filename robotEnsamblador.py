import threading
import time
from colores import Colores

class RobotEnsamblador(threading.Thread):
    def __init__(self, nombre, lock, cola_ordenes, inventario):
        super().__init__()
        self.nombre = nombre
        self.lock = lock
        self.cola_ordenes = cola_ordenes
        self.inventario = inventario
        self.activo = True
        self.vehiculos_terminados = []

    def verificar_partes(self, tipo):
        with self.lock:
            if tipo == "moto":
                return (self.inventario["chasis_moto"] >= 1 and
                        self.inventario["motor_moto"] >= 1 and
                        self.inventario["tanque_moto"] >= 1 and
                        self.inventario["rueda_moto"] >= 2)
            elif tipo == "auto":
                return (self.inventario["chasis_auto"] >= 1 and
                        self.inventario["motor_auto"] >= 1 and
                        self.inventario["tanque_auto"] >= 1 and
                        self.inventario["rueda_auto"] >= 4)
        return False

    def usar_partes(self, tipo):
        with self.lock:
            if tipo == "moto":
                self.inventario["chasis_moto"] -= 1
                self.inventario["motor_moto"] -= 1
                self.inventario["tanque_moto"] -= 1
                self.inventario["rueda_moto"] -= 2
            elif tipo == "auto":
                self.inventario["chasis_auto"] -= 1
                self.inventario["motor_auto"] -= 1
                self.inventario["tanque_auto"] -= 1
                self.inventario["rueda_auto"] -= 4

    def ensamblar(self, tipo):
        color = Colores.CIAN if tipo == "moto" else Colores.MAGENTA
        print(f"{Colores.VERDE}{self.nombre} ensamblando {color}{tipo}{Colores.RESET}...")
        time.sleep(3)
        print(f"{Colores.VERDE}{self.nombre} termino de ensamblar un {color}{tipo}{Colores.RESET}.")
        self.vehiculos_terminados.append(tipo)

    def run(self):
        while self.activo:
            try:
                orden = self.cola_ordenes.get(timeout=2)
                tipo = "moto" if "moto" in orden else "auto"

                esperando_partes = False  # bandera para controlar mensaje único

                while self.activo:
                    if self.verificar_partes(tipo):
                        self.usar_partes(tipo)
                        self.ensamblar(tipo)
                        break
                    else:
                        if not esperando_partes:
                            print(f"{Colores.VERDE}{self.nombre} esperando partes para {tipo}...{Colores.RESET}")
                            esperando_partes = True
                        time.sleep(2)

            except Exception:
                time.sleep(1)

    def apagar(self):
        self.activo = False
        print(f"{Colores.VERDE}{self.nombre} apagado.{Colores.RESET}")
