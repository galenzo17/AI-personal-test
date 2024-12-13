import os
import sys
import subprocess

def main():
    # Directorio actual (donde se encuentra main.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Obtener todos los archivos .py excepto el propio main.py
    py_files = [f for f in os.listdir(current_dir) if f.endswith(".py") and f != os.path.basename(__file__)]

    if not py_files:
        print("No se encontraron otros archivos .py para ejecutar.")
        sys.exit(0)

    # Mostrar un menú con los archivos encontrados
    print("Archivos disponibles:")
    for i, f in enumerate(py_files, start=1):
        print(f"{i}. {f}")

    # Pedir al usuario que seleccione uno
    while True:
        try:
            choice = int(input("Selecciona el número del archivo a ejecutar (0 para salir): "))
            if choice == 0:
                print("Saliendo...")
                sys.exit(0)
            if 1 <= choice <= len(py_files):
                chosen_file = py_files[choice - 1]
                break
            else:
                print(f"Por favor, elige un número entre 0 y {len(py_files)}.")
        except ValueError:
            print("Entrada inválida. Por favor ingresa un número.")

    # Ejecutar el archivo seleccionado en un proceso separado
    print(f"Ejecutando {chosen_file}...")
    try:
        # Lanza el archivo con el intérprete de Python
        subprocess.run([sys.executable, os.path.join(current_dir, chosen_file)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {chosen_file}: {e}")

if __name__ == "__main__":
    main()