import sys
import os
import time
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize, Qt
from app.main_window import MainWindow

def actualizar_carga(mensaje, progreso):
    # Muestra un texto sobre la imagen (Color blanco, alineación inferior)
    splash.showMessage(f"{mensaje}...", Qt.AlignmentFlag.AlignBottom |
                       Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
    # Mantiene la GUI viva mientras "cargamos"
    app.processEvents()
    # Simula tiempo de trabajo
    time.sleep(0.5)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        # Si falla, estamos en modo de desarrollo (script normal)
        base_path = os.path.abspath(".")
    print(os.path.join(base_path, relative_path))

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    imagen_splash = QPixmap(resource_path('app/assets/horno_inicio.PNG'))
    nuevo_tamano = QSize(600, 400)
    imagen_redimensionada = imagen_splash.scaled(
        nuevo_tamano,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )
    splash = QSplashScreen(imagen_redimensionada)
    splash.show()
    actualizar_carga("Cargando configuración", 25)
    actualizar_carga("Verificando puertos COM", 50)
    actualizar_carga("Iniciando motor gráfico", 75)
    actualizar_carga("Listo", 100)
    app.setWindowIcon(QIcon(resource_path('app/assets/icono_horno.ico')))
    window = MainWindow()
    window.show()
    splash.finish(window)
    app.exec()