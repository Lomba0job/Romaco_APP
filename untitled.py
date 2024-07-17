import ezdxf

# Carica il file DXF
doc = ezdxf.readfile('/Users/lavoro/Documents/PROGETTI_LAVORO/Romaco_4/05_software/Romaco_APP/ICO/bilancia.dxf')

# Estrai le entità geometriche
lines = []
circles = []

for entity in doc.modelspace().query('LINE CIRCLE'):
    if entity.dxftype() == 'LINE':
        start = entity.dxf.start
        end = entity.dxf.end
        lines.append(((start.x, start.y, start.z), (end.x, end.y, end.z)))
    elif entity.dxftype() == 'CIRCLE':
        center = entity.dxf.center
        radius = entity.dxf.radius
        circles.append((center.x, center.y, center.z, radius))

# Stampa le coordinate estratte
print("Linee:")
for line in lines:
    print(line)

print("\nCerchi:")
for circle in circles:
    print(circle)

import pythreejs as p3js
from IPython.display import display
import numpy as np

# Funzione per creare una linea
def create_line(start, end):
    return p3js.Line(
        geometry=p3js.Geometry(vertices=[start, end]),
        material=p3js.LineBasicMaterial(color='blue')
    )

# Funzione per creare un cerchio
def create_circle(center, radius):
    segments = 100
    theta = np.linspace(0, 2 * np.pi, segments)
    vertices = [(center[0] + radius * np.cos(t), center[1] + radius * np.sin(t), center[2]) for t in theta]
    vertices.append(vertices[0])  # Close the circle
    return p3js.Line(
        geometry=p3js.Geometry(vertices=vertices),
        material=p3js.LineBasicMaterial(color='red')
    )

# Crea le linee e i cerchi
line_objects = [create_line(start, end) for start, end in lines]
circle_objects = [create_circle((x, y, z), radius) for x, y, z, radius in circles]

# Crea la scena
scene = p3js.Scene(children=[p3js.AmbientLight(color='#777777')] + line_objects + circle_objects)

# Aggiungi una camera
camera = p3js.PerspectiveCamera(position=[50, 50, 50], up=[0, 0, 1], children=[
    p3js.DirectionalLight(color='white', position=[3, 5, 1], intensity=0.6)
])

# Aggiungi un controllo orbitale per permettere la rotazione della scena
controller = p3js.OrbitControls(controlling=camera)

# Renderer
renderer = p3js.Renderer(camera=camera, scene=scene, controls=[controller], width=800, height=600)

# Mostra il renderer
display(renderer)