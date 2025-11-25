from PySide6.QtCore import Signal, QObject
import os
import json
import sys

class JsonManager(QObject):

    signal_json_err = Signal(str)
    signal_json_save = Signal(str)

    def __init__(self):
        super().__init__()

    def get_absolute_path(self, name_file):
        base_path = ''
        try:
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
            self.signal_json_err.emit('[Perfil] NO se encontró la base de datos de materiales')

        return os.path.join(base_path, name_file)

    def cargar_perfiles_json(self):
        perfiles = []
        materiales = self.cargar_json()
        for nombre_perfil in materiales.keys():
            perfiles.append(nombre_perfil)
        return perfiles

    def cargar_json(self):
        path = self.get_absolute_path('app/storage/materials.json')
        materiales = {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                perfiles = json.load(f)

                for nombre_perfil, datos_perfil in perfiles.items():
                    materiales[nombre_perfil] = datos_perfil
        except FileNotFoundError:
            self.signal_json_err.emit("[Material] Error: No se encontró el archivo de materiales")
        except json.JSONDecodeError:
            self.signal_json_err.emit("[Material] Error: El archivo de materiales no es un JSON válido")
        except Exception as e:
            self.signal_json_err.emit(f"[Material] Ocurrió un error al cargar materiales: {e}")
        return materiales

    def guardar_json(self, materiales):
        path = self.get_absolute_path('app/storage/materials.json')
        try:
            with open(path, 'w') as file:
                json.dump(materiales, file, indent=4)
            self.signal_json_save.emit('[Materiales] Se agrego el nuevo material correctamente')
        except:
            self.signal_json_err.emit('[Materiales] Hubo un error al agregar un nuevo material')

