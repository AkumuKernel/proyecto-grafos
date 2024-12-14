import csv
import os

# Definir intervalos de tiempo (cada 30 minutos desde las 5:30 hasta las 0:00)
time_slots = [
    "05:30:00", "06:00:00", "06:30:00", "07:00:00", "07:30:00", "08:00:00", "08:30:00", "09:00:00", "09:30:00", "10:00:00", "10:30:00",
    "11:00:00", "11:30:00", "12:00:00", "12:30:00", "13:00:00", "13:30:00", "14:00:00", "14:30:00", "15:00:00", "15:30:00", "16:00:00",
    "16:30:00", "17:00:00", "17:30:00", "18:00:00", "18:30:00", "19:00:00", "19:30:00", "20:00:00", "20:30:00", "21:00:00", "21:30:00",
    "22:00:00", "22:30:00", "23:00:00", "23:30:00"
]

# Archivos de entrada y salida
density_csv = "predicted_density_matrix.csv"
stops_txt = "graphs/santiago/gtfs/stops.txt"
output_file = "stops_with_density.txt"

# Cargar densidades del archivo CSV
density_data = {}

def load_density_data():
    with open(density_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stop_id = row['paradero']
            if stop_id not in density_data:
                density_data[stop_id] = {}
            for time_slot in time_slots:
                value = row.get(time_slot, "")
                # Convertir a valor absoluto si es numérico
                density_data[stop_id][time_slot] = abs(float(value)) if value.strip() else 0

# Procesar stops.txt y combinar con las densidades
def process_stops():
    stops_with_density = []
    with open(stops_txt, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + time_slots  # Agregar los intervalos de tiempo como columnas
        for row in reader:
            stop_id = row['stop_id']
            densities = density_data.get(stop_id, {slot: 0 for slot in time_slots})
            # Combinar datos originales con las densidades
            row.update(densities)
            stops_with_density.append(row)
        return stops_with_density, fieldnames

# Guardar los resultados en el archivo de salida
def write_output(data, fieldnames):
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Ejecutar el programa
def main():
    if not os.path.exists(density_csv):
        print(f"Error: Archivo {density_csv} no encontrado.")
        return
    if not os.path.exists(stops_txt):
        print(f"Error: Archivo {stops_txt} no encontrado.")
        return

    print("Cargando datos de densidad...")
    load_density_data()
    print(f"Densidades cargadas para {len(density_data)} paraderos.")

    print("Procesando stops.txt...")
    processed_data, fieldnames = process_stops()
    print(f"Se procesaron {len(processed_data)} paraderos.")

    print("Escribiendo archivo de salida...")
    write_output(processed_data, fieldnames)
    print(f"Archivo generado: {output_file}")

if __name__ == "__main__":
    main()
