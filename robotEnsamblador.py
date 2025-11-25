import threading
import time
from colores import Colores

#Constructor
class RobotEnsamblador(threading.Thread):
    def __init__(self, nombre, lock, cola_ordenes, inventario):
        super().__init__()
        self.nombre = nombre
        self.lock = lock
        self.cola_ordenes = cola_ordenes
        self.inventario = inventario
        self.activo = True
        self.vehiculos_terminados = []

    # Verifica si hay partes suficientes
    def verificar_partes(self, tipo):
        resultado = False

        #SECCION CRITICA
        self.lock.acquire()
        try:
            if tipo == "moto":
                resultado = (
                    self.inventario["chasis_moto"] >= 1 and
                    self.inventario["motor_moto"] >= 1 and
                    self.inventario["tanque_moto"] >= 1 and
                    self.inventario["rueda_moto"] >= 2
                )
            elif tipo == "auto":
                resultado = (
                    self.inventario["chasis_auto"] >= 1 and
                    self.inventario["motor_auto"] >= 1 and
                    self.inventario["tanque_auto"] >= 1 and
                    self.inventario["rueda_auto"] >= 4
                )
        finally:
            self.lock.release()
        # ------------------------

        return resultado

    # Usa las partes si estan disponibles y las resta del inventario
    def usar_partes(self, tipo):
        #SECCION CRITICA
        self.lock.acquire()
        try:
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
        finally:
            self.lock.release()
        # ------------------------

    # simula ensamblar un vehiculo y lo agrega a la lista terminados
    def ensamblar(self, tipo):
        color = Colores.CIAN if tipo == "moto" else Colores.MAGENTA
        print(f"{Colores.VERDE}{self.nombre} ensamblando {color}{tipo}{Colores.RESET}...")
        time.sleep(3)
        print(f"{Colores.VERDE}{self.nombre} terminó de ensamblar un {color}{tipo}{Colores.RESET}.")
        self.vehiculos_terminados.append(tipo)

    # Bucle principal
    def run(self):
        while self.activo:
            try:
                orden = self.cola_ordenes.get(timeout=2)
                tipo = "moto" if "moto" in orden else "auto"

                esperando_partes = False

                while self.activo:
                    # Determina si hay inventario para ensamblar
                    if self.verificar_partes(tipo):
                        self.usar_partes(tipo)
                        self.ensamblar(tipo)
                        break
                    else:
                        # Si no hay partes disponibles espera dos segundos
                        if not esperando_partes:
                            print(f"{Colores.VERDE}{self.nombre} esperando partes para {tipo}...{Colores.RESET}")
                            esperando_partes = True
                        time.sleep(2)

            except Exception:
                time.sleep(1)

    # Apaga el robot
    def apagar(self):
        self.activo = False
        print(f"{Colores.VERDE}{self.nombre} apagado.{Colores.RESET}")
