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

# Cola de impresion
cola_impresion = Queue()

def mostrar_inventario():
    print("\n=== INVENTARIO ACTUAL ===")
    for k, v in INVENTARIO_PARTES.items():
        print(f"{k}: {v}")
    print("=========================\n")

# Agrega las piezas a la cola segun tipo
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

def pedir_numero(mensaje, minimo=1):
    while True:
        try:
            n = int(input(mensaje))
            if n >= minimo:
                return n
            print(f"Debe ser un número >= {minimo}")
        except ValueError:
            print("Ingrese un número válido.")

# --- Proceso principal ---
def main():
    lock = threading.Lock()
    cola_ordenes = Queue()

    print("\n=== CONFIGURACIÓN DE LA FÁBRICA ===")

    cant_impresoras = pedir_numero("Cantidad de impresoras 3D: ")
    cant_robot_inv = pedir_numero("Cantidad de robots de inventario: ")
    cant_robot_ens = pedir_numero("Cantidad de robots ensambladores: ")

    print("\nInicializando fábrica...\n")

    # Crear impresoras
    impresoras = [
        Impresora3D(f"Impresora-{i+1}", lock, TIEMPOS_PIEZAS, cola_impresion)
        for i in range(cant_impresoras)
    ]
    for imp in impresoras:
        imp.start()

    # Crear robots de inventario
    robots_inv = [
        RobotInventario(f"RobotInventario-{i+1}", lock, impresoras, INVENTARIO_PARTES)
        for i in range(cant_robot_inv)
    ]
    for r in robots_inv:
        r.start()

    # Crear robots ensambladores
    robots_ens = [
        RobotEnsamblador(f"RobotEnsamblador-{i+1}", lock, cola_ordenes, INVENTARIO_PARTES)
        for i in range(cant_robot_ens)
    ]
    for e in robots_ens:
        e.start()

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
                print("Opción no válida.")
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        print("\nApagando fábrica...")

        for imp in impresoras:
            imp.apagar()
        for r in robots_inv:
            r.apagar()
        for e in robots_ens:
            e.apagar()

        for imp in impresoras:
            imp.join()
        for r in robots_inv:
            r.join()
        for e in robots_ens:
            e.join()

        print("\nFábrica cerrada correctamente.")
        terminados = []
        for e in robots_ens:
            terminados.extend(e.vehiculos_terminados)

        print("Vehículos terminados:", terminados)

if __name__ == "__main__":
    main()
