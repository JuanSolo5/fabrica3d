import threading
import time
from queue import Queue
from impresora3D import Impresora3D
from robotInventario import RobotInventario
from robotEnsamblador import RobotEnsamblador

# --- Inventario global ---
INVENTARIO_PARTES = {
    "chasis_moto": 0,
    "motor_moto": 0,
    "tanque_moto": 0,
    "rueda_moto": 0,
    "chasis_auto": 0,
    "motor_auto": 0,
    "tanque_auto": 0,
    "rueda_auto": 0
}

# --- Tiempos de impresión por tipo de pieza ---
TIEMPOS_PIEZAS = {
    "chasis_moto": 5,
    "motor_moto": 7,
    "tanque_moto": 4,
    "rueda_moto": 2,
    "chasis_auto": 11,
    "motor_auto": 9,
    "tanque_auto": 6,
    "rueda_auto": 3
}

# --- Cola global de impresión ---
cola_impresion = Queue()

def mostrar_inventario():
    print("\n=== INVENTARIO ACTUAL ===")
    for k, v in INVENTARIO_PARTES.items():
        print(f"{k}: {v}")
    print("=========================\n")

def agregar_piezas_a_cola(tipo):
    if tipo == "moto":
        piezas = ["chasis_moto", "motor_moto", "tanque_moto", "rueda_moto", "rueda_moto"]
    elif tipo == "auto":
        piezas = ["chasis_auto", "motor_auto", "tanque_auto",
                  "rueda_auto", "rueda_auto", "rueda_auto", "rueda_auto"]
    else:
        return

    print(f"Agregando piezas para {tipo} a la cola de impresión...")
    for p in piezas:
        cola_impresion.put(p)
    print(f"Piezas para {tipo} agregadas correctamente.\n")

def main():
    lock = threading.Lock()
    cola_ordenes = Queue()

    # Crear impresoras (4 hilos)
    impresoras = [Impresora3D(f"Impresora-{i+1}", lock, TIEMPOS_PIEZAS, cola_impresion) for i in range(4)]
    for imp in impresoras:
        imp.start()

    # Crear robots
    robot_inv = RobotInventario("RobotInventario-1", lock, impresoras, INVENTARIO_PARTES)
    robot_inv.start()

    ensamblador = RobotEnsamblador("RobotEnsamblador-1", lock, cola_ordenes, INVENTARIO_PARTES)
    ensamblador.start()

    try:
        while True:
            mostrar_inventario()
            orden = input("Ingrese orden (moto/auto/salir): ").strip().lower()
            if orden == "salir":
                break
            elif orden in ("moto", "auto"):
                agregar_piezas_a_cola(orden)
                cola_ordenes.put(f"orden_{orden}")
            else:
                print("Opcion no valida.")
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        print("Apagando fabrica...")

        for imp in impresoras:
            imp.apagar()
        robot_inv.apagar()
        ensamblador.apagar()

        for imp in impresoras:
            imp.join()
        robot_inv.join()
        ensamblador.join()

        print("\nFabrica cerrada correctamente.")
        print("Vehiculos terminados:", ensamblador.vehiculos_terminados)

if __name__ == "__main__":
    main()
