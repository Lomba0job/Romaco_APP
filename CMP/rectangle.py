import sys
from PyQt6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QPointF, QTimer, QThread, pyqtSignal, QObject
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import numpy as np
from API import funzioni as f
import traceback
import logging

# Configurazione del logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class VTKWorker(QObject):
    finished = pyqtSignal(object)  # Signal to notify when finished with the loaded model and materials
    error = pyqtSignal(str)        # Signal to notify in case of errors

    def __init__(self, num_rectangles):
        super().__init__()
        self.num_rectangles = num_rectangles

    def process(self):
        try:
            logging.debug("VTKWorker: Inizio elaborazione della logica 3D.")
            # Load the MTL and OBJ files
            materials_info = self.load_mtl(f.get_img("mat.mtl"))
            model, materials = self.load_obj(f.get_img("bilancia_def.obj"), materials_info)
            logging.debug("VTKWorker: Logica 3D completata.")
            self.finished.emit((model, materials))  # Emit signal with model and materials
        except Exception as e:
            logging.error(f"Errore nel VTKWorker: {e}")
            logging.error(traceback.format_exc())
            self.error.emit(str(e))  # Emit error signal

    def load_mtl(self, filepath):
        logging.debug(f"Caricamento file MTL: {filepath}")
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

    def load_obj(self, filepath, materials_info):
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
                        materials[current_material] = self.get_material_color(current_material, materials_info)

        logging.debug(f"Loaded model with {len(vertices)} vertices and {len(faces)} faces.")
        return (vertices, faces, face_materials), materials

    def get_material_color(self, material_name, materials_info):
        material_info = materials_info.get(material_name, {})
        kd = material_info.get('Kd', ['0.3', '0.3', '0.3'])
        return [float(c) for c in kd]
    
    

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
        self.vtkWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.vtkWidget)

        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1, 1, 1)
        self.render_window = self.vtkWidget.GetRenderWindow()
        self.render_window.SetMultiSamples(0)
        self.render_window.AddRenderer(self.renderer)
        self.interactor = self.render_window.GetInteractor()

        self.worker_thread = QThread()  # Create a thread
        self.worker = VTKWorker(num_rectangles)  # Create a worker instance
        self.worker.moveToThread(self.worker_thread)  # Move worker to the thread
        self.worker.finished.connect(self.on_worker_finished)  # Connect the signal
        self.worker.error.connect(self.handle_error)  # Connect the error signal
        self.worker_thread.started.connect(self.worker.process)  # Start the processing method when thread starts
        self.worker_thread.start()  # Start the thread

    def on_worker_finished(self, result):
        logging.debug("Worker completato, aggiornamento dell'interfaccia utente.")
        try:
            model, materials = result
            self.model = model
            self.materials = materials
            QTimer.singleShot(0, self.setup_scene)
        except Exception as e:
            logging.error(f"Errore in on_worker_finished: {e}")
            logging.error(traceback.format_exc())

    def handle_error(self, error_message):
        logging.error(f"Errore nel thread: {error_message}")

    def closeEvent(self, event):
        self.worker_thread.quit()  # Stop the worker thread
        self.worker_thread.wait()  # Wait for the thread to finish
        super().closeEvent(event)

    def setup_scene(self):
        logging.debug("VTKWidget: Impostazione della scena.")
        try:
            self.setup_rect_positions()
            self.create_actors()
            self.add_base_plane()
            self.setup_camera()
            self.update_scene()  # Rendering iniziale
        except Exception as e:
            logging.error(f"Errore durante setup_scene: {e}")
            logging.error(traceback.format_exc())
        
    def create_actors(self):
        logging.debug("Creazione degli attori...")
        # Codice per creare attori

        for position in self.rect_positions:
            actor = self.create_actor(position)
            self.renderer.AddActor(actor)
            
    def add_base_plane(self):
        logging.debug("Aggiunta del piano di base trasparente...")
        # Codice per aggiungere il piano di base
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
            color = self.materials.get(material_name, [0.3, 0.3, 0.3])
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
        
    def showEvent(self, event):
        super().showEvent(event)
        logging.debug("showEvent triggered")

        try:
            if not self.interactor.GetInitialized():
                logging.debug("Inizializzazione dell'interactor VTK...")
                QTimer.singleShot(1000, self.start_interactor)

            if self.render_window and self.render_window.GetRenderers().GetNumberOfItems() > 0:
                logging.debug("Esecuzione del rendering iniziale...")
                QTimer.singleShot(1500, self.render_initial_scene)
        except Exception as e:
            logging.error(f"Errore in showEvent: {e}")
            logging.error(traceback.format_exc())

    def start_interactor(self):
        try:
            if self.interactor is not None and self.isVisible():
                logging.debug("Avvio dell'interactor VTK...")
                self.interactor.Start()
                logging.debug("VTK Interactor avviato.")
            else:
                logging.error("L'interactor VTK è None o la finestra non è visibile.")
        except Exception as e:
            logging.error(f"Errore durante l'avvio dell'interactor VTK: {e}")
            logging.error(traceback.format_exc())

    def render_initial_scene(self):
        try:
            if self.render_window and self.render_window.GetRenderers().GetNumberOfItems() > 0 and self.isVisible():
                logging.debug("Render della scena iniziale...")
                self.render_window.Render()
                self.update_scene()
                logging.debug("Scena iniziale renderizzata.")
            else:
                logging.error("Render window o renderer non pronto, o finestra non visibile.")
        except Exception as e:
            logging.error(f"Errore durante il rendering iniziale: {e}")
            logging.error(traceback.format_exc())

    def update_scene(self):
        try:
            if self.renderer and self.render_window:
                if self.renderer.GetActors().GetNumberOfItems() > 0:
                    self.renderer.Render()
                    # logging.debug("Scene updated.")
                else:
                    logging.debug("No actors to render.")
            else:
                logging.debug("Renderer or render window not initialized.")
        except Exception as e:
            logging.error(f"Error during scene update: {e}")

    # Aggiungi il resto dei metodi per gestire le posizioni, la creazione degli attori, ecc.
    def setup_rect_positions(self):
        logging.debug("Impostazione delle posizioni dei rettangoli...")
        # Codice per impostare le posizioni
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


    def setup_camera(self):
        logging.debug("Impostazione della camera...")
        self.camera = vtk.vtkCamera()
        self.camera.SetPosition(self.camera_position_x, self.camera_position_y, self.camera_position_z)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 1, 0)
        self.camera.Zoom(1.2)
        self.renderer.SetActiveCamera(self.camera)
        logging.debug("Camera impostata correttamente.")


    
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