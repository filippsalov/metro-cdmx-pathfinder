# Metro CDMX — Optimal Route Finder

A full-stack web application that calculates the optimal route between any two stations on the Mexico City Metro network. Built with Python, Flask, and vanilla JavaScript, using a two-phase A* algorithm on a graph of all 12 metro lines.

![Metro CDMX Map](static/map.png)

---

## How It Works

### Data Pipeline
Station coordinates were extracted manually from a metro map image using a custom Python tool (`pick_coords.py`): clicking on each station registers its position as relative coordinates (0–1) independent of image resolution. A second script (`generate_lines_json.py`) processes the raw coordinates, averages repeated stations (transfer nodes), and generates `lines.json` — the data file that powers both the frontend and the backend graph.

### Pathfinding — Two-Phase A*
The backend builds a `networkx` graph where each node is a `(station, line)` pair, allowing the same physical station to appear on multiple lines:

1. **Phase 1 — Metro graph only:** runs A* (equivalent to Dijkstra with zero heuristic) to find the optimal metro-only path and compute distances to the destination
2. **Phase 2 — Extended graph:** adds virtual `ORI` (street origin) and `FIN` (street destination) nodes. Every station connects to `FIN` with a cost of `exit time + walking time`. A* runs again with an informed heuristic built from Phase 1 distances, returning the globally optimal path including walking segments and transfers

Each step type has a cost:
- Metro between consecutive stations: **2 min**
- Transfer between lines at the same station: **5 min**
- Walking: distance in px / speed constant

### Frontend
The interactive map renders station dots as HTML elements positioned using the relative coordinates from `lines.json`. Clicking two stations sends a `POST /ruta` request to the Flask backend. The response is rendered as an SVG overlay with colour-coded segments (metro, transfer, walking) and a step-by-step breakdown below the map.

---

## Technologies

- **Backend:** Python, Flask, NetworkX
- **Algorithm:** Two-phase A* with informed heuristic
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Data pipeline:** Python, Pillow, Matplotlib

---

## How to Run

### Requirements
```bash
pip install flask networkx pillow matplotlib
```

### Run the server
```bash
python app.py
```

Open `http://localhost:5000` in your browser.

### Regenerate station data (optional)
To re-extract coordinates from a new map image:
```bash
python pick_coords.py        # click each station on the map
python generate_lines_json.py  # generates static/lines.json
```

---

## Project Structure

```
├── app.py                    # Flask server + two-phase A* algorithm
├── pick_coords.py            # Interactive coordinate extraction tool
├── generate_lines_json.py    # JSON generator from raw coordinates
├── coords_raw.txt            # Raw clicked coordinates (all 12 lines)
├── templates/
│   └── index.html            # Main page
└── static/
    ├── map.png               # Metro CDMX map image
    ├── lines.json            # Station data (coordinates + line colors)
    ├── map.js                # Frontend logic (rendering + API calls)
    └── style.css             # Map overlay styles
```

---

## Authors

- Philip Daniel Salov Draganov
- Samuel Sánchez
- Jorge Vázquez Linares
- Daniel Domingo
- Pablo Campo Herrero
