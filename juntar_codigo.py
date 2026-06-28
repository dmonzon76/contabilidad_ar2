import os

# Archivos que queremos juntar
ARCHIVOS_PY = ["views.py", "models.py", "urls.py", "forms.py", "admin.py", "serializers.py"]
ARCHIVOS_HTML = [".html"]
ARCHIVOS_STATIC = [".css", ".js"]

ARCHIVOS_IMPORTANTES = ARCHIVOS_PY

ARCHIVO_SALIDA = "todo_mi_codigo.txt"

def es_archivo_importante(nombre):
    # Archivos Python
    if nombre in ARCHIVOS_PY:
        return True

    # Templates HTML
    for ext in ARCHIVOS_HTML:
        if nombre.endswith(ext):
            return True

    # Archivos estáticos
    for ext in ARCHIVOS_STATIC:
        if nombre.endswith(ext):
            return True

    return False


def carpeta_ignorada(ruta):
    IGNORADAS = ["venv", ".git", "__pycache__", "migrations", "staticfiles"]
    return any(ign in ruta for ign in IGNORADAS)


with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as salida:

    salida.write("### ARCHIVO GENERADO AUTOMÁTICAMENTE ###\n")
    salida.write("### Proyecto Django ERP — Código Completo ###\n\n")

    for ruta, carpetas, archivos in os.walk("."):

        if carpeta_ignorada(ruta):
            continue

        for archivo in archivos:
            if es_archivo_importante(archivo):
                ruta_completa = os.path.join(ruta, archivo)

                salida.write(f"\n\n--- INICIO DE ARCHIVO: {ruta_completa} ---\n\n")

                try:
                    with open(ruta_completa, "r", encoding="utf-8") as f:
                        salida.write(f.read())
                except Exception as e:
                    salida.write(f"[ERROR AL LEER ARCHIVO: {e}]")

                salida.write(f"\n\n--- FIN DE ARCHIVO: {ruta_completa} ---\n\n")

print("¡Listo! Todo tu código está en todo_mi_codigo.txt")
