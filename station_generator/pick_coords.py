# pick_coords_auto_list.py
# Herramienta para hacer clic en cada estación y registrar sus coordenadas
# en la imagen del Mapa del Metro CDMX.

from PIL import Image
import matplotlib.pyplot as plt
import csv

# CONFIGURACIÓN

MAP_IMAGE = "map.png"                   # Imagen del mapa
OUT_CSV   = "stations_full_coords.csv"  # Archivo de salida

# LISTA DE TODAS LAS ESTACIONES
# EN ORDEN EXACTO DE CLIC

STATIONS = [

    # ---- Línea 1 (Pantitlán – Observatorio)
    "Pantitlán","Zaragoza","Gómez Farías","Boulevard Puerto Aéreo",
    "Balbuena","Moctezuma","San Lázaro","Candelaria","Merced",
    "Pino Suárez","Isabel la Católica","Salto del Agua","Balderas",
    "Cuauhtémoc","Insurgentes","Sevilla","Chapultepec","Juanacatlán",
    "Tacubaya","Observatorio",

    # ---- Línea 2 (Cuatro Caminos – Tasqueña)
    "Cuatro Caminos","Panteones","Tacuba","Cuitláhuac","Popotla",
    "Colegio Militar","Normal","San Cosme","Revolución","Hidalgo",
    "Bellas Artes","Allende","Zócalo/Tenochtitlan","Pino Suárez",
    "San Antonio Abad","Chabacano","Viaducto","Xola","Villa de Cortés",
    "Nativitas","Portero","Ermita","General Anaya","Tasqueña",

    # ---- Línea 3 (Indios Verdes – Universidad)
    "Indios Verdes", "Deportivo 18 de Marzo", "Potrero", "La Raza","Tlatelolco",
    "Guerrero","Hidalgo","Juárez","Balderas","Niños Héroes",
    "Hospital General","Centro Médico","Etiopía-Plaza de la Transparencia",
    "Eugenia","División del Norte","Zapata","Coyoacán",
    "Viveros-Derechos Humanos","Miguel Ángel de Quevedo","Copilco","Universidad",

    # ---- Línea 4 (Martín Carrera – Santa Anita)
    "Martín Carrera","Talismán","Bondojito","Consulado",
    "Canal del Norte","Morelos","Candelaria","Fray Servando",
    "Jamaica","Santa Anita",

    # ---- Línea 5 (Pantitlán – Politécnico)
    "Pantitlán","Hangares","Terminal Aérea","Oceanía","Aragón",
    "Eduardo Molina","Consulado","Valle Gómez","Misterios",
    "La Raza","Autobuses del Norte","Instituto del Petróleo","Politécnico",

    # ---- Línea 6 (El Rosario – Martín Carrera)
    "El Rosario","Tezozómoc","UAM-Azcapotzalco","Ferrería/Arena Ciudad de México",
    "Norte 45","Vallejo","Instituto del Petróleo","Lindavista",
    "Deportivo 18 de Marzo","La Villa-Basílica","Martín Carrera",

    # ---- Línea 7 (El Rosario – Barranca del Muerto)
    "El Rosario","Aquiles Serdán","Camarones","Refinería","Tacuba",
    "San Joaquín","Polanco","Auditorio","Constituyentes","Tacubaya",
    "San Pedro de los Pinos","San Antonio","Mixcoac","Barranca del Muerto",

    # ---- Línea 8 (Garibaldi – Constitución de 1917)
    "Garibaldi-Lagunilla","Bellas Artes","San Juan de Letrán",
    "Salto del Agua","Doctores","Obrera","Chabacano","La Viga",
    "Santa Anita","Coyuya","Iztacalco","Apatlaco","Aculco","Escuadrón 201",
    "Atlalilco","Iztapalapa","Cerro de la Estrella","UAM-I",
    "Constitución de 1917",

    # ---- Línea 9 (Pantitlán – Centro Médico)
    "Pantitlán","Puebla","Ciudad Deportiva","Velódromo","Mixiuhca",
    "Jamaica","Chabacano","Lázaro Cárdenas","Centro Médico", "Chilipancingo", "Patriotismo", "Tacubaya", 

    # ---- Línea A (Pantitlán – La Paz)
    "Pantitlán","Agrícola Oriental","Canal de San Juan","Tepalcates",
    "Guelatao","Peñón Viejo","Acatitla","Santa Marta","Los Reyes","La Paz",

    # ---- Línea B (Buenavista – Ciudad Azteca)
    "Buenavista","Guerrero","Garibaldi-Lagunilla","Lagunilla", "Tepito", "Morelos", "San Lázaro",
    "Ricardo Flores Magón","Romero Rubio","Oceanía","Deportivo Oceanía",
    "Bosque de Aragón","Villa de Aragón","Nezahualcóyotl","Impulsora",
    "Río de los Remedios","Múzquiz","Ecatepec","Olímpica","Plaza Aragón",
    "Ciudad Azteca",

    # ---- Línea 12 (Tláhuac – Mixcoac)
    "Tláhuac","Tlaltenco","Zapotitlán","Nopalera","Olivos","Tezonco",
    "Periférico Oriente","Calle 11","Lomas Estrella","San Andrés Tomatlán",
    "Cuhualcan","Atlalilco","Mexicaltzingo","Ermita","Eje Central",
    "Parque de los Venados","Zapata","Hospital 20 de Noviembre",
    "Insurgentes Sur","Mixcoac",
]

# CARGAR MAPA
img = Image.open(MAP_IMAGE)
W, H = img.size

# Datos de salida
coords = {}
index = 0

# INTERFAZ
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1,1,1)
plt.imshow(img)
plt.axis("off")

sidebar = plt.figtext(
    0.82, 0.5,
    "",
    fontsize=12,
    va="center",
    ha="left"
)

def refresh_sidebar():
    if index < len(STATIONS):
        sidebar.set_text(
            f"Siguiente estación:\n\n{STATIONS[index]}\n\n"
            f"{index + 1} / {len(STATIONS)}"
        )
    else:
        sidebar.set_text("TODAS CAPTURADAS\nPuedes cerrar la ventana")

    plt.draw()

def onclick(event):
    global index

    if event.xdata is None or event.ydata is None:
        return

    if index >= len(STATIONS):
        return

    name = STATIONS[index]

    x = int(event.xdata)
    y = int(event.ydata)

    x_rel = round(x / W, 4)
    y_rel = round(y / H, 4)

    coords[name] = (x, y, x_rel, y_rel)

    print(f"{name}: X={x}, Y={y}, XR={x_rel}, YR={y_rel}")

    index += 1
    refresh_sidebar()

    plt.draw()

refresh_sidebar()

fig.canvas.mpl_connect("button_press_event", onclick)
plt.show()
