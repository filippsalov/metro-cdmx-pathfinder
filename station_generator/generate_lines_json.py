# generate_lines_json.py
# Lee coords_raw.txt (formato: "Nombre: ... XR=0.8011, YR=0.4838" por línea)
# Calcula promedio de coordenadas para estaciones repetidas
# Genera lines.json en el formato usado por tu proyecto.
#
# Uso:
# 1) python generate_lines_json.py
# 2) Se creará "lines.json" en el mismo directorio.

import re, json
from collections import defaultdict, OrderedDict

# ----- Colores oficiales -----
COLORES = {
    "L1": "#C23C7F",
    "L2": "#1469B5",
    "L3": "#8D8926",
    "L4": "#89C6A9",
    "L5": "#F6B600",
    "L6": "#C90B13",
    "L7": "#E58126",
    "L8": "#1F822C",
    "L9": "#774234",
    "LA": "#780C62",
    "LB": "#999999",
    "L12": "#A88C39"
}

# ----- Estructura de líneas -----
LINE_ORDER = [
    ("L1", [
        "Pantitlán","Zaragoza","Gómez Farías","Boulevard Puerto Aéreo",
        "Balbuena","Moctezuma","San Lázaro","Candelaria","Merced",
        "Pino Suárez","Isabel la Católica","Salto del Agua","Balderas",
        "Cuauhtémoc","Insurgentes","Sevilla","Chapultepec","Juanacatlán",
        "Tacubaya","Observatorio"
    ]),
    ("L2", [
        "Cuatro Caminos","Panteones","Tacuba","Cuitláhuac","Popotla",
        "Colegio Militar","Normal","San Cosme","Revolución","Hidalgo",
        "Bellas Artes","Allende","Zócalo/Tenochtitlan","Pino Suárez",
        "San Antonio Abad","Chabacano","Viaducto","Xola","Villa de Cortés",
        "Nativitas","Portero","Ermita","General Anaya","Tasqueña"
    ]),
    ("L3", [
        "Indios Verdes", "Deportivo 18 de Marzo", "Potrero", "La Raza","Tlatelolco",
        "Guerrero","Hidalgo","Juárez","Balderas","Niños Héroes",
        "Hospital General","Centro Médico","Etiopía-Plaza de la Transparencia",
        "Eugenia","División del Norte","Zapata","Coyoacán",
        "Viveros-Derechos Humanos","Miguel Ángel de Quevedo","Copilco","Universidad"
    ]),
    ("L4", [
        "Martín Carrera","Talismán","Bondojito","Consulado",
        "Canal del Norte","Morelos","Candelaria","Fray Servando",
        "Jamaica","Santa Anita"
    ]),
    ("L5", [
        "Pantitlán","Hangares","Terminal Aérea","Oceanía","Aragón",
        "Eduardo Molina","Consulado","Valle Gómez","Misterios",
        "La Raza","Autobuses del Norte","Instituto del Petróleo","Politécnico"
    ]),
    ("L6", [
        "El Rosario","Tezozómoc","UAM-Azcapotzalco","Ferrería/Arena Ciudad de México",
        "Norte 45","Vallejo","Instituto del Petróleo","Lindavista",
        "Deportivo 18 de Marzo","La Villa-Basílica","Martín Carrera"
    ]),
    ("L7", [
        "El Rosario","Aquiles Serdán","Camarones","Refinería","Tacuba",
        "San Joaquín","Polanco","Auditorio","Constituyentes","Tacubaya",
        "San Pedro de los Pinos","San Antonio","Mixcoac","Barranca del Muerto"
    ]),
    ("L8", [
        "Garibaldi-Lagunilla","Bellas Artes","San Juan de Letrán",
        "Salto del Agua","Doctores","Obrera","Chabacano","La Viga",
        "Santa Anita","Coyuya","Iztacalco","Apatlaco","Aculco","Escuadrón 201",
        "Atlalilco","Iztapalapa","Cerro de la Estrella","UAM-I",
        "Constitución de 1917"
    ]),
    ("L9", [
        "Pantitlán","Puebla","Ciudad Deportiva","Velódromo","Mixiuhca",
        "Jamaica","Chabacano","Lázaro Cárdenas","Centro Médico", "Chilipancingo", "Patriotismo", "Tacubaya"
    ]),
    ("LA", [
        "Pantitlán","Agrícola Oriental","Canal de San Juan","Tepalcates",
        "Guelatao","Peñón Viejo","Acatitla","Santa Marta","Los Reyes","La Paz"
    ]),
    ("LB", [
        "Buenavista","Guerrero","Garibaldi-Lagunilla","Lagunilla", "Tepito", "Morelos", "San Lázaro",
        "Ricardo Flores Magón","Romero Rubio","Oceanía","Deportivo Oceanía",
        "Bosque de Aragón","Villa de Aragón","Nezahualcóyotl","Impulsora",
        "Río de los Remedios","Múzquiz","Ecatepec","Olímpica","Plaza Aragón",
        "Ciudad Azteca"
    ]),
    ("L12", [
        "Tláhuac","Tlaltenco","Zapotitlán","Nopalera","Olivos","Tezonco",
        "Periférico Oriente","Calle 11","Lomas Estrella","San Andrés Tomatlán",
        "Cuhualcan","Atlalilco","Mexicaltzingo","Ermita","Eje Central",
        "Parque de los Venados","Zapata","Hospital 20 de Noviembre",
        "Insurgentes Sur","Mixcoac"
    ])
]

# ----- Parse coords_raw.txt -----
coords_file = "coords_raw.txt"
with open(coords_file, "r", encoding="utf-8") as f:
    raw = f.read()

# regex para líneas con XR, YR
pairs = re.findall(r"([A-Za-z0-9ÁÉÍÓÚáéíóúÑñ\-\s\./]+):.*?XR=([0-9.]+),\s*YR=([0-9.]+)", raw)
if not pairs:
    print("No se encontraron pares 'XR'/'YR' en coords_raw.txt. Asegúrate del formato.")
    exit(1)

# agrupar por nombre y almacenar listas de (xr, yr)
by_name = defaultdict(list)
for name, xr, yr in pairs:
    name = name.strip()
    xr_v = float(xr)
    yr_v = float(yr)
    by_name[name].append((xr_v, yr_v))

# calcular promedios
avg_coords = {}
for name, vals in by_name.items():
    xs = [v[0] for v in vals]
    ys = [v[1] for v in vals]
    avg_x = sum(xs) / len(xs)
    avg_y = sum(ys) / len(ys)
    avg_coords[name] = [round(avg_x, 6), round(avg_y, 6)]

# ----- Construir JSON final -----
lines_json = OrderedDict()
for line_key, stations in LINE_ORDER:
    color = COLORES.get(line_key, "#999999")
    stations_dict = OrderedDict()
    for s in stations:
        if s in avg_coords:
            stations_dict[s] = avg_coords[s]
        else:
            # si falta una estación en coords, avisamos y colocamos [0,0] para que la revises
            print(f"Atención: no existe coordenada para estación '{s}' en coords_raw.txt")
            stations_dict[s] = [0, 0]
    lines_json[line_key] = {"color": color, "stations": stations_dict}

# ----- Guardar lines.json -----
with open("lines.json", "w", encoding="utf-8") as f:
    json.dump(lines_json, f, ensure_ascii=False, indent=2)

print("lines.json generado con éxito.")
