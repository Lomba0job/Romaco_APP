import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QPointF, QTimer
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtkmodules.vtkRenderingOpenGL2
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingFreeType

import vtk
import numpy as np
from API import funzioni as f

import ctypes
import ctypes.util
import logging
import signal

# Set up logging
logging.basicConfig(
    filename='vtk_widget.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add a console handler for immediate output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

logging.info("Starting application")

# Signal handling to catch segmentation faults and aborts
def handle_signal(signum, frame):
    logging.error(f"Received signal: {signum}")
    sys.exit(1)

signal.signal(signal.SIGSEGV, handle_signal)  # Handle segmentation faults
signal.signal(signal.SIGABRT, handle_signal)  # Handle aborts

# X11 error handler
def x11_error_handler(display, event):
    logging.error("X11 error occurred")
    return 0

try:
    x11 = ctypes.cdll.LoadLibrary(ctypes.util.find_library('X11'))
    x11.XSetErrorHandler(ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(x11_error_handler))
    logging.info("X11 error handler set up successfully")
except Exception as e:
    logging.error(f"Failed to set up X11 error handler: {e}")
    
class VTKWidget(QWidget):
    def __init__(self, num_rectangles, parent=None):
        super().__init__(parent)
        logging.debug("Initializing VTKWidget")
        
        self.num_rectangles = num_rectangles
        self.rect_size = [35.0, 7.0, 35.0]
        self.selected_rect = None
        self.last_pos = QPointF()
        self.camera_angle_x = 0
        self.camera_angle_y = 20
        self.camera_position_x = 0
        self.camera_position_y = 60  # Aumentato per una vista più alta
        self.camera_position_z = 300  # Aumentato per una distanza maggiore
        self.rotating_camera = False
        self.moving_camera = False
        
        logging.debug("VTKWidget properties initialized")

        self.layout = QVBoxLayout(self)
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.layout.addWidget(self.vtkWidget)

        # Renderer and RenderWindow
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1, 1, 1)  # Set background color to white
        self.render_window = self.vtkWidget.GetRenderWindow()
        self.render_window.SetMultiSamples(0)  # Disable anti-aliasing
        # self.render_window.SetOffScreenRendering(1)
        self.render_window.AddRenderer(self.renderer)
        self.interactor = self.render_window.GetInteractor()
        
        logging.debug("VTK rendering setup complete")

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_scene)
        self.timer.start(30)

        # Load material info and model
        self.materials_info = self.load_mtl(f.get_img("mat.mtl"))
        self.model, self.materials = self.load_obj(f.get_img("bilancia_def.obj"))

        # Set up positions and create actors
        self.setup_rect_positions()
        self.create_actors()

        # Add transparent base plane
        self.add_base_plane()

        # Camera setup
        self.setup_camera()

        # Forzare il calcolo del devicePixelRatio
        print(self.devicePixelRatioF())

    def showEvent(self, event):
        logging.debug("showEvent started")
        super().showEvent(event)

        logging.debug("Initializing interactor")
        # self.interactor.Initialize()  # Commenta questa linea

        logging.debug("Rendering window")
        self.render_window.Render()
        logging.debug("Window rendered")

        logging.debug("Updating scene")
        self.update_scene()
        logging.debug("Scene updated")

        # self.interactor.Start()  # Commenta questa linea
        logging.debug("Interactor not started")

        QApplication.processEvents()  # Keep the UI responsive
        logging.debug("showEvent finished")

        self.update()
        logging.debug("Widget updated")
        self.render_window.Render()
        logging.debug("Window rendered again")
        self.render_window.Modified()
        logging.debug("Render window modified")
        self.render_window.GetInteractor().Render()
        logging.debug("Interactor rendered")
        print("Mostrato")
    def setup_rect_positions(self):
        logging.debug("Setting up rectangle positions")
        if self.num_rectangles == 4:
            self.rect_positions = [
                (-50, 0, 50),  # Top-left
                (50, 0, 50),   # Top-right
                (50, 0, -50),  # Bottom-left
                (-50, 0, -50)  # Bottom-right
            ]
        elif self.num_rectangles == 3:
            self.rect_positions = [
                (-50, 0, 50),  # Top-left
                (50, 0, 50),   # Top-right
                (0, 0, -50)    # Bottom-center
            ]
        elif self.num_rectangles == 2:
            self.rect_positions = [
                (0, 0, 50),    # Top-center
                (0, 0, -50)    # Bottom-center
            ]
        elif self.num_rectangles == 1:
            self.rect_positions = [
                (0, 0, 0)      # Center
            ]
        elif self.num_rectangles == 6:
            self.rect_positions = [
                (-50, 0, 60),  # Top-left
                (50, 0, 60),   # Top-right
                (50, 0, 0),    # Center-left
                (-50, 0, 0),   # Center-right
                (50, 0, -60),  # Bottom-left
                (-50, 0, -60)  # Bottom-right
            ]
        elif self.num_rectangles == 5:
            self.rect_positions = [
                (-50, 0, 60),  # Top-left
                (50, 0, 60),   # Top-right
                (50, 0, 0),    # Center-left
                (-50, 0, 0),   # Center-right
                (0, 0, -60)    # Bottom-center
            ]

        logging.debug("Rectangle positions set up")

    def load_mtl(self, filepath):
        logging.debug(f"Loading MTL file from {filepath}")
        materials_info = {}
        current_material = None

        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('newmtl '):
                    current_material = line.split()[1]
                    materials_info[current_material] = {}
                elif current_material:
                    if line.startswith('Ka '):
                        materials_info[current_material]['Ka'] = line.split()[1:]
                    elif line.startswith('Kd '):
                        materials_info[current_material]['Kd'] = line.split()[1:]
                    elif line.startswith('Ks '):
                        materials_info[current_material]['Ks'] = line.split()[1:]
                    elif line.startswith('Ns '):
                        materials_info[current_material]['Ns'] = line.split()[1]
                    elif line.startswith('Tr '):
                        materials_info[current_material]['Tr'] = line.split()[1]

        logging.debug("MTL file loaded")
        return materials_info

    def load_obj(self, filepath):
        logging.debug(f"Loading OBJ file from {filepath}")
        vertices = []
        faces = []
        face_materials = []
        materials = {}
        current_material = None

        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('v '):
                    vertex = [float(x) for x in line.split()[1:]]
                    vertices.append([vertex[0], vertex[2], -vertex[1]])
                elif line.startswith('f '):
                    face = [int(vertex.split('/')[0]) - 1 for vertex in line.split()[1:]]
                    faces.append(face)
                    face_materials.append(current_material)
                elif line.startswith('usemtl '):
                    current_material = line.split()[1]
                    if current_material not in materials:
                        materials[current_material] = self.get_material_color(current_material)

        logging.debug(f"Loaded model with {len(vertices)} vertices and {len(faces)} faces.")
        return (vertices, faces, face_materials), materials

    def create_actors(self):
        logging.debug("Creating actors")
        for position in self.rect_positions:
            actor = self.create_actor(position)
            self.renderer.AddActor(actor)
        logging.debug("Actors created")

    def add_base_plane(self):
        logging.debug("Adding base plane")
        # Create a plane source
        plane = vtk.vtkPlaneSource()
        plane.SetOrigin(-100, 0, -100)
        plane.SetPoint1(100, 0, -100)
        plane.SetPoint2(-100, 0, 100)

        # Create a mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Set the plane color and transparency
        actor.GetProperty().SetColor(1, 1, 1)  # White color
        actor.GetProperty().SetOpacity(0.2)    # 50% transparency

        # Add the plane actor to the renderer
        self.renderer.AddActor(actor)
        logging.debug("Base plane added")

    def create_actor(self, position):
        logging.debug(f"Creating actor at position {position}")
        vertices, faces, face_materials = self.model
        points = vtk.vtkPoints()
        polys = vtk.vtkCellArray()
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")

        # Calculate the current bounding box
        min_x = min(v[0] for v in vertices)
        max_x = max(v[0] for v in vertices)
        min_y = min(v[1] for v in vertices)
        max_y = max(v[1] for v in vertices)
        min_z = min(v[2] for v in vertices)
        max_z = max(v[2] for v in vertices)

        current_width = max_x - min_x
        current_height = max_y - min_y
        current_depth = max_z - min_z

        # Calculate the scale factors needed to match rect_size
        x_scale = self.rect_size[0] / current_width if current_width != 0 else 1
        y_scale = self.rect_size[1] / current_height if current_height != 0 else 1
        z_scale = self.rect_size[2] / current_depth if current_depth != 0 else 1

        for v in vertices:
            points.InsertNextPoint(v[0] * x_scale, v[1] * y_scale, v[2] * z_scale)

        for i, face in enumerate(faces):
            triangle = vtk.vtkTriangle()
            for j, vertex in enumerate(face):
                triangle.GetPointIds().SetId(j, vertex)
            polys.InsertNextCell(triangle)

            material_name = face_materials[i]
            color = self.get_material_color(material_name)
            colors.InsertNextTuple3(*[int(c * 255) for c in color])

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetPolys(polys)
        polydata.GetCellData().SetScalars(colors)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polydata)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Set the actor's position
        actor.SetPosition(*position)
        logging.debug("Actor created")
        return actor
    
    def get_material_color(self, material_name):
        material_info = self.materials_info.get(material_name, {})
        kd = material_info.get('Kd', ['0.3', '0.3', '0.3'])
        return [float(c) for c in kd]
    
    def setup_camera(self):
        logging.debug("Setting up camera")
        self.camera = vtk.vtkCamera()
        self.camera.SetPosition(self.camera_position_x, self.camera_position_y, self.camera_position_z)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 1, 0)
        self.camera.Zoom(1.2)  # Aumentato leggermente lo zoom per una visione migliore
        self.renderer.SetActiveCamera(self.camera)
        logging.debug("Camera setup complete")

    def update_scene(self):
        # logging.debug("Updating scene")
        self.renderer.Render()
        QApplication.processEvents()  # Keep the UI responsive during rendering
        # logging.debug("Scene updated")

    
    def mousePressEvent(self, event):
        # logging.debug("Mouse press event")
        self.last_pos = event.position()
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.moving_camera = True
        elif event.buttons() == Qt.MouseButton.RightButton:
            self.rotating_camera = True

    def mouseMoveEvent(self, event):
        # logging.debug("Mouse move event")
        if self.moving_camera:
            dx = (event.position().x() - self.last_pos.x()) / 0.05
            dy = (event.position().y() - self.last_pos.y()) / 0.05
            self.camera_position_x -= dx
            self.camera_position_y += dy
            self.camera.SetPosition(self.camera_position_x, self.camera_position_y, self.camera_position_z)
            self.last_pos = event.position()
        elif self.rotating_camera:
            dx = (event.position().x() - self.last_pos.x()) / 0.05
            dy = (event.position().y() - self.last_pos.y()) / 0.05
            self.camera_angle_y += dx
            self.camera_angle_x += dy
            self.camera.Elevation(dy)
            self.camera.Azimuth(dx)
            self.last_pos = event.position()

    def mouseReleaseEvent(self, event):
        # logging.debug("Mouse release event")
        self.moving_camera = False
        self.rotating_camera = False

    def wheelEvent(self, event):
        # logging.debug("Mouse wheel event")
        delta = event.angleDelta().y() / 120
        self.camera_position_z -= delta * 10
        self.camera_position_z = max(100, min(self.camera_position_z, 1000))
        self.camera.SetPosition(self.camera_position_x, self.camera_position_y, self.camera_position_z)


