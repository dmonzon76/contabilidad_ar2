import json
from pathlib import Path

# Carpeta donde está este script
SCRIPT_DIR = Path(__file__).resolve().parent

# Archivo TXT dentro de /tools/
input_file = SCRIPT_DIR / "ACTIVIDADES_ECONOMICAS_F883.txt"

# Archivo JSON dentro de /fiscal/data/
output_file = SCRIPT_DIR.parent / "fiscal" / "data" / "afip_activities.json"

print("Leyendo desde:", input_file)
print("Generando JSON en:", output_file)

actividades = []

with open(input_file, 'r', encoding='utf-8') as f:
    next(f)  # saltar cabecera

    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split(';')

        if len(parts) >= 3:
            actividades.append({
                "code": parts[0].strip(),
                "description": parts[1].strip(),
                "description_long": parts[2].strip()
            })

with open(output_file, 'w', encoding='utf-8') as f_json:
    json.dump(actividades, f_json, ensure_ascii=False, indent=2)

print(f"Listo. Procesadas {len(actividades)} actividades.")
