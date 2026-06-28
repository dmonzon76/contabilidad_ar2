archivo = "todo_mi_codigo.txt"
lineas_por_parte = 300

with open(archivo, "r", encoding="utf-8") as f:
    lineas = f.readlines()

total = len(lineas)
partes = (total // lineas_por_parte) + 1

for i in range(partes):
    inicio = i * lineas_por_parte
    fin = inicio + lineas_por_parte
    contenido = lineas[inicio:fin]

    nombre_parte = f"codigo_parte_{i+1}.txt"
    with open(nombre_parte, "w", encoding="utf-8") as salida:
        salida.writelines(contenido)

print(f"Listo. Se generaron {partes} archivos.")
