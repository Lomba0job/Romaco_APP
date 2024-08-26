import sys
import os
import platform
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QPointF, QTimer
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import numpy as np
from API import funzioni as f

class VTKWidget(QWidget):
    def __init__(self, num_rectangles, parent=None):
        super().__init__(parent)
        self.num_rectangles = num_rectangles
        self.rect_size = [35.0, 7.0, 35.0]
        self.selected_rect = None
        self.last_pos = QPointF()
        self.camera_angle_x = 0
        self.camera_angle_y = 20
        self.camera_position_x = 0
        self.camera_position_y = 60
        self.camera_position_z = 300
        self.rotating_camera = False
        self.moving_camera = False

        self.layout = QVBoxLayout(self)
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.layout.addWidget(self.vtkWidget)

        # Renderer and RenderWindow
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1, 1, 1)
        self.render_window = self.vtkWidget.GetRenderWindow()
        self.render_window.SetMultiSamples(0)
        self.render_window.AddRenderer(self.renderer)
        
        # Sistema operativo specifico setup
        self.setup_os_specific()

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

    def setup_os_specific(self):
        if platform.system() == "Darwin":  # macOS
            # Usa il rendering OpenGL di default
            self.interactor = self.render_window.GetInteractor()
        elif platform.system() == "Linux":
            # Usa il backend XCB e forza VTK a usare X11
            os.environ['QT_QPA_PLATFORM'] = 'xcb'
            os.environ['VTK_USE_X'] = '1'
            self.interactor = vtk.vtkXRenderWindowInteractor()
            self.interactor.SetRenderWindow(self.render_window)
        elif platform.system() == "Windows":
            # Usa il rendering OpenGL di default
            self.interactor = self.render_window.GetInteractor()
        else:
            # Fallback per altri sistemi operativi
            self.interactor = self.render_window.GetInteractor()

    def showEvent(self, event):
        super().showEvent(event)
        self.interactor.Initialize()
        self.render_window.Render()
        self.update_scene()
        self.interactor.Start()

    def setup_rect_positions(self):
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

    def load_mtl(self, filepath):
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

        return materials_info

    def load_obj(self, filepath):
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

        print(f"Loaded model with {len(vertices)} vertices and {len(faces)} faces.")
        return (vertices, faces, face_materials), materials

    def create_actors(self):
        for position in self.rect_positions:
            actor = self.create_actor(position)
            self.renderer.AddActor(actor)
            
    def add_base_plane(self):
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

    def create_actor(self, position):
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
        return actor

    def get_material_color(self, material_name):
        material_info = self.materials_info.get(material_name, {})
        kd = material_info.get('Kd', ['0.3', '0.3', '0.3'])
        return [float(c) for c in kd]

    def setup_camera(self):
        self.camera = vtk.vtkCamera()
        self.camera.SetPosition(self.camera_position_x, self.camera_position_y, self.camera_position_z)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 1, 0)
        self.camera.Zoom(1.2)  # Aumentato leggermente lo zoom per una visione migliore
        self.renderer.SetActiveCamera(self.camera)

    def update_scene(self):
        self.render_window.Render()

    def mousePressEvent(self, event):
        self.last_pos = event.position()
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.moving_camera = True
        elif event.buttons() == Qt.MouseButton.RightButton:
            self.rotating_camera = True

    def mouseMoveEvent(self, event):
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
        self.update_scene()

    def mouseReleaseEvent(self, event):
        self.moving_camera = False
        self.rotating_camera = False
        
    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.camera_position_z -= delta * 10
        self.camera_position_z = max(100, min(self.camera_position_z, 1000))
        self.camera.SetPosition(self.camera_position_x, self.camera_position_y, self.camera_position_z)
        self.update_scene()