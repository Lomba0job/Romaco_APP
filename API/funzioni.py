import os 
import sys

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)


def get_img(ico):
    directory = get_resource_path("ICO")
    ico_new = os.path.join(directory, ico)
    return ico_new

def get_style(style):
    directory = get_resource_path("STYLE")
    ico_new = os.path.join(directory, style)
    return ico_new

def get_db():
    # Usage
    directory = get_resource_path(os.path.join("data", "db"))
    file_name = "peso.db"
    file_path = os.path.join(directory, file_name)
    
    return file_path


def get_app_log():
    # Usage
    directory = get_resource_path(os.path.join("data", "logs"))
    file_name = "app.log"
    file_path = os.path.join(directory, file_name)
    
    return file_path


def get_thread_log():
    # Usage
    directory = get_resource_path(os.path.join("data", "logs"))
    file_name = "thread.log"
    file_path = os.path.join(directory, file_name)
    
    return file_path