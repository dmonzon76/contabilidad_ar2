import os

# Archivos que queremos juntar
archivos_importantes = ['views.py', 'models.py', 'urls.py', 'forms.py', 'admin.py']
archivo_salida = "todo_mi_codigo.txt"

with open(archivo_salida, "w", encoding="utf-8") as salida:
    for ruta, carpetas, archivos in os.walk("."):
        # Evitamos carpetas basura como la del entorno virtual o migraciones
        if "venv" in ruta or ".git" in ruta or "migrations" in ruta:
            continue

        for archivo in archivos:
            if archivo in archivos_importantes:
                ruta_completa = os.path.join(ruta, archivo)
                salida.write(f"\n--- INICIO DE ARCHIVO: {ruta_completa} ---\n")
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    salida.write(f.read())
                salida.write(f"\n--- FIN DE ARCHIVO: {ruta_completa} ---\n")

print("¡Listo! Todo tu código está en todo_mi_codigo.txt")
